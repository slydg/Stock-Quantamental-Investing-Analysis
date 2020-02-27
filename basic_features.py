import pandas as pd 
import numpy as np 
import tushare as ts 
import datetime
import time 
from dateutil.relativedelta import relativedelta
from sklearn.linear_model import LassoCV
import matplotlib
import matplotlib.pyplot as plt
from sklearn.preprocessing import Imputer
import seaborn as sns

"""
This file will find out the features that may influent the average return of the next 3 months
using LASSO model and Cross Validation method.
"""

# Calculating the relative rank. (Which means the percentage of total number of the stocks that are better than the given stock)
def function_rank(df,target,value):
    data = df.groupby(target)[value].rank(ascending=False)
    cont = df.groupby(target)[value].count()
    return data/df[target].map(lambda x: cont[x])

# Reading files
data_s1 = pd.read_csv('./basic_data/s12.csv', encoding='utf_8_sig').drop(['Unnamed: 0'], axis=1).fillna(0)
data_s2 = pd.read_csv('./basic_data/s23.csv', encoding='utf_8_sig').drop(['Unnamed: 0'], axis=1).fillna(0)
data_s1 = data_s1.drop(['symbol','comp_type','name','list_date','ts_code','f_ann_date_x','f_ann_date_y','end_date','ann_date','area','report_type'], axis=1)
data_s2 = data_s2.drop(['symbol','comp_type','name','list_date','ts_code','f_ann_date_x','f_ann_date_y','end_date','ann_date','area','report_type'], axis=1)
data = pd.concat([data_s1,data_s2])

# Building dependent and independent variables
X = data.drop(['re_s','re_m','re_l','re_bf'],axis=1)
X.replace([np.inf, -np.inf], np.nan, inplace=True)
X.fillna(0, inplace=True)
for cl in X.columns:
    if cl == 'industry':
        continue
    X[cl] = function_rank(X,'industry',cl)
X = X.drop(['industry'],axis=1).astype(np.float64)
re = data[['re_l','industry']].copy()
re.replace([np.inf, -np.inf], np.nan, inplace=True)
re.fillna(0, inplace=True)
re['re_l'] = function_rank(re,'industry','re_l')
y = re['re_l'].astype(np.float64)

# Define ML model used
model_lasso = LassoCV(cv=10, normalize=True, max_iter=50000).fit(X, y)

# Finding the features that are relative to the return rate
coef = pd.Series(model_lasso.coef_, index = X.columns)
print("Lasso picked " + str(sum(coef != 0)) + " variables and eliminated the other " +  str(sum(coef == 0)) + " variables")
imp_coef = coef.replace(0,np.nan).dropna().sort_values()

# Plot 
matplotlib.rcParams['figure.figsize'] = (10.0, 10.0)
colors = sns.color_palette('colorblind')
imp_coef.plot(kind = "barh",color = colors)
plt.yticks(fontsize = 10)
plt.subplots_adjust(left=0.3, wspace=0.25, hspace=0.25,
                bottom=0.13, top=0.91)
colors = sns.color_palette('colorblind')
plt.title("Coefficients in the Lasso Model of 3-Month Return",fontsize=15)  
plt.savefig('seasonal_factors.png') 
plt.close()

print(imp_coef.index)