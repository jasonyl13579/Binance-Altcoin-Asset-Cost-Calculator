# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 18:16:30 2020

@author: Corn
"""
import pickle
import pandas as pd
from source.timeutil import *
from clients.clientinfo import ClientInfo
from openpyxl import load_workbook
from openpyxl.styles import Border, Side, Font
#import styleframe as styleframe



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
def load_excel(filename, sheet_name, truncate_sheet):
    startrow = None
    writer = pd.ExcelWriter(filename, engine='openpyxl')
    try:
        # try to open an existing workbook
        writer.book = load_workbook(filename)

        # get the last row in the existing Excel sheet
        # if it was not specified explicitly
        if startrow is None and sheet_name in writer.book.sheetnames:
            startrow = writer.book[sheet_name].max_row

        # truncate sheet
        if truncate_sheet and sheet_name in writer.book.sheetnames:
            # index of [sheet_name] sheet
            idx = writer.book.sheetnames.index(sheet_name)
            # remove [sheet_name]
            writer.book.remove(writer.book.worksheets[idx])
            # create an empty sheet [sheet_name] using old index
            writer.book.create_sheet(sheet_name, idx)

        # copy existing sheets
        writer.sheets = {ws.title:ws for ws in writer.book.worksheets}
    except FileNotFoundError:
        # file does not exist yet, we will create it
        pass
    return (startrow, writer)
def generate_single_report_to_excel(assets, accountname, file_path='./', truncate_sheet=False):
    if 'USDT' in assets: del assets['USDT']
    if 'USD' in assets: del assets['USD']
    source = [v.__dict__ for k, v in sorted(assets.items(), key=lambda d:d[0])]
    
    df = pd.DataFrame(source)
    df['last_query_timestamp'].fillna(value=DEFAULT_EPOCH_TIME, inplace=True)
    most_recent_date = df['last_query_timestamp'].max()
    df['last_query_timestamp'] = [datetime_to_utc_time(x) for x in df['last_query_timestamp']]
    df['利潤'] = df['current_price'] * df['qty'] - df['quoteQty']
    df['USDT 價值'] = df['current_price'] * df['qty']
    
    df.rename(columns = {'name':'貨幣種類', 'cost': '價格成本', 'qty': '持有數量', 'quoteQty': '買進總成本', \
                         'current_price': '現價', 'transection_count': '交易次數', 'last_query_timestamp' : '最後交易時間'}, inplace = True)    
    df = df[['貨幣種類','利潤','價格成本','現價','買進總成本','USDT 價值','持有數量', '交易次數', '最後交易時間' ]]    
    df = df.sort_values('利潤', ascending=False)
    summary = pd.DataFrame.from_dict( {"貨幣種類": ['TOTAL'],
                               "利潤":[df['利潤'].sum()],
                               "價格成本":[None],
                               "現價":[None],
                               "買進總成本":[None],
                               'USDT 價值':[None],
                               '持有數量':[None], 
                               '交易次數':[df['交易次數'].sum()], 
                               '最後交易時間':[datetime_to_utc_time(most_recent_date)]}) 
    df = df.append(summary,ignore_index=True)
    
    
    filename = file_path + '電子貨幣實時盈虧計算.xlsx'
    sheet_name = accountname
    header = False
    (startrow, writer) = load_excel(filename, sheet_name, truncate_sheet)
    df.style.applymap(color_negative_red, subset = ['利潤']).to_excel(writer, sheet_name=sheet_name, float_format="%.4f")
    
    #df[positive].style.applymap(lambda x: 'background-color: green', subset=df['利潤'] ).to_excel(writer, sheet_name='成本計算')
    
    worksheet = writer.sheets[sheet_name] 
    for column_cells in worksheet.columns:
        worksheet.column_dimensions[column_cells[0].column_letter].width = 18
    #Iterate through each column and set the width == the max length in that column. A padding length of 2 is also added. 
    # for i in range(len(df.columns)): 
    #     worksheet.set_column(i+1, i+1, 12)  
    # i = df.columns.get_loc("最後交易時間")
    # worksheet.set_column(i+1, i+1, 20) 
    '''
    srcfile = openpyxl.load_workbook(file_path + '電子貨幣實時盈虧計算.xlsx',read_only=False, keep_vba= True)#to open the excel sheet and if it has macros
    sheetname = srcfile.get_sheet_by_name('成本計算')
    sheetname.cell(row=20,column=1).value = time.ctime() 
    srcfile.save(file_path + '電子貨幣實時盈虧計算.xlsx')
    '''
    writer.save() 
    writer.close()
    #df.to_html('filename.html')
#save_to_excel('assets', '../')
#sf = styleframe.StyleFrame(df) 
'''
with pd.ExcelWriter('output.xlsx') as writer:
    df.to_excel(writer, sheet_name='Sheet1', float_format="%.4f")
    writer.save()
'''

def generate_summary_report_to_excel(clients_dict, meta_file_path='./', truncate_sheet=False):
    
    
    for client in clients_dict.values():
        print (client)
    #source_dict = { '資產更新時間': datetime_to_utc_time(get_current_timestamp())}
    #sorted(assets.items(), key=lambda d:d[0]
    source_columns = ['資產更新時間']
    profit_data = []
    source_data = [datetime_to_utc_time(get_current_timestamp())]
    for client_name, client in sorted(clients_dict.items(),key=lambda d:d[1].info.index):
        profit_data.append(client_name + '_利潤')
        source_columns.append(client_name + '_利潤')
        source_columns.append(client_name + '_資產數量')
        source_data.append(client.info.profit)
        source_data.append(client.info.asset_num)
        #source_dict[ client_name + '_利潤'] = client.info.profit
        #source_dict[ client_name + '_資產數量'] = client.info.asset_num
    
    df = pd.DataFrame([source_data], columns=source_columns)
    filename = meta_file_path + '電子貨幣實時盈虧計算.xlsx'
    sheet_name = 'Summary'
    header = False
    (startrow, writer) = load_excel(filename, sheet_name, truncate_sheet)
    if startrow is None:
        startrow = 0
        header = True
    # write out the new sheet
     
    df.style.applymap(color_negative_red, subset = profit_data).to_excel(writer, sheet_name=sheet_name, startrow=startrow, float_format="%.4f", index=False, header=header)
    ws= writer.sheets[sheet_name]
    thin = Side(border_style="thin", color="000000")
    for index, column_cells in enumerate(ws.columns):
        cell = ws.cell(row=1, column=index+1)
        cell.value = source_columns[index]
        cell.font = Font(bold=True)
        cell.border = Border(top=thin, left=thin, right=thin, bottom=thin)
        ws.column_dimensions[column_cells[0].column_letter].width = 24
    
    # save the workbook
    writer.save()