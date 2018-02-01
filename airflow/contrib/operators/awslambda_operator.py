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

class AWSLambdaOperator(BaseOperator):
    """
    Interact with AWS Lambda

    :param function_name: AWS Lambda Function Name
    :type function_name: str
    :param region_name: AWS Region Name (example: us-west-2)
    :type region_name: str
    :param log_type: Tail Invocation Request
    :type log_type: str
    :param qualifier: AWS Lambda Function Version or Alias Name
    :type qualifier: str
    :param invocation_type: AWS Lambda Invocation Type (RequestResponse, Event etc)
    :type invocation_type: str
    :param aws_conn_id: connection id of AWS credentials / region name. If None,
           credential boto3 strategy will be used (http://boto3.readthedocs.io/en/latest/guide/configuration.html).
    :type aws_conn_id: str
    """

    ui_color = '#c3dae0'
    client = None
    arn = None

    @apply_defaults
    def __init__(self, function_name, payload='', region_name=None, log_type='None', qualifier='$LATEST',
                 invocation_type='RequestResponse', aws_conn_id=None, *args, **kwargs):
        self.function_name = function_name
        self.payload = payload
        self.region_name = region_name
        self.log_type = log_type
        self.invocation_type = invocation_type
        self.qualifier = qualifier
        self.aws_conn_id = aws_conn_id
        self.hook = self.get_hook()
        self.client = self.hook.get_client_type(
            'lambda',
            region_name=self.region_name
        )
        super(AwsLambdaOperator, self).__init__(*args, **kwargs)

    def execute(self, context):
        """
        Invoke Lambda Function
        """
        try:
            response = self.client.invoke(
                FunctionName=self.function_name,
                InvocationType=self.invocation_type,
                LogType=self.log_type,
                Payload=self.payload,
                Qualifier=self.qualifier
            )
            self.log.info(
                'Got response: %s',
                str(response)
            )

        except Exception as e:
            raise AirflowException("AWS Lambda operator error: %s" % str(e))

    def get_hook(self):
        return AwsHook(
            aws_conn_id=self.aws_conn_id
        )
