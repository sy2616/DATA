import pandas as pd
data2=pd.read_excel(r'C:\Users\Jack\OneDrive\桌面\1013.xlsx')

print(data2.describe())
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
ee.to_csv('筛选10133.csv',encoding='utf-8-sig')

