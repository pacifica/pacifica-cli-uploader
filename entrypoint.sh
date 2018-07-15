#!/bin/bash -e
RUN printf $UPLOAD_URL'\n'$STATE_URL'\n'$POLICY_URL'\nTrue\nNone\n' | CLIUploader configure
exec CLIUploader "$@"
