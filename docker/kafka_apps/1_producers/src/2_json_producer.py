import time
import os, json
import logging

from confluent_kafka import SerializingProducer
from confluent_kafka.serialization import StringSerializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.json_schema import JSONSerializer

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

  with open('utils/schemas/schema-client-json.json') as f:
    json_schema = json.load(f)

  json_schema = json.dumps(json_schema)
  print(type(json_schema))
  schema_registry_client = SchemaRegistryClient({'url': os.getenv('SCHEMA_REGISTRY_URL')})
  json_serializer = JSONSerializer(
    json_schema,
    schema_registry_client,
    lambda msg, ctx: dict(msg)
  )
  return SerializingProducer({
    **gen_configs,
    "key.serializer": StringSerializer('utf_8'),
    "value.serializer": json_serializer,
    "partitioner": "murmur2_random"
  })

if __name__ == '__main__':

  FREQ = float(os.getenv('FREQUENCY'))
  TOPIC_NAME = os.getenv('KAFKA_TOPIC')
  
  PRODUCER_CONFIGS = get_kafka_config_1()
  PRODUCER = make_producer(PRODUCER_CONFIGS)
  fake_data_generator = FakeGenerator()

  logging.basicConfig(level=logging.INFO)
  logger = logging.getLogger(__name__)


  while 1:
    msg = fake_data_generator.fake_client()
    future = PRODUCER.produce(
      TOPIC_NAME,
      key='client',
      value=msg,
      on_delivery=acked
      )
    PRODUCER.poll(1)
    time.sleep(FREQ)