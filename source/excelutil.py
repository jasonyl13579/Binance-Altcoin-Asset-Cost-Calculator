# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 18:16:30 2020

@author: Corn
"""
import pickle
import pandas as pd
#import styleframe as styleframe
from datetime import datetime


def load_obj(name):
    try:
        with open('obj/' + name + '.pkl', 'rb') as f:
            return pickle.load(f)
    except:
        return {}
def highlight_max(data, color='yellow'):
    '''
    highlight the maximum in a Series or DataFrame
    '''
    attr_g = 'background-color: green'
    attr_r = 'background-color: red'
    print (data)
    is_max = data > 0
    return [attr_g if v else '' for v in is_max]
def color_negative_red(val):
    """
    Takes a scalar and returns a string with
    the css property `'color: red'` for negative
    strings, black otherwise.
    """
    color = 'red' if val < 0 else 'green'
    return 'color: %s' % color
def save_to_excel(file_name, file_path='./'):
    assets = load_obj(file_name)
    source = [v.__dict__ for k, v in sorted(assets.items(), key=lambda d:d[0])]
   # for k, v in sorted(assets.items(), key=lambda d:d[0]):
    #sorted(assets.items(), key=lambda d:d[0])
    #print (source)
    df = pd.DataFrame(source)
    df['last_query_timestamp'].fillna(value=1097000000000, inplace=True)
    df['last_query_timestamp'] = [datetime.utcfromtimestamp(x/1000).strftime("%Y-%m-%d %H:%M:%S") for x in df['last_query_timestamp']]
    df['利潤'] = df['current_price'] * df['qty'] - df['quoteQty']
    df['USDT 價值'] = df['current_price'] * df['qty']
    
    df.rename(columns = {'name':'貨幣種類', 'cost': '價格成本', 'qty': '持有數量', 'quoteQty': '買進總成本', \
                         'current_price': '現價', 'transection_count': '交易次數', 'last_query_timestamp' : '最後交易時間'}, inplace = True)    
    df = df[['貨幣種類','利潤','價格成本','現價','買進總成本','USDT 價值','持有數量', '交易次數', '最後交易時間' ]]    
    positive = (df['利潤'] > 0)

    writer = pd.ExcelWriter(file_path + '電子貨幣實時盈虧計算.xlsx')
    df.style.applymap(color_negative_red, subset = ['利潤']).to_excel(writer, sheet_name='成本計算', float_format="%.4f")
    
    #df[positive].style.applymap(lambda x: 'background-color: green', subset=df['利潤'] ).to_excel(writer, sheet_name='成本計算')
    
    worksheet = writer.sheets['成本計算'] 
    #Iterate through each column and set the width == the max length in that column. A padding length of 2 is also added. 
    for i in range(len(df.columns)): 
        worksheet.set_column(i+1, i+1, 12)  
    i = df.columns.get_loc("最後交易時間")
    worksheet.set_column(i+1, i+1, 20) 
    
    writer.save() 
    #df.to_html('filename.html')
#save_to_excel('assets', '../')
#sf = styleframe.StyleFrame(df) 
'''
with pd.ExcelWriter('output.xlsx') as writer:
    df.to_excel(writer, sheet_name='Sheet1', float_format="%.4f")
    writer.save()
'''