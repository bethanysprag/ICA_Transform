#!/bin/bash
aws --region $AWS_DEFAULT_REGION cloudformation deploy --template-file cf/codebuild.yml --stack-name codebuild-ica --no-fail-on-empty-changeset --capabilities CAPABILITY_IAM

