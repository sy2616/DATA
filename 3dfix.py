
import pandas as pd
data=pd.read_csv('3d.csv')
data.head()
data2=data[1::]
# data2
# data2['中奖号码']
data3=data2['中奖号码'].str.split('',expand=True)
# data3[[1,3,6]]
# data3[['1','3','6']]
pd.concat([data2,data3[[1,3,6]]],axis=1).to_csv('3dfix.csv',encoding='utf-8-sig')