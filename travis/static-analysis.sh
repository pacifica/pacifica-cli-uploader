#!/bin/bash
pre-commit run --all-files
pylint --rcfile=pylintrc uploader bundler metadata *.py
radon cc uploader bundler metadata
