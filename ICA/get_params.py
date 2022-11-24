import boto3
import os
import json
import logging


def get_param_list(param='/ica/testing/variables/'):
    """ retrieves env variables for testing that have been stored in the parameter store 
        as a list of dictionaries with the format {'parameter name':'parameter value'}
    """
    ssm = boto3.client('ssm')
    try:
        parameters = ssm.get_parameters_by_path(Path=param, Recursive=True, WithDecryption=True)
        param_list = []
        for entry in parameters['Parameters']:
            p_value = entry['Value']
            p_name = entry['Name'].split('/')[-1]
            param_list.append({"name": p_name,"value":p_value})
    except Exception as e:
        logging.error('Unable to retrieve test job parameters')
        logging.error(e)
        param_list = []
    return param_list


def set_env_variables_by_parameter(param_list):
    """ converts list of parameter dict to env variables """
    try:
        for key in param_list:
            name = key['name']
            val = key['value']
            os.environ[name] = val
        return True
    except Exception as e:
        logging.error('unable to parse ica test env variables from parameter store')
        logging.error(e)
        return False


def main():
    """ gets list of parameters from store then sets env variables """
    param_list = get_param_list()
    status = set_env_variables_by_parameter(param_list)
    return status

if __name__ == '__main__':
    status = main()
