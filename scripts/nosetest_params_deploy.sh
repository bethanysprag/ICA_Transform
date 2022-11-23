#!/bin/bash
#set -e
aws cloudformation deploy  --template-file cf/nosetest_params.yml --stack-name param-store-ica --no-fail-on-empty-changeset --capabilities CAPABILITY_IAM

