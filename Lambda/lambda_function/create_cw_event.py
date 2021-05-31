import boto3
from config import config
import os
import json
scheduleExpression = "cron(0 12 ? * SUN *)"
os.environ["AWS_DEFAULT_REGION"] = config.default_region
client = boto3.client('events')
lambda_client = boto3.client('lambda')
dynamo = boto3.client('dynamodb')

USERNAME_KEY = "userName"
ENABLED_KEY = "enable"

#Status for event
CREATING = "CREATION"
ENABLED = "ENABLED"
DISABLED = "DISABLED"
DISABLING = "DISABLING"

def create_cloudwatch_event(event, context): 
    config.username = event[USERNAME_KEY]
    event_name = ''.join(c for c in config.username if c.isalnum()) + "-budgeter"
    enabled = event[ENABLED_KEY]
    if(enabled):
        update_schedule_status(CREATING)
        build_cloudwatch_event(event_name)
        build_cloudwatch_event_target(event_name)
        update_schedule_status(ENABLED)
    else:
        #disable the event by username
        update_schedule_status(DISABLING)
        disable_cloudwatch_event(event_name)
        update_schedule_status(DISABLED)
    return successStatus()


def build_cloudwatch_event(event_name):
    # Every SUNDAY
    return client.put_rule(
        Name=event_name,
        ScheduleExpression=scheduleExpression,
        State='DISABLED'
    )

def update_schedule_status(status):
    dynamo.put_item(
        TableName=config.schedule_table_name,
        Item={
                "user": {
                    "S": config.username
                },
                "status": {
                    "S": status
                },
                "schedule": {
                    "S": scheduleExpression
                }
            }
        
    )
def build_cloudwatch_event_target(event_name):
    '''
    Add the lambda target to the cloudwatch event
    '''
    lambda_arn = get_lambda_arn()
    lambda_input = get_input_for_lambda()
    return client.put_targets(
        Rule=event_name,
        Targets=[
            {
                'Id': event_name,
                'Arn': lambda_arn,
                'Input': lambda_input
            }
        ]
    )

def disable_cloudwatch_event(event_name):
    return client.disable_rule(
        Name=event_name
    )

def enable_cloudwatch_event(event_name):
    return client.enable_rule(
        Name=event_name
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

def delete_event_rule(event_name):
    '''
    Delete the cloudwatch event rule 
    '''
    return client.delete_rule(
            Name=event_name,
            Force=True
    )

def delete_event_rule_targets(event_name):
    '''
    Delete the target from the cloudwatch event rule targets
    '''
    return client.remove_targets(
        Rule=event_name,
        Ids = [
            event_name
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

