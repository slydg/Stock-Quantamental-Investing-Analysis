import pandas as pd 
import numpy as np 
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.externals import joblib

"""
Building the pricing model, which would find the relationship between
the financial features and the market performance
and testing with cross validation
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

# Dependent and independent variables
X = data.drop(['re_s','re_m','re_l'],axis=1)
X.replace([np.inf, -np.inf], np.nan, inplace=True)
X.fillna(0, inplace=True)
for cl in X.columns:
    if cl in ['industry','re_bf']:
        continue
    X[cl] = function_rank(X,'industry',cl)
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
for i in X.columns:
    if i not in features:
        X = X.drop([i],axis=1)
X = X.astype(np.float64)
y = data[['re_l','industry']].copy()
y.replace([np.inf, -np.inf], np.nan, inplace=True)
y.fillna(0, inplace=True)
y = function_rank(y,'industry','re_l').map(lambda x: 1 if x < 0.5 else 0) # Notice: to avoid classes imbalance

# Defining the model used (RandomForest)
model = RandomForestClassifier(n_estimators=2000,max_depth=5,max_leaf_nodes=54) 
train_X,test_X, train_y, test_y = train_test_split(X,
                                                   y,
                                                   test_size = 0.2,
                                                   random_state = 0)
model.fit(train_X, train_y) 

print('Training score: ')
print(model.score(train_X,train_y))

print('Testing score: ')
print(model.score(test_X,test_y))

# Saving model
joblib.dump(model,'./price_model.model')