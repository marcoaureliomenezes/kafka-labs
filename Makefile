current_branch = 1.0.0



build_personalized_images:
	docker build -t marcoaureliomenezes/labs-kafka-connect:$(current_branch) ./docker/kafka-connect
	docker build -t marcoaureliomenezes/labs-postgres:$(current_branch) ./docker/postgres
	docker build -t marcoaureliomenezes/labs-prometheus:$(current_branch) ./docker/prometheus
	docker build -t marcoaureliomenezes/labs-scylladb:$(current_branch) ./docker/scylladb
	docker build -t marcoaureliomenezes/hadoop-base:$(current_branch) ./docker/hadoop/base
	docker build -t marcoaureliomenezes/postgres-hive:$(current_branch) ./docker/hive/postgres
	docker build -t marcoaureliomenezes/hive-base:$(current_branch) ./docker/hive/base

publish_personalized_images:
	docker push marcoaureliomenezes/labs-kafka-connect:$(current_branch)
	docker push marcoaureliomenezes/labs-postgres:$(current_branch)
	docker push marcoaureliomenezes/labs-prometheus:$(current_branch)
	docker push marcoaureliomenezes/labs-scylladb:$(current_branch)

###################################################################################
############################    KAFKA SERVICES    #################################

deploy_compose_kafka:
	docker-compose -f services/cluster_compose/kafka_services.yml up -d --build

stop_compose_kafka:
	docker-compose -f services/cluster_compose/kafka_services.yml down

watch_compose_kafka:
	watch docker-compose -f services/cluster_compose/kafka_services.yml ps

deploy_swarm_kafka:
	docker stack deploy -c services/cluster_swarm/kafka_services.yml kafka

watch_swarm_kafka:
	watch docker-compose -f services/cluster_swarm/kafka_services.yml ps

stop_swarm_kafka:
	docker stack rm kafka

###################################################################################
########################    OPERATIONS SERVICES    ################################

deploy_operations_services:
	docker-compose -f services/cluster_compose/operations_services.yml up -d --build

stop_operations_services:
	docker-compose -f services/cluster_compose/operations_services.yml down

watch_operations_services:
	watch docker-compose -f services/cluster_compose/operations_services.yml ps

deploy_swarm_monitoring:
	docker stack deploy -c services/cluster_swarm/monitoring_services.yml monitoring

watch_swarm_monitoring:
	watch docker-compose -f services/cluster_swarm/monitoring_services.yml ps

stop_swarm_monitoring:
	docker stack rm monitoring


###################################################################################
###########################    HADOOP SERVICES    #################################

deploy_compose_hadoop:
	docker-compose -f services/cluster_compose/hadoop_services.yml up -d --build

stop_compose_hadoop:
	docker-compose -f services/cluster_compose/hadoop_services.yml down

watch_compose_hadoop:
	watch docker-compose -f services/cluster_compose/hadoop_services.yml ps


deploy_swarm_hadoop:
	docker stack deploy -c services/cluster_swarm/hadoop_services.yml hadoop
	

###################################################################################
############################    DATABASE SERVICES    #############################

start_database_services:
	docker-compose -f services/layer_streaming/database_services.yml up -d --build



start_spark_cluster:
	docker-compose -f services/spark_services.yml up -d

###################################################################################
###############################    APP SERVICES    ################################

deploy_app_services:
	docker-compose -f services/layer_streaming/app_services.yml up -d --build

stop_app_services:
	docker-compose -f services/layer_streaming/app_services.yml down

watch_app_services:
	watch docker-compose -f services/layer_streaming/app_services.yml ps


enter_scylla_cqlsh:
	docker exec -it scylladb cqlsh

enter_postgres_psql:
	docker exec -it postgres psql -U postgres


begin_postgres_seeder:
	docker exec -it postgres_seeder /bin/bash




deploy_pg_source_connector:
	http PUT :8083/connectors/postgres-source/config @connectors/postgres-source-connector.json -b

status_pg_source_connector:
	http :8083/connectors/postgres-source/status -b

stop_pg_source_connector:
	http DELETE :8083/connectors/postgres-source -b

pause_pg_source_connector:
	http PUT :8083/connectors/postgres-source/pause -b

validate_pg_source_connector:
	http POST :8083/connectors/postgres-source/validate -b



create_docker_networks:
	sh ./scripts/create_docker_networks.sh