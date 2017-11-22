#!/bin/sh

docker build -t 326027360148.dkr.ecr.us-east-1.amazonaws.com/airflow:latest .  > /dev/null
docker push 326027360148.dkr.ecr.us-east-1.amazonaws.com/airflow:latest > /dev/null
