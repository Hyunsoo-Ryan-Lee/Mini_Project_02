import requests
from selenium import webdriver 
from bs4 import BeautifulSoup 
import time
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import numpy as np

url='https://www.un.org/en/about-us/member-states'
res = requests.get(url)
html = res.text
soup = BeautifulSoup(html, 'html.parser')

country_names = soup.select('.mb-0')
country_list = []
for i in country_names:
    country_list.append(i.text)
    
col = ['country']
country_df = pd.DataFrame(country_list, columns=col)

# 영국의 경우 UN에 북아일랜드와 함께 가입되어있는데 gdp 자료는 영국 기준이라서 이름 변경
country_df.iloc[182, 0] = 'United Kingdom'

# 국가별 2018, 2019 gdp 정보가 있는 엑셀 파일 read
gdp_cap = pd.read_excel('gdp_per_capita.xls')
gdp_df = pd.merge(left=country_df,
                 right=gdp_cap,
                 how='left',
                 left_on='country',
                 right_on='Country Name')

# df_nulls = gdp_df.isnull().sum()
# un 가입국이지만 gdp 정보가 없는 국가 3개
# 2018년, 2019년 모두 gdp 정보가 없는 국가 drop 필요
# thresh: 해당 row에서 NaN이 아닌 값이 최소 3개 이상 나와야 한다는 설정
gdp_pop = gdp_df.dropna(axis = 0, thresh = 3)
del gdp_pop['Country Name']
gdp_pop = gdp_pop.reset_index()
del gdp_pop['index']

# gdp_pop[gdp_pop['2019'].isnull()]
# 2019 nan값을 2018 정보로 대체
gdp_pop.iloc[94, 2] = gdp_pop.iloc[94, 1]
gdp_pop.iloc[183, 2] = gdp_pop.iloc[183, 1]
del gdp_pop['2018']

# 데이터 타입 변환
gdp_pop = gdp_pop.astype({'2019':'int64'})
