#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Check the metadata for right metadata but not more."""
import json
import unittest


class MetadataContentTest(unittest.TestCase):
    """Test the metadata content."""

    @classmethod
    def setUpClass(cls):
        """Read the content of the metadata file and save it."""
        with open('metadata.txt', 'r') as md_fd:
            cls.meta = json.loads(md_fd.read())

    def test_query_results(self):
        """Test the json for query results that we've selected and nothing more."""
        for query_obj in self.meta:
            if query_obj['destinationTable'] == 'Files':
                continue
            self.assertEqual(len(query_obj['query_results']), 1, 'Length of query results should only be one value.')
            self.assertEqual(query_obj['query_results'][0][query_obj['valueField']],
                             query_obj['value'], 'Value of the query results should be the one we picked')


if __name__ == '__main__':
    unittest.main()
