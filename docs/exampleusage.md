# Example Usage

There are many things to consider when packaging up yours or
someone elses data. We will help by going over some senerios we
have experienced in the past and their solutions.

## Example Configuration Output

```
$ pacifica-cli configure
Generating New Configuration.

Endpoints are an HTTP URL that looks similar to a website but
are designed for an uploader to interact with.

What are the endpoint URLs for the following...

Upload URL (https://ingest.example.com/upload):
Upload Status URL (https://ingest.example.com/get_state):
Upload Policy URL (https://policy.example.com/uploader):
Upload Validation URL (https://policy.example.com/ingest):
Download URL (https://cartd.example.com):
Download Policy URL (https://policy.example.com/status/transactions/by_id):

CA certificate bundle is the path to your certificate authority bundle.

Use this if you have a custom site SSL Certificate for your Site.

Valid values:
- True: verify the SSL server certificiate using system bundle
- False: do not verify the SSL server certificate (not recommended)
- a/path/to/a/cacert/bundle: custom path to the server certificate

CA Certificate Bundle (True):

There are three kinds of authentication types supported.

- clientssl - This is where you have an SSL client key and cert
- basic     - This is a username and password
- None      - Do not perform any authentication

Authentication Type (None): basic
Username (None): jdoe
Password (None): password
```

## Example Usage

### Download Examples

```
$ pacifica-cli download --destination down --transaction-id 1234
```

### Upload Examples

```
$ pacifica-cli upload --interactive test_file_upload.txt

Instrument ID - Select an ID
=====================================

54 Nittany Liquid Probes - NMR PROBES: Nittany Liquid Probes
104 Transmogriscope - Nanoscale Transmogriscope
Select ID (54): 54

Project ID - Select an ID
=====================================

1234a - Pacifica Development (active no close)
1235 - Pacifica Development (no close or end)
1236e - Pacifica Development (expired closed and end)
1237 - Pacifica Development (expired closed no end)
1238 - Pacifica Development (pre-active)
Select ID (1234a): 1234a
Done 10240.
Waiting job to complete (1).
Done.
{
    "created": "2017-09-26 01:32:34",
    "exception": "",
    "job_id": 1,
    "state": "OK",
    "task": "ingest metadata",
    "task_percent": "100.00000",
    "updated": "2017-09-26 01:32:36"
}
```
