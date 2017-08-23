#!/bin/bash
export POSTGRES_ENV_POSTGRES_USER=postgres
export POSTGRES_ENV_POSTGRES_PASSWORD=
export UPLOADER_CONFIG=travis/uploader.json
coverage run --include='uploader_cli/*,CLIUploader.py' CLIUploader.py --help
coverage report --show-missing --fail-under 100
if [[ $CODECLIMATE_REPO_TOKEN ]] ; then
  codeclimate-test-reporter
fi
