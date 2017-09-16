#!/bin/bash
############################
# Setup
############################
sudo mkdir /etc/pacifica-cli
sudo cp config/example.ini /etc/pacifica-cli/config.ini
############################
# Help commands
############################
coverage run --include='uploader_cli/*,CLIUploader.py' CLIUploader.py --config travis/uploader.json --help
coverage run --include='uploader_cli/*,CLIUploader.py' -a CLIUploader.py --config=travis/uploader.json --help
export UPLOADER_CONFIG=travis/uploader.json
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
coverage run --include='uploader_cli/*,CLIUploader.py' -a CLIUploader.py upload --dry-run --instrument 54 --logon dmlb2001
coverage run --include='uploader_cli/*,CLIUploader.py' -a CLIUploader.py upload --dry-run --interactive --logon dmlb2001
curl -X POST -H 'content-type: application/json' 'localhost:8121/users?_id=11' -d'{ "network_id": "'`whoami`'"}'
# this will fail...
coverage run --include='uploader_cli/*,CLIUploader.py' -a CLIUploader.py --verbose debug upload --dry-run --instrument 54 || true

############################
# Upload commands
############################
coverage run --include='uploader_cli/*,CLIUploader.py' -a CLIUploader.py upload --logon 10 --instrument 54 --proposal 1234a --user-of-record 11 file.txt

############################
# PyTest coverage
############################
coverage run --include='uploader_cli/*,CLIUploader.py' -a -m pytest -v

coverage report --show-missing --fail-under 100
if [[ $CODECLIMATE_REPO_TOKEN ]] ; then
  codeclimate-test-reporter
fi
