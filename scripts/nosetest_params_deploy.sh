#!/bin/bash
#set -e
aws cloudformation deploy  --template-file cf/nosetest_params.yml --stack-name paramstore-ica --no-fail-on-empty-changeset --capabilities CAPABILITY_IAM

