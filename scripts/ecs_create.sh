#!/bin/bash
set -e
aws cloudformation deploy --template-file cf/ecs_template.yml --stack-name ecs-ica --no-fail-on-empty-changeset --capabilities CAPABILITY_IAM 

