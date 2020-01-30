#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Pacifica CLI Version Module."""
from pkg_resources import get_distribution, DistributionNotFound

try:
    __version__ = get_distribution('pacifica-cli').version
except DistributionNotFound:  # pragma: no cover not sure how to test this
    # package is not installed
    pass
