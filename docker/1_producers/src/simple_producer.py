import time
import os, json
import json
import logging
import os
import time

from kafka import KafkaProducer
from confluent_kafka import Producer
from kafka.producer.future import FutureRecordMetadata

import logging

from utils.data_generator import FakeGenerator
from utils.message_handlers import SuccessHandler, ErrorHandler

def config_producer_confluent():
  return {
    'bootstrap.servers': os.getenv('KAFKA_BROKERS'),
    'linger.ms': 100,
    'retries': 5,
    'acks': 1
  }

def config_producer_kafka():
  return {
    'linger_ms': 1000,
    'retries': 5,
    'acks': 1
  }


def get_producer_kafka():
  special_configs = config_producer_kafka()
  return KafkaProducer(bootstrap_servers=os.getenv('KAFKA_BROKERS'), **special_configs)

def get_producer_confluent():
  configs = config_producer_confluent()
  return Producer(**configs)


def acked(err, msg):
  if err is not None: ErrorHandler()(err)
  else: SuccessHandler()(msg)


if __name__ == '__main__':

  FREQ = int(os.getenv('FREQUENCY', 1))
  TOPIC_NAME = os.getenv('KAFKA_TOPIC')
  
  PRODUCER_KAFKA = get_producer_kafka()
  PRODUCER_CONFLUENT = get_producer_confluent()

  FAKE_GENERATOR = FakeGenerator()

  logging.basicConfig(level=logging.INFO)
  logger = logging.getLogger(__name__)


  while 1:
    msg_client = FAKE_GENERATOR.fake_client()
    encoded_msg = json.dumps(msg_client).encode('utf-8')
    future = PRODUCER_CONFLUENT.produce(TOPIC_NAME, encoded_msg, callback=acked)
    PRODUCER_CONFLUENT.poll(1)
    time.sleep(FREQ)








if __name__ == '__main__':

  FREQ = float(os.getenv('FREQUENCY', 1))
  KAFKA_BROKERS = {'bootstrap.servers':  os.getenv('KAFKA_BROKERS')}
  TOPIC_NAME = os.getenv('KAFKA_TOPIC_1')
  
  kafka_producers = KafkaProducer(bootstrap_servers=KAFKA_BROKERS['bootstrap.servers'])
  fake_data_generator = FakeGenerator()

  logging.basicConfig(level=logging.INFO)
  logger = logging.getLogger(__name__)

  while 1:
    msg = fake_data_generator.fake_client()
    encoded_msg = json.dumps(msg).encode('utf-8')
    future: FutureRecordMetadata = kafka_producers.send(TOPIC_NAME, encoded_msg)
    future.add_callback(SuccessHandler())
    future.add_errback(ErrorHandler())
    time.sleep(FREQ)


"""
Kafka producer configurations:
  - linger.ms: Number of milliseconds to wait before sending a message to the broker.
  - batch.size: The maximum size of a message batch.
  - retries: The number of retries before the producer gives up and drops the message.
  - acks: The number of acknowledgments the producer requires the leader to have received before considering a request complete.
  - enable.idempotence: When set to true, the producer will ensure that messages are successfully produced in the order they were sent.
"""