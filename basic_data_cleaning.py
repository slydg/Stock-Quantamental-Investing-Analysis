import numpy as np 
import pandas as pd
import tushare as ts 
from time import sleep
import datetime
import math


def data_processing(dataset_income,dataset_income_next,dataset_balancesheet,dataset_cashflow,dataset_fina,industry,posit,s3=False):
    # try to find the rows with year of 2019, we only want to keep year 2019
    def first_four(d):
        return(d//10000)

    #the original data has lots of annual report of 2018, we onl want ququartely report
    dataset_income['year']=dataset_income.end_date.apply(first_four)
    dataset_income=dataset_income[dataset_income.year!=2018]

    dataset_income_next['year']=dataset_income_next.end_date.apply(first_four)
    dataset_income_next=dataset_income_next[dataset_income_next.year!=2018]

    dataset_balancesheet['year']=dataset_balancesheet.end_date.apply(first_four)
    dataset_balancesheet=dataset_balancesheet[dataset_balancesheet.year!=2018]

    dataset_cashflow['year']=dataset_cashflow.end_date.apply(first_four)
    dataset_cashflow=dataset_cashflow[dataset_cashflow.year!=2018]

    dataset_fina['year']=dataset_fina.end_date.apply(first_four)
    dataset_fina=dataset_fina[dataset_fina.year!=2018]


    #delect columns with missing values more than 30%
    dataset_income= dataset_income.loc[:, dataset_income.isnull().mean() < .3]

    dataset_income_next = dataset_income_next.loc[:, dataset_income_next.isnull().mean() < .3]

    dataset_balancesheet = dataset_balancesheet.loc[:, dataset_balancesheet.isnull().mean() < .3]

    dataset_cashflow = dataset_cashflow.loc[:, dataset_cashflow.isnull().mean() < .3]

    dataset_fina = dataset_fina.loc[:, dataset_fina.isnull().mean() < .3]

    #delete duplicated rows with the same stock code
    dataset_income      = dataset_income.drop_duplicates('ts_code')
    dataset_income_next       = dataset_income_next.drop_duplicates('ts_code')
    dataset_cashflow    = dataset_cashflow.drop_duplicates('ts_code')
    dataset_balancesheet = dataset_balancesheet.drop_duplicates('ts_code')
    dataset_fina        = dataset_fina.drop_duplicates('ts_code')


    #combine different datasets into one

    if not s3:
        #at first, we have to drop unnecessary columns and add date from income sheet quarter 3 to income sheet quarter 2
        dataset_income_next       = dataset_income_next.loc[:,['ts_code','f_ann_date']]
        session12_income          = pd.DataFrame.merge(dataset_income,dataset_income_next,on='ts_code')
    else:
        session12_income          = dataset_income
    session12_income              = session12_income.drop(['year'],axis=1)
    dataset_cashflow    = dataset_cashflow.drop(['year','ann_date','f_ann_date','end_date','comp_type','report_type'],axis=1)
    dataset_balancesheet = dataset_balancesheet.drop(['year','ann_date','f_ann_date','end_date','comp_type','report_type'],axis=1)
    dataset_fina        = dataset_fina.drop(['ann_date','end_date','year'],axis=1)

    #second, we can combine these columns together
    session12_income_cashflow                    = pd.DataFrame.merge(session12_income,dataset_cashflow,on='ts_code')
    session12_income_cashflow_balancesheet       = pd.DataFrame.merge(session12_income_cashflow,dataset_balancesheet,on='ts_code')
    session12_income_cashflow_balancesheet_fina  = pd.DataFrame.merge(session12_income_cashflow_balancesheet,dataset_fina,on='ts_code')
    session12_income_cashflow_balancesheet_fina  = session12_income_cashflow_balancesheet_fina.loc[:, ~session12_income_cashflow_balancesheet_fina.columns.str.contains('^Unnamed')]

    #third, we have to fill missing value based on different industry
    session12_income_cashflow_balancesheet_fina_clean = pd.DataFrame.merge(session12_income_cashflow_balancesheet_fina,industry,on='ts_code')
    gk                                                = session12_income_cashflow_balancesheet_fina_clean.groupby('industry').transform(lambda x: x.fillna(x.mean())).reset_index(drop=True)
    gk.isnull().values.sum()
    gk                                                = gk.fillna(0)
    columnnames                                       = ['ts_code','industry','area','name']
    gk[columnnames]                                   = session12_income_cashflow_balancesheet_fina_clean[columnnames]
    #through this way you can clean all the datafile that you have downloaded

    #combine the dataset
    gk.to_csv(posit)



for i in range(1,4):
    dataset_income       = pd.read_csv('./basic_data/session'+str(i)+'_income.csv')
    dataset_income_next  = pd.read_csv('./basic_data/session'+str(i+1 if i != 3 else 3)+'_income.csv')
    dataset_balancesheet = pd.read_csv('./basic_data/session'+str(i)+'_balance.csv')
    dataset_cashflow     = pd.read_csv('./basic_data/session'+str(i)+'_cashflow.csv')
    dataset_fina         = pd.read_csv('./basic_data/session'+str(i)+'_fina_indicator.csv')
    industry             = pd.read_csv('./basic_data/stock_info.csv')
    if i != 3:
        posit = 'season' + str(i) + str(i+1) + '_final.csv'
        s3 = False
    else:
        s3 = True
        posit = './basic_data/season' + str(i) + '_final.csv'
    data_processing(dataset_income, dataset_income_next, dataset_balancesheet, dataset_cashflow, dataset_fina, industry, posit, s3=s3)
