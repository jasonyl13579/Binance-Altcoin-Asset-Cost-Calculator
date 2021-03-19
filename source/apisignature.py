# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 14:27:02 2020

@author: Corn
"""
import base64
import hashlib
import hmac
import datetime
import time
#from urllib import parse
#import urllib.parse


def create_signature(secret_key, builder):

#    keys = builder.param_map.keys()
#    query_string = '&'.join(['%s=%s' % (key, parse.quote(builder.param_map[key], safe='')) for key in keys])
    query_string = builder.build_url()
    signature = hmac.new(secret_key.encode(), msg=query_string.encode(), digestmod=hashlib.sha256).hexdigest()
    builder.put_url("signature", signature)


def create_signature_with_query(secret_key, query):
    signature = hmac.new(secret_key.encode(), msg=query.encode(), digestmod=hashlib.sha256).hexdigest()
    
    return signature


def utc_now():
    return datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')

def get_current_timestamp():
    return int(round(time.time() * 1000))