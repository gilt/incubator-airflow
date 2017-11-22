#!/bin/sh
aws ecs update-service --cluster airflow --service airflow-worker-prod
aws ecs update-service --cluster airflow --service airflow-master-prod
