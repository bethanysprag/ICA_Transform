#!/bin/bash
set -e 
if [ "$local" = 'True' ]; then
  echo 'configuring aws using local keys'
  echo 'AWS_ACCOUNT_ID' && echo 'AWS_DEFAULT_REGION'
  echo $AWS_ACCOUNT_ID && echo $AWS_DEFAULT_REGION
  aws configure set aws_access_key_id $AWS_ACCESS_KEY && aws configure set aws_secret_access_key $AWS_SECRET_KEY && aws configure set region $AWS_DEFAULT_REGION
else
  echo 'running test in ecs container mode'
fi
cd /work/ICA
# . /work/scripts/test_environment.sh
nosetests --with-coverage --cover-package ICA --cover-package main -v -s
#cd /work
# . /work/scripts/test_cleanup.sh
