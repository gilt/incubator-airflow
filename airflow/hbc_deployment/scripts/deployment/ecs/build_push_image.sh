#!/bin/sh

TAG=$1

{
  eval $(aws --region us-east-1 ecr get-login --no-include-email)
  docker build --no-cache -t 326027360148.dkr.ecr.us-east-1.amazonaws.com/airflow:${TAG} .
  docker push 326027360148.dkr.ecr.us-east-1.amazonaws.com/airflow:${TAG}
} || exit 1
