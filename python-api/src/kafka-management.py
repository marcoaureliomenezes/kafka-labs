import os, logging
from dotenv import load_dotenv
from kafka import KafkaAdminClient
from kafka.admin import NewTopic, ConfigResource, ConfigResourceType
from kafka.errors import TopicAlreadyExistsError


def with_kafka_connection(func):
    def wrapper(*args, **kwargs):
        client = KafkaAdminClient(bootstrap_servers=args[0].bootstrap_servers)
        try: return func(*args, **kwargs, client=client)
        finally: client.close()
    return wrapper


class KafkaAdmin: 


    def __init__(self, bootstrap_servers):
        self.bootstrap_servers = bootstrap_servers


    @with_kafka_connection
    def create_topic(self, topic_name, num_partitions, replication_factor, client=None):
        topic = NewTopic(
            name=topic_name,
            num_partitions=num_partitions,
            replication_factor=replication_factor
        )
        try: client.create_topics([topic])
        except TopicAlreadyExistsError: logger.info("Topic already exists")

    @with_kafka_connection
    def create_advanced_topic(self, topic_name, num_partitions, replication_factor, client=None, **kwargs):
        topic = NewTopic(
            name=topic_name,
            num_partitions=num_partitions,
            replication_factor=replication_factor,
            topic_configs =  kwargs
        )
        try: client.create_topics([topic])
        except TopicAlreadyExistsError: logger.info("Topic already exists")


    @with_kafka_connection
    def delete_topic(self, topic_name, client=None):
       client.delete_topics([topic_name])


    @with_kafka_connection
    def list_topics(self, client=None):
        topics = client.list_topics()
        return topics

    @with_kafka_connection
    def describe_topic(self, topic_name, client=None):
        topic = ConfigResource(ConfigResourceType.TOPIC, topic_name)
        topic = client.describe_configs([topic])
        return [i for i in topic][0].resources


    @with_kafka_connection
    def configure_topic(self, topic_name, client=None, **kwargs):
        cfg_resource_update = ConfigResource(ConfigResourceType.TOPIC, topic_name, configs=kwargs)
        client.alter_configs([cfg_resource_update])


if __name__ == "__main__":

    load_dotenv(verbose=True)
    logger = logging.getLogger()
    
    bootstrap_servers = os.getenv("BOOTSTRAP_SERVERS")
    admin = KafkaAdmin(bootstrap_servers=bootstrap_servers)
    admin.create_topic("test_1", 1, 1)
    admin.create_topic("test_2", 1, 1)
    admin.create_advanced_topic("test_3", 1, 1, **{'retention.ms': '1000'})
    print(admin.describe_topic("test_3"))

    admin.configure_topic("test_2", **{'retention.ms': '1000'})
