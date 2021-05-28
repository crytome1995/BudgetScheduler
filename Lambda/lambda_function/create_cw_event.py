import boto3
from config import config
import os
import json

os.environ["AWS_DEFAULT_REGION"] = config.default_region
client = boto3.client('events')
lambda_client = boto3.client('lambda')

USERNAME_KEY = "userName"

def create_cloudwatch_event(event, context): 
    config.username = event[USERNAME_KEY]
    print(config.username)


def build_cloudwatch_event(eventName):
    # Every SUNDAY
    scheduleExpression = "cron(0 12 ? * SUN *)"
    client.put_rule(
        Name=eventName,
        ScheduleExpression=scheduleExpression,
        State='DISABLED'
    )

def build_cloudwatch_event_target(eventName):
    lambda_arn = get_lambda_arn()
    lambda_input = get_input_for_lambda()
    client.put_targets(
        Rule=eventName,
        Targets=[
            {
                'Id': eventName,
                'Arn': lambda_arn,
                'Input': lambda_input
            }
        ]
    )

def get_input_for_lambda():
    '''
    Build the input that will be passed to the lambda function
    '''
    lambda_input = {}
    lambda_input[USERNAME_KEY] = config.username
    return json.dumps(lambda_input)

def get_lambda_arn():
    '''
    based on the name of the lambda function return the associated ARN of the function
    '''
    alias_dict = lambda_client.get_function(
        FunctionName=config.lambda_rule_name
    )
    #ARN of the function
    return alias_dict['Configuration']['FunctionArn']

build_cloudwatch_event_target('testevent')