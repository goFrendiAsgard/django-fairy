#!/usr/bin/env python
'''
Created on May 19, 2012

@author: gofrendi
'''

from django.core.management import execute_manager
import imp
import sys, os, shutil
try:
    imp.find_module('settings') # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n" % __file__)
    sys.exit(1)

import settings

def edit_file(file_name, replace_lines=[], add_before_lines=[], add_after_lines=[]):
    shutil.move(file_name, file_name+'~')
    dest = open(file_name, 'w')
    src = open(file_name+'~', 'r')    
    
    for line in src:
        for add_before_line in add_before_lines:
            if line == add_before_line[0]+'\n':
                new_line = add_before_line[1]+'\n'
                dest.write(new_line)
        for replace_line in replace_lines:
            if line == replace_line[0]+'\n':
                line = replace_line[1]+'\n'
        dest.write(line)
        for add_after_line in add_after_lines:
            if line == add_after_line[0]+'\n':
                new_line = add_after_line[1]+'\n'
                dest.write(new_line)
    
    dest.close()
    src.close()
    os.remove(file_name+'~')

def create_file(file_name, content=""):
    f = open(file_name, 'w')
    f.write(content)
    f.close()

def append_file(file_name, content):
    f = open(file_name, 'a+')
    f.write(content)
    f.close

def delete_file(file_name):
    os.remove(file_name)

def fairy_startApp(app_name=None):
    if app_name == None:
        app_name = raw_input(" * Enter a new app name : ")
        app_name = str(app_name)        
    #copy from fairy_app/new_app
    shutil.copytree("fairy_app/new_app", app_name)
    #create __init__.py
    create_file("%s/__init__.py" %(app_name), "")
    #link the app urls to project urls
    add_after_lines = [
        ["urlpatterns = patterns('',", 
         "    url(r'^%s/', include('%s.urls'))," %(app_name, app_name)],
    ]
    edit_file('urls.py', add_after_lines=add_after_lines)
    os.mkdir('templates/%s'%(app_name))
    print(" * New app has been created : %s" %(app_name))
    return app_name

def fairy_newModel(app_name = None, model_name = None):
    if app_name == None:
        app_name = raw_input(" * Enter an app name : ")
        app_name = str(app_name)  
    if model_name == None:
        model_name = raw_input(" * Enter a new model name : ")
        model_name = str(model_name) 
    #create new model
    result = ""
    result += "class %s(models.Model):\n" % (model_name)
    result += "    name = models.CharField(max_length=100)\n" 
    result += "    def __unicode__(self):\n"
    result += "        return self.name\n\n"
    append_file("%s/models.py" %(app_name), result)
    #create admin
    result = ""
    result += "class %s_admin(admin.ModelAdmin):\n" % (model_name)
    result += "    #list_display=('any_field',)\n" 
    result += "    #search_fields=('any_field',)\n" 
    result += "    #list_filter=('any_field',)\n"
    result += "    #date_hierarchy = 'date_field'\n"
    result += "    #ordering = ('any_field',)\n"
    result += "    #fields = ('any_field',)\n"
    result += "    #filter_horizontal = ('any_field',)\n"  
    result += "    #raw_id_fields = ('foreign_key_field',)\n"
    result += "    pass\n\n"
    result += "admin.site.register(models.%s, %s_admin)\n\n" %(model_name, model_name)
    append_file("%s/admin.py" %(app_name), result)
    print(" * New model has been created : %s.models.%s" %(app_name, model_name))
    return app_name, model_name

def fairy_newView(app_name = None, view_name = None):
    if app_name == None:
        app_name = raw_input(" * Enter an app name : ")
        app_name = str(app_name)  
    if view_name == None:
        view_name = raw_input(" * Enter a new view name : ")
        view_name = str(view_name) 
    #create new view
    result = ""
    result += "def %s(request):\n" % (view_name)
    result += "    data = {'message' : '%s.views.%s is active'}\n" %(app_name, view_name)
    result += "    return render(request, '%s/%s.html', data)\n\n" %(app_name, view_name) 
    append_file("%s/views.py" %(app_name), result)
    #add new entry in urls.py
    add_after_lines = [
        ["urlpatterns = patterns('',", 
         "    url(r'^%s/', views.%s)," %(view_name, view_name)],
    ]
    edit_file('%s/urls.py' %(app_name), add_after_lines=add_after_lines)
    #new template
    shutil.copy('fairy_app/new_template/new_template.html', 'templates/%s/%s.html' %(app_name, view_name))    
    print(" * New view has been created : %s.views.%s" %(app_name, view_name))
    return app_name, view_name
    
def fairy():
    menus = [
       ["Start a new Application", fairy_startApp],
       ["Make a new Model", fairy_newModel],
       ["Make a new View", fairy_newView],
    ]
    print(" * django-fairy, here to help you :D")
    i=1
    for menu in menus:
        print("   %d : %s" %(i, menu[0]))
        i+=1
    print ("   x : Exit")
    response = raw_input(" * How can I help you (enter your choice)? : ")
    if str(response) == "x":
        print(" * Bye....")
    elif int(response) in xrange(1, len(menus)+1):
        menus[int(response)-1][1]()
        fairy()

def normal():
    execute_manager(settings)

if __name__ == "__main__":    
    if len(sys.argv)>=2:
        if sys.argv[1] == 'fairy':
            fairy()
        else:
            normal()
    else:
        normal()