#-*- coding: utf-8 -*-
'''
Created on 28/07/2010

@author: Tassio
'''

def printt(label=''):
    def f(*args, **kwargs):
        print(label, args, kwargs)
    return f
