# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 23:40:24 2021

@author: Corn
"""
from time import time 
from re import sub
from datetime import datetime


DEFAULT_EPOCH_TIME = 1483228800000

def get_current_timestamp():
    return int(round(time() * 1000))

def datetime_to_utc_time(dt):
    if not dt: return None
    #tw = pytz.timezone('Asia/Taipei')
    return datetime.fromtimestamp(dt/1000).strftime("%Y-%m-%d %H:%M:%S")
def phrase_iso_to_time(dt):
    conformed_timestamp = sub(r"[:]|([-](?!((\d{2}[:]\d{2})|(\d{4}))$))", '', dt)
    d = datetime.strptime(conformed_timestamp, "%Y%m%dT%H%M%S.%f%z" )
    return int(round(d.timestamp()) * 1000)