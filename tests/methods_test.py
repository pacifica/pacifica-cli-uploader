#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the methods module for things we need to test."""
from unittest import TestCase
try:  # python 2 import
    from ConfigParser import ConfigParser
except ImportError:  # pragma: no cover python 3 import
    from configparser import ConfigParser
from pacifica.cli.methods import generate_requests_auth, verify_type


# pylint: disable=too-few-public-methods
class ConfigClient(object):
    """Class to generate sample config."""

    def __init__(self, auth_type):
        """Construct the config client stub object."""
        self.auth_type = auth_type
        self.config = None

    def __enter__(self):
        """Create a config parser object with appropriate values."""
        config = ConfigParser()
        config.add_section('endpoints')
        config.set('endpoints', 'ca_bundle', 'True')
        config.add_section('authentication')
        config.set('authentication', 'type', self.auth_type)
        config.set('authentication', 'username', 'username')
        config.set('authentication', 'password', 'password')
        config.set('authentication', 'key', 'key')
        config.set('authentication', 'cert', 'cert')
        self.config = config
        return config

    def __exit__(self, exec_type, _exec_value, _exec_traceback):
        """Exit the code using the config parser."""
        return exec_type is None
# pylint: enable=too-few-public-methods


class TestMethods(TestCase):
    """Test methods that require no state."""

    def test_gen_req_auth(self):
        """Test the requests authentication generator."""
        with ConfigClient('clientssl') as conf:
            self.assertTrue('cert' in generate_requests_auth(conf))
            self.assertEqual(generate_requests_auth(conf)['cert'][0], 'cert')
            self.assertTrue(generate_requests_auth(conf)['cert'][1], 'key')
            self.assertTrue(generate_requests_auth(conf)['verify'], 'True')
        with ConfigClient('basic') as conf:
            self.assertTrue('auth' in generate_requests_auth(conf))
            self.assertTrue(generate_requests_auth(conf)
                            ['auth'][0], 'username')
            self.assertTrue(generate_requests_auth(conf)['auth'], 'password')

    def test_verify_type(self):
        """Test the verify_type method to cover everything."""
        self.assertEqual(verify_type('True'), True)
        self.assertEqual(verify_type('False'), False)
        self.assertEqual(verify_type('README.md'), 'README.md')
        hit_exception = False
        try:
            verify_type('blarg')
        except ValueError:
            hit_exception = True
        self.assertTrue(hit_exception)
