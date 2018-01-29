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
#

from airflow.exceptions import AirflowException
from airflow.models import BaseOperator
from airflow.utils import apply_defaults

from airflow.contrib.hooks.aws_hook import AwsHook


class AWSSnsOperator(BaseOperator):
    """
    Send a notification to AWS SNS service
    :param message: required message to send to SNS
    :type message: str
    :param topic_name: the name for the SNS topic to publish to
    :type topic_name: str
    :param target_arn: either TopicArn or EndpointArn, but not both
    :type target_arn: str
    :param phone_number: the phone number to which you want to deliver an SMS message. use E.164 format.
    :type phone_number: str
    :param: subject: optional parameter to be used as the "Subject" line when the message is delivered to email endpoints. this field will also be included, if present, in the standard JSON messages delivered to other endpoints.
    :type: subject: str
    :param: message_structure: set MessageStructure to json if you want to send a different message for each protocol.
    :type: message_structure: str
    :param: message_attributes: message attributes for Publish action.
    :type: message_attributes: dict
    :param aws_conn_id: connection id of AWS credentials / region name. If None,
            credential boto3 strategy will be used (http://boto3.readthedocs.io/en/latest/guide/configuration.html).
    :type aws_conn_id: str
    :param region_name: region name to use in AWS Hook. Override the region_name in connection (if provided)
    :type region_name: str
    """

    ui_color = '#c3dae0'
    client = None
    arn = None

    @apply_defaults
    def __init__(self, message, topic_name=None, target_arn=None, phone_number=None, subject=None,
                 message_structure=None, message_attributes=None, aws_conn_id=None,
                 region_name=None, **kwargs):
        super(AWSSnsOperator, self).__init__(**kwargs)

        self.message = message
        self.topic_name = topic_name
        self.target_arn = target_arn
        self.phone_number = phone_number
        self.subject = subject
        self.message_structure = message_structure
        self.message_attributes = message_attributes
        self.aws_conn_id = aws_conn_id
        self.region_name = region_name

        self.success = None
        self.hook = self.get_hook()
        self.client = self.hook.get_client_type(
            'sns',
            region_name=self.region_name
        )

    def execute(self, context):
        try:
            params = {'Message': self.message}

            topic_arn = None
            if self.topic_name:
                self.log.info(
                    'Creating or getting topic %s',
                    self.topic_name
                )
                topic_arn = self.client.create_topic(
                    Name=self.topic_name
                )
            if topic_arn:
                self.log.info(
                    'Topic arn: %s',
                    topic_arn['TopicArn']
                )
                params['TopicArn'] = topic_arn['TopicArn']

            if self.target_arn:
                params['TargetArn'] = self.target_arn
            if self.phone_number:
                params['PhoneNumber'] = self.phone_number
            if self.subject:
                params['Subject'] = self.subject
            if self.message_structure:
                params['MessageStructure'] = self.message_structure
            if self.message_attributes:
                params['MessageAttributes'] = self.message_attributes

            self.log.info('Sending an SNS notification')
            self.log.info(
                'Parameters: %s',
                self.params
            )

            response = self.client.publish(params)

            self.log.info(
                'Message sent successfully, with ID: %s',
                response['MessageId']
            )

        except Exception as e:
            raise AirflowException("AWS Sns operator error: %s" % str(e))

    def get_hook(self):
        return AwsHook(
            aws_conn_id=self.aws_conn_id
        )
