#!/bin/bash
export POSTGRES_ENV_POSTGRES_USER=postgres
export POSTGRES_ENV_POSTGRES_PASSWORD=
coverage run --include='uploader_cli/*,CLIUploader.py' -p CLIUploader.py --help
coverage report --show-missing --fail-under 100
if [[ $CODECLIMATE_REPO_TOKEN ]] ; then
  codeclimate-test-reporter
fi
