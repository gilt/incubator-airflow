from airflow.operators.sensors import  BaseSensorOperator
import logging
from airflow.hooks.aws_batch_hook import AwsBatchHook
from airflow.utils.decorators import apply_defaults
from airflow.exceptions import AirflowException
import time

class AwsBatchSensor(BaseSensorOperator):
    """
    Runs a job on AWS Batch and keeps poking until state 'SUCCEEDED' or 'FAILED' is returned

    see http://boto3.readthedocs.io/en/latest/reference/services/batch.html#Batch.Client.submit_job
    for accepted arguments
    """
    ui_color = '#7c7287'

    @apply_defaults
    def __init__(self, job_definition, aws_batch_queue, container_overrides = {}, parameters = {}, *args, **kwargs):
        super(AwsBatchSensor, self).__init__(*args, **kwargs)
        self.job_definition = job_definition
        self.parameters = parameters
        self.container_overrides = container_overrides
        self.job_id = None
        self.aws_batch_queue = aws_batch_queue
        self.job_name = self.generate_job_name()

    def generate_job_name(self):
        return '{task}_{time}'.format(task=self.task_id, time=int(time.time()))

    def poke(self, context):
        hook = AwsBatchHook()

        if self.task_id:
            # job_name is unique so we can get the job_id from that
            jobs = hook.client.list_jobs(jobQueue=self.aws_batch_queue, jobStatus='RUNNING')['jobSummaryList']
            matching_jobs = [job for job in jobs if job['jobName'] == self.job_name]
            if matching_jobs:
                self.job_id = matching_jobs[0]['jobId']

        if not self.job_id:
            response = hook.client.submit_job(
                jobName = self.job_name,
                jobQueue = self.aws_batch_queue,
                jobDefinition = self.job_definition,
                containerOverrides = self.container_overrides,
                parameters = self.parameters
            )
            self.job_id = response['jobId']

        status = hook.get_job_status(self.job_id)

        if status == 'SUCCEEDED':
            return True
        elif status == 'FAILED':
            raise AirflowException("Batch job failed with status: {}".format(status))
        else:
            logging.info('Job: {}, status: {}'.format(self.task_id, status))
            return False
