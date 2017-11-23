#!/bin/sh
aws ecs update-service --cluster airflow --service airflow-worker-prod --task-definition airflow-worker > /dev/null
aws ecs update-service --cluster airflow --service airflow-master-prod --task-definition airflow-master > /dev/null
