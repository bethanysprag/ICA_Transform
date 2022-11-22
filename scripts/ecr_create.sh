#!/bin/bash
set -e
aws cloudformation deploy --template-file cf/ecr_template.yml --stack-name ecr-ica --no-fail-on-empty-changeset
