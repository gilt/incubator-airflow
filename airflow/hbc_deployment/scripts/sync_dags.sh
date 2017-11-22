#!/bin/bash
AWS_PATH=$(which aws || echo "/usr/local/bin/aws")
source /usr/local/airflow/scripts/commons.sh
echo "Syncing dags" | addDate
${AWS_PATH} s3 sync s3://airflow-dags/ /usr/local/airflow/dags  --delete --include "*.py" --exclude "*" | addDate
