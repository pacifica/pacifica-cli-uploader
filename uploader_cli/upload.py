#!/usr/bin/python
"""The upload module used to send the data to ingest."""


def upload_main(_md_update, args):
    """Main upload method."""
    if args.dry_run:
        return
