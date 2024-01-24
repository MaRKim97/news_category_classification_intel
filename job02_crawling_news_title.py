from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time
import datetime

category = ['Politics', 'Economy', 'Social', 'Culture', 'World', 'IT']
pages = [105, 105, 105, 81, 105, 81]

options = ChromeOptions()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
options.add_argument('user_agent=' + user_agent)
options.add_argument('lang=ko_KR')

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

df_title = pd.DataFrame()
for l in range(6):
    section_url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}'.format(l)
    titles = []
    for k in range(1, pages[l]):
        url = section_url + '#&date=%2000:00:00&page={}'.format(k)
        try:
            driver.get(url)
            time.sleep(0.5)
        except:
            print('driver.get', l, k)
        for i in range(1, 5):
            for j in range(1, 6):
                try:
                    title = driver.find_element('xpath', '//*[@id="section_body"]/ul[{}]/li[{}]/dl/dt[2]/a'.format(i, j)).text
                    title = re.compile('[^가-힣]').sub(' ', title)
                    titles.append(title)
                except:
                    print('find element', l, k, i, j)
        if k % 5 == 0:
            print(l, k)
            df_section_titles = pd.DataFrame(titles, columns=['titles'])
            df_section_titles['category'] = category[l]
            df_section_titles.to_csv('./crawling_data/data_{}_{}.csv'.format(l, k))
            # df_title = pd.concat([df_title, df_section_titles], axis='rows', ignore_index=True)
driver.close()