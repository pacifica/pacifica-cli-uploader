#!/bin/bash -xe

if [ "$RUN_LINTS" = "true" ] ; then
  bash -xe ./travis/static-analysis.sh
else
  bash -xe ./travis/unit-tests.sh
  bash -xe ./travis/test-deploy.sh
fi
