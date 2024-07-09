current_branch = 1.0.0


start_kafka_cluster:
	docker-compose -f services/kafka_services.yml up -d

stop_kafka_cluster:
	docker-compose -f services/kafka_services.yml down

watch_kafka_cluster:
	watch docker-compose -f services/kafka_services.yml ps

start_app_services:
	docker-compose -f services/app_services.yml up -d

stop_app_services:
	docker-compose -f services/app_services.yml down

watch_app_services:
	watch docker-compose -f services/app_services.yml ps