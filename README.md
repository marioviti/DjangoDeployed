# DjangoDeployed

Django (1.11) app with settings for deployements (python 2.7) on server with UWSGI and NGINX.

I'm following this guide:

http://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html

I had issues with installing uwsgi:
run this and than it works (only python 2.7).
```
sudo apt-get -y install build-essential python-dev zlib1g-dev libssl-dev
```
## structure

The project sits in a virtualenv

DjangoDeployed          #root of env
DjangoDeployed/mysite   # project

## to start

``` sudo service nginx start

source DjangoDeployed/bin/activate

cd DjangoDeployed/mysite

uwsgi --socket mysite.sock --module mysite.wsgi --chmod-socket=664
```
check the ip on the browser

## Troubleshooting

 *  #### Django not showing up.
    ##### Cause:
    if nginx default paga shows up it's because when not modified the default directory for sites
    falls back to defaults.
    ##### Solution:
    simply relink the config file
    sudo ``` ln -s  DjangoDeployed/mysite/mysite_nginx.conf /etc/nginx/sites-enabled/```

