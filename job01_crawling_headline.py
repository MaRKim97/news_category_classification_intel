from bs4 import BeautifulSoup #pip install bs4로 설치
import requests
import re
import pandas as pd
import datetime

category = ['Politics', 'Economy', 'Social', 'Culture', 'World', 'IT']

# url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100'
# # resp = requests.get(url)
# resp = requests.get(url, headers=headers)
# #resp: Response 객체
# # 만약 naver에서 request 요청을 막아서 오류가 생긴다면 headers에 있는 문구를 붙여서 요청하면 된다
#
# print(resp)
# print(type(resp))
#
# soup = BeautifulSoup(resp.text, 'html.parser')
# # print(soup)
# title_tags = soup.select('.sh_text_headline') #.: 클래스를 의미
# print(title_tags)
# print(len(title_tags))
# print(type(title_tags[0]))
# titles = []
# for title_tag in title_tags:
#     titles.append(re.compile('[^가-힣|a-z|A-Z]').sub(' ', title_tag.text))
#     #re: 정규 표현식, ^:정해준 값들 빼고 나머지, sub(' ': 빈 칸으로 채우라고 지정
# print(titles)

df_title = pd.DataFrame()
re_title = re.compile('[^가-힣|a-z|A-Z]')
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

for i in range(6):
    url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}'.format(i)
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    title_tags = soup.select('.sh_text_headline')
    titles = []
    for title_tag in title_tags:
        titles.append(re_title.sub(' ', title_tag.text))
    df_section_titles = pd.DataFrame(titles, columns=['titles'])
    df_section_titles['category'] = category[i]
    df_title = pd.concat([df_title, df_section_titles], axis='rows', ignore_index=True)
print(df_title.head())
df_title.info()
print(df_title['category'].value_counts())
df_title.to_csv('./crawling_data/naver_headline_news_{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d')), index=False)
#datetime: 단위가 ns로 되어있음->strftime: 연월일을 문자열로 바꿔줌