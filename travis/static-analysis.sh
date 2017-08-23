#!/bin/bash
pre-commit run --all-files
pylint --rcfile=pylintrc uploader_cli *.py
radon cc uploader_cli *.py
