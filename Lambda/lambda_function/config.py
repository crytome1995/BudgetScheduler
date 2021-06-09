import os


class ConfigDefaults:
    LAMBDA_RULE_NAME = 'budget_reporter'
    DEFAULT_AWS_REGION = 'us-east-2'
    SCHEDULE_TABLE_NAME = "schedulers"

class Configuration(ConfigDefaults):

    def __init__(self,
                 lambda_rule_name=ConfigDefaults.LAMBDA_RULE_NAME,
                 default_region=ConfigDefaults.DEFAULT_AWS_REGION,
                 schdule_table_name=ConfigDefaults.SCHEDULE_TABLE_NAME
                 ):

        self._lambda_rule_name = lambda_rule_name
        self._default_region = default_region
        self._schedule_table_name = schdule_table_name
        self._username = "test"

    @property
    def lambda_rule_name(self):
        return self._lambda_rule_name

    @property
    def default_region(self):
        return self._default_region

    @property
    def username(self):
        return self._username
    
    @username.setter
    def username(self, u):
        self._username = u

    @property
    def schedule_table_name(self):
        return self._schedule_table_name
    

config = Configuration()