import json
import os
import logging

from kafka.consumer import KafkaConsumer


def key_deserializer(key):
    return key.decode('utf-8') if key else key

def value_deserializer(value):
    return json.loads(value.decode('utf-8'))

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()

    KAFKA_BROKERS = os.getenv('KAFKA_BROKERS')
    KAFKA_TOPIC ="simple.clients" # os.getenv('KAFKA_TOPIC')
    GROUP_ID = os.getenv('GROUP_ID', 'simple-consumer')

    logging.info(f"KAFKA_BROKERS: {KAFKA_BROKERS}")
    logging.info(f"KAFKA_TOPIC: {KAFKA_TOPIC}")
    logging.info(f"GROUP_ID: {GROUP_ID}")

    CONSUMER = KafkaConsumer(
        bootstrap_servers=KAFKA_BROKERS,
        group_id=GROUP_ID,
        #key_deserializer=key_deserializer,
        value_deserializer=value_deserializer
    )
    
    CONSUMER.subscribe([KAFKA_TOPIC])

    for msg in CONSUMER:
        value = msg.value
        logger.info(f"Message received: {value}")
        partition, offset = msg.partition, msg.offset
        logger.info(f"Message from partition {partition} with offset {offset}")
