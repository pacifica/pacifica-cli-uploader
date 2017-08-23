#!/usr/bin/python
"""The CLI module contains all the logic needed to run a CLI."""
import sys
import argparse
from os import getenv
from pacifica.uploader.metadata import metadata_decode
from .methods import query, upload, configure


def mangle_config_argument(argv):
    """Get the config argument out of argv and return stripped version."""
    config_arg = '--config'
    len_arg = len(config_arg)
    starts_argv = [arg[:len_arg] for arg in argv]
    if config_arg in starts_argv:
        if config_arg in argv:
            config_file = argv[argv.index(config_arg)+1]
            del argv[argv.index(config_arg)+1]
            del argv[argv.index(config_arg)]
        else:
            config_file = argv[starts_argv.index(config_arg)][len_arg+1:]
            del argv[starts_argv.index(config_arg)]
        return (config_file, argv)
    return (None, argv)


def main():
    """Main method to deal with command line argument parsing."""
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='sub-command help')
    upload_parser = subparsers.add_parser('upload', help='upload help', description='perform upload')
    query_parser = subparsers.add_parser('query', help='query help', description='perform query')
    config_parser = subparsers.add_parser('configure', help='configure help', description='setup configuration')

    default_config = getenv('UPLOADER_CONFIG', 'uploader.json')
    config_file, argv = mangle_config_argument(sys.argv)
    if not config_file:
        config_file = default_config
    config_data = metadata_decode(open(config_file).read())
    query_choices = []
    for config_part in config_data:
        if not config_part.value:
            upload_parser.add_argument(
                '--{}'.format(config_part.metaID), '-{}'.format(config_part.metaID[0]),
                help=config_part.displayTitle, required=True
            )
            query_choices.append(config_part.metaID)
    query_parser.add_argument(
        '--query', '-q', choices=query_choices, required=True,
        help='Query on the metadata for results.'
    )

    query_parser.add_argument(
        'regex', metavar='REGEX',
        help='regular expression over the returned data.'
    )
    query_parser.set_defaults(func=query)
    upload_parser.add_argument(
        'files', metavar='FILES', nargs='+', help='files you want to upload.'
    )
    upload_parser.set_defaults(func=upload)
    config_parser.set_defaults(func=configure)

    args = parser.parse_args(argv[1:])
    args.func(args, config_data)
