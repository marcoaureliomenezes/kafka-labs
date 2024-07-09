import time
import os, json
import logging

from confluent_kafka import SerializingProducer
from confluent_kafka.serialization import StringSerializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer

from utils.data_generator import FakeGenerator
from utils.message_handlers import SuccessHandler, ErrorHandler


def get_kafka_config_1():
  return {
    'bootstrap.servers': os.getenv('KAFKA_BROKERS'),
    'linger.ms': 100,
    'retries': 5,
    'acks': 1
  }


def acked(err, msg):
  if err is not None: ErrorHandler()(err)
  else: SuccessHandler()(msg)


def make_producer(gen_configs) -> SerializingProducer:

  avro_schema = json.dumps(FakeGenerator().get_client_avro_schema())
  schema_registry_client = SchemaRegistryClient({'url': os.getenv('SCHEMA_REGISTRY_URL')})
  avro_serializer = AvroSerializer(
    schema_registry_client,
    avro_schema,
    lambda msg, ctx: dict(msg)
  )
  return SerializingProducer({
    **gen_configs,
    "key.serializer": StringSerializer('utf_8'),
    "value.serializer": avro_serializer,
    "partitioner": "murmur2_random"
  })

if __name__ == '__main__':

  FREQ = int(os.getenv('FREQUENCY', 1))
  TOPIC_NAME = os.getenv('KAFKA_TOPIC')
  
  PRODUCER_CONFIGS = get_kafka_config_1()
  PRODUCER = make_producer(PRODUCER_CONFIGS)
  fake_data_generator = FakeGenerator()

  logging.basicConfig(level=logging.INFO)
  logger = logging.getLogger(__name__)

  print(fake_data_generator.get_client_avro_schema())

  while 1:
    msg = fake_data_generator.fake_client()
    encoded_msg = json.dumps(msg).encode('utf-8')
    future = PRODUCER.produce(
      TOPIC_NAME,
      key='client',
      value=msg,
      on_delivery=acked
      )
    PRODUCER.poll(1)
    time.sleep(FREQ)