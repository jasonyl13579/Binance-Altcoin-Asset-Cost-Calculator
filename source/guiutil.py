# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 22:56:20 2021

@author: Corn
"""
from tkinter import Toplevel, StringVar, Label, Entry, Button, Text, CENTER, END
from threading import Thread

def get_system_metrics():
    from win32api import GetSystemMetrics
    return GetSystemMetrics(0),GetSystemMetrics(1)

def get_window_positons(width, height):
    system_metrics = get_system_metrics()
    window_x_position = (system_metrics[0] - width)//2
    window_y_position = (system_metrics[1] - height) // 2
    return window_x_position, window_y_position
def setUIToCenter(window, width, height):
    pos = get_window_positons(width, height)
    window.geometry(f'{width}x{height}+{pos[0]}+{pos[1]}')  
    window.resizable(0, 0)
    
class Language:
    def __init__(self, lg='tw'):
        self.lg = lg

class BaseThread(Thread):
    def __init__(self, callback=None, callback_args=None, *args, **kwargs):
        target = kwargs.pop('target')
        first_agrs = kwargs.pop('first')
        super(BaseThread, self).__init__(target=self.target_with_callback, *args, **kwargs)
        self.first_agrs = first_agrs
        self.callback = callback
        self.method = target
        self.callback_args = callback_args

    def target_with_callback(self):
        res = self.method(self.first_agrs)
        if self.callback is not None:
            if self.callback_args:
                self.callback(*self.callback_args)
            else:
                self.callback(res)
## https://www.itread01.com/articles/1502375899.html
class inputDialog(Toplevel):
    def __init__(self, app, msg):
        super().__init__()
        self.setupUI(msg)
        self.output = 0
        
    def onConfirm(self):
        self.output = self.entry_input.get()
        self.destroy()
    def setupUI(self, msg):
        self.title("輸入以下資訊")
        setUIToCenter(self, 300, 150)
        
        self.cost = StringVar()  
        self.cost.set("10")  
        Label(self, text=msg).pack(ipady=10)  
        self.entry_input = Entry(self, textvariable=self.cost) 
        self.entry_input.pack(ipady=10) 
        btn_confirm = Button(self, text='確認', command=self.onConfirm, width=15)
        btn_confirm.pack(ipady=10)

#dialog = inputDialog("Enter cost of DOT in USDT\n (Amount:1000, Date:2020/01/01):")

#print (dialog.output)

#dialog.destroy()

class infodialog(Toplevel):
    def __init__(self, title, msg):
        super().__init__()
        self.setupUI(title, msg)
        
    def onConfirm(self):
        self.destroy()
    def setupUI(self, title, msg):
        self.title(title)
        setUIToCenter(self, 300, 150)
        url = Text(self, height=1, borderwidth=0)
        url.delete("1.0", END) 
        url.insert(1.0, msg, "center")
        url.pack(padx= len(msg), pady=30)
        url.configure(state="disabled", bg=self.cget('bg'))
        
        btn_confirm = Button(self, text='確認', command=self.onConfirm, width=15)
        btn_confirm.pack(anchor= CENTER, pady=20)