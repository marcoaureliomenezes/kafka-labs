import logging
import os


from confluent_kafka import DeserializingConsumer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import StringDeserializer



def make_consumer(gen_configs) -> DeserializingConsumer:
  
  schema_registry_client = SchemaRegistryClient({'url': os.getenv('SCHEMA_REGISTRY_URL')})
  avro_deserializer = AvroDeserializer(
    schema_registry_client,
    
    
    )


if __name__ == '__main__':
  logging.basicConfig(level=logging.INFO)
  logger = logging.getLogger(__name__)

  consumer_conf = {
    'bootstrap.servers': os.getenv('KAFKA_BROKERS'),
    'group.id': 'client_group',
    'auto.offset.reset': 'earliest'
  }

  schema_registry_conf = {'url': os.getenv('SCHEMA_REGISTRY_URL')}

  schema_registry_client = SchemaRegistryClient(schema_registry_conf)

  avro_deserializer = AvroDeserializer(schema_registry_client)

  consumer_conf['key.deserializer'] = StringDeserializer('utf_8')
  consumer_conf['value.deserializer'] = avro_deserializer

  consumer = DeserializingConsumer(consumer_conf)
  consumer.subscribe([os.getenv('KAFKA_TOPIC_1')])

  while True:
    msg = consumer.poll(1.0)
    if msg is None:
      continue
    if msg.error():
      logger.error(f"Consumer error: {msg.error()}")
      continue
    logger.info(f"Message key: {msg.key()}; Message value: {msg.value()}")

  consumer.close()
