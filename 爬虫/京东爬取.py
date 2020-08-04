from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
browser=webdriver.Chrome()
wait=WebDriverWait(browser,15)

def search(keyword):
    try:
        browser.get('https://www.taobao.com/')
        input=wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'#q'))
        )
        submit=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#J_TSearchForm > div.search-button > button')))
        input.send_keys(keyword)
        submit.click()
        total=wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'#J_bottomPage > span.p-skip > em:nth-child(1) > b')))
        return total.text
    except TimeoutException:
        return search(keyword)

def next_page(page_number):
    try:
        input=wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#J_bottomPage > span.p-skip > input'))
        )
        submit=wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_bottomPage > span.p-skip > a')))
        input.clear()
        input.send_keys(page_number)
        submit.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#J_bottomPage > span.p-num > a.curr'),str(page_number)))
    except TimeoutException:
        next_page(page_number)

def main():
    total=int(search('手机'))
    print(total)
    for i in range(2,total+1):
        next_page(i)
        time.sleep(5)

if __name__ == '__main__':
    main()
