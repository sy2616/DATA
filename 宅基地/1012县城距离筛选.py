import pandas as pd
data=pd.read_excel(r'C:\Users\Jack\OneDrive - mails.ucas.ac.cn\桌面\宅基地筛选1010.xlsx')
#省份数据统计
# print(data.groupby('省（区、市）').count())
list=['湖北省','云南省','四川省','广东省','广西壮族自治区','湖南省','西藏自治区','贵州省','陕西省','黑龙江省']
for i in list:
    a = data[data['省（区、市）'].isin([i])]
    print('{}大于1000的村庄：{}'.format(i,a[a['村庄面积']>=1000].count()))
    print('{}500到1000的村庄：{}'.format(i,a[a['村庄面积']<1000][a[a['村庄面积']<1000]['村庄面积']>=500].count()))
    print('{}200到500的村庄：{}'.format(i,a[a['村庄面积']<500][a[a['村庄面积']<500]['村庄面积']>=200].count()))
    print('{}小于200的村庄：{}'.format(i,a[a['村庄面积']<200].count()))