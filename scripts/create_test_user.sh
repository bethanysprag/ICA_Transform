#!/bin/bash
aws cloudformation deploy  --template-file cf/test-user.yml --stack-name ICA-Test-User --no-fail-on-empty-changeset --capabilities CAPABILITY_IAM --capabilities CAPABILITY_NAMED_IAM
