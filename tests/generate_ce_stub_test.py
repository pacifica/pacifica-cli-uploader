#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Generate a CloudEvents stub used for testing."""
from hashlib import sha1
from os.path import join
from json import dumps


def main():
    """Main method when calling the module directly."""
    def sha1sum(text_data):
        """sha1sum the text_data and return string for sha1."""
        hashsum = sha1()
        hashsum.update(text_data)
        return hashsum.hexdigest()
    cloud_event_stub = {
        'data': [
            {
                'destinationTable': 'Files',
                '_id': 103,
                'name': 'foo.txt',
                'subdir': 'a/b',
                'hashsum': sha1sum(open('README.md').read().encode('utf8')),
                'hashtype': 'sha1'
            },
            {
                'destinationTable': 'Files',
                '_id': 104,
                'name': 'bar.txt',
                'subdir': 'a/b',
                'hashsum': sha1sum(open('README.md').read().encode('utf8')),
                'hashtype': 'sha1'
            }
        ]
    }
    with open(join('tests', 'ce_stub.json'), 'w') as ce_stub_fd:
        ce_stub_fd.write(dumps(cloud_event_stub))


if __name__ == '__main__':
    main()
