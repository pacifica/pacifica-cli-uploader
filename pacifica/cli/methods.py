#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Methods for the sub commands to run."""
from __future__ import absolute_import, print_function
import logging
try:  # try loading python 2 module first
    from ConfigParser import ConfigParser
except ImportError:  # pragma: no cover python 3
    from configparser import ConfigParser
from getpass import getuser
from os import environ, getenv
from os.path import isfile
from json import loads
import requests
from pacifica.uploader.uploader import LOGGER as UP_LOGGER
from pacifica.uploader.metadata.policyquery import LOGGER as PQ_LOGGER
from pacifica.uploader.metadata import MetaUpdate
from pacifica.downloader import Downloader
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
    environ['POLICY_UPLOADER_URL'] = global_ini.get(
        'endpoints', 'upload_policy_url')
    environ['POLICY_INGEST_URL'] = global_ini.get(
        'endpoints', 'upload_validation_url')
    environ['INGEST_UPLOAD_URL'] = global_ini.get('endpoints', 'upload_url')
    environ['INGEST_STATUS_URL'] = global_ini.get(
        'endpoints', 'upload_status_url')


def generate_global_config():
    """Generate a default configuration."""
    user_config = user_config_path('config.ini')
    system_config = system_config_path('config.ini')
    global_ini = ConfigParser()
    global_ini.add_section('globals')
    global_ini.set('globals', 'interactive', 'False')
    global_ini.add_section('endpoints')
    global_ini.set(
        'endpoints', 'upload_url',
        getenv('UPLOAD_URL', 'https://ingest.example.com/upload')
    )
    global_ini.set(
        'endpoints', 'upload_status_url',
        getenv('UPLOAD_STATUS_URL', 'https://ingest.example.com/get_state')
    )
    global_ini.set(
        'endpoints', 'upload_policy_url',
        getenv('UPLOAD_POLICY_URL', 'https://policy.example.com/uploader')
    )
    global_ini.set(
        'endpoints', 'upload_validation_url',
        getenv('UPLOAD_VALIDATION_URL', 'https://policy.example.com/ingest')
    )
    global_ini.set(
        'endpoints', 'download_url',
        getenv('DOWNLOAD_URL', 'https://cartd.example.com')
    )
    global_ini.set(
        'endpoints', 'download_policy_url',
        getenv('DOWNLOAD_POLICY_URL',
               'https://policy.example.com/status/transactions/by_id')
    )
    global_ini.set('endpoints', 'ca_bundle', 'True')
    global_ini.add_section('authentication')
    global_ini.set(
        'authentication', 'type',
        getenv('AUTHENTICATION_TYPE', 'None')
    )
    global_ini.set(
        'authentication', 'username',
        getenv('AUTHENTICATION_USERNAME', '')
    )
    global_ini.set(
        'authentication', 'password',
        getenv('AUTHENTICATION_PASSWORD', '')
    )
    global_ini.set(
        'authentication', 'cert',
        getenv('AUTHENTICATION_CERT', '')
    )
    global_ini.set(
        'authentication', 'key',
        getenv('AUTHENTICATION_KEY', '')
    )
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


def download(args, _interface_data):
    """Download data specified in args."""
    set_verbose(args.verbose)
    global_ini = generate_global_config()
    auth = generate_requests_auth(global_ini)
    dl_obj = Downloader(
        cart_api_url=global_ini.get('endpoints', 'download_url'),
        auth=auth
    )
    if args.trans_id:
        resp = requests.get('{}/{}'.format(global_ini.get('endpoints',
                                                          'download_policy_url'), args.trans_id), **auth)
        assert resp.status_code == 200
        return dl_obj.transactioninfo(args.destination, resp.json())
    return dl_obj.cloudevent(args.destination, loads(args.cloudevent.read()))


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
