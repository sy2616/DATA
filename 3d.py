import pandas as pd
data=pd.read_html('http://kaijiang.zhcw.com/zhcw/html/3d/list.html')
a=data[0][['开奖日期','期号','中奖号码']][0:-1]
for i in range(2,285):
    url='http://kaijiang.zhcw.com/zhcw/html/3d/list_{}.html'.format(i)
    print(url)
    data=pd.read_html(url)
    b=data[0][['开奖日期','期号','中奖号码']][0:-1]
    #print(b)
    a=a.append(b,ignore_index=True)
    print('已抓取%d次'%i)
a.to_csv('3d.csv',encoding='utf-8-sig')