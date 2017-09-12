#!/usr/bin/python
"""Methods for the sub commands to run."""
from __future__ import absolute_import
from ConfigParser import ConfigParser
from getpass import getuser
from os import makedirs, environ
from os.path import expanduser, join, isfile, isdir
from uploader.metadata import MetaUpdate
from .configure import configure_url_endpoints, configure_auth
from .query import query_main


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


def set_environment_vars(global_ini):
    """Set some environment variables to be used later."""
    for var in ['upload_url', 'status_url', 'policy_url']:
        value = global_ini.get('endpoints', var)
        environ[var.upper()] = value


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
    set_environment_vars(global_ini)
    return global_ini


def generate_requests_auth(global_ini):
    """Generate arguments to requests for authentication."""
    auth_type = global_ini.get('authentication', 'type')
    if auth_type == 'clientssl':
        return {
            'cert': (
                global_ini.get('authentication', 'cert'),
                global_ini.get('authentication', 'key')
            )
        }
    elif auth_type == 'basic':
        return {
            'auth': (
                global_ini.get('authentication', 'username'),
                global_ini.get('authentication', 'password')
            )
        }
    return {}


def upload(args, interface_data):
    """Upload the data based on bits."""
    # global_ini = generate_global_config()
    print args.upload
    print interface_data


def query(args, interface_data):
    """Query from the metadata configuration."""
    global_ini = generate_global_config()
    auth = generate_requests_auth(global_ini)
    md_update = MetaUpdate(getuser(), auth=auth)
    md_update.extend(interface_data)
    query_main(md_update, args)


def configure(args, config_data):
    """Configure the client by parsing current configuration."""
    global_ini = generate_global_config()
    configure_url_endpoints(global_ini)
    configure_auth(global_ini)
    save_global_config(global_ini)
