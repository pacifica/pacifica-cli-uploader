# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.5.0] - 2020-02-05
### Added
- Pull #73 Add Python 3.7 and 3.8 by [dmlb2000](https://github.com/dmlb2000)
- Pull #70 Add Version Moodule by [dmlb2000](https://github.com/dmlb2000)
- Pull #68 Add JSONSchema Validation by [dmlb2000](https://github.com/dmlb2000)
- Pull #66 Add Kerberos/GSSAPI Authentication by [dmlb2000](https://github.com/dmlb2000)
- Fix #55 Add Basic Authentication Env Vars by [casey-pnnl](https://github.com/casey-pnnl)
### Changed
- Fix #52 Add File Not Found Error by [dmlb2000](https://github.com/dmlb2000)
- Fix #56 Resolve User Logon Always by [dmlb2000](https://github.com/dmlb2000)
- Fix #53 Add Env/CLI for config.ini by [dmlb2000](https://github.com/dmlb2000)
- Fix #61 Do not save during global read by [dmlb2000](https://github.com/dmlb2000)
- Pull #67 Add Ansible to Travis CI by [dmlb2000](https://github.com/dmlb2000)
- Pull #65 Updated Pylint 2.0+ by [dmlb2000](https://github.com/dmlb2000)
- Pull #64 Remove Python 2.7 by [dmlb2000](https://github.com/dmlb2000)
- Fix #51 Remove Query Results by [dmlb2000](https://github.com/dmlb2000)

## [0.4.0] - 2019-05-17
### Added
- Download of data from the cartd service
  - Using cloud events
  - Using metadata transaction ID
- Upload of data to the ingest service
  - Compressed and uncompressed options
  - Local save of data uploaded
  - Create bundle in bundle support
  - Data checksum validation
- ReadtheDocs supported Sphinx docs

### Changed
