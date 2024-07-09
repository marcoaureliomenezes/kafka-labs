from kafka_client import KafkaClient
import logging


if __name__ == "__main__":


    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()

    kafka_client = KafkaClient(kafka_bootstrap_servers="broker0:29092")
    adv_consumer_config = {
        "enable_auto_commit": "False"
    }

    consumer = kafka_client.configure_consumer(group_id="group_1")
    for message in kafka_client.consume_data("dadaia", consumer):
        logger.info(message.value)