# -*- coding: utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
### Example AWS Batch operator/sensor
"""
import airflow
from airflow import DAG
from airflow.operators.aws_batch_sensor import AwsBatchSensor
from datetime import timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(2),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('example_aws_batch', default_args=default_args)

dag.doc_md = __doc__

job_1 = AwsBatchSensor(
    task_id='job_1',
    job_name='job_1',
    job_definition='tester_job:1',
    queue_name='default-job-queue',
    container_overrides={
        'vcpus': 123,
        'memory': 123,
        'command': [
            'string',
        ],
        'environment': [
            {
                'name': 'string',
                'value': 'string'
            },
        ]
    },
    parameters={
        'string': 'string'
    },
    poke_interval=5,
    dag=dag)
job_2 = AwsBatchSensor(
    task_id='job_2',
    job_definition='tester_job:1',
    job_name='job_2',
    queue_name='default-job-queue',
    poke_interval=5,
    dag=dag)
job_3 = AwsBatchSensor(
    task_id='job_3',
    job_definition='tester_job:1',
    job_name='job_3',
    queue_name='default-job-queue',
    poke_interval=5,
    dag=dag)

job_3 >> job_2 << job_1
