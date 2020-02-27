import pandas as pd 
import numpy as np 
import tushare as ts 
import datetime
import time 
from dateutil.relativedelta import relativedelta
from sklearn.linear_model import LassoCV
import matplotlib

# Preparing data downloading
# set your tushare.pro token here 
token = 'your token'
ts.set_token(token)
pro = ts.pro_api()

# All stocks
data = pd.read_csv('./basic_data/season3_final.csv', encoding='utf_8_sig')

# Downloading market daily data begining on 2019.10.31
for line in data[['ts_code','f_ann_date']].values:
    code, begin_time = line[0], '20191031'
    print(code+'_'+str(begin_time))
    sdate = datetime.datetime.strptime(str(begin_time)[:4] + '.' + str(begin_time)[4:6] + '.' + str(begin_time)[6:] ,'%Y.%m.%d')
    edate = sdate + relativedelta(months=3)
    end_date = str(edate.strftime("%Y%m%d"))
    try:
        stock_time_series = ts.pro_bar(ts_code=code, ma=[5,10,20], asset='E', adj='qfq', start_date=str(begin_time), end_date=end_date, factors=['tor', 'vr'])
        stock_time_series.to_csv('./ts_data/'+code+'_'+str(begin_time)+'.csv')
    except:
        time.sleep(0.5)
        continue
    time.sleep(0.5)

