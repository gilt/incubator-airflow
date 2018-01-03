FROM python:2.7-jessie

ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux
ENV AIRFLOW_HOME /usr/local/airflow

ARG AIRFLOW_PIP=https://github.com/gilt/incubator-airflow/archive/hbc_prod.zip

# ADDING FILES
COPY scripts/* ${AIRFLOW_HOME}/scripts/
COPY airflow.cfg ${AIRFLOW_HOME}/airflow.cfg
COPY crontab ${AIRFLOW_HOME}/crontab
COPY aws_credentials ${AIRFLOW_HOME}/.aws/credentials

# CREATING DIRECTORIES / ADDING USER
RUN mkdir ${AIRFLOW_HOME}/logs && \
    useradd -ms /bin/bash -d ${AIRFLOW_HOME} airflow && echo "airflow:airflow" | chpasswd && adduser airflow sudo && \
    chown -R airflow:airflow ${AIRFLOW_HOME}

# INSTALLS
RUN apt-get update -yqq && \
    apt-get install python-pip python-setuptools python-dev build-essential cron sudo libssl-dev libcurl4-openssl-dev -y && \
    pip install --upgrade pip && \
    python -m pip install \
    six==1.10.0 \
    psycopg2 \
    gevent \
    boto3 \
    awscli \
    pycurl \
    celery \
    cryptography

# TURNS OFF CACHE AND GETS GITHUB CODE
ARG CACHEBUST=1
RUN python -m pip install ${AIRFLOW_PIP}

USER airflow

RUN crontab ${AIRFLOW_HOME}/crontab

WORKDIR ${AIRFLOW_HOME}

EXPOSE 8080 8793
