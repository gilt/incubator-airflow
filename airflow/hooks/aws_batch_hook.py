from airflow.hooks.base_hook import  BaseHook
import logging

logger = logging.getLogger('aws-batch-logger')
POLL_TIME = 10

class AwsBatchHook(BaseHook):
    """
    Interact with AWS Batch. This class is a wrapper around the boto library.
    """
    def __init__(self, aws_batch_conn_id='aws_batch_default'):
        self.aws_batch_conn_id = aws_batch_conn_id
        self.queues = None
        self.default_queue_name = None
        self.client = None
        self.connection = self.get_conn()

    def get_conn(self):
        try:
            import boto3
            self.client = boto3.client('batch',
                region_name='us-east-1')

            # Get dict of active queues keyed by name
            self.queues = {q['jobQueueName']:q for q in self.client.describe_job_queues()['jobQueues']
                      if q['state'] == 'ENABLED' and q['status'] == 'VALID'}
            if not self.queues:
                logger.warning('No job queues with state=ENABLED and status=VALID')

            # Pick the first queue as default
            self.default_queue_name = list(self.queues.keys())[0]

        except ImportError:
            logger.error('boto3 is not installed. AWS Batch scheduling require boto3')

    def get_job_status(self, job_id):
        """
        Retrieve task statuses from ECS API

        Returns list of {SUBMITTED|PENDING|RUNNABLE|STARTING|RUNNING|SUCCEEDED|FAILED} for each id in job_ids
        """
        response = self.client.describe_jobs(jobs=[job_id])

        # Error checking
        status_code = response['ResponseMetadata']['HTTPStatusCode']
        if status_code != 200:
            msg = 'Job status request received status code {0}:\n{1}'
            logger.error(msg.format(status_code, response))
            raise Exception(msg.format(status_code, response))

        return response['jobs'][0]['status']


    def register_job_definition(self, json_fpath):
        """Register a job definition with AWS Batch, using a JSON"""
        with open(json_fpath) as f:
            job_def = json.load(f)
        response = self.client.register_job_definition(**job_def)
        status_code = response['ResponseMetadata']['HTTPStatusCode']
        if status_code != 200:
            msg = 'Register job definition request received status code {0}:\n{1}'
            logger.error(msg.format(status_code, response))
            raise Exception(msg.format(status_code, response))
        return response
