# sysdweb
Control systemd services through Web or REST API

## Installation

### Prerequisites

If you are a Ubuntu/Debian user you need to install `libsystemd-dev`, for
CentOS users the package is `systemd-devel`.

### From source

```sh
git clone https://github.com/ogarcia/sysdweb.git
virtualenv3 ./sysdweb-venv
source ./sysdweb-venv/bin/activate
cd sysdweb
pip install .
```

### From pypi

```sh
virtualenv3 ./sysdweb-venv
source ./sysdweb-venv/bin/activate
pip install sysdweb
```

### For Arch Linux users

Arch Linux users can install sysdweb from [AUR][1].

## Run

First take a look to `sysdweb.conf` file to configure sysdweb. Is self
explanatory.

You can place `sysdweb.conf` in `/etc` for system, in user home
`~/.config/sysdweb/sysdweb.conf` or in same directory where you run sysdweb.

Once you have configured sysdweb, simply run.

```
sysdweb
```

By default sysdweb listen in 10088 port to 127.0.0.1, you can change listen
port and address with `-p` and `-l` or via environment variables.

```sh
sysdweb -p 9080 -l 0.0.0.0
```

Current config environment variables are the following.

| Variable | Description |
| --- | --- |
| `SYSDWEB_CONFIG` | Config file location |
| `SYSDWEB_HOST` | Listen address |
| `SYSDWEB_PORT` | Listen port |
| `SYSDWEB_LOGLEVEL` | Log level, effective values are `WARNING`, `INFO` and `DEBUG` |

## API

You can control configured services via REST API, for example, with curl.

The API endpoint is `/api/v1/<service>/<action>`, always `GET` and response
a json with following format.

```json
{
  "<action>": "<result>"
}
```

The `<service>` tag is defined in config file and match with section label.
For example, in following config, the service would be `ngx`.

```ini
[ngx]
title = Nginx
unit = nginx.service
```

The posible `<actions>` are.

* start
* stop
* restart
* reload
* reloadorrestart
* status
* journal

All actions (except `status` and `journal`) return as result `OK` if can
communicate with DBUS or `Fail` if any error occurs.

For `status` action, the posible responses are.

* active (started unit)
* reloading
* inactive (stopped unit)
* failed (stopped unit)
* activating
* deactivating
* not-found (for inexistent unit)

By default `/api/v1/<service>/journal` returns 100 tail lines of journal
file of `<service>` unit. You can specify the number of lines by this way.

```
/api/v1/<service>/journal/200
```

In the example defined above all valid endpoints are.

```
http://127.0.0.1:10088/api/v1/ngx/start
http://127.0.0.1:10088/api/v1/ngx/stop
http://127.0.0.1:10088/api/v1/ngx/restart
http://127.0.0.1:10088/api/v1/ngx/reload
http://127.0.0.1:10088/api/v1/ngx/reloadorrestart
http://127.0.0.1:10088/api/v1/ngx/status
http://127.0.0.1:10088/api/v1/ngx/journal
http://127.0.0.1:10088/api/v1/ngx/journal/<number>
```

[1]: https://aur.archlinux.org/packages/sysdweb/
