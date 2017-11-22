#!/bin/sh

eval $(aws --region us-east-1 ecr get-login --no-include-email)
docker build -t 326027360148.dkr.ecr.us-east-1.amazonaws.com/airflow:latest .
docker push 326027360148.dkr.ecr.us-east-1.amazonaws.com/airflow:latest
