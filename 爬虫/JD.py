import requests
import pandas as pd
from bs4 import BeautifulSoup
import time

url='https://search.jd.com/Search?'
mm={'keyword':'笔记本','wq':'笔记本'}
kk={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}

def get_onepage1(url):
    kk={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}
    try:
        response=requests.get(url,params=mm,headers=kk)
        response.raise_for_status
        response.encoding=response.apparent_encoding
        return response.text
    except:
        print('False')


def one_parser(detail, html):
    soup=BeautifulSoup(html,'lxml')
    for a,b,c,d,e in zip(soup.select('#J_goodsList > ul > li'),
                             soup.select('#J_goodsList > ul > li > div > div.p-name.p-name-type-2 > a > em'),
                             soup.select('#J_goodsList > ul > li > div > div.p-img > a'),
                             soup.select('#J_goodsList > ul > li > div > div.p-img > a > img'),
                             soup.select('#J_goodsList > ul > li > div > div.p-price > strong > i')):
        detail.append([eval(a['data-sku']),b.get_text(),'http:'+c['href'],'http:'+d['data-lazy-img'],e.string])
    return detail
        # /pd.DataFrame(detail, columns=['SKU', '名称', '链接', '图片', '价格'])

def main():
    detail=[]
    hh=[]
    for i in range(1,3):
        url2=url+'page={}&s={}'.format(i*2-1,(i-1)*50+1)
        print('爬取:%s'%url2)
        html=get_onepage1(url2)
        detail=one_parser(detail, html)
        items=[]
        for n in detail[i-1:i*30]:
            items.append(n[0])
        time.sleep(1)
        url3=url+'page={}&s={}'.format(i*2,(i-1)*50+26)+'show_items={}'.format(items)
        print('爬取:%s'%url3)
        html2=get_onepage1(url3)
        hh=one_parser(hh, html2)

    print(pd.DataFrame(detail+hh,columns=['SKU','名称','链接','图片','价格']))
    # print(pd.DataFrame(hh, columns=['SKU', '名称', '链接', '图片', '价格']))

if __name__ == '__main__':
    main()