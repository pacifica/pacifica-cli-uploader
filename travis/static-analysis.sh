#!/bin/bash
pre-commit run --all-files
radon cc uploader_cli *.py
