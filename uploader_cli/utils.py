#!/usr/bin/python
"""Utilities module for common methods."""
import sys
import logging
from os import makedirs, pathsep
from os.path import expanduser, join, isdir, isfile


logging.basicConfig()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel('DEBUG')


def system_config_path(config_file):
    """Return the system configuration path."""
    for config_dir_path in [join('{}etc'.format(pathsep), 'pacifica-cli'), join(sys.prefix, 'pacifica-cli')]:
        config_path = join(config_dir_path, config_file)
        LOGGER.debug('Trying system config %s', config_path)
        if isfile(config_path):
            return config_path
    return config_file


def user_config_path(config_file):
    """Return the global configuration path."""
    home = expanduser('~')
    pacifica_local_state = join(home, '.pacifica_cli')
    if not isdir(pacifica_local_state):
        makedirs(pacifica_local_state, 0700)
    return join(pacifica_local_state, config_file)
