#!/bin/bash
set -e
aws cloudformation deploy --template-file cf/ubuntu_ecr.yml --stack-name ecr-ubuntu --no-fail-on-empty-changeset
