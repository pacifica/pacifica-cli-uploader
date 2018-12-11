CLI Options
===========

These are the command line options reference all the options are present
here and have a description.

Global Options
--------------

These options are common to all commands and affects behavior of the cli.

--verbose   This options requires an option which tells python
            logging what messages to print.

--config    This specifies the system metadata configuration
            for use when uploading data.

Download Sub-Command Options
----------------------------

The download sub-command requires interfacing with the cartd service.
The cart requires file metadata about what to download and there is
several methods for getting that file metadata.

--destination      Download the files to this folder (default to cwd).

--cloudevent       Use the cloudevents file from the notifications service to download.

--transaction-id   Setup a cart from this transaction ID.


Upload Sub-Command Options
--------------------------

There are two sets of options to the upload sub-command. The first comes
from the missing values in the metadata configuration json file. The
second are common for all uploads and will be documented further.

--follow-links     This will follow symlinked directories as you walk a directory tree
                   building the list of files to upload.

--nowait           The uploader will not wait for the successful or failed ingest of the
                   upload. Instead you will have to query for this information later.

--local-retry      Upload an already generated bundle by the `--local-save` option. This
                   option will honor the `--local-save` and `--tar-in-tar` options as
                   well.

--local-save       The uploader will save off a copy of the uploaded bundle of data. The
                   path is defined as the argument to the option.

--local-compress   Use a compression algorithm (gzip, bzip2) when creating the local save.


--tar-in-tar       A second bundler will be running generating a TAR in a TAR for upload.

--dry-run          Do just the query portion of the upload and print off what the metadata
                   will be set to. This will not upload or generate a local save or retry.

--interactive      Interact with the results of the query engine to manually select the
                   values for each metadata entry requested.

--do-not-upload    This forces the upload process to stop before uploading. This works
                   well with the --local-save option.
