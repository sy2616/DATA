import requests
import re
import time
import pymysql
import pymysql
from requests.exceptions import RequestException
import bs4
from bs4 import BeautifulSoup
import pandas as pd
from lxml import etree
start_time=time.time()
# client=pymongo.MongoClient('mongodb://127.0.0.1:27017/')
# my_db=client['gupiaodaima']
headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.44'}
def get_one_page(url):
    try:
        response=requests.get(url,headers=headers)
        response.raise_for_status()
        response.encoding=response.apparent_encoding
        return response.text
    except RequestException:
        print('response failed')

def parse_one(html):
    soup=BeautifulSoup(html,'lxml')
    content = soup.select('#myTable04')[0]  # [0]将返回的list改为bs4类型
    tbl = pd.read_html(content.prettify(), header=0)[0]
    tbl.rename(columns={'序号': 'serial_number', '股票代码': 'stock_code', '股票简称': 'stock_abbre', '公司名称': 'company_name',
                        '省份': 'province', '城市': 'city', '主营业务收入(201712)': 'main_bussiness_income',
                        '净利润(201712)': 'net_profit', '员工人数': 'employees', '上市日期': 'listing_date', '招股书': 'zhaogushu',
                        '公司财报': 'financial_report', '行业分类': 'industry_classification', '产品类型': 'industry_type',
                        '主营业务': 'main_business'}, inplace=True)
    return tbl
def Mysql():
    connect=pymysql.connect(
        host='localhost',
        user='root',
        password='Jacl1234',
        port=3306,
        charset='utf8',
        db='gupiao'
    )
    cursor=connect.cursor()
    sql='CREAT TABLE IF NOT EXTSIS listed company (serial_number INT(20) NOT NULL,stock_code INT(20) ,stock_abbre VARCHAR(20) ,company_name VARCHAR(20) ,province VARCHAR(20) ,city VARCHAR(20) ,main_bussiness_income VARCHAR(20) ,net_profit VARCHAR(20) ,employees INT(20) ,listing_date DATETIME(0) ,zhaogushu VARCHAR(20) ,financial_report VARCHAR(20) , industry_classification VARCHAR(20) ,industry_type VARCHAR(100) ,main_business VARCHAR(200) ,PRIMARY KEY (serial_number))'
    cursor.execute(sql)
    connect.close()
def write_to_sql(tbl,db='gupiao'):
    engine=creat_engine('mysql+pymysql://root:Jack1234@localhost:3306/{0}?charset=utf8'.format(db))
    try:
        tbl.to_sql('listed_company2',connect=engine,if_exists='append',index=False)
    except Exception as e:
        print(e)
def main(page):
    Mysql()
    for i in range(1,page):
        url='https://s.askci.com/stock/a/0-0?reportTime=2020-03-31&pageNum=%d+'%i
        html=get_one_page(url)
        tbl=parse_one(html)
        write_to_sql(tbl)
if __name__ == '__main__':
    main(10)
