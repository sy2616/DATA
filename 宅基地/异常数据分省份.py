# coding=utf-8
import pandas as pd
data=pd.read_excel(r'C:\Users\Jack\OneDrive\桌面\异常人员名单1001（含正常范围）.xlsx')
print(data.head())
print(data.groupby('省（区、市）').count())
g=data.copy()
g.groupby('省（区、市）').count().to_excel('宅基地异常宅基地各省份数据异常筛选后各省份样本数.xls',encoding='utf-8-sig')
list=['湖北省','云南省','四川省','广东省','广西壮族自治区','湖南省','西藏自治区','贵州省','陕西省','黑龙江省']
for i in list:
    k = g['省（区、市）'].isin([i])
    print(g[k].describe())
    g[k].to_excel('%s异常村庄宅基地3.xls'%i, encoding='utf-8-sig')
    print('保存%s的数据成功'%i)
