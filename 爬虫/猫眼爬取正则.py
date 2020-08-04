import requests
import re
import pandas as pd
from multiprocessing import Pool
import json
import pymongo

myclient=pymongo.MongoClient('mongodb://127.0.0.1:27017/')
mydb=myclient['maoyan']

def get_one_page(url):
    try:
        headers={'user-agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'}
        response=requests.get(url,headers=headers)
        response.raise_for_status()
        print(response.status_code)
        response.encoding=response.apparent_encoding
        return response.text
    except:
        return None

def htmlparse(html):
    pattern=re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?src="(.*?)".*?name"><a'
                         + '.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         + '.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)

    items=re.findall(pattern,str(html))
    for item in items:
        yield {
            'rank':item[0],
            'image':'https'+item[1],
            'name':item[2].strip(),
            'actor':item[3].strip(),
            'time':item[4],
            'score':item[5]+item[6]
        }

def save_mongodb(content):
    if mydb['maoyan'].insert(content):
        print('save to mongodb')
        return True
    return False

def write(content):
    with open('maoyan.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')
        f.close()

def main(offset):
    url='https://maoyan.com/board/4?offset='+str(offset)
    html=get_one_page(url)
    for item in htmlparse(html):
        print(item)
        write(item)
        save_mongodb(item)
        print('done!')

if __name__ == '__main__':
    # for i in range(10):
    #     main(i*10)
    pool=Pool()
    pool.map(main,[i*10 for i in range(10)])




