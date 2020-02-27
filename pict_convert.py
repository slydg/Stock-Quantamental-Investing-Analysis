import base64
f=open('./seasonal_factors.png','rb') 
ls_f=base64.b64encode(f.read()) 
f.close()
print(ls_f)