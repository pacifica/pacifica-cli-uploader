#!/usr/bin/python
"""Methods for the sub commands to run."""
from __future__ import absolute_import, print_function
import logging
from ConfigParser import ConfigParser
from getpass import getuser
from os import environ
from os.path import isfile
from uploader.Uploader import LOGGER as UP_LOGGER
from uploader.metadata.PolicyQuery import LOGGER as PQ_LOGGER
from uploader.metadata import MetaUpdate
from .configure import configure_url_endpoints, configure_auth, configure_ca_bundle
from .query import query_main
from .upload import upload_main
from .upload import LOGGER as UPC_LOGGER
from .utils import system_config_path, user_config_path


logging.basicConfig()
LOGGER = logging.getLogger(__name__)


def set_verbose(verbose):
    """Set the log level to arg value."""
    UP_LOGGER.setLevel(verbose.upper())
    PQ_LOGGER.setLevel(verbose.upper())
    UPC_LOGGER.setLevel(verbose.upper())
    LOGGER.setLevel(verbose.upper())


def save_user_config(global_ini):
    """Save the global config to the path."""
    user_config = user_config_path('config.ini')
    global_ini.write(open(user_config, 'w'))


def set_environment_vars(global_ini):
    """Set some environment variables to be used later."""
    environ['POLICY_URL'] = global_ini.get('endpoints', 'policy_url')
    environ['INGEST_UPLOAD_URL'] = global_ini.get('endpoints', 'upload_url')
    environ['INGEST_STATUS_URL'] = global_ini.get('endpoints', 'status_url')


def generate_global_config():
    """Generate a default configuration."""
    user_config = user_config_path('config.ini')
    system_config = system_config_path('config.ini')
    global_ini = ConfigParser()
    global_ini.add_section('globals')
    global_ini.set('globals', 'interactive', 'False')
    global_ini.add_section('endpoints')
    global_ini.set('endpoints', 'upload_url', 'https://ingest.example.com/upload')
    global_ini.set('endpoints', 'status_url', 'https://ingest.example.com/get_state')
    global_ini.set('endpoints', 'policy_url', 'https://policy.example.com/uploader')
    global_ini.set('endpoints', 'ca_bundle', 'True')
    global_ini.add_section('authentication')
    global_ini.set('authentication', 'type', None)
    global_ini.set('authentication', 'username', None)
    global_ini.set('authentication', 'password', None)
    global_ini.set('authentication', 'cert', None)
    global_ini.set('authentication', 'key', None)
    LOGGER.debug('System Config: %s', system_config)
    LOGGER.debug('User Config: %s', user_config)
    if isfile(system_config):
        global_ini.read(system_config)
    if isfile(user_config):
        global_ini.read(user_config)
    else:
        print('Generating New Configuration.')
    save_user_config(global_ini)
    set_environment_vars(global_ini)
    return global_ini


def verify_type(obj):
    """
    Convert obj to requests verify argument.

    Verify the type of obj that it will be consumed by requests
    verify option correctly.
    """
    if obj in ['True', 'False']:
        return obj == 'True'
    if isfile(str(obj)):
        return str(obj)
    raise ValueError('{} is not a valid bool or file.'.format(obj))


def generate_requests_auth(global_ini):
    """Generate arguments to requests for authentication."""
    auth_type = global_ini.get('authentication', 'type')
    ret = {}
    if auth_type == 'clientssl':
        ret = {
            'cert': (
                global_ini.get('authentication', 'cert'),
                global_ini.get('authentication', 'key')
            )
        }
    elif auth_type == 'basic':
        ret = {
            'auth': (
                global_ini.get('authentication', 'username'),
                global_ini.get('authentication', 'password')
            )
        }
    ret['verify'] = verify_type(global_ini.get('endpoints', 'ca_bundle'))
    return ret


def upload(args, interface_data):
    """Upload the data based on bits."""
    md_update = query(args, interface_data)
    return upload_main(md_update, args)


def query(args, interface_data):
    """Query from the metadata configuration."""
    set_verbose(args.verbose)
    global_ini = generate_global_config()
    auth = generate_requests_auth(global_ini)
    user_name = getattr(args, 'logon', None)
    if not user_name:
        user_name = getuser()
    md_update = MetaUpdate(user_name, auth=auth)
    md_update.extend(interface_data)
    return query_main(md_update, args)


def configure(_args, _config_data):
    """Configure the client by parsing current configuration."""
    global_ini = generate_global_config()
    configure_url_endpoints(global_ini)
    configure_ca_bundle(global_ini)
    configure_auth(global_ini)
    save_user_config(global_ini)
