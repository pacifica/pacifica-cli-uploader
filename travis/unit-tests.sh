#!/bin/bash
############################
# Setup
############################
sudo mkdir /etc/pacifica-cli
sudo cp config/example.ini /etc/pacifica-cli/config.ini
############################
# Help commands
############################
coverage run --include='pacifica/*' -m pacifica.cli --config travis/uploader.json --help
coverage run --include='pacifica/*' -a -m pacifica.cli --config=travis/uploader.json --help
export UPLOADER_CONFIG=travis/uploader.json
coverage run --include='pacifica/*' -a -m pacifica.cli upload --help
coverage run --include='pacifica/*' -a -m pacifica.cli configure --help

############################
# Configure commands
############################
yes | coverage run --include='pacifica/*' -a -m pacifica.cli configure
printf '\n\n\nTrue\nclientssl\n~/.pacifica-cli/my.key\n~/.pacifica-cli/my.cert\n' |
coverage run --include='pacifica/*' -a -m pacifica.cli configure
printf '\n\n\nFalse\nbasic\nusername\npassword\n' |
coverage run --include='pacifica/*' -a -m pacifica.cli configure

############################
# Build testing config
############################
printf 'http://localhost:8066/upload\nhttp://localhost:8066/get_state\nhttp://localhost:8181/uploader\nTrue\nNone\n' |
python -m pacifica.cli configure

############################
# Query commands
############################
coverage run --include='pacifica/*' -a -m pacifica.cli upload --dry-run --instrument 54 --logon dmlb2001
export PAGER=""
printf '\n\n\n\n' | coverage run --include='pacifica/*' -a -m pacifica.cli upload --dry-run --interactive --logon dmlb2001
export PAGER=cat
printf '\n\n\n\n' | coverage run --include='pacifica/*' -a -m pacifica.cli upload --dry-run --interactive --logon dmlb2001
printf '8192\n\n\n\n\n' | coverage run --include='pacifica/*' -a -m pacifica.cli upload --dry-run --interactive --logon dmlb2001
curl -X POST -H 'content-type: application/json' 'localhost:8121/users?_id=11' -d'{ "network_id": "'`whoami`'"}'
# this will fail...
coverage run --include='pacifica/*' -a -m pacifica.cli upload --dry-run --instrument 54 || true
coverage run --include='pacifica/*' -a -m pacifica.cli upload --dry-run --instrument 9876 || true
coverage run --include='pacifica/*' -a -m pacifica.cli upload --dry-run --logon dmlb2001 --proposal-regex 'expired closed and end'

############################
# Upload commands
############################
curl -X POST -H 'content-type: application/json' 'localhost:8121/users?_id=10' -d'{ "network_id": "'`whoami`'"}'
curl -X POST -H 'content-type: application/json' 'localhost:8121/users?_id=11' -d'{ "network_id": "someoneelse"}'
coverage run --include='pacifica/*' -a -m pacifica.cli upload README.md
coverage run --include='pacifica/*' -a -m pacifica.cli upload travis
coverage run --include='pacifica/*' -a -m pacifica.cli upload --tar-in-tar README.md
coverage run --include='pacifica/*' -a -m pacifica.cli upload --local-save retry.tar README.md
coverage run --include='pacifica/*' -a -m pacifica.cli upload --local-retry retry.tar
coverage run --include='pacifica/*' -a -m pacifica.cli upload --nowait README.md

############################
# PyTest coverage
############################
coverage run --include='pacifica/*' -a -m pytest -v

coverage report --show-missing --fail-under 100
if [[ $CODECLIMATE_REPO_TOKEN ]] ; then
  codeclimate-test-reporter
fi
