#!/bin/bash
pre-commit run --all-files
pylint --rcfile=pylintrc pacifica/uploader/cli *.py
radon cc pacifica/uploader/cli *.py
