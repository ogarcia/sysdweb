# sysdweb
Control systemd services through Web or REST API

## Installation

```sh
git clone https://github.com/ogarcia/sysdweb.git
virtualenv3 ./sysdweb-venv
source ./sysdweb-venv/bin/activate
cd sysdweb
python setup.py install
```

Arch Linux users can install sysdweb from [AUR][1].

## Run

First take a look to `sysdweb.conf` file to configure sysdweb. Is self
explanatory.

Once you have configured sysdweb, simply run.

```
sysdweb
```

By default sysdweb listen in 10080 port to all hosts, you can change listen
port and address with `-p` and `-l`.

```sh
sysdweb -p 9080 -l 127.0.0.1
```

[1]: https://aur.archlinux.org/packages/sysdweb/
