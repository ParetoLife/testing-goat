How to setup a new server
=========================

## Dependencies

* nginx
* python 3.6
* pip
* git

## Setting up Nginx

Template can be found in template.nginx.conf.
Replace DOMAIN with your actual domain.
Put the template in `/etc/nginx/conf.d/`
Ensure that your config is working by running `nginx -t`

## Setting up gunicorn systemd service

See template.gunicorn-systemd.service for a template.
Replace DOMAIN and USER in the template.

## Directory structure

Assuming you put the sites at the root of your user account:

```bash
/home/username
└── sites
    ├── DOMAIN1
    │    ├── .env
    │    ├── db.sqlite3
    │    ├── manage.py etc
    │    ├── static
    │    └── venv
    └── DOMAIN2
         ├── .env
         ├── db.sqlite3
         ├── etc
```
