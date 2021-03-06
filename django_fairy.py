#!/usr/bin/env python
'''
Created on May 19, 2012

@author: gofrendi
'''

from django.core.management import execute_from_command_line
import sys, os

FAIRY_DIR = os.path.dirname(__file__)
TEMPLATE_DIR = os.path.join(FAIRY_DIR, 'template')

def pre_startproject():
    param = []
    param.append(sys.argv[0])
    param.append('startproject')
    param.append('--template')
    param.append(TEMPLATE_DIR)
    param.append(sys.argv[2])
    sys.argv = param

if __name__ == "__main__":
    PRE_ACT = {
        'fairy-startproject' : pre_startproject,
    }
        
    first_param = sys.argv[1] if len(sys.argv)>1 else ""   
    if first_param in PRE_ACT:
        PRE_ACT[first_param]()    
    execute_from_command_line(sys.argv)