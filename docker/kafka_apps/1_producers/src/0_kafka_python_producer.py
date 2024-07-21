
from kafka.producer import KafkaProducer
import os



def config_producer_kafka():
  return {
    'linger_ms': 1000,
    'retries': 5,
    'acks': 1
  }


def get_producer_kafka():
  special_configs = config_producer_kafka()
  return KafkaProducer(bootstrap_servers=os.getenv('KAFKA_BROKERS'), **special_configs)