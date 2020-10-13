import pandas as pd
data1=pd.read_csv(r'C:\Users\Jack\OneDrive\桌面\新建文件夹\宅基地筛选3.csv')
data2=pd.read_excel(r'C:\Users\Jack\OneDrive\桌面\新建文件夹\宅基地所有信息22.xls')
data2.columns=list(data2.iloc[0].values)
a=[x for x in data1['填表人姓名'] if x not in data2['填表人姓名']]
m=data2[~data2['填表人姓名'].isin(list(a))]
n=m[1::]
n.to_csv('异常人员名单.csv',encoding='utf-8-sig')
print(n.农户数.isin(['0']))