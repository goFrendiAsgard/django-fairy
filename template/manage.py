#!/usr/bin/env python
import os, sys, shutil
from django.core.management import execute_from_command_line

CURRENT_DIR = os.path.dirname(__file__)
PROJECT_DIR = os.path.join(CURRENT_DIR, '{{ project_name }}')
RESOURCE_DIR = os.path.join(CURRENT_DIR, 'fairy-resource')
APP_TEMPLATE_DIR = os.path.join(RESOURCE_DIR, 'app_template')

def edit_file(file_name, replaces=[]):
    shutil.move(file_name, file_name+'~')
    dest = open(file_name, 'w')
    src = open(file_name+'~', 'r')    
    
    for line in src:
        for replace_pair in replaces:
            line = line.replace(replace_pair[0], replace_pair[1])
        dest.write(line)
    
    dest.close()
    src.close()
    os.remove(file_name+'~')

def pre_startapp():    
    param = []
    param.append(sys.argv[0])
    param.append('startapp')
    param.append('--template')
    param.append(APP_TEMPLATE_DIR)
    param.append(sys.argv[2])
    sys.argv = param    

def post_startapp():
    '''registers our newly generated app to the project'''
    app_name = sys.argv[4]
    urls_file = os.path.join(PROJECT_DIR, 'urls.py')
    urls_replaces = [
       ['##[include_app_url]##', '##[include_app_url]##\n    url(r\'^%s/\', include(\'%s.urls\')),' %(app_name, app_name)]
    ]
    edit_file(urls_file, urls_replaces)    
    settings_file = os.path.join(PROJECT_DIR, 'settings.py')
    settings_replaces = [
       ['##[app_name]##', '##[app_name]##\n    \'%s\',' %(app_name)]
    ]
    edit_file(settings_file, settings_replaces)

def act_makemodel():
    app_name = sys.argv[2]
    model_name = sys.argv[3]
    app_dir = os.path.join(CURRENT_DIR, app_name)
    if not os.path.exists(app_dir):
        raise('app %s doesn\'t exists' %(app_name))    
    #edit model file
    model_file = os.path.join(app_dir, 'models.py')
    model_function = '##[model]##\n\n'
    model_function += 'class %s(models.Model):\n' %(model_name)
    model_function += '    name = models.CharField(max_length=100)\n'
    model_function += '    def __unicode__(self):\n'
    model_function += '        return self.name\n\n'
    model_replaces = [
        ['##[model]##', model_function],
    ]
    edit_file(model_file, model_replaces)    
    #register admin
    admin_file = os.path.join(app_dir, 'admin.py')
    admin_function = '##[model]##\n\n'
    admin_function += 'class %s_admin(admin.ModelAdmin):\n' %(model_name)
    admin_function += '    #list_display=(\'any_field\',)\n'
    admin_function += '    #search_fields=(\'any_field\',)\n'
    admin_function += '    #list_filter=(\'any_field\',)\n'
    admin_function += '    #date_hierarchy = \'date_field\'\n'
    admin_function += '    #ordering = (\'any_field\',)\n'
    admin_function += '    #fields = (\'any_field\',)\n'
    admin_function += '    #filter_horizontal = (\'any_field\',)\n'
    admin_function += '    #raw_id_fields = (\'foreign_key_field\',)\n'
    admin_function += '   pass\n\n'
    admin_function += 'admin.site.register(models.%s, %s_admin)\n\n' %(model_name, model_name)
    admin_replaces = [
        ['##[model]##', admin_function],
    ]
    edit_file(admin_file, admin_replaces)

def act_makeview():
    app_name = sys.argv[2]
    view_name = sys.argv[3]
    app_dir = os.path.join(CURRENT_DIR, app_name)
    if not os.path.exists(app_dir):
        raise('app %s doesn\'t exists' %(app_name))
    #edit view file
    view_file = os.path.join(app_dir, 'views.py')
    view_function = '##[view]##\n\n'
    view_function += 'def %s(request):\n' %(view_name)
    view_function += '    data = {\'message\' : \'%s.views.%s is active\'}\n' %(app_name, view_name)
    view_function += '    return render(request, \'%s/%s.html\', data)\n\n' %(app_name, view_name)
    view_replaces = [
        ['##[view]##', view_function],
    ]
    edit_file(view_file, view_replaces)
    #make corresponding template
    src = os.path.join(RESOURCE_DIR, 'template.html')
    dest = os.path.join(app_dir, 'templates', app_name, '%s.html'%(view_name))
    shutil.copy(src,dest)
    #register url
    urls_file = os.path.join(app_dir, 'urls.py')
    urls_replaces =[
        ['##[view]##', '##[view]##\n    url(r\'^%s/\', views.%s),' %(view_name, view_name)],
    ]
    edit_file(urls_file, urls_replaces)

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{{ project_name }}.settings')

    pre_act = {
        'fairy-startapp' : pre_startapp,
    }    
    post_act = {
        'fairy-startapp' : post_startapp,
    }
    new_act = {
        'fairy-makemodel' : act_makemodel,
        'fairy-makeview' : act_makeview,
    }
    
    first_param = sys.argv[1] if len(sys.argv)>1 else ""  
    if first_param in new_act:
        new_act[first_param]()
    else:
        if first_param in pre_act:
            pre_act[first_param]()        
        execute_from_command_line(sys.argv)    
        if first_param in post_act:
            post_act[first_param]()
