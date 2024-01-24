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
pages = [105, 105, 105, 81, 105, 81] # 페이지 개수가 상이하나 적당한 값에 맞춰서 페이지를 세팅해 줌
#크롬을 세팅하고 여는 과정
options = ChromeOptions()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
options.add_argument('user_agent=' + user_agent)
options.add_argument('lang=ko_KR')

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

df_title = pd.DataFrame()
for l in range(2): #몇개의 카테고리를 크롤링할 지 결정
    section_url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}'.format(l)
    titles = []
    for k in range(1, pages[l]): #해당하는 페이지를 세팅하는 과정
        url = section_url + '#&date=%2000:00:00&page={}'.format(k)
        try:
            driver.get(url)
            time.sleep(0.5)
        except: #인터넷 연결이 너무 느리거나 하는 경우 오류 메시지만 띄운 뒤 이후 과정을 수행하도록 세팅
            print('driver.get', l, k)
        for i in range(1, 5):
            for j in range(1, 6):
                try:
                    title = driver.find_element('xpath', '//*[@id="section_body"]/ul[{}]/li[{}]/dl/dt[2]/a'.format(i, j)).text
                    #네이버의 html문서에서 확인한 각 페이지 별 뉴스 타이틀들이 가지는 xpath를 값으로 줘 크롤링이 되도록 세팅
                    title = re.compile('[^가-힣]').sub(' ', title)
                    titles.append(title)
                except:
                    print('find element', l, k, i, j)
                    #xpath 값이 달라 크롤링이 안될 경우 오류 예외를 줘 크롤링이 멈추지 않게 함
        if k % 5 == 0:
            print('save ing...', l, k) #한번에 모든 크롤링 결과를 저장하는 것이 아닌 5페이지 마다 나눠서 저장하도록
            df_section_titles = pd.DataFrame(titles, columns=['titles'])
            df_section_titles['category'] = category[l]
            df_section_titles.to_csv('./crawling_data/data_{}_{}.csv'.format(l, k), index=False)
            # df_title = pd.concat([df_title, df_section_titles], axis='rows', ignore_index=True)
driver.close()