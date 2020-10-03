# coding=utf-8
import pandas as pd
data=pd.read_excel(r'C:\Users\Jack\Downloads\宅基地所有信息22.xls')
print(data.head())
data2=pd.DataFrame(data=data[1::])
data2.columns=list(data.iloc[0].values)
print(data2.describe())
print(data2.groupby('省（区、市）').count())
data2.groupby('省（区、市）').count().to_csv('各省份统计.csv',encoding='utf-8-sig')
#去零
data3=data2[data2.农户数!=0]
#村庄面积=村庄面积/农户数
d=data3.apply(lambda x:float(x['村庄面积'])/float(x['农户数']),axis=1)
data2['村庄面积筛选']=d
dd=data2[data2.村庄面积筛选>0.1][data2[data2.村庄面积筛选>0.1].村庄面积筛选<3]
#村庄人口数
mm=dd.apply(lambda x:float(x['村庄人口数'])/float(x['农户数']),axis=1)
dd['村庄人口数筛选']=mm
cc=dd[dd.村庄人口数筛选>1][dd[dd.村庄人口数筛选>1].村庄人口数筛选<7]
#宅基地宗数
nn=cc.apply(lambda x:float(x['宅基地宗数'])/float(x['农户数']),axis=1)
cc['宅基地宗数筛选']=nn
bb=cc[cc.宅基地宗数筛选>0.5][cc[cc.宅基地宗数筛选>0.5].宅基地宗数筛选<5]
#宅基地总面积筛选
n1=bb.apply(lambda x:float(x['农户数']*75/667),axis=1)
n2=bb.apply(lambda x:float(x['农户数']*1000/667),axis=1)
bb['宅基地总面下限']=n1
bb['宅基地总面上限']=n2
a=bb.apply(lambda x:float(x.宅基地总面上限)>float(x.宅基地面积)>float(x.宅基地总面下限),axis=1)
ee=bb[a].copy()
ee.to_csv('筛选3.csv',encoding='utf-8-sig')
