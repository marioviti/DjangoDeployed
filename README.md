# DjangoDeployed

Django app with settings for deployements (python 2.7)

I'm following this guide:

http://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html#emperor-mode

I had issues with installing uwsgi
run this and than it works (only python 2.7)
sudo apt-get -y install build-essential python-dev zlib1g-dev libssl-dev

## to start

sudo service nginx start

uwsgi --socket mysite.sock --module mysite.wsgi --chmod-socket=664


