#!/bin/sh

ENV=$1

#useradd airflow -g web -d /usr/local/airflow
mkdir /usr /usr/local /usr/local/airflow
chown -R dwuser /usr/local/airflow
#echo "Created user airflow"
#passwd -f -u airflow

yum -y install gcc gcc-c++ make openssl-devel libxml2-devel libxslt-devel vixie-cron libcurl-devel mysql-devel python-devel python-setuptools postgresql-devel

yes | pip install virtualenv

#su - airflow
sudo su - dwuser

cd /usr/local/airflow

virtualenv --python=/usr/bin/python27 $HOME/venv
source $HOME/venv/bin/activate

mkdir logs
export HOME=/usr/local/airflow
export PYCURL_SSL_LIBRARY=nss
export AIRFLOW_PIP=https://github.com/gilt/incubator-airflow/archive/hbc_prod.zip
export QUEUES=elt_$ENV
export AIRFLOW__CORE__AIRFLOW_HOME=$(pwd)

yes | pip install --upgrade pip
yes | pip install ${AIRFLOW_PIP} \
    six==1.10.0 \
    psycopg2 \
    gevent \
    boto3 \
    awscli \
    celery --upgrade
yes | pip install --compile --no-cache-dir pycurl

aws s3 cp --recursive s3://gilt-data-assets/airflow/ .
chmod -R 775 script/*
crontab crontab
script/entrypoint_worker.sh >> logs/airflow.log &
