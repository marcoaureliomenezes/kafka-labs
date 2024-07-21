#!/bin/bash


kafka-consumer-groups --bootstrap-server broker:29092 --list 

kafka-consumer-groups --bootstrap-server broker:29092 --describe --group lag-consumer-group