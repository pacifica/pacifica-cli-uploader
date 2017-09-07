#!/bin/bash
############################
# Help commands
############################
coverage run --include='uploader_cli/*,CLIUploader.py' CLIUploader.py --config travis/uploader.json --help
coverage run --include='uploader_cli/*,CLIUploader.py' -a CLIUploader.py --config=travis/uploader.json --help
export UPLOADER_CONFIG=travis/uploader.json
coverage run --include='uploader_cli/*,CLIUploader.py' -a CLIUploader.py query --help
coverage run --include='uploader_cli/*,CLIUploader.py' -a CLIUploader.py upload --help
coverage run --include='uploader_cli/*,CLIUploader.py' -a CLIUploader.py configure --help

############################
# Query commands
############################
coverage run --include='uploader_cli/*,CLIUploader.py' -a CLIUploader.py query -q instrument regex

############################
# Upload commands
############################
coverage run --include='uploader_cli/*,CLIUploader.py' -a CLIUploader.py upload --logon 10 --instrument 54 --proposal 1234a --user-of-record 11 file

############################
# Configure commands
############################
yes | coverage run --include='uploader_cli/*,CLIUploader.py' -a CLIUploader.py configure
printf '\r\r\rclientssl\r\r\r' | coverage run --include='uploader_cli/*,CLIUploader.py' -a CLIUploader.py configure

coverage report --show-missing --fail-under 100
if [[ $CODECLIMATE_REPO_TOKEN ]] ; then
  codeclimate-test-reporter
fi
