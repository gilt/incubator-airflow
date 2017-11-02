#!/bin/bash
AIRFLOW_HOME=/usr/local/airflow
source ${AIRFLOW_HOME}/script/commons.sh
echo "Cleaning orphan dags" | addDate
#  Deleting orphans .pyc
ls -1 ${AIRFLOW_HOME}/dags/*.py | sort > ${AIRFLOW_HOME}/dags/py | addDate
ls -1 ${AIRFLOW_HOME}/dags/*.pyc | sed 's/pyc$/py/g' | sort > ${AIRFLOW_HOME}/dags/pyc | addDate
join -v 2 -1 1 -2 1 ${AIRFLOW_HOME}/dags/py ${AIRFLOW_HOME}/dags/pyc | sed 's/$/c/' | xargs rm $1 | addDate
rm ${AIRFLOW_HOME}/dags/py ${AIRFLOW_HOME}/dags/pyc | addDate
