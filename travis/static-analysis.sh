#!/bin/bash
pre-commit run --all-files
pylint --rcfile=pylintrc cli *.py
radon cc uploader bundler metadata
