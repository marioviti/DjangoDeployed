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

## Referr to the posts app with urls and views
In ```DjangoDeployed/mysite/mysite/urls.py``` modify the urls 
```
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^posts/', include('posts.urls')),
]
```
firsr argument of url is a [regex](https://github.com/codingforentrepreneurs/Guides/blob/master/all/common_url_regex.md)

This will raise an error, next create ```posts/urls.py```

```
from django.conf.urls import url
from django.contrib import admin

import views

urlpatterns = [
    url(r'^$', views.post_home),
```
This will raise an error, next define the post_home function in ```posts/views.py```

##### The request response cycle.

Websites mostly work as a pull server.
For each request a response spawns, this mechanism is implemented in practice by the http protocol.
In ```posts/views.py``` add:
```
def post_home(req):
    return HttpResponse("<h1>Hello</h1>")
```
restart the server and goto <yourIP>/posts and a Hello will appear.
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

## Custom admin and CRUD

A model can be added (registered in Django gergon) to the admin panel.
The vanilla version displays the returned ```__unicode__``` or ```__str__``` for the posts present in the database.
It's good to have more info displayed in your admin panel i.e. the title and date of update and publish.
Create a ModelAdmin by extending the ModelAdmin class and add few options for better search and organization.

in ```DjangoDeployed/mysite/posts/admin.py```

```
from .models import Post

# Register your models here.

class PostModelAdmin(admin.ModelAdmin):
    list_display = ['title','updated','timestamp']
    list_display_links = ['title']
    list_filter = ['updated','timestamp']
    search_fields = ['title','content']
    class Meta:
        model = Post

admin.site.register(Post, PostModelAdmin)
```
For more options visit the documentation:
[ModelAdminOptions](https://docs.djangoproject.com/en/1.11/ref/contrib/admin/#modeladmin-options)
### CRUD
The Admin panel is an example of good software developement, the AdminModels follow [CRUD](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete).
##### URLS and Views
Each CRUD task can be implemented within the req-resp cycle with the url-views system (actually CRUDL).

in ```post/urls.py``` add the follwing patterns:
```
    url(r'^create/$', views.post_create),
    url(r'^read/$', views.post_read),
    url(r'^update/$', views.post_update),
    url(r'^delete/$', views.post_delete),
    url(r'^list/$', views.post_list),
```

in the  ```post/views.py ``` define the following functions:
```
def post_create(req):
    return HttpResponse("<h1>Create</h1>")

def post_read(req):
    return HttpResponse("<h1>Read</h1>")

def post_update(req):
    return HttpResponse("<h1>Update</h1>")

def post_delete(req):
    return HttpResponse("<h1>Delete</h1>")

def post_list(req):
    return HttpResponse("<h1>List</h1>")
```
By now it's not doing anything but serving simple html but this is correct.

## Templates

to separate backend from frontend use templates:
* save html/frontend code in ```DjangoDeployed/mysite/templates```
* add ```DjangoDeployed/mysite/templates``` path to the ```DjangoDeployed/mysite/mysite/settings.py``` files
    * add to the TEMPLATES dict
    ```
    TEMPLATES = { ...,
    'DIRS': [os.path.join(BASE_DIR, 'templates')],
    ...,}
    ```
    BASE_DIR aka root dir of the django project.
* add a view response to test templates
    * add to ```posts/views.py```:
    ```
    def post_home(req):
        return render(req,"index.html",{})
    ```
    
### HTML Hello World: the index.html template

in templates directory create a file ```index.html```

```
<!-- DOCTYPE html -->
<html>
<body>
  <h1>
    Hello World
  </h1>
</body>
</html>
```
this is referenced by the root url of the posts app aka <yourIP>/posts.

### here commit 66ce07f81e6d85400c90b0271351010bbf6ce58d

## Django Shell and Database API
[DB_API_DOC](https://docs.djangoproject.com/en/1.11/topics/db/queries/)
#### Cheat list for using the DB API
* Access the shell and model:
``` $ python manage.py shell```
* Import the model
``` >>> from posts.models import Post ```
* CREATE objects
```>>>Post.objects.create(title="new title", content="new content")``` create entry in database with defined content for specified fields (each command a query to the underlying database).
* LIST all objects
``` >>> Post.object.all() ```    returns a query set.
* FILTER objects
```>>> Post.object.filter(title="hi")``` return the matched field query set.
```>>> Post.object.filter(title__icontains="hi")``` same query case insensitive.

### use DB API in the req-resp cycle
##### context in the backend
Add a "context" to the request 
```
from models impor Post
def post_list(req):
    queryset = Post.objects.all()
    context = { 'queryset' : queryset }
    return render(req,"list.html",context)
```
this will raise an error upon request to the /list url because the list.html file has not been created yet.
##### context in the frontend
A queryset is an iterable object, each field is an attribute of the items:
```
    queryset = Post.objects.all()
    for item in queryset:
        print item.title
        print item.content
        print item.uploaded
        print item.updated
        print item.timestamp
        print item.id
        print item.pk # primary key field
```
The same pythonic syntax can be used (slightly) in html templates to list resutls coming from a request.
Create a ```templates/list.html``` file:
```
<!-- DOCTYPE html -->

<html>

<body>
{% for item in queryset %}
  <h1>
  {{ item.title }}<br/>
  {{ item.content }}<br/>
  {{ item.uploaded }}<br/>
  {{ item.updated }}<br/>
  {{ item.timestamp }}<br/>
  {{ item.id }}<br/>
  {{ item.pk }}<br/>
  </h1>
{% endfor %}
</body>

</html>
```
commit 6d662b837589b11649affd498cb0c357a361bccd


