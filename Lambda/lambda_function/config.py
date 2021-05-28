import os


class ConfigDefaults:
    LAMBDA_RULE_NAME = 'testfunction'
    DEFAULT_AWS_REGION = 'us-east-1'

class Configuration(ConfigDefaults):

    def __init__(self,
                 lambda_rule_name=ConfigDefaults.LAMBDA_RULE_NAME,
                 default_region=ConfigDefaults.DEFAULT_AWS_REGION,
                 ):

        self._lambda_rule_name = lambda_rule_name
        self._default_region = default_region
        self._username = ""

    @property
    def lambda_rule_name(self):
        return self._lambda_rule_name

    @property
    def default_region(self):
        return self._default_region

    @property
    def username(self):
        return 'ethan'
    
    @username.setter
    def username(self, u):
        self._username = u

config = Configuration()