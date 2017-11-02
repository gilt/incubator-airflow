#!/bin/sh
echo 'airflow' | sudo -S cron -f &
airflow worker --queues=${QUEUES} --stdout=/usr/local/airflow/logs/worker.log --stderr=/usr/local/airflow/logs/worker.log --log-file=/usr/local/airflow/logs/worker.log
