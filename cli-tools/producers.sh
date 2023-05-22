#!/bin/bash

kafka-console-producer --broker-list broker0:29092 --topic people

kafka-console-producer --broker-list broker0:29092 --topic people --property "parse.key=true" --property "key.separator=|"

kafka-console-consumer --bootstrap-server broker0:29092 --topic people --from-beginning

kafka-console-consumer --bootstrap-server broker0:29092 --topic people --from-beginning --property print.key=true
