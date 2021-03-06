#!/bin/sh

# airflow-worker
aws ecs register-task-definition \
  --family airflow-worker \
  --task-role-arn arn:aws:iam::326027360148:role/ecs_task_role \
  --container-definitions '[
        {
            "volumesFrom": [],
            "essential": true,
            "entryPoint": ["/usr/local/airflow/scripts/entrypoint_worker.sh"],
            "mountPoints": [],
            "name": "airflow-worker",
            "portMappings": [
              {
                "hostPort": 7777,
                "containerPort": 7777,
                "protocol": "tcp"
              }
            ],
            "environment": [{"name": "QUEUES", "value": "aws_batch,aws_emr,default"}],
            "image": "326027360148.dkr.ecr.us-east-1.amazonaws.com/airflow:latest",
            "cpu": 0,
            "memoryReservation": 300
        }
    ]' > /dev/null

# airflow-master
aws ecs register-task-definition \
  --family airflow-master \
  --task-role-arn arn:aws:iam::326027360148:role/ecs_task_role \
  --container-definitions '[
        {
            "volumesFrom": [],
            "portMappings": [
              {
                "hostPort": 80,
                "containerPort": 8080,
                "protocol": "tcp"
              },
              {
                "hostPort": 7777,
                "containerPort": 7777,
                "protocol": "tcp"
              }
            ],
            "essential": true,
            "entryPoint": ["/usr/local/airflow/scripts/entrypoint_master.sh"],
            "mountPoints": [],
            "name": "airflow-master",
            "environment": [],
            "image": "326027360148.dkr.ecr.us-east-1.amazonaws.com/airflow:latest",
            "cpu": 0,
            "memoryReservation": 300
        }
    ]' > /dev/null
