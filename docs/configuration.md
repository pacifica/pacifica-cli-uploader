# Configuration

The `configure` subcommand generates a local configuration file for the
user. It will read the system configuration to preseed its defaults and
asks the user to enter the values required. An example configuration is
located [here](_static/example.ini).

The system configuration is processed first and the two directories are,
`/etc/pacifica-cli/config.ini` then
`PYTHON_PREFIX/pacifica-cli/config.ini`. Which ever is found first the
client uses that as the system default.

The user configuration is processed second, if found. The directory the
client looks in by default is `~/.pacifica_cli/config.ini`. The `~`
translates to the users home directory on any platform.

## System Metadata

The metadata is managed by a JSON configuration file referenced by an
environment variable `UPLOADER_CONFIG`. By default the environment
variable is set to `uploader.json`. However, it could be managed at a
system level or changed on the command line by the `--config` option.

The directories the `UPLOADER_CONFIG` are looked for in order are:

 - `/etc/pacifica-cli/uploader.json`
 - `VIRTUAL_ENV_ROOT/pacifica-cli/uploader.json`
 - `~/.pacifica_cli/uploader.json`
 - `$PWD/uploader.json`

The command line is evaluated last so it will override any of the
previous paths.

The contents of the metadata configuration file is complex and should
be read from
[here](https://pacifica-uploader.readthedocs.io/en/latest/metadataconfig.html).
Please get your systems administrator to help create this file for you.
An example to start from is [here](_static/uploader.json).
