import time
import json
import logging
import os
import time

from confluent_kafka import Producer
from kafka.producer.future import FutureRecordMetadata

from utils.data_generator import FakeGenerator
from utils.message_handlers import SuccessHandler, ErrorHandler



def acked(err, msg):
  if err is not None: ErrorHandler()(err)
  else: SuccessHandler()(msg)


if __name__ == '__main__':

  FREQ = float(os.getenv('FREQUENCY'))
  KAFKA_BROKERS = os.getenv('KAFKA_BROKERS')
  TOPIC_NAME = os.getenv('KAFKA_TOPIC')
  
  logging.basicConfig(level=logging.INFO)
  logger = logging.getLogger(__name__)

  specific_configs = {'retries': 2, 'acks': 1, 'batch.size': 16384, 'linger.ms': 1000}
  producer_configs = {'bootstrap.servers': KAFKA_BROKERS, **specific_configs}
  PRODUCER_CONFLUENT = Producer(producer_configs)
  FAKE_GENERATOR = FakeGenerator()

  counter = 0
  while 1:
    msg_client = FAKE_GENERATOR.fake_client()
    encoded_msg = json.dumps(msg_client).encode('utf-8')
    future = PRODUCER_CONFLUENT.produce(TOPIC_NAME, encoded_msg, callback=acked)
    if counter % 10000 == 0: PRODUCER_CONFLUENT.poll(1)
    #PRODUCER_CONFLUENT.flush()
    time.sleep(FREQ)
    counter += 1








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