import os
import sys
import argparse
import logging
import boto3
from botocore.client import Config
import json


version="1.0.0"

logging.basicConfig()
logging.root.setLevel(20)


def get_secret_arn_from_cf(key='ICATestServiceUserAccessKeySecretArn',stackname='ICA-Test-User'):
    import boto3
    cf_client = boto3.client('cloudformation')
    response = cf_client.describe_stacks(StackName=stackname)
    outputs = response["Stacks"][0]["Outputs"]
    arn = None
    for output in outputs:
        keyName = output["OutputKey"]
        if keyName == key:
            arn = output["OutputValue"]
    if arn is None:
        logging.error('Unable to retrieve arn for key:%s and stack:%s' % (key,stackname))
    os.environ['secretname'] = arn
    return arn


def get_secret(secret_name=None,region_name='us-east-1'):
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
        else:
            secret = base64.b64decode(get_secret_value_response['SecretBinary'])
    return json.loads(secret)


def main():
    #get ica-test-user creds from secret manager
    try:
        secret_name=os.environ['secretname']
    except:
        secret_name=get_secret_arn_from_cf()
    region = os.environ['AWS_DEFAULT_REGION']
    secrets = get_secret(secret_name=secret_name,region_name=region)
    ACCESS_KEY = secrets['aws_access_key_id']
    SECRET_KEY = secrets['aws_secret_access_key']
    os.environ['ACCESS_KEY'] = ACCESS_KEY
    os.environ['SECRET_KEY'] = SECRET_KEY
    print('export AWS_ACCESS_KEY=%s export AWS_SECRET_KEY=%s' % (ACCESS_KEY,SECRET_KEY))

main()
