import pandas as pd 
import numpy as np 
import tushare as ts 
import datetime
import time 
from dateutil.relativedelta import relativedelta
from sklearn.linear_model import LassoCV
import matplotlib

# Preparing for the data download.
# set your tushare.pro token here 
token = 'your token'
ts.set_token(token)
pro = ts.pro_api()

"""
# First, we may want to built the dependent variables.
# We choose the average return rate after 3 months after the publication of the seasonal financial report of each company
# This should have some relationship with the basic financial information of the company.
"""

def reter_r(data):
    # Getting the seasonal return data
    re_s = []
    re_m = []
    re_l = []
    re_bf = []
    date = 'f_ann_date_x' if 'f_ann_date_x' in data.columns else 'f_ann_date'
    for stock in data[['ts_code',date]].values:
        code, date = stock[0], stock[1]
        date = stock[1] if 'f_ann_date_x' in data.columns else '20191031'
        sdate = datetime.datetime.strptime(str(date)[:4] + '.' + str(date)[4:6] + '.' + str(date)[6:] ,'%Y.%m.%d')
        edate = sdate + relativedelta(months=4)
        edate = str(edate.strftime("%Y%m%d"))
        df = ts.pro_bar(ts_code=code, adj='qfq',freq='M', asset='E', start_date=str(date), end_date=str(edate))['pct_chg']
        if len(df) < 1:
            re_s.append(0)
        else:
            re_s.append(df[0])
        if len(df) < 2:
            re_m.append(0)
        else:
            re_m.append( 100 * (((1+df[0]*0.01) * (1+df[1]*0.01)) ** (1/2) - 1) )
        if len(df) < 3:
            re_l.append(0)
        else:
            re_l.append( 100 * (((1+df[0]*0.01) * (1+df[1]*0.01) * (1+df[2]*0.01)) ** (1/3) - 1) )

        edate = sdate + relativedelta(months=-3)
        edate = str(edate.strftime("%Y%m%d"))
        try:
            df = ts.pro_bar(ts_code=code, adj='qfq',freq='M', asset='E', start_date=str(edate), end_date=str(date))['pct_chg']
        except:
            df = [0,0,0]
        if len(df) < 3:
            re_bf.append(0)  
        else:    
            re_bf.append(100 * (((1+df[0]*0.01) * (1+df[1]*0.01) * (1+df[2]*0.01)) ** (1/3) - 1))
            print(((1+df[0]*0.01) * (1+df[1]*0.01) * (1+df[2]*0.01)) ** (1/3) - 1)
        print(code)
        time.sleep(0.5)

    data['re_s'] = re_s
    data['re_m'] = re_m
    data['re_l'] = re_l
    data['re_bf'] = re_bf

    return data



data = pd.read_csv('basic_data/season12_final.csv')

data = reter_r(data)

data.to_csv('basic_data/s12.csv',index=False)



data = pd.read_csv('basic_data/season23_final.csv')

data = reter_r(data)

data.to_csv('basic_data/s23.csv',index=False)



data = pd.read_csv('basic_data/season3_final.csv')

data = reter_r(data)

data.to_csv('basic_data/s3.csv',index=False)




