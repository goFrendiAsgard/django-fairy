django-fairy
============

This is a project to make django development easier (just like in fairy-tale)
When you make a project, admin will automatically activated, template, static, and media folder will also be prepared.
When you make a new app, the app will be registered in "INSTALLED_APP". Also, the urls will be registered in project url automatically.
When you make a new model, it will automatically registered in admin settings
When you make a new view, the new url and template will automatically created

Usage
-----
To make a new project : 
* python django_fairy/django_fairy.py fairy-startproject your_new_project
To make a new app, model and view respectively :
* python manage.py fairy-startapp your_app_name
* python manage.py fairy-makemodel your_app_name your_model_name
* python manage.py fairy-makeview your_app_name your_model_name

Django-fairy was created to make your life easier, not take the freedom from you.
Anytime you think, you need the default django behavior, you can use any regular command as usual.


TODO
----
* When startapp performed, urls and admins should be added automatically (done)
* When startapp performed, global urls should include app url (done)
* Fairy app that include several function to avoid verbosity
