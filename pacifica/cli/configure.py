#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Methods for configuring the client."""
from __future__ import print_function
from sys import stdin, stdout

__all__ = [
    'configure_url_endpoints',
    'configure_ca_bundle',
    'configure_auth'
]


def configure_url_endpoints(global_ini):
    """Query and set the URL endpoints."""
    print("""
Endpoints are an HTTP URL that looks similar to a website but
are designed for an uploader to interact with.

What are the endpoint URLs for the following...
""")
    for endpnt in ['upload', 'upload_status', 'upload_policy', 'upload_validation', 'download', 'download_policy']:
        default_url = global_ini.get('endpoints', '{}_url'.format(endpnt))
        endpnt_nice = ' '.join([
            part.capitalize() for part in endpnt.split('_')
        ])
        stdout.write('{} URL ({}): '.format(endpnt_nice, default_url))
        stdout.flush()
        strip_input = stdin.readline().strip()
        if strip_input:
            global_ini.set('endpoints', '{}_url'.format(endpnt), strip_input)


def configure_ca_bundle(global_ini):
    """Query for the ca bundle when using https."""
    default_verify = global_ini.get('endpoints', 'ca_bundle')
    print("""
CA certificate bundle is the path to your certificate authority bundle.

Use this if you have a custom site SSL Certificate for your Site.

Valid values:
- True: verify the SSL server certificiate using system bundle
- False: do not verify the SSL server certificate (not recommended)
- a/path/to/a/cacert/bundle: custom path to the server certificate
""")
    stdout.write('CA Certificate Bundle ({}): '.format(default_verify))
    stdout.flush()
    strip_input = stdin.readline().strip()
    if strip_input:
        global_ini.set('endpoints', 'ca_bundle', strip_input)


def configure_client_ssl(global_ini):
    """Query and set the client ssl key and cert."""
    for ssl_part in ['key', 'cert']:
        default_cfg = global_ini.get('authentication', ssl_part)
        stdout.write('Client {} ({}): '.format(
            ssl_part.capitalize(), default_cfg))
        stdout.flush()
        strip_input = stdin.readline().strip()
        if strip_input:
            global_ini.set('authentication', ssl_part, strip_input)


def configure_basic_auth(global_ini):
    """Query and set the client ssl key and cert."""
    for auth_part in ['username', 'password']:
        default_cfg = global_ini.get('authentication', auth_part)
        stdout.write('{} ({}): '.format(auth_part.capitalize(), default_cfg))
        stdout.flush()
        strip_input = stdin.readline().strip()
        if strip_input:
            global_ini.set('authentication', auth_part, strip_input)


def configure_auth(global_ini):
    """Query and set the authentication configuration."""
    print("""
There are three kinds of authentication types supported.

- clientssl - This is where you have an SSL client key and cert
- basic     - This is a username and password
- None      - Do not perform any authentication
""")
    default_auth_type = global_ini.get('authentication', 'type')
    stdout.write('Authentication Type ({}): '.format(default_auth_type))
    stdout.flush()
    strip_input = stdin.readline().strip()
    if strip_input and strip_input in ['clientssl', 'basic', 'None']:
        global_ini.set('authentication', 'type', strip_input)
    auth_type = global_ini.get('authentication', 'type')
    if auth_type == 'clientssl':
        configure_client_ssl(global_ini)
    elif auth_type == 'basic':
        configure_basic_auth(global_ini)
