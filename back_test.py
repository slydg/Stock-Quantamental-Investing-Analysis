import pandas as pd 
import numpy as np 
from sklearn.metrics import r2_score
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
import os
import datetime
import time 
from dateutil.relativedelta import relativedelta
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt 
import matplotlib.patches as mpatches
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
import seaborn as sns

"""
This file is used to define a trading strategy and back testing the performance of our model
and conpare the poeformance using stock chosing with portfolio adjustment and that without adjustment.
"""

# Calculating the relative rank. (Which means the percentage of total number of the stocks that are better than the given stock)
def function_rank(df,target,value):
    data = df.groupby(target)[value].rank(ascending=False)
    cont = df.groupby(target)[value].count()
    return data/df[target].map(lambda x: cont[x])

# Loading the model saved before
price_model = joblib.load('./price_model.model')

features = ['roe_yearly', 'roa2_yearly', 'equity_yoy', 'prepayment',
       'invest_capital', 'networking_capital', 'taxes_payable',
       'tangible_asset', 'st_borr', 'capital_rese_ps', 'notes_receiv',
       'c_fr_oth_operate_a', 'current_exint', 'payroll_payable',
       'n_incr_cash_cash_equ', 'working_capital', 'minority_int',
       'q_saleexp_to_gr', 'defer_inc_non_cur_liab', 'ar_turn',
       'non_oper_income', 'saleexp_to_gr', 'non_oper_exp', 'st_cash_out_act',
       'cogs_of_sales', 'lt_eqt_invest', 'defer_tax_assets', 'lt_amor_exp',
       'longdeb_to_debt', 'surplus_rese_ps', 'dt_eps_yoy', 'roe_dt',
       'stot_cash_in_fnc_act', 'c_paid_to_for_empl', 'compr_inc_attr_p',
       'q_sales_yoy', 'fcfe', 'invest_income', 'roic', 'ocfps', 'retainedps',
       'turn_days', 'assets_turn', 'stot_out_inv_act', 'adminexp_of_gr',
       'eff_fx_flu_cash', 'biz_tax_surchg', 'dt_netprofit_yoy',
       'tbassets_to_totalassets', 'c_pay_dist_dpcp_int_exp', 'ca_turn',
       'admin_exp', 'roe', 'roe_waa']

# All stocks exchanged in Shanghai with data usable 
stock_lst = pd.read_csv('./basic_data/s3.csv')[features+['ts_code', 'f_ann_date', 'industry','re_bf']]

# Processing variables
for cl in stock_lst.columns:
    if cl in ['industry','f_ann_date','ts_code']:
        continue
    stock_lst[cl] = function_rank(stock_lst,'industry',cl)

# Calculating predicted label
stock_lst['forecast'] = price_model.predict(stock_lst[features])

# Finding all the industries performed well (top 20) in last season
inds = pd.read_csv('./basic_data/s3.csv')[['industry','re_bf']]
means = inds.groupby('industry')['re_bf'].mean()
inds['re_bf'] = inds['industry'].map(lambda x: means[x])
inds = inds.drop_duplicates()
inds['re_bf_rank'] = inds['re_bf'].rank(ascending=False)
inds = inds[inds['re_bf_rank']<=20]['industry']

# Choosing stocks in the selected industries and with a lable 1
stocks_chosen = stock_lst[stock_lst['industry'].isin(inds.values)]
stocks_chosen = stocks_chosen[stocks_chosen['forecast']==1][['ts_code','f_ann_date','re_bf']]

# Dropping stocks with no complete data
l = len(pd.read_csv('./ts_data/000001.SZ_20191031.csv'))
for stock in stocks_chosen[['ts_code','f_ann_date']].values:
    price = pd.read_csv('./ts_data/'+stock[0]+'_20191031.csv')
    if len(price) != l:
        stocks_chosen = stocks_chosen.drop(index=stocks_chosen[stocks_chosen['ts_code'] == stock[0]].index[0])

# Getting the price of the given date
def price_today(stocks, date):
    prices = {}
    for stock in stocks[['ts_code','f_ann_date']].values:
        price = pd.read_csv('./ts_data/'+stock[0]+'_20191031.csv')
        price = price[price['trade_date']==date]['close'].values
        prices[stock[0]] = price
    pt = stocks['ts_code'].map(lambda x: prices[x])
    return pt

# Getting top stocks based on the given column
def tops(stocks, col):
    stocks['rank'] = stocks[col].rank(ascending=False)
    return stocks[stocks['rank']<len(stocks)/3]['ts_code']

# Distributing the money to every stock in our portfolio
def stock_input(stocks, port):
    return stocks.apply(lambda x: 100000 if x['ts_code'] in port.values else 0, axis=1) 

