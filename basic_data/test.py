import pandas as pd 

data = pd.read_csv('season12_final.csv', encoding='utf_8_sig')

print(data['industry'])