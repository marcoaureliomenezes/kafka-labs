import json
from typing import Any
from kafka import KafkaAdminClient, KafkaConsumer
from kafka.admin import NewTopic
from kafka import TopicPartition, OffsetAndMetadata
from kafka.errors import TopicAlreadyExistsError
from kafka.producer import KafkaProducer
import logging
from handlers import SuccessHandler, ErrorHandler



class KafkaPublisher:
    def __init__(self, kafka_bootstrap_servers, kafka_topic):
        self.kafka_bootstrap_servers = kafka_bootstrap_servers
        self.kafka_topic = kafka_topic

    def publish(self, key, value):
        producer = KafkaProducer(bootstrap_servers=self.kafka_bootstrap_servers)
        producer.send(
                        topic=self.kafka_topic, 
                        key=key.encode('utf-8'),
                        value=value.encode('utf-8'))
        producer.flush()



    def configure_producer(self, **kwargs):
        producer = KafkaProducer(bootstrap_servers=self.kafka_bootstrap_servers, **kwargs)
        return producer
    

    def configure_consumer(self, group_id, **kwargs):
        consumer = KafkaConsumer(
                                    bootstrap_servers=self.kafka_bootstrap_servers, 
                                    group_id=group_id,
                                    key_serializer=self.__key_serializer,
                                    value_serializer=self.__value_serializer,
                                    **kwargs)
        return consumer


    def __key_serializer(self, key):
        return key.encode('utf-8')
    
    def __value_serializer(self, value):
        return json.loads(value.encode('utf-8'))


    def produce_data(self, producer, key, value):
        producer.send(topic=self.kafka_topic, key=key.encode('utf-8'), value=value.encode('utf-8')) \
                .add_callback(SuccessHandler(value)).add_errback(ErrorHandler(value))
        

    def consume_data(self, consumer):
        consumer.subscribe(topics=[self.kafka_topic])
        for message in consumer:

            topic_partition = TopicPartition(topic=self.kafka_topic, partition=message.partition)
            offset = OffsetAndMetadata(offset=message.offset + 1, metadata=message.timestamp)
            consumer.commit({topic_partition: offset})
            yield message



if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()

    kafka_bootstrap_servers = "broker0:29092"
    kafka_topic = "test-topic"
    kafka_publisher = KafkaPublisher(kafka_bootstrap_servers, kafka_topic)
    kafka_publisher.publish(key="1", value="Hello World!")

    adv_producer_config = {
        "acks": "all",
        "linger_ms": "600",
        "retries": "5",
        "max_in_flight_requests_per_connection": "1",
    }

    kafka_publisher.configure_producer(**adv_producer_config)
    kafka_publisher.publish(key="2", value="Hello World!")


    adv_consumer_config = {
        "enable_auto_commit": "True",

    }