# Calculating the amount of each stock
def amount(stocks):
    prices = {}
    for stock in stocks[['ts_code','f_ann_date']].values:
        price = pd.read_csv('./ts_data/'+stock[0]+'_20191031.csv')
        price = price[price['trade_date']==20191031]['close'].values
        prices[stock[0]] = price
    am = stocks.apply(lambda x: x['input'] / prices[x['ts_code']], axis=1) 
    return am

# Calculating the new assets and returns of each stock if no changing portfolio 
def returns(stocks, end_time):
    assets = (stocks['price_today'] * stocks['amount'])
    _returns = stocks['price_today'] / stocks['price_begin']
    return _returns, assets

# Adjusting portfolio
def change(stocks, ranks, port):
    # stocks['in_rank'] = stocks['re_bf'].rank(ascending=True)
    avrage_assets = sum(stocks['asset']) / len(ranks)
    stocks['asset_should_be'] = stocks.apply(lambda x: avrage_assets if x['ts_code'] in ranks.values else 0, axis=1) 
    stocks['change'] = stocks['asset_should_be'] - stocks['asset'] 
    stocks['asset'] = stocks.apply(lambda x: x['asset'] + 0.9995 * x['change'] if x['change'] >= 0 else x['asset'] + x['change'], axis=1)
    stocks['amount'] = stocks['asset'] / stocks['price_today']
    return ranks, stocks['amount'], stocks['asset']

# All the information needed before going into the market
portfolio = tops(stocks_chosen,'re_bf')
stocks_chosen['input'] = stock_input(stocks_chosen, portfolio)
stocks_chosen['price_begin'] = price_today(stocks_chosen, 20191031)
stocks_chosen['asset'] = stocks_chosen['input']
stocks_chosen['amount'] = amount(stocks_chosen)
total_input = sum(stocks_chosen['input'])

print('****************** Begin Investing ******************')
print('Our total input: ')
print(total_input)

# All the trading days

days = pd.read_csv('./ts_data/000001.SZ_20191031.csv')['trade_date'].values[:-1]

# Begining back testing
rate_without_portfolio_adjustment=[]
rate_with_portfolio_adjustment=[]
for end_date in days[::-1]:
    stocks_chosen['price_today'] = price_today(stocks_chosen, int(end_date))
    stocks_chosen['return_till_today'], stocks_chosen['asset'] = returns(stocks_chosen,end_date)
    ranks = tops(stocks_chosen,'return_till_today')
    portfolio, stocks_chosen['amount'] , stocks_chosen['asset'] = change(stocks_chosen, ranks, portfolio)
    total_asset = sum(stocks_chosen['asset']) 
    rate_without_portfolio_adjustment.append(sum(stocks_chosen['return_till_today'])/len(stocks_chosen))
    rate_with_portfolio_adjustment.append(total_asset/total_input)

# Calculating return rate
print('Return rate using portfolio adjustment: ')
print(rate_with_portfolio_adjustment[-1][0])
print('Return rate without portfolio adjustment: ')
print(rate_without_portfolio_adjustment[-1][0])

#drawing the plot
reinstatement = pd.read_csv('./basic_data/reinstatement.csv')['close'].values
market_return_list=[]
for close in reinstatement[:-1]:
    return_rate=close/reinstatement[-1]
    market_return_list.append(return_rate)
date_list=[]
for day in days:
    day=datetime.strptime(str(day),'%Y%m%d')
    date_list.append(day)
days=pd.to_datetime(date_list,format="%Y%m%d")
matplotlib.rcParams['figure.figsize'] = (25.0, 10.0)
plt.plot(days[::-1],rate_with_portfolio_adjustment,color=sns.xkcd_rgb["pale red"],linewidth=1.5)
plt.plot(days[::-1],rate_without_portfolio_adjustment,color=sns.xkcd_rgb["medium green"],linewidth=1.5)
plt.plot(days[::-1],market_return_list[::-1],color= sns.xkcd_rgb["denim blue"],linewidth=1.5)
plt.xlabel('Trading Days')
plt.ylabel('Return Rate')
red_patch = mpatches.Patch(color=sns.xkcd_rgb["pale red"], label='Return rate with portfolio adjustment')
green_patch = mpatches.Patch(color=sns.xkcd_rgb["medium green"], label='Return rate without portfolio adjustment')
black_patch = mpatches.Patch(color=sns.xkcd_rgb["denim blue"], label='The Market Return Rate')
plt.legend(handles=[red_patch,green_patch,black_patch])
plt.gcf().autofmt_xdate()
sns.set_style("darkgrid")
plt.grid()
plt.savefig('back_test_result.png') 
plt.show()