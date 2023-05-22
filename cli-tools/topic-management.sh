#!/bin/bash

brokers="broker0:29092,broker1:29093,broker2:29094"

# List topics:

kafka-topics --bootstrap-server broker0:29092 --list

# Describe topic:

kafka-topics --bootstrap-server broker0:29092 --describe --topic my-topic


kafka-configs --bootstrap-server broker0:29092 --describe --all --topic my-topic

##################################################################################################################################################
# Create a simple topic:

kafka-topics --bootstrap-server broker0:29092 --create --topic my-topic --partitions 3 --replication-factor 3

# Create a compacted topic:

kafka-topics --bootstrap-server broker0:29092 --create --topic my-topic --partitions 3 --replication-factor 3 --config cleanup.policy=compact

# Create topics with custom retention time

kafka-topics --bootstrap-server broker0:29092 --create --topic my-topic --partitions 3 --replication-factor 3 --config retention.ms=360000

##################################################################################################################################################
# Delete topic:

kafka-topics --bootstrap-server broker0:29092 --delete --topic my-topic


# Alter topic retention time:

kafka-configs --bootstrap-server broker0:29092 --alter --entity-type topics --entity-name my-topic --add-config retention.ms=4200000