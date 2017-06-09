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

# Developing

Initialize DB
```
python manage.py migrate
```
Create a super user
```
python manage.py createsuperuser
```
follow instruction and login to the admin panel to check if credentials works ```<your IP>/admin```

## create an app and first model
```
python manage.py startapp posts
```

creates an app within a folder named after the app (posts).


First list it under the others to the INSTALLED_APPS dictionary in ```DjangoDeployed/mysite/mysite/settings.py```

### the model

A model is a class permitting django to create foramtted tables in the database: to create one modify posts/models.py
and add the desired model(class->table) i.e:

```
class Post(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    """python 2.7"""
    def __unicode__(self):
        return self.title

    """ pythot 3.0 """
    def __str__(self):
        return self.title

```

to apply changes 
```
python manage.py makemigrations
python manage.py migrate
```
