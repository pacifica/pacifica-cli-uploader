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
# Configure commands
############################
yes | coverage run --include='uploader_cli/*,CLIUploader.py' -a CLIUploader.py configure
printf '\n\n\nclientssl\n~/.pacifica-cli/my.key\n~/.pacifica-cli/my.cert\n' |
coverage run --include='uploader_cli/*,CLIUploader.py' -a CLIUploader.py configure
printf '\n\n\nbasic\nusername\npassword\n' |
coverage run --include='uploader_cli/*,CLIUploader.py' -a CLIUploader.py configure

############################
# Build testing config
############################
printf 'http://localhost:8066/upload\nhttp://localhost:8066/get_state\nhttp://localhost:8181/uploader\nNone\n' |
python CLIUploader.py configure

############################
# Query commands
############################
coverage run --include='uploader_cli/*,CLIUploader.py' -a CLIUploader.py query --instrument 54 --logon dmlb2001

############################
# Upload commands
############################
coverage run --include='uploader_cli/*,CLIUploader.py' -a CLIUploader.py upload --logon 10 --instrument 54 --proposal 1234a --user-of-record 11 file

############################
# PyTest coverage
############################
coverage run --include='uploader_cli/*,CLIUploader.py' -m pytest -v

coverage report --show-missing --fail-under 100
if [[ $CODECLIMATE_REPO_TOKEN ]] ; then
  codeclimate-test-reporter
fi
