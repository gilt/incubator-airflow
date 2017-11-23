from airflow.operators.sensors import  BaseSensorOperator
import logging
from airflow.hooks.aws_batch_hook import AwsBatchHook
from airflow.utils.decorators import apply_defaults

class AwsBatchSensor(BaseSensorOperator):
    """
    Runs a job on AWS Batch and keeps poking until state 'SUCCEEDED' or 'FAILED' is returned

    see http://boto3.readthedocs.io/en/latest/reference/services/batch.html#Batch.Client.submit_job
    for accepted arguments
    """
    ui_color = '#7c7287'

    @apply_defaults
    def __init__(self, job_name, queue_name, job_definition, container_overrides = {}, parameters = {}, *args, **kwargs):
        super(AwsBatchSensor, self).__init__(*args, **kwargs)
        self.job_name = job_name
        self.queue_name = queue_name
        self.job_definition = job_definition
        self.parameters = parameters
        self.container_overrides = container_overrides
        self.job_id = None

    def poke(self, context):
        hook = AwsBatchHook()

        logging.info('Poking: ' + self.job_name)
        if self.job_name:
            # job_name is unique so we can get the job_id from that
            jobs = hook.client.list_jobs(jobQueue=self.queue_name, jobStatus='RUNNING')['jobSummaryList']
            matching_jobs = [job for job in jobs if job['jobName'] == self.job_name]
            if matching_jobs:
                self.job_id = matching_jobs[0]['jobId']

        if not self.job_id:
            response = hook.client.submit_job(
                jobName = self.job_name or random_id(),
                jobQueue = self.queue_name or hook.default_queue_name,
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
            logging.info('Job: {}, status: {}'.format(self.job_name, status))
            return False
