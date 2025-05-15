# mouth2_oc
[![pypi version](https://img.shields.io/pypi/v/mouth2-oc.svg)](https://pypi.org/project/mouth2-oc) ![Custom License](https://img.shields.io/pypi/l/mouth2-oc.svg)

[body_oc](https://pypi.org/project/body-oc/) 2.0 service that handles outgoing
communications like emails and sms messages.

Please see [LICENSE](https://github.com/ouroboroscoding/mouth2/blob/main/LICENSE)
for further information.

# Requires
mouth2_oc requires python 3.10 or higher

# Install
```bash
pip install mouth2_oc
```

##### mouth.send_error_emails
If true, error emails will be sent to the address in `config.email.error_to`
whenever a request to mouth causes an uncaught exception.

##### mouth.verbose
If `true` all requests to mouth and the corresponding response will be printed
to stdout.

## Install Tables and Records
After installing the module into the project via pip, you will need to install
the tables to your database.

```console
(myenv) foo@bar:~$ mouth install
Installing tables
Setting lastest version
Do you want to install default brain templates? [y]es / [n]o: y
Installing templates
Done
(myenv) foo@bar:~$
```

## Upgrade Tables and Records
If you upgrade to a new version of mouth2_oc be sure to run the upgrade script.
This will ensure any data and tables are up to date with the version.

```console
(myenv) foo@bar:~$ mouth upgrade
Already up to date
(myenv) foo@bar:~$
```

# RESTlike Documentation
For full documentation on the individual requests avaialable via the service,
check the [RESTlike](https://github.com/ouroboroscoding/mouth2/blob/main/rest.md)
docs.