import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
from urllib.parse import urlencode
from requests.exceptions import RequestException
import json

def get_one_page(url):
    # # data={
    #     'aid':'24',
    #     'app_name':'web_search',
    #     'offset':offset,
    #     'format':'json',
    #     'keyword':keyword,
    #     'autoload':'true',
    #     'count':'20',
    #     'cur_tab':1
    # }
    headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.40'}
    # url='https://www.toutiao.com/api/search/content/?aid=24&app_name=web_search&offset=0&format=json&keyword=%E6%B1%BD%E8%BD%A6&autoload=true&count=20&en_qc=1&cur_tab=1&from=search_tab&pd=synthesis&timestamp=1595382031497&_signature=yKCC0AAgEBAjdvdrFDy-RMihw8AAJfAnf2GLIThu6PnGbZJ7KODfAGdnChdQIy3YUPnpZXqdtDQ45t7ixBqZ3OYQYkSgGshVUzT5A1zMyH3cMPpZS4AI0wJTKxVkUDZ7rV'
    try:
        response=requests.get(url,headers=headers)
        response.raise_for_status()
        response.encoding=response.apparent_encoding
        return response.text
    except RequestException:
        print('请求错误')
        return None

def main():
    url='https://www.toutiao.com/api/search/content/?aid=24&app_name=web_search&offset=0&format=json&keyword=%E6%B1%BD%E8%BD%A6&autoload=true&count=20&en_qc=1&cur_tab=1&from=search_tab&pd=synthesis&timestamp=1595382031497&_signature=yKCC0AAgEBAjdvdrFDy-RMihw8AAJfAnf2GLIThu6PnGbZJ7KODfAGdnChdQIy3YUPnpZXqdtDQ45t7ixBqZ3OYQYkSgGshVUzT5A1zMyH3cMPpZS4AI0wJTKxVkUDZ7rV.'
    html=get_one_page(url)
    print(json.loads(html))

if __name__ == '__main__':
    main()
