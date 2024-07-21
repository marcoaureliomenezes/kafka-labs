#!/bin/bash


docker network create -d overlay --attachable cluster_swarm_kafka

docker network create -d overlay --attachable cluster_swarm_monitoring

docker network create -d overlay --attachable cluster_swarm_hadoop
