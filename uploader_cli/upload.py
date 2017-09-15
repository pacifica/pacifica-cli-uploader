#!/usr/bin/python
"""The upload module used to send the data to ingest."""


def upload_main(args, _md_update):
    """Main upload method."""
    if args.dry_run:
        return
