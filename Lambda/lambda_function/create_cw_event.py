import boto3
from config import config
import os
import json

os.environ["AWS_DEFAULT_REGION"] = config.default_region
client = boto3.client('events')
lambda_client = boto3.client('lambda')

USERNAME_KEY = "userName"
ENABLED_KEY = "enable"

def create_cloudwatch_event(event, context): 
    config.username = event[USERNAME_KEY]
    enabled = event[ENABLED_KEY]
    if(enabled):
        # setup the event and rule pointing to function
        print("SUCC")
    else:
        #delete the event by username
        print("ERROR")
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
    '''
    Add the lambda target to the cloudwatch event
    '''
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

def delete_event_rule(eventName):
    '''
    Delete the cloudwatch event rule 
    '''
    delete_response = client.delete_rule(
            Name=eventName,
            Force=True
    )

def delete_event_rule_targets(eventName):
    '''
    Delete the target from the cloudwatch event rule targets
    '''
    delete_response = client.remove_targets(
        Rule=eventName,
        Ids = [
            eventName
        ],
        Force=True
    )


def errorStatus(error):
    return {
        'statusCode': 500,
        'body': error
    }

def successStatus():
    return {
        'statusCode': 200,
        'body': 'Ok'
    }