#!/bin/bash -e
cat > /etc/pacifica-cli/config.ini <<EOF
EOF
y | pacifica-cli configure
exec pacifica-cli "$@"
