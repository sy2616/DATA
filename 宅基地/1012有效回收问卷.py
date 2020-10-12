import pandas as pd
data=pd.read_excel(r'C:\Users\Jack\OneDrive\桌面\宅基地筛选1010.xlsx')
# print(data.columns)
# print(data['黑龙江省'])
# print(data[data['省（区、市）'].isin(['黑龙江'])].groupby('describe())
list=['湖北省','云南省','四川省','广东省','广西壮族自治区','湖南省','西藏自治区','贵州省','陕西省','黑龙江省']
for i in list:
    dat22 = data[data['省（区、市）'].isin([i])].copy()
    print('{}的有效问卷统计：{}'.format(i,dat22.groupby('县（市、区）').describe()))