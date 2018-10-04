#!/bin/bash -e
printf $UPLOAD_URL'\n'$STATE_URL'\n'$POLICY_URL'\nTrue\nNone\n' | pacifica-cli configure
exec pacifica-cli "$@"
