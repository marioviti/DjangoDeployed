**Table of Contents**  *generated with [DocToc](http://doctoc.herokuapp.com/)*

- [DjangoDeployed](#)
	- [structure](#)
	- [to start](#)
	- [Troubleshooting](#)
- [Developing](#)
	- [create an app and first model](#)
	- [Access the posts app with urls and views](#)
		- [The request response cycle](#)
		- [The model](#)
	- [Custom admin and CRUD](#)
		- [CRUD](#)
			- [URLS and Views](#)
	- [Templates](#)
		- [HTML Hello World: the index.html template](#)
				- [commit 66ce07f81e6d85400c90b0271351010bbf6ce58d](#)
	- [Django Shell and Database API](#)
			- [Cheat list for using the DB API](#)
		- [use DB API in the req-resp cycle](#)
			- [context in the backend](#)
			- [context in the frontend](#)
				- [commit 6d662b837589b11649affd498cb0c357a361bccd](#)
	- [Dynamic urls](#)
		- [kwargs in django regex](#)
		- [url view template](#)
				- [commit 67da321a4400d851758b294c873f5c49b11c90c2](#)
		- [Links and dynamic url](#)
			- [Namespaces and names.](#)
			- [Comodity method.](#)
				- [commit a6f48678a8f0b358ce68a362c04cb30bbfbebd83](#)

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

## Access the posts app with urls and views

Django is built as an MDV(Model View Controller) in our case these are:
* Model: SQLite3 db (vanilla db shipped with django)
* View: html, json, any readable format for a browser.
* Controller: Python.

The controller handles the HTTP request via urls pattern that are mapped to python functions that serve html or json as response.

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

### The request response cycle

Websites mostly work as a pull server.
For each request a response spawns, this mechanism is implemented in practice by the http protocol.
In ```posts/views.py``` add:
```
def post_home(req):
    return HttpResponse("<h1>Hello</h1>")
```
restart the server and goto <yourIP>/posts and a Hello will appear.

### The model

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
#### URLS and Views
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
##### commit 66ce07f81e6d85400c90b0271351010bbf6ce58d

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
#### context in the backend
Add a "context" to the request 
```
from models impor Post
def post_list(req):
    queryset = Post.objects.all()
    context = { 'queryset' : queryset }
    return render(req,"list.html",context)
```
this will raise an error upon request to the /list url because the list.html file has not been created yet.
#### context in the frontend
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
##### commit 6d662b837589b11649affd498cb0c357a361bccd

## Dynamic urls

Dynamic urls implement passing of argument via url.
This is sliglty different from a post method in HTTP because an argument is passed in order to query the database with a filter option (search by title, id, content or any other field), a POST method should trigger a write or update in the database.

We'll extend the CRUD paradigm with detail: ask for a specific post via url in the database and return it in the browser.
* urls to pass the pk argumet to the view function.
* a view function to handle the request and fire the query and return a template page.
* template page to be rendere by the browser.

### kwargs in django regex

In django urls regex are bind to view methods and typed kwargs can be passed via a specific django regex syntax.

update the ```urlpatterns``` dictionary in the ```urls.py``` file.
```
...
url(r'^detail/(?P<pk>\d+)/$', posts_detail),
...
```

### url view template

This must be matched with the view function

```
from djangoshortcuts import render, get_object_or_404

def posts_detail(req, pk=None):
    query_set = get_object_or_404(Post, pk=pk)
    context = {
        "query_set":query_set
    }
    return render(request, "detail.html", context)
```

We've also introduced the get_object_or_404 method which handles the exception in case the queryset is empty and returns a http 404 page.

Finally add ```detail.html``` in the templates folder:

```
<!-- DOCTYPE html -->

<html>

<body>
  <h1>
  {{ item.title }}<br/>
  {{ item.content }}<br/>
  {{ item.updated }}<br/>
  {{ item.timestamp }}<br/>
  {{ item.id }}<br/>
  {{ item.pk }}<br/>
  </h1>
</body>

</html>
```

##### commit 67da321a4400d851758b294c873f5c49b11c90c2


### Links and dynamic url

We'd like to add clickable links to address the dynamic url of a post.

To do so we'll use 3 things:
* urls names and namespaces: name the url to be referred globally within the project (no hardcoding!).
* comodity Post Model method get_absolute_url: each post instance will have this method.
* reverse method: a method linking the comodity method to the name of the url.

#### Namespaces and names.

For urls namespaces map to different names, so two urls can have the same name in different namespaces.

Add namespace in the ```mysite/urls.py``` file in the mysite directory (the main router at the top of the project):

```
    url(r'^posts/', include('posts.urls', namespace='posts') ),
```

all the names of urls in posts.urls will belong now to the same namespace 'posts'
Add a name to the url pattern in ```posts/urls.py```:

```
    url(r'^detail/(?P<pk>\d+)/$', views.post_detail, name='post'),
```

#### Comodity method.

Add this method to the Post class in models.py:
```
from django.core.urlresolvers import reverse

Class Post(model.Model):
...
    def get_absolute_url(self):
        return reverse('posts:post', kwargs={'pk':self.pk})
```
First parameters is the name of the urls preceded by its namespace: in our case 'posts:post', second parameters refers to the typed kwargs specified in the url regex.
This method is called within the template so that a string for the url will be generated and passed to the <href> html tag.

```
<!-- DOCTYPE html -->

<html>

<body>
  <h1>
  <a href='{{ item.get_absolute_url }}'> {{ item.title }}</a><br/>
  {{ item.content }}<br/>
  {{ item.updated }}<br/>
  {{ item.timestamp }}<br/>
  {{ item.id }}<br/>
  {{ item.pk }}<br/>
  </h1>
</body>

</html>
```

Notice that the view has not been modified.
So if now you change the name of the url in the regex, you do not need to change anything in the model all will be associated with the name and reverse will resolve the actual url specified in the regex.

##### commit a6f48678a8f0b358ce68a362c04cb30bbfbebd83
