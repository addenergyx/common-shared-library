import boto3
import os
from dotenv import load_dotenv


class AWSConnector:
    def __init__(self, region_name="eu-west-1"):
        self.AWS_DEFAULT_REGION = region_name
        self.session = self.get_session()

    @staticmethod
    def get_session():
        if os.getenv('AWS_LAMBDA_FUNCTION_NAME'):
            return boto3.Session(
                aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
                aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
                aws_session_token=os.environ["AWS_SESSION_TOKEN"]
            )
        load_dotenv(verbose=True, override=True)
        return boto3.Session(
            aws_access_key_id=os.environ["AWS_ACCESS_KEY"],
            aws_secret_access_key=os.environ["AWS_SECRET_KEY"],
        )

    def connect_to_dynamodb(self, table_name):
        dynamodb = self.session.resource('dynamodb', region_name=self.AWS_DEFAULT_REGION)
        return dynamodb.Table(table_name)

    def connect_to_s3(self):
        return self.session.resource('s3', region_name=self.AWS_DEFAULT_REGION)

    def connect_to_sqs_queue(self, queue_name):
        return self.session.resource('sqs').get_queue_by_name(QueueName=queue_name)

    @staticmethod
    def queue_active(queue):
        return (
                int(queue.attributes["ApproximateNumberOfMessages"]) > 0
                and queue.attributes["ApproximateNumberOfMessagesNotVisible"] == '0'
        )

    @staticmethod
    def fetch_current_data_from_dynamodb(table_name):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(table_name)
        response = table.scan()
        return {item['merchant_id']: item for item in response['Items']}

# Usage
# aws_connector = AWSConnector()
# dynamodb_table = aws_connector.connect_to_dynamodb("your_table_name")
# s3 = aws_connector.connect_to_s3()
# sqs_queue = aws_connector.connect_to_sqs_queue("your_queue_name")
# is_queue_active = AWSConnector.queue_active(sqs_queue)
