import logging
import os
import json

from confluent_kafka import DeserializingConsumer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import StringDeserializer



from utils.data_generator import FakeGenerator
from utils.message_handlers import SuccessHandler, ErrorHandler



def make_consumer(gen_configs) -> DeserializingConsumer:
  avro_schema = json.dumps(FakeGenerator().get_client_avro_schema())
  schema_registry_client = SchemaRegistryClient({'url': os.getenv('SCHEMA_REGISTRY_URL')})
  avro_deserializer = AvroDeserializer(
    schema_registry_client,
    avro_schema,
    lambda msg, ctx: dict(msg)
    )
  return DeserializingConsumer({
    **gen_configs,
    "key.deserializer": StringDeserializer('utf_8'),
    "value.deserializer": avro_deserializer
  })

if __name__ == '__main__':


  logging.basicConfig(level=logging.INFO)
  logger = logging.getLogger(__name__)


  KAFKA_BROKERS = os.getenv('KAFKA_BROKERS')
  KAFKA_TOPIC = os.getenv('KAFKA_TOPIC')
  GROUP_ID = os.getenv('GROUP_ID')
  
  consumer_conf = {
    'bootstrap.servers': KAFKA_BROKERS,
    'group.id': GROUP_ID,
    'enable.auto.commit': 'true'
  }


  consumer = make_consumer(consumer_conf)
  consumer.subscribe([KAFKA_TOPIC])

  while True:
    msg = consumer.poll(1.0)
    if msg is None:
      continue
    if msg.error():
      logger.error(f"Consumer error: {msg.error()}")
      continue
    logger.info(f"Message key: {msg.key()}; Message value: {msg.value()}")
