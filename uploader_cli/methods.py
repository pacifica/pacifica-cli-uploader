#!/usr/bin/python
"""Methods for the sub commands to run."""
from __future__ import absolute_import
from ConfigParser import ConfigParser
from os import makedirs
from os.path import expanduser, join, isfile, isdir
from .configure import configure_url_endpoints, configure_auth


def global_config_paths():
    """Return the global configuration path."""
    home = expanduser('~')
    pacifica_local_state = join(home, '.pacifica_cli')
    if not isdir(pacifica_local_state):
        makedirs(pacifica_local_state, 0700)
    return join(pacifica_local_state, 'config.ini')


def save_global_config(global_ini):
    """Save the global config to the path."""
    global_config = global_config_paths()
    global_ini.write(open(global_config, 'w'))


def generate_global_config():
    """Generate a default configuration."""
    global_config = global_config_paths()
    global_ini = ConfigParser()
    global_ini.add_section('endpoints')
    global_ini.set('endpoints', 'upload_url', 'https://ingest.example.com/upload')
    global_ini.set('endpoints', 'status_url', 'https://ingest.example.com/get_state')
    global_ini.set('endpoints', 'policy_url', 'https://policy.example.com/uploader')
    global_ini.add_section('authentication')
    global_ini.set('authentication', 'type', None)
    global_ini.set('authentication', 'username', None)
    global_ini.set('authentication', 'password', None)
    global_ini.set('authentication', 'cert', None)
    global_ini.set('authentication', 'key', None)
    if isfile(global_config):
        global_ini.read(global_config)
    else:
        print 'Generating New Configuration.'
    save_global_config(global_ini)
    return global_ini


def query_user_section():
    """Query the user for a section of config."""


def upload(args, config_data):
    """Upload the data based on bits."""
    print args
    print config_data


def query(args, config_data):
    """Query from the metadata configuration."""
    print args
    print config_data


def configure(args, config_data):
    """Configure the client by parsing current configuration."""
    global_ini = generate_global_config()
    configure_url_endpoints(global_ini)
    configure_auth(global_ini)
    print args
    print config_data
    save_global_config(global_ini)
