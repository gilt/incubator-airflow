#!/bin/sh

docker build --build-arg AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} --build-arg AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} -t 326027360148.dkr.ecr.us-east-1.amazonaws.com/airflow:latest .  > /dev/null
docker push 326027360148.dkr.ecr.us-east-1.amazonaws.com/airflow:latest
