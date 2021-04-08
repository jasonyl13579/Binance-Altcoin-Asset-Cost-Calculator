# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 23:57:48 2021

@author: Corn
"""
import sys
from os import path
#import tkinter as tk
from tkinter import Tk, Toplevel, StringVar, Button, Label, Entry, Listbox, Menu, Text
from tkinter import END, PhotoImage, messagebox
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog

from clients.clients import Clients
import source.guiutil as gu

APP_BUTTON_WIDTH = 10
EDIT_CLIENT_BUTTON_WIDTH = 8 
CONFIG_FILENAME = '.config'
VERSION = 'v1.0'
EMAIL = 'jasonyl13579@yahoo.com.tw'
ERC20 = '0x8F6081F6394350104cebe70C76d8c2cDa524dd29'
TRC20 = 'TKLy4fSedhEKJD1HRMoNaqZt4usUk7MCbr'
root_width = 600
root_height = 400

#%% window UI util
class PrintLogger(): # create file like object
    def __init__(self, textbox): # pass reference to text widget
        self.textbox = textbox # keep ref

    def write(self, text):
        self.textbox.insert(END, text) # write text to textbox
        self.textbox.see(END)

    def flush(self): # needed for file like object
        pass
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
class inputDialog(Toplevel):
    def __init__(self, app, msg):
        super().__init__()
        self.setupUI(msg)
        self.output = 0
        
    def onConfirm(self):
        #print (self.entry_input.get())
        self.output = self.entry_input.get()
        self.destroy()
    def setupUI(self, msg):
        self.title("輸入以下資訊")
        setUIToCenter(self, 300, 150)
        
        self.cost = StringVar()  
        self.cost.set("10")  
        Label(self, text=msg).pack(ipady=10)   # 將`User name:`放置在座標（10,10）。
        self.entry_input = Entry(self, textvariable=self.cost)  # 建立一個註冊名的`entry`，變數為`new_name`
        self.entry_input.pack(ipady=10)  # `entry`放置在座標（150,10）.
        btn_confirm = Button(self, text='確認', command=self.onConfirm, width=15)
        btn_confirm.pack(ipady=10)
#%% action
class GUI():
    def __init__(self):
        self.app = None
        self.clients = Clients()
        self.clients.restore_client_config(CONFIG_FILENAME)
        self.originIO = sys.stdout
    def onDeleteClient(self):
        pass
    def onViewClient(self):
        def refreshAccountList():
            account_list.set(value = [name for name in self.clients.client_dict])
        def onOpenFile():
            old_path = new_directory.get()
            dir_path = filedialog.askdirectory(initialdir = self.clients.meta_save_path, title="請選擇要報告輸出的資料夾")
            new_directory.set(dir_path if dir_path != '' else old_path)
        def editClient(new = True, old_name = None):
            def onProcessClientData():
                name = new_name.get()
                exchange = new_exchange.get()
                api_key = new_api_key.get()
                api_secret = new_api_secret.get()
                query_str = new_query_list.get()            
                ## Check name
                try:
                    for s in name:
                        if s in "~!@#$%^&*()+-*/<>,.[]\/":
                            msg.set('Error: ' + "名稱勿含特殊符號")
                            return     
                    for s in query_str:
                        if s in "~!@#$%^&*()+-*/<>.[]\/":
                            msg.set('Error: ' + 'Query List勿含除了","以外的特殊符號')
                            return
                    if len(name) > 15:
                        msg.set('Error: ' + '名稱勿超過15字')
                    elif name in self.clients.client_dict and new:
                        msg.set('Error: ' + '名字勿重複')
                    elif not len(api_key) or not len(api_secret) or not len(name) or not len(exchange):
                        msg.set('Error: ' + "請輸入名稱、金錀或交易所")
                    elif exchange not in ['binance', 'ftx']:
                        msg.set('Error: ' + "目前交易所僅支援 binance 和 ftx")
                    else:
                    ## Add client to config
                        specialChars = " \n!\"#$%^&*()" 
                        for specialChar in specialChars:
                            query_str = query_str.replace(specialChar, '')
                        client_data = {
                                        'api_key': api_key,
                                        'api_secret':api_secret,
                                        'query_list': query_str.upper().split(','),
                                        'exchange': exchange
                                      }
                        if new:
                            client_data['index'] = self.clients.count
                            self.clients.count += 1
                            self.clients.process_client_data(name, client_data)
                            refreshAccountList()
                            messagebox.showinfo('Welcome', '成功增加帳戶 %s!' % name)
                        else:
                            self.clients.client_dict[name].info.setinfo(client_data)
                            messagebox.showinfo('Welcome', '成功修改帳戶 %s!' % name)
                        self.clients.save_client_config(CONFIG_FILENAME)
                        window_add_client.destroy()
                        
                except Exception as e:
                        msg.set('Error')
                        print (e)
            window_add_client = Toplevel(self.app)
            window_add_client.title("編輯您的帳戶資訊")
            window_add_client.geometry('400x300')  
            try:
                window_add_client.iconphoto(False, PhotoImage(file='icon/doge_icon.png'))
            except:
                pass
            setUIToCenter(window_add_client, 400, 300)
            new_name = StringVar()  
            new_name.set('binance_Name')  
            Label(window_add_client, text='User name: ').place(x=10, y=10)  # 將`User name:`放置在座標（10,10）。
            entry_new_name = Entry(window_add_client, textvariable=new_name, width=35)  # 建立一個註冊名的`entry`，變數為`new_name`
            entry_new_name.place(x=130, y=10)  # `entry`放置在座標（150,10）.
            
            new_exchange = StringVar()
            new_exchange.set('binance') 
            Label(window_add_client, text='Exchange: ').place(x=10, y=50)
            entry_new_exchange= Entry(window_add_client, textvariable=new_exchange, width=35)
            entry_new_exchange.place(x=130, y=50)
            
            new_api_key = StringVar()
            Label(window_add_client, text='API key: ').place(x=10, y=90)
            entry_usr_api_key = Entry(window_add_client, textvariable=new_api_key, width=35)
            entry_usr_api_key.place(x=130, y=90)
        
            new_api_secret = StringVar()
            Label(window_add_client, text='Secret key: ').place(x=10, y=130)
            Entry(window_add_client, textvariable=new_api_secret, width=35) \
            .place(x=130, y=130)
        
            new_query_list = StringVar()
            new_query_list.set("ETH, BTC")
            Label(window_add_client, text='Query list: ').place(x=10, y=170)
            Entry(window_add_client, textvariable=new_query_list, width=35) \
            .place(x=130, y=170)
            
            msg = StringVar()
            Label(window_add_client, textvariable=msg, fg='red').place(x=20, y=210)
            btn_comfirm_sign_up = Button(window_add_client, text='確認', command=onProcessClientData)
            btn_comfirm_sign_up.place(x=180, y=250)
            
            if not new:
                entry_new_name['state'] = 'disabled'
                info = self.clients.client_dict[old_name].info
                new_name.set(old_name)  
                new_exchange.set(info.exchange)
                new_api_key.set(info.api_key)
                new_api_secret.set(info.api_secret)
                new_query_list.set(','.join(info.query_list))
        def onImportClient():
            file_path = filedialog.askopenfile(initialdir = self.clients.meta_save_path, title="請選擇要匯入的key.txt").name
            self.clients.init_client_from_key(file_path, CONFIG_FILENAME)
            refreshAccountList()
            new_directory.set(self.clients.meta_save_path)
        def onEditClient():
            index = accountListBox.curselection()
            if len(index) == 0: return
            old_name = accountListBox.get(index)
            editClient(new = False, old_name = old_name)
        def onDeleteClient():
            index = accountListBox.curselection()
            if len(index) == 0: return
            name = accountListBox.get(index)
            self.clients.delete_client(name)
            refreshAccountList()
        def onViewConfirm():
                self.clients.owner = new_name.get()
                self.clients.meta_save_path = new_directory.get()
                self.clients.save_client_config(CONFIG_FILENAME) 
                close()
        def close():
            self.app.deiconify()
            window_view_client.destroy()
        self.app.withdraw()
        window_view_client = Toplevel(self.app)
        window_view_client.title("Edit your infomation")
        window_view_client.geometry('400x300')
        window_view_client.resizable(0, 0)
        try:
            window_view_client.iconphoto(False, PhotoImage(file='icon/eth_icon.png'))
        except:
            pass
        window_view_client.protocol("WM_DELETE_WINDOW", close)
        setUIToCenter(window_view_client, 400, 300)
        
        new_name = StringVar()  
        new_name.set(self.clients.owner)  
        Label(window_view_client, text='英文名稱: ').place(x=10, y=10, height=25)
        Entry(window_view_client, textvariable=new_name, width=35).place(x=70, y=10, height=25)
        
        new_directory = StringVar()
        new_directory.set(self.clients.meta_save_path)
        Label(window_view_client, text='儲存目錄: ').place(x=10, y=40, height=25)
        Entry(window_view_client, textvariable=new_directory, width=35).place(x=70, y=40, height=25)
        Button(window_view_client, text='瀏覽目錄', command=onOpenFile, width=EDIT_CLIENT_BUTTON_WIDTH) \
        .place(x=330, y=40, height=25)
        
        Button(window_view_client, text='增加帳戶', command=lambda: editClient(new = True), width=EDIT_CLIENT_BUTTON_WIDTH) \
        .place(x=330, y=70, height=25)
           
        account_list = StringVar() 
        account_list.set(value = [name for name in self.clients.client_dict])
        accountListBox = Listbox(window_view_client, listvariable= account_list, width=44, height=14)
        accountListBox.place(x=10, y=70)
    
        Button(window_view_client, text='編輯帳戶', command=onEditClient, width=EDIT_CLIENT_BUTTON_WIDTH) \
        .place(x=330, y=100, height=25)
        
        Button(window_view_client, text='匯入帳戶', command=onImportClient, width=EDIT_CLIENT_BUTTON_WIDTH) \
        .place(x=330, y=130, height=25)
        
        Button(window_view_client, text='刪除帳戶', command=onDeleteClient, width=EDIT_CLIENT_BUTTON_WIDTH) \
        .place(x=330, y=160, height=25)
        
        Button(window_view_client, text='確認', command=onViewConfirm, width=EDIT_CLIENT_BUTTON_WIDTH) \
        .place(x=330, y=270, height=25)
        
    
    def setMainUI(self):
        def start(cal_deposite = True):
            try:
                if not cal_deposite:
                    return self.clients.start_generate_summary_report_to_excel(save_filename = CONFIG_FILENAME)
                else:
                    return self.clients.start_summary_deposite_history(gui = True, save_filename = CONFIG_FILENAME)
            except Exception as e:
                print (e)
        def onGenerateReportFinish(res):
            enableUI()
        def onCheckDespositeFinish(res):
            if res: self.clients.process_summary_deposite_history(res, gui=True, app=self.app)
            enableUI()
            print("Deposit Finished")
        def onGenerateReportBtn():
            if self.clients.count == 0:
                print ('請先新增帳戶再進行操作。')
                return
            disableUI()
            scrolledTextBox.delete(1.0, END)
            t = gu.BaseThread(target = start, first= False, callback=onGenerateReportFinish, callback_args=())
            #t = threading.Thread(target = start, args=[False])
            t.start()
        def onCheckDespositeBtn():
            if self.clients.count == 0:
                print ('請先新增帳戶再進行操作。')
                return
            disableUI()
            scrolledTextBox.delete(1.0, END)
            t = gu.BaseThread(target = start, first= True, callback=onCheckDespositeFinish, callback_args=())
            t.setDaemon(True)
            t.start()
        def onDisplayAuthorInfo():
            def copy(widget):
                self.app.clipboard_clear()
                self.app.clipboard_append(widget.get(1.0, END))
                self.app.update()
            def onCopyEmail():
                return copy(email)
            def onCopyERC20():
                return copy(erc20)
            def onCopyTRC20():
                return copy(trc20)
            window_author_info = Toplevel(self.app)
            window_author_info.title("聯絡/贊助作者")
            window_author_info.geometry('400x300')  
            try:
                window_author_info.iconphoto(False, PhotoImage(file='icon/doge_icon.png'))
            except:
                pass
            setUIToCenter(window_author_info, 400, 300) 
            Label(window_author_info, text='Jason Huang', fg='blue').place(x=10, y=10)
            Label(window_author_info, text='立志轉職軟體工程師，熱衷研究幣圈投資', fg='blue').place(x=10, y=40)
            Label(window_author_info, text='若您覺得本軟體對您有幫助，歡迎小額贊助支持作者').place(x=10, y=70)
            
            ybase = 100
            Label(window_author_info, text='聯絡信箱:',fg='red').place(x=10, y=ybase)
            email = Text(window_author_info, height=1, borderwidth=0)
            email.insert(1.0, EMAIL)
            email.place(x=10, y=ybase+30)
            email.configure(state="disabled", bg=self.app.cget('bg'))
            Button(window_author_info, text='複製', command=onCopyEmail).place(x=120, y=ybase-2)
            
            Label(window_author_info, text='USDT ERC20地址:',fg='red').place(x=10, y=ybase+60)
            erc20 = Text(window_author_info, height=1, borderwidth=0)
            erc20.insert(1.0, ERC20)
            erc20.place(x=10, y=ybase+90)
            erc20.configure(state="disabled", bg=self.app.cget('bg'))
            Button(window_author_info, text='複製', command=onCopyERC20).place(x=120, y=ybase+58)
            
            Label(window_author_info, text='USDT TRC20地址:',fg='red').place(x=10, y=ybase+120)
            trc20 = Text(window_author_info, height=1, borderwidth=0)
            trc20.insert(1.0, TRC20)
            trc20.place(x=10, y=ybase+150)
            trc20.configure(state="disabled", bg=self.app.cget('bg'))
            Button(window_author_info, text='複製', command=onCopyTRC20).place(x=120, y=ybase+118)
            
            #Label(window_author_info, text='聯絡信箱: jasonyl13579@yahoo.com.tw').place(x=10, y=10)
        def onDisplayUsage():
            gu.infodialog('說明網址', 'https://reurl.cc/mqAKQG')
            #messagebox.showinfo('說明網址', 'https://medium.com/p/4c5a1c114552/')
        def onDisplayVersion():
            messagebox.showinfo('版本', VERSION)
        def disableUI():
            generateReportBtn['state'] = 'disabled'
            checkDepositeBtn['state'] = 'disabled'
        def enableUI():
            generateReportBtn['state'] = 'active'
            checkDepositeBtn['state'] = 'active'
        def onCloseApp():
            sys.stdout = self.originIO
            self.app.destroy()
        self.app = Tk() 
        self.app.title("Altcoin Account Management System")
        self.app.geometry(f'{root_width}x{root_height}')  
        self.app.resizable(0, 0)
        self.app.protocol("WM_DELETE_WINDOW", onCloseApp)
        try:
            self.app.iconphoto(False, PhotoImage(file='icon/bitcoin_icon.png'))
        except:
            pass
        setUIToCenter(self.app, root_width, root_height)
        
        menubar = Menu(self.app)
        
        clientmenu = Menu(menubar, tearoff=0)
        clientmenu.add_command(label="檢視帳戶 (View Client)", command=self.onViewClient)
        menubar.add_cascade(label="帳戶(Client)", menu=clientmenu)
        
        authormenu = Menu(menubar, tearoff=0)
        authormenu.add_command(label="使用說明(Usage)", command=onDisplayUsage)
        authormenu.add_command(label="聯絡/贊助作者(Author Info)", command=onDisplayAuthorInfo)
        authormenu.add_command(label="版本資訊(Version Info)", command=onDisplayVersion)
        menubar.add_cascade(label="其他(Other)", menu=authormenu)
        self.app.config(menu=menubar)
        
        Label(self.app, text='請小心保管您的API私錀，切勿外洩！如有疑慮可以關閉交易功能。本軟體僅使用查閱API', fg='red').place(x=20, y=8, height=25)
         
        scrolledTextBox = ScrolledText(self.app, width=60, height=18,font=18)
        scrolledTextBox.place(x=20, y=32)
        p1 = PrintLogger(scrolledTextBox)
        sys.stdout = p1
        
        generateReportBtn = Button(self.app, text="計算報告", command=onGenerateReportBtn, width=APP_BUTTON_WIDTH)
        generateReportBtn.place(x=20, y=340)
        
        checkDepositeBtn = Button(self.app, text="匯入入金紀錄", command=onCheckDespositeBtn, width=APP_BUTTON_WIDTH)
        checkDepositeBtn.place(x=120, y=340)
        '''
        entry_deposite = Entry(app, width=35)
        entry_deposite.place(x=220, y=340, height=25)
        r1 = InputLogger(scrolledTextBox)
        sys.stdin = r1
        '''
    def run(self):
        self.app.mainloop()
#%% main
if __name__ == '__main__':
    pass
   # window = GUI()
   # window.setMainUI()
   # window.run()
    