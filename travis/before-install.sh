#!/bin/bash -xe
pip install -r requirements-dev.txt
psql -c 'create database pacifica_metadata;' -U postgres
export PEEWEE_URL="postgres://postgres:@127.0.0.1:5432/pacifica_metadata"
export METADATA_CPCONFIG="$PWD/travis/metadata/server.conf"
pacifica-metadata-cmd dbsync
pacifica-metadata &
echo $! > metadata.pid
export ARCHIVEINTERFACE_CONFIG="$PWD/travis/archivei/config.cfg"
export ARCHIVEINTERFACE_CPCONFIG="$PWD/travis/archivei/server.conf"
pacifica-archiveinterface &
echo $! > archiveinterface.pid
export UNIQUEID_CONFIG="$PWD/travis/uniqueid/config.cfg"
export UNIQUEID_CPCONFIG="$PWD/travis/uniqueid/server.conf"
pacifica-uniqueid-cmd dbsync
pacifica-uniqueid &
echo $! > uniqueid.pid
export CARTD_CONFIG="$PWD/travis/cartd/config.cfg"
export CARTD_CPCONFIG="$PWD/travis/cartd/server.conf"
pacifica-cartd-cmd dbsync
pacifica-cartd &
echo $! > cart.pid
celery -A pacifica.cartd.tasks worker --loglevel=info &
echo $! > cartd.pid
export INGEST_CONFIG="$PWD/travis/ingest/config.cfg"
export INGEST_CPCONFIG="$PWD/travis/ingest/server.conf"
pacifica-ingest-cmd dbsync
pacifica-ingest &
echo $! > ingest.pid
celery -A pacifica.ingest.tasks worker --loglevel=info &
echo $! > ingestd.pid
MAX_TRIES=60
HTTP_CODE=$(curl -sL -w "%{http_code}\\n" 'localhost:8066/get_state?job_id=42' -o /dev/null || true)
while [[ $HTTP_CODE != 404 && $MAX_TRIES > 0 ]] ; do
  sleep 1
  HTTP_CODE=$(curl -sL -w "%{http_code}\\n" 'localhost:8066/get_state?job_id=42' -o /dev/null || true)
  MAX_TRIES=$(( MAX_TRIES - 1 ))
done
MAX_TRIES=60
HTTP_CODE=$(curl -sL -w "%{http_code}\\n" localhost:8121/keys -o /dev/null || true)
while [[ $HTTP_CODE != 200 && $MAX_TRIES > 0 ]] ; do
  sleep 1
  HTTP_CODE=$(curl -sL -w "%{http_code}\\n" localhost:8121/keys -o /dev/null || true)
  MAX_TRIES=$(( MAX_TRIES - 1 ))
done
VERSION=$(pip show pacifica-metadata | grep Version: | awk '{ print $2 }')
TOP_DIR=$PWD
MD_TEMP=$(mktemp -d)
git clone https://github.com/pacifica/pacifica-metadata.git ${MD_TEMP}
pushd ${MD_TEMP}
git checkout v${VERSION}
python tests/test_files/loadit_test.py
popd
export POLICY_CPCONFIG="$PWD/travis/policy/server.conf"
pacifica-policy &
echo $! > policy.pid
curl -X PUT -H 'Last-Modified: Sun, 06 Nov 1994 08:49:37 GMT' --upload-file README.md http://127.0.0.1:8080/103
curl -X PUT -H 'Last-Modified: Sun, 06 Nov 1994 08:49:37 GMT' --upload-file README.md http://127.0.0.1:8080/104
readme_size=$(stat -c '%s' README.md)
readme_sha1=$(sha1sum README.md | awk '{ print $1 }')
echo '{ "hashsum": "'$readme_sha1'", "hashtype": "sha1", "size": '$readme_size'}' > /tmp/file-104-update.json
curl -X POST -H 'content-type: application/json' -T /tmp/file-104-update.json 'http://localhost:8121/files?_id=103'
curl -X POST -H 'content-type: application/json' -T /tmp/file-104-update.json 'http://localhost:8121/files?_id=104'
python tests/generate_ce_stub_test.py
