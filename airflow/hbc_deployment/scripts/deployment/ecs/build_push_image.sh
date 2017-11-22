#!/bin/sh

eval $(aws --region us-east-1 ecr get-login)
docker build -t 326027360148.dkr.ecr.us-east-1.amazonaws.com/airflow:latest .  > /dev/null
docker push 326027360148.dkr.ecr.us-east-1.amazonaws.com/airflow:latest > /dev/null
