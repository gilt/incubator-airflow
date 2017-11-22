# HBC Deployment

## Important notes

Always specify a `queue` in your operators! the `default` queue is used by the local test environment so your jobs could be picked up!

## Introduction

The HBC set up is as follows:
** airflow-master **
The airflow scheduler and web server is Dockerized and runs on AWS ECS. It will be referred to as `airflow-master`. It does not run any job but uses Celery and AWS SQS to populate queues which will be consumed by `airflow-worker`s.

** airflow-worker **
The nodes that run the airflow jobs will be referred to as `airflow-worker`, and those, listen on some queues (examples: `elt-uat`, `elt-prod`, `aws-batch`), and will run the DAGs locally. In the case of Batch, the DAG takes care of starting and monitoring the job on Batch by polling continuously.

The workers not running legacy ELT jobs (all the `/web/dw-*` repos) are Dockerized and run on AWS ECS. Others need to be on the ELT machine matching their environment (elt.uat, elt.prod etc).

## Running tests

You can run the tests following the `README` in `/incubator-airflow`, although they will run in the CodePipeline before any deployment.

You can do further testing using the `docker-compose` environment provided (uses test SQS queues, a local test DB and a test SQS queue). You will have to push your local changes to the `hbc_test` branch (no better deployment method was found yet)
```
# your credentials will be used locally
cp ~/.aws/credentials ./.private_aws

# docker uses `pip install` from `GitHub`
# so we need to push our changes first
git add -A
git commit -m "testing new changes"
git push origin hbc_test

docker-compose up
```

You will have your local Airflow webserver running on `http://192.168.99.100:8080` by default.

## Deployment

The deployment runs on every new push to the branch `hbc_prod`, it:
* builds and updates the docker images for `airflow-master` and `airflow-tester`
* updates the ECS services
* re-installs airflow on ELT machines (that are also `airflow-worker`s)
