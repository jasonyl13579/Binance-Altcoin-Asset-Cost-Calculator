# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 23:57:48 2021

@author: Corn
"""
import tkinter as tk
from tkinter.scrolledtext import ScrolledText


def onAddClient():
    pass
def onDeleteClient():
    pass
def onViewClient():
    pass
def onDisplayAuthorInfo():
    pass
def onDisplayUsage():
    pass
app = tk.Tk() 
app.geometry('600x400')
app.title("Altcoin Account Management System")

menubar = tk.Menu(app)

clientmenu = tk.Menu(menubar, tearoff=0)
clientmenu.add_command(label="增加帳戶(Add Client)", command=onAddClient)
clientmenu.add_command(label="刪除帳戶(Delete Client)", command=onDeleteClient)
clientmenu.add_command(label="檢視帳戶(View Client)", command=onViewClient)
menubar.add_cascade(label="帳戶(Client)", menu=clientmenu)

menu = tk.Menu(menubar, tearoff=0)

authormenu = tk.Menu(menubar, tearoff=0)
authormenu.add_command(label="使用說明(Usage)", command=onDisplayUsage)
authormenu.add_command(label="作者資訊(Author Info)", command=onDisplayAuthorInfo)
menubar.add_cascade(label="其他(Other)", menu=authormenu)

scrolledTextBox = ScrolledText(app, width=40, height=13,font=18)
scrolledTextBox.place(x=20, y=20)
    
app.config(menu=menubar)
app.mainloop()
