import boto3
from config import config

import os

os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
client = boto3.client('events')
def create_cloudwatch_event(event, context): 
    x = "ethan"


def build_cloudwatch_event(eventName, scheduleExpression):
    client.put_rule(
        Name=eventName,
        ScheduleExpression=scheduleExpression,
        State='DISABLED'
    )



build_cloudwatch_event("test","cron(0 0 ? * SUN *)")
