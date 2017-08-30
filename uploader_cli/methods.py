#!/usr/bin/python
"""Methods for the sub commands to run."""
from sys import stdin, stdout
from ConfigParser import ConfigParser
from os import makedirs
from os.path import expanduser, join, isfile, isdir


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


def configure_url_endpoints(global_ini):
    """Query and set the URL endpoints."""
    print """
Endpoints are an HTTP URL that looks similar to a website but
are designed for an uploader to interact with.

What are the endpoint URLs for the following...
"""
    for endpnt in ['upload', 'status', 'policy']:
        default_url = global_ini.get('endpoints', '{}_url'.format(endpnt))
        stdout.write('{} URL ({}): '.format(endpnt.capitalize(), default_url))
        strip_input = stdin.readline().strip()
        if strip_input:
            global_ini.set('endpoints', '{}_url'.format(endpnt), strip_input)


def configure_client_ssl(global_ini):
    """Query and set the client ssl key and cert."""
    for ssl_part in ['key', 'cert']:
        default_cfg = global_ini.get('authentication', ssl_part)
        stdout.write('Client {} ({}): '.format(ssl_part.capitalize(), default_cfg))
        strip_input = stdin.readline().strip()
        if strip_input:
            global_ini.set('authentication', ssl_part, strip_input)


def configure_basic_auth(global_ini):
    """Query and set the client ssl key and cert."""
    for auth_part in ['username', 'password']:
        default_cfg = global_ini.get('authentication', auth_part)
        stdout.write('{} ({}): '.format(auth_part.capitalize(), default_cfg))
        strip_input = stdin.readline().strip()
        if strip_input:
            global_ini.set('authentication', auth_part, strip_input)


def configure_auth(global_ini):
    """Query and set the authentication configuration."""
    print """
There are three kinds of authentication types supported.

- clientssl - This is where you have an SSL client key and cert
- basic     - This is a username and password
- None      - Do not perform any authentication
"""
    default_auth_type = global_ini.get('authentication', 'type')
    stdout.write('Authentication Type ({}): '.format(default_auth_type))
    strip_input = stdin.readline().strip()
    if strip_input and strip_input in ['clientssl', 'basic', 'None']:
        global_ini.set('authentication', 'type', strip_input)
    auth_type = global_ini.get('authentication', 'type')
    if auth_type == 'clientssl':
        configure_client_ssl(global_ini)
    elif auth_type == 'basic':
        configure_basic_auth(global_ini)


def configure(args, config_data):
    """Configure the client by parsing current configuration."""
    global_ini = generate_global_config()
    configure_url_endpoints(global_ini)
    configure_auth(global_ini)
    print args
    print config_data
    save_global_config(global_ini)
