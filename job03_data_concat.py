import pandas as pd
import glob
import datetime

data_path = glob.glob('./crawling_data/*')
print(data_path)

df = pd.DataFrame()
for path in data_path:
    df_temp = pd.read_csv(path, index_col=0)
    #만약 tiltes에 결측치(NaN)이 있을 경우
    #df_temp.dropna(inplace=True)
    df = pd.concat([df, df_temp])
print(df.head())
print(df['category'].value_counts())
df.info()
df.to_csv('./naver_news_titles...{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d')),index=False)
