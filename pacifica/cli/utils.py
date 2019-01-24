#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Utilities module for common methods."""
import sys
from os import makedirs, sep
from os.path import expanduser, join, isdir, isfile


def system_config_path(config_file):
    """Return the system configuration path."""
    for config_dir_path in [join('{}etc'.format(sep), 'pacifica-cli'), join(sys.prefix, 'pacifica-cli')]:
        config_path = join(config_dir_path, config_file)
        if isfile(config_path):
            return config_path
    return config_file


def user_config_path(config_file):
    """Return the global configuration path."""
    home = expanduser('~')
    pacifica_local_state = join(home, '.pacifica_cli')
    if not isdir(pacifica_local_state):
        makedirs(pacifica_local_state, 0o700)
    return join(pacifica_local_state, config_file)


def compressor_generator(compressor_type):
    """Return a compressor based on type, bzip2, gzip."""
    class Compressor(object):
        """Compressor object has consistent interface for compressing data."""

        def __init__(self):
            """Constructor to build the appropriate compressor type."""
            if compressor_type == 'bzip2':
                from bz2 import BZ2Compressor
                self._comp = BZ2Compressor(9)
                self._comp_func = self._comp.compress
                self._flush_passthru = False
            elif compressor_type == 'gzip':
                from zlib import compress
                self._comp = None
                self._comp_func = lambda x: compress(x, 9)
                self._flush_passthru = True
            else:
                self._comp = None
                self._comp_func = lambda x: x
                self._flush_passthru = True

        def compress(self, buf):
            """Compress the data and return it."""
            return self._comp_func(buf)

        def flush(self):
            """Flush the data internally if required."""
            if self._flush_passthru:
                return bytearray()
            return self._comp.flush()
    return Compressor()
