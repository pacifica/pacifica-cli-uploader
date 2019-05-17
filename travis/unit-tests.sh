#!/bin/bash
############################
# Setup
############################
sudo mkdir /etc/pacifica-cli
sudo cp config/example.ini /etc/pacifica-cli/config.ini
pip install .
cd tests
cp -r ../README.md ../travis .
############################
# Help commands
############################
COV_RUN="coverage run --include=*/site-packages/pacifica/cli/*"
$COV_RUN -m pacifica.cli --help
$COV_RUN -a -m pacifica.cli upload --help
$COV_RUN -a -m pacifica.cli download --help
$COV_RUN -a -m pacifica.cli --config ../travis/uploader.json --help
$COV_RUN -a -m pacifica.cli --config=../travis/uploader.json --help
export UPLOADER_CONFIG=$PWD/../travis/uploader.json
$COV_RUN -a -m pacifica.cli upload --help
$COV_RUN -a -m pacifica.cli download --help
$COV_RUN -a -m pacifica.cli configure --help
unset UPLOADER_CONFIG
cp $PWD/../travis/uploader.json ~/.pacifica_cli/uploader.json
$COV_RUN -a -m pacifica.cli upload --help
export UPLOADER_CONFIG=$PWD/../travis/uploader.json

############################
# Configure commands
############################
yes | $COV_RUN -a -m pacifica.cli configure
printf '\n\n\n\n\n\nTrue\nclientssl\n~/.pacifica-cli/my.key\n~/.pacifica-cli/my.cert\n' |
$COV_RUN -a -m pacifica.cli configure
printf '\n\n\n\n\n\nFalse\nbasic\nusername\npassword\n' |
$COV_RUN -a -m pacifica.cli configure

############################
# Build testing config
############################
printf 'http://localhost:8066/upload\nhttp://localhost:8066/get_state\nhttp://localhost:8181/uploader\nhttp://localhost:8181/ingest\nhttp://localhost:8081\nhttp://localhost:8181/status/transactions/by_id\nTrue\nNone\n' |
python -m pacifica.cli configure

############################
# Download commands
############################
$COV_RUN -a -m pacifica.cli download --transaction-id 67
$COV_RUN -a -m pacifica.cli download --cloudevent ce_stub.json

############################
# Query commands
############################
$COV_RUN -a -m pacifica.cli upload --dry-run --instrument 54 --logon dmlb2001
export PAGER=""
printf '\n\n\n\n' | $COV_RUN -a -m pacifica.cli upload --dry-run --interactive --logon dmlb2001
export PAGER=cat
printf '\n\n\n\n' | $COV_RUN -a -m pacifica.cli upload --dry-run --interactive --logon dmlb2001
printf '8192\n\n\n\n\n' | $COV_RUN -a -m pacifica.cli upload --dry-run --interactive --logon dmlb2001
curl -X POST -H 'content-type: application/json' 'localhost:8121/users?_id=11' -d'{ "network_id": "'`whoami`'"}'
# this will fail...
$COV_RUN -a -m pacifica.cli upload --dry-run --instrument 54 || true
$COV_RUN -a -m pacifica.cli upload --dry-run --instrument 9876 || true
$COV_RUN -a -m pacifica.cli upload --dry-run --local-save retry.tar --local-compress BLAH || true
$COV_RUN -a -m pacifica.cli upload --dry-run --logon dmlb2001 --project-regex 'expired closed and end'

############################
# Upload commands
############################
curl -X POST -H 'content-type: application/json' 'localhost:8121/users?_id=10' -d'{ "network_id": "'`whoami`'"}'
curl -X POST -H 'content-type: application/json' 'localhost:8121/users?_id=11' -d'{ "network_id": "someoneelse"}'
$COV_RUN -a -m pacifica.cli upload README.md
$COV_RUN -a -m pacifica.cli upload travis
$COV_RUN -a -m pacifica.cli upload --tar-in-tar README.md
$COV_RUN -a -m pacifica.cli upload --local-save retry.tar README.md
$COV_RUN -a -m pacifica.cli upload --local-save retry.tar --local-compress bzip2 README.md
$COV_RUN -a -m pacifica.cli upload --local-save retry.tar --local-compress gzip README.md
$COV_RUN -a -m pacifica.cli upload --local-save retry.tar --do-not-upload README.md
$COV_RUN -a -m pacifica.cli upload --local-retry retry.tar
$COV_RUN -a -m pacifica.cli upload --nowait README.md

############################
# PyTest coverage
############################
$COV_RUN -a -m pytest -v

coverage report --show-missing --fail-under 100
