#!/usr/bin/env python
'''
Created on May 19, 2012

@author: gofrendi
'''

from django.core.management import execute_manager, execute_from_command_line
import sys, os, shutil

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

if __name__ == "__main__":
    #call django-admin
    execute_from_command_line()    
    #special action
    if len(sys.argv)>=3:
        if sys.argv[1] == 'startproject':
            #prepare locations
            project_name = sys.argv[2]
            project_directory = os.path.join(os.getcwd(), project_name)
            current_directory = os.path.dirname(__file__)
            resource_directory = os.path.join(current_directory,'resources')            
            #copy ./resources/fairmanage.py to project_directory
            src = os.path.join(resource_directory, 'fairmanage.py')
            dest = os.path.join(project_directory, 'fairmanage.py')
            shutil.copy(src, dest)
            #copy ./resources/templates to project_directory
            src = os.path.join(resource_directory, 'templates')
            dest = os.path.join(project_directory, 'templates')
            shutil.copytree(src, dest)
            #copy ./resources/templates to project_directory
            src = os.path.join(resource_directory, 'media')
            dest = os.path.join(project_directory, 'media')
            shutil.copytree(src, dest)            
            #prepare_settings(project_directory)
            file_name = os.path.join(project_directory, 'settings.py')
            replace_lines = [
                    ["STATIC_ROOT = ''", "STATIC_ROOT = os.path.join(os.path.dirname(__file__),'static')"],
                    ["    # 'django.contrib.admin',", "    'django.contrib.admin',"]
                ]
            add_before_lines = [
                    ["DEBUG = True", "import os"],
                ]
            add_after_lines = [
                    ["TEMPLATE_DIRS = (", "    os.path.join(os.path.dirname(__file__),'templates')"],
                ]
            edit_file(file_name, replace_lines, add_before_lines, add_after_lines)
            #message
            print(' * Your fairy-django-project has been created')
            print(' * You can now enjoy fairy features by using fairmanage.py')