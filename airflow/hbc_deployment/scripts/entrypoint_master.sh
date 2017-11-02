#!/bin/sh
echo 'airflow' | sudo -S cron -f &
sleep 20  # wait for DB to be ready
airflow initdb
airflow scheduler --stdout=/usr/local/airflow/logs/scheduler.log --stderr=/usr/local/airflow/logs/scheduler.log --log-file=/usr/local/airflow/logs/scheduler.log &
airflow webserver -k=gevent --stdout=/usr/local/airflow/logs/webserver.log --stderr=/usr/local/airflow/logs/webserver.log --log-file=/usr/local/airflow/logs/webserver.log -p 8080
