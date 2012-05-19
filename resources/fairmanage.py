#!/usr/bin/env python
'''
Created on May 19, 2012

@author: gofrendi
'''

from django.core.management import execute_manager
import imp
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

if __name__ == "__main__":
    execute_manager(settings)
    #special action
    if len(sys.argv)>=3:
        if sys.argv[1] == 'startapp':
            #prepare locations
            app_name = sys.argv[2]