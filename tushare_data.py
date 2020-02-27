import numpy as np 
import pandas as pd
import tushare as ts 
from time import sleep
import datetime

# set your tushare.pro token here 
token = 'your token'


# get all the stock code
ts.set_token(token)
pro    = ts.pro_api()
stocks = pro.stock_basic(exchange='SSE', list_status='L', fields='ts_code')
stocks = pro.stock_basic()['ts_code']

# back_test stock index 
reinstatement=ts.pro_bar(ts_code='000001.SH', asset='I', start_date='20191031', end_date='20200123')
#save data 
reinstatement.to_csv('./basic_data/reinstatement.csv')

# back_test stock index 
info=pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
#save data 
info.to_csv('./basic_data/stock_info.csv')

#seeting date of the financial statement
quarter1_start_date = '20190401'
quarter1_end_date   = '20190431'
quarter2_start_date = '20190701'
quarter2_end_date   = '20190831'
quarter3_start_date = '20191001'
quarter3_end_date   = '20191031'

#initalize 3 dataframes
dataset1 = pd.DataFrame()
dataset2 = pd.DataFrame()
dataset3 = pd.DataFrame()


#income
#use API to get the income sheet from tushare
frequency=0
for stock in stocks:
    try:
        Financial_data_income_stock_first  = pro.income(ts_code=stock, start_date= quarter1_start_date, end_date=quarter1_end_date)
        Financial_data_income_stock_second = pro.income(ts_code=stock, start_date= quarter2_start_date, end_date=quarter2_end_date)
        Financial_data_income_stock_third  = pro.income(ts_code=stock, start_date= quarter3_start_date, end_date=quarter3_end_date)
    except:
        continue
    dataset1 = dataset1.append(Financial_data_income_stock_first)
    dataset2 = dataset2.append(Financial_data_income_stock_second)
    dataset3 = dataset3.append(Financial_data_income_stock_third)
    frequency+=1
    if frequency%100==0:
        print(frequency)

   

print(dataset1,dataset2,dataset3)

#save data in your location
dataset1.to_csv('./basic_data/session1_income.csv')
dataset2.to_csv('./basic_data/session2_income.csv')
dataset3.to_csv('./basic_data/session3_income.csv')


#initalize 3 dataframes
dataset1 = pd.DataFrame()
dataset2 = pd.DataFrame()
dataset3 = pd.DataFrame()
#balance sheet
#use API to get the banalce sheet from tushare
frequency=0
for stock in stocks:
    try:
        Financial_data_balancesheet_stock_first  = pro.balancesheet(ts_code=stock, start_date= quarter1_start_date, end_date=quarter1_end_date)
        Financial_data_balancesheet_stock_second = pro.balancesheet(ts_code=stock, start_date= quarter2_start_date, end_date=quarter2_end_date)
        Financial_data_balancesheet_stock_third  = pro.balancesheet(ts_code=stock, start_date= quarter3_start_date, end_date=quarter3_end_date)
    except:
        continue
    dataset1 = dataset1.append(Financial_data_balancesheet_stock_first)
    dataset2 = dataset2.append(Financial_data_balancesheet_stock_second)
    dataset3 = dataset3.append(Financial_data_balancesheet_stock_third)
    frequency+=1
    if frequency%100==0:
        print(frequency)

print(dataset1,dataset2,dataset3)

#save data in your location
dataset1.to_csv('./basic_data/session1_balance.csv')
dataset2.to_csv('./basic_data/session2_balance.csv')
dataset3.to_csv('./basic_data/session3_balance.csv')


#initalize 3 dataframes
dataset1 = pd.DataFrame()
dataset2 = pd.DataFrame()
dataset3 = pd.DataFrame()

#cashflow
#use API to get the fina_indicator from tushare
frequency=0
for stock in stocks:
    try:
        Financial_data_cashflow_stock_first  = pro.cashflow(ts_code=stock, start_date= quarter1_start_date, end_date=quarter1_end_date)
        Financial_data_cashflow_stock_second = pro.cashflow(ts_code=stock, start_date= quarter2_start_date, end_date=quarter2_end_date)
        Financial_data_cashflow_stock_third  = pro.cashflow(ts_code=stock, start_date= quarter3_start_date, end_date=quarter3_end_date)
    except:
        continue
    dataset1 = dataset1.append(Financial_data_cashflow_stock_first)
    dataset2 = dataset2.append(Financial_data_cashflow_stock_second)
    dataset3 = dataset3.append(Financial_data_cashflow_stock_third)
    frequency+=1
    if frequency%100==0:
        print(frequency)

print(dataset1,dataset2,dataset3)

#save data in your location
dataset1.to_csv('./basic_data/session1_cashflow.csv')
dataset2.to_csv('./basic_data/session2_cashflow.csv')
dataset3.to_csv('./basic_data/session3_cashflow.csv')


#initalize 3 dataframes
dataset1 = pd.DataFrame()
dataset2 = pd.DataFrame()
dataset3 = pd.DataFrame()

#fina_indicator
#use API to get the fina_indicator from tushare
frequency=0
for stock in stocks:
    try:
        Financial_data_fina_indicator_stock_first  = pro.fina_indicator(ts_code=stock, start_date= '20190101', end_date='20190431')
        Financial_data_fina_indicator_second = pro.fina_indicator(ts_code=stock, start_date= '20190601', end_date='20190831')
        Financial_data_fina_indicator_third  = pro.fina_indicator(ts_code=stock, start_date= '20190901', end_date='20191031')
    except:
        continue
    dataset1 = dataset1.append(Financial_data_fina_indicator_stock_first)
    dataset2 = dataset2.append(Financial_data_fina_indicator_second)
    dataset3 = dataset3.append(Financial_data_fina_indicator_third)
    frequency+=1
    if frequency%100==0:
        print(frequency)

print(dataset1,dataset2,dataset3)

#save data in your location
dataset1.to_csv('./basic_data/session1_fina_indicator.csv')
dataset2.to_csv('./basic_data/session2_fina_indicator.csv')
dataset3.to_csv('./basic_data/session3_fina_indicator.csv')

