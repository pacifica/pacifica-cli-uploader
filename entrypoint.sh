#!/bin/bash -e
cat > /etc/pacifica-cli/config.ini <<EOF
EOF
yes '' | pacifica-cli configure
exec pacifica-cli "$@"
