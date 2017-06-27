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
			- [Namespaces and names](#)
			- [Comodity method](#)
				- [commit a6f48678a8f0b358ce68a362c04cb30bbfbebd83](#)
	- [Forms](#)
		- [Extend the ModelForm](#)
			- [the form view](#)
			- [the form template](#)
		- [CSRF cross site request forgery](#)
			- [Validating input data](#)
	- [How to modify posts (crUd)](#)
	- [Delete a POST (cruD)](#)
	- [Messagges](#)

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

#### Namespaces and names

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

#### Comodity method

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


## Forms

Building a form includes:
* building the html form for http POST method.
* validate data coming upon a request.
* storing or perist the data sent in the database.
* 
Django provides ready-to-use forms class.
This class should also be held as example for any object interacting with the MVC(Model View Controller).

### Extend the ModelForm

create a new file ```forms.py```

```

from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "content"
        ]
```

#### the form view

This wraps the input fields of the Post model into a form object.
Now add a view function to display the form in ```views.py```

```
from .forms import PostForm

def post_create(req):
    form = PostForm()
    context = { 'form' : form }
    return render(req, "post_create.html", context)
```

#### the form template

Create a new template file ```templates/post_create.html```

```
<!-- DOCTYPE html -->

<html>

<body>
  <h1>Form</h1>
  <form method='POST' action=''>
  {{ form.as_p }}
  <input type='submit' value='create post'>
  </form>
</body>

</html>
```
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
POST is a standard method of the HTTP protocol.
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
* form.as_p is a method of the ModelForm object standing for as paragraph which generate the html to render the post input fields.
* <form> html tag stands for post object: <input> is the child of form that includes a button at the bottom.
* the default method for a post is GET which is usually changed to POST as the data inserted will be sent to a url specified in action to the server via HTTP request, leaving action empty will reuse the current url to send data to.

### CSRF cross site request forgery
Post methods are insicure as any website could forge a url and send a POST request via Http client.
A basic DOS attack strategy is to siege both web server and database by spawning POST requests, filling the disk quota and making the website unreachable.

Luckly enough Django provides default security measures easy to implement.

```
<!-- DOCTYPE html -->

<html>

<body>
  <h1>Form</h1>
  <form method='POST' action=''>{% csrf_token %}
  {{ form.as_p }}
  <input type='submit' value='create post'>
  </form>
</body>

</html>
```

#### Validating input data
Some field have constraints on them, to secure consistency of data before storing data in the database we'll need to check for validation (for example the title filed has a max lenght). Django provides simple method for data validation.

In the ```views.py``` file:

```
def post_create(req):
    form = PostForm(req.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
    ...
```

This is very handy but there's a lot going on.
* ```req.POST```: the http request has a field for the method input data POST this will be passed to the PostForm Object to initialize the form with the input data.
* A ```None``` initialized ```PostForm``` will be invalid, remeber we use this view for both storing data and showing the post, is_valid() will be true only upon a POST request coming from a client.
* ```commit=False``` databases have caches to temporary store data, commit means storing from the cache to the database, not commiting will leave the database manager deciding when to store so that the use of a cache minimizes accesses to database (J2LUK).

## How to modify posts (crUd)

We'll need to show the content in a form and modify the correct instance instead of adding new instances.
To do so we need to keep track of the post id.

In ```views.py```

```
def post_update(req, id=None):
	instance = get_object_or_404(Post,id=id)
	form = PostForm(request.POST or None, instance=instance)
	if form.is_valid():
		instance=form.save(commit=False)
		instance.save()
	context = {
		'title': instance.title,
		'instance':instance,
		'form':form
	}
	return render(req, "post_form.html", context)
	
```
Notice we're passing instance to the PostForm constructor to initialize the values title and content.
We've set the function in the view but we need an url to point to the view itself.

In ```urls.py```:

```
urlpatterns= {
	...
	url(r'^(?P<id>\d+)/edit/$', post_update, name='update',
	...
}
```

To add a better feel to the website we'll modify the view to redirect us to the detail page of the created/updated post.

In ```views.py```
```
from django.http import HttpResponseRedirect

def post_update(req,id=None):
	...
	instance.save()
	return HttpResponseRedirect(instance.get_absolute_url())
	...
```

Same for the create view, this will have the same effect of clicking on the link in the post list.

## Delete a POST (cruD)

edit ```views.py```:

```
...
from django.shortcuts import redirect
...
def post_delete(req.pk=None):
    instance=get_object_or_404(Post, id=pk)
    instance.delete()
    return redirect('posts:list')
```

Update the names in the ``urls.py```
```
urlpatterns = {
	...
	url(r'^list/$', views.post_list, name='list'),
	url(r'^delete/(?P<pk>\d+)/$$', views.post_delete),
	...
```

## Messagges

https://docs.djangoproject.com/en/1.9/ref/contrib/messages/

Show a message after update/create of post, edit ```views.py```:

```
from django.contrib import messages

...
def post_create(req):
	...
	instance.save()
	messages.success(req, "successfully created")
else:
	messages.error(req, "unsuccessfully created")
...
def post_update(req):
	...
	instance.save()
	messages.success(req, "successfully updated")
else:
	messages.error(req, "unsuccessfully updated")
	...
	
def post_delete(req.pk=None):
	...
	instance.delete()
	messages.succes(req, "Successfully deleted")
	...
```

Update the template to display messages, edit ```detail.html```:

```
...
<body>
{% if messages %}
<ul class="messages">
	{% for message in messages %}
		<li>{{message}}</li>
	{% endfor %}
</ul>

{% endif %}
```

## Manage Static

Because of the NGINX settings we've already our server serving static files in ```/media/```
To make django point to the same directory for static files we'll have to change variables in  ```mysite/settings.py```:


```
STATIC_URL='/media/'
STATIC_ROOT=os.path.join(BASE_DIR, 'media/')
```

now to test this modify the base template ```base.html```

```
  {% load static %}
	<img src="{% static "gatto.jpeg" %} " alt="gatto" height="42" width="42" />
```

now run ```python manage.py collectstatic``` to copy from /static/ to /media/.

## Adding Bootstrap with CDN

http://getbootstrap.com/getting-started/

To use bootstrap for all pages simply reference it from the ```base.html``` template.

```
<!-- DOCTYPE html -->

<html>
<head>
  <!-- Latest compiled and minified CSS -->
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
  <!-- Optional theme -->
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css" integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous">
</head>
<body>

  {% load static %}
	<img src="{% static "gatto.jpeg" %} " alt="gatto" height="42" width="42" />
  {% if messages %}
  <div class="messages">
    <ul class="messages">
      {% for message in messages %}
        <li>{{message}}</li>
      {% endfor %}
    </ul>
  </div>
  {% endif %}

  <div class="container">
    {% block content %}
      {% for item in queryset %}
        <h1>
        <a href='{{ item.get_absolute_url }}'> {{ item.title }}</a><br/>
        {{ item.content }}<br/>
        {{ item.updated }}<br/>
        {{ item.timestamp }}<br/>
        {{ item.id }}<br/>
        {{ item.pk }}<br/>
        </h1>
      {% endfor %}
    {% endblock content %}
  </div>

<!-- Latest compiled and minified JavaScript -->
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>

</body>
</html>
```

##Pagination

To inverse the order in queries, in ```views.py```
```
def post_list(req):
	queryset = Post.objects.all().order_by("-timestamp")
```

This is pretty dumb as records are reordered everytime, instead modify the model.

```

class Post(models.Model):
	...
	class Meta:
		ordering = ["-timestamp","-updated"]
		
```

## Django Paginator

[1.9 Paginator](https://docs.djangoproject.com/en/1.9/topics/pagination/#using-paginator-in-a-view)

The example from the page:
```
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

def listing(request):
    contact_list = Contacts.objects.all()
    paginator = Paginator(contact_list, 25) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    return render(request, 'list.html', {'contacts': contacts})
```

We'll merge this code in the post_list view:

```
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
...

def post_list(req):
    page_title = 'articoli'
    queryset_list = Post.objects.all()#.order_by("-timestamp")
    paginator = Paginator(contact_list, 25) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)
    context = {
        'page_title':page_title,
        'queryset':queryset
    }
    return render(req, "list.html", context)
```

Now integrate in html the pagination by mergin from the example at the doc page as follwowing:

```
<div class="pagination">
    <span class="step-links">
        {% if queryset.has_previous %}
            <a href="?page={{ queryset.previous_page_number }}">previous</a>
        {% endif %}

        <span class="current">
            Page {{ queryset.number }} of {{ queryset.paginator.num_pages }}.
        </span>

        {% if queryset.has_next %}
            <a href="?page={{ queryset.next_page_number }}">next</a>
        {% endif %}
    </span>
</div>
```




