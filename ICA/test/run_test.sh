#!/bin/bash
set -e 
if [ "$local" = 'True' ]; then
  echo 'configuring aws using local keys'
  aws configure set aws_access_key_id $AWS_ACCESS_KEY && aws configure set aws_secret_access_key $AWS_SECRET_KEY && aws configure set region us-east-2
else
  echo 'running test in ecs container mode'
fi
cd /work
# . /work/scripts/test_environment.sh
nosetests --with-coverage --cover-package main -v -s
#cd /work
# . /work/scripts/test_cleanup.sh
