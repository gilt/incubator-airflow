#!/bin/sh
aws ecs update-service --cluster airflow --service airflow-worker-prod > /dev/null
aws ecs update-service --cluster airflow --service airflow-master-prod > /dev/null
