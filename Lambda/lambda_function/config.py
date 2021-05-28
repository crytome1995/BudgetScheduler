import os


class ConfigDefaults:
    LAMBDA_RULE_NAME = 'budget_reporter'
    DEFAULT_AWS_REGION = 'us-east-1'



class Configuration(ConfigDefaults):

    def __init__(self,
                 lambda_rule_name=ConfigDefaults.LAMBDA_RULE_NAME,
                 default_region=ConfigDefaults.DEFAULT_AWS_REGION
                 ):

        self._lambda_rule_name = lambda_rule_name
        self._default_region = default_region


    @property
    def lambda_rule_name(self):
        return self._lambda_rule_name

    @property
    def default_region(self):
        return self._default_region


config = Configuration()