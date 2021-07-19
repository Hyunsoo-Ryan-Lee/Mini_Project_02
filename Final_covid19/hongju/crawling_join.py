from selenium import webdriver 
from bs4 import BeautifulSoup 
import time
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import numpy as np
import requests


class Crawling():
    def crawl_covid():
        browser = webdriver.Chrome('c:/driver/chromedriver.exe')
        results = []
        try:
            url = "https://www.worldometers.info/coronavirus/#countries" 
            browser.get(url)
            time.sleep(2)
            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
            table_list = soup.select('#main_table_countries_today > tbody:nth-child(2) > tr')

            for i in range(0, len(table_list)):
                if table_list[i].select('a.mt_a'):
                    country  = table_list[i].select('a.mt_a')[0].text
                    tot_cases  = table_list[i].select('td.sorting_1')[0].text
                    new_cases  = table_list[i].select('tr > td:nth-child(4)')[0].text
                    tot_deaths = table_list[i].select('tr > td:nth-child(5)')[0].text
                    new_deaths = table_list[i].select('tr > td:nth-child(6)')[0].text
                    tot_recov = table_list[i].select('tr > td:nth-child(7)')[0].text
                    new_recov = table_list[i].select('tr > td:nth-child(8)')[0].text
                    tests = table_list[i].select('tr > td:nth-child(13)')[0].text
                    pop = table_list[i].select('tr > td:nth-child(15)')[0].text
                    data = [country, tot_cases, new_cases, tot_deaths, new_deaths, tot_recov, new_recov, tests, pop]
                    results.append(data)
                else:
                    continue


        except Exception as e:
            print("페이지 파싱 에러", e)
        finally:
            time.sleep(3)
            browser.quit()
            df = pd.DataFrame(results)
            df.columns = ["country", "tot_cases", "new_cases", "tot_deaths", "new_deaths", "tot_recov", "new_recov", "tests", "pop"]
            df.to_excel('./covid19.xlsx', index = False)


        try:
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
        except Exception as e:
            print("페이지 파싱 에러", e)
        finally:
            time.sleep(3)
            browser.quit()

        
        try:
            df = pd.read_excel('covid19.xlsx')
            df['tot_cases'] = df['tot_cases'].str.replace(',', '')
            df['new_cases'] = df['new_cases'].str.replace('+', '')
            df['new_cases'] = df['new_cases'].str.replace(',', '')
            df['tot_deaths'] = df['tot_deaths'].str.replace(',', '')
            df['new_deaths'] = df['new_deaths'].replace('+', '')
            df['new_deaths'] = df['new_deaths'].replace(',', '')
            df['new_deaths'] = df['new_deaths'].replace(' ', '')
            df['tot_recov'] = df['tot_recov'].str.replace(',', '')
            df['new_recov'] = df['new_recov'].str.replace('+', '')
            df['new_recov'] = df['new_recov'].str.replace(',', '')
            df['tests'] = df['tests'].str.replace(',', '')
            df['pop'] = df['pop'].str.replace(',', '')
            df = df.replace(np.nan, 0)
            df = df.replace(' ', 0)
            df[['tot_cases', 'new_cases', 'tot_deaths', 'new_deaths', 'tot_recov', 'new_recov', 'tests', 'pop']] = df[['tot_cases', 'new_cases', 'tot_deaths', 'new_deaths', 'tot_recov', 'new_recov', 'tests', 'pop']].astype('int')
        
            df.loc[0,"country"] = "United States of America"
            df.loc[4,"country"] = "Russian Federation"
            df.loc[6,"country"] = "United Kingdom"
            df.loc[12,"country"] = "Iran (Islamic Republic of)"
            df.loc[20,"country"] = "Czech Republic" 
            df.loc[40,"country"] = "United Arab Emirates"
            df.loc[47,"country"] = "Bolivia (Plurinational State of)"
            df.loc[66,"country"] = "Venezuela, Bolivarian Republic of"
            df.loc[67,"country"] = "Egypt, Arab Rep."
            df.loc[75,"country"] = "Republic of Moldova"
            df.loc[85,"country"] = "Republic of Korea"
            df.loc[88,"country"] = "Kyrgyz Republic" 
            df.loc[116,"country"] = "Democratic Republic of the Congo" 
            df.loc[126,"country"] = "Viet Nam"
            df.loc[128,"country"] = "Syrian Arab Republic"
            df.loc[137,"country"] = "French Polynesia"
            df.loc[151,"country"] = "Curacao"
            df.loc[153,"country"] = "Hong Kong SAR, China"
            df.loc[156,"country"] = "Aruba" 
            df.loc[157,"country"] = "South Sudan" 
            df.loc[163,"country"] = "Central African Republic" 
            df.loc[166,"country"] = "Gambia (Republic of The)"
            df.loc[167,"country"] = "Eritrea"
            df.loc[172,"country"] = "Channel Islands"
            df.loc[176,"country"] = "Gibraltar"
            df.loc[179,"country"] = "Guinea Bissau"
            df.loc[183,"country"] = "Sint Maarten (Dutch part)"
            df.loc[185,"country"] = "Bermuda"
            df.loc[186,"country"] = "Turks and Caicos Islands"
            df.loc[190,"country"] = "Saint Vincent and the Grenadines"
            df.loc[192,"country"] = "Isle of Man"
            df.loc[193,"country"] = "Netherlands" 
            df.loc[197,"country"] = "British Virgin Islands"
            df.loc[198,"country"] = "Cayman Islands"
            df.loc[200,"country"] = "United Republic of Tanzania"
            df.loc[202,"country"] = "Brunei Darussalam"
            df.loc[205,"country"] = "New Caledonia"
            df.loc[208,"country"] = "Macao SAR, China"
            df.loc[209,"country"] = "Greenland"
            df.loc[219,"country"] = "Micronesia (Federated States of)"
            covid_gdp_1 = pd.merge(df, gdp_pop, how='left', on='country')
            covid_gdp_1 = covid_gdp_1.dropna(axis=0)
            covid_gdp_1 = covid_gdp_1.astype({'2019':'int64'})
            
        except Exception as e:
            print("페이지 파싱 에러", e)
        finally:
            covid_gdp_1.columns = ["country", "tot_cases", "new_cases", "tot_deaths", "new_deaths", "tot_recov", "new_recov", "tests", "pop", "2019"]
            covid_gdp_1.to_excel('./covid_gdp.xlsx', index = False)
        



    def visual1():
        path = 'c:/Windows/Fonts/malgun.ttf'
        font_name = font_manager.FontProperties(fname = path).get_name()
        rc('font', family = font_name)

        df = pd.read_excel('covid19.xlsx')


if __name__ == '__main__':
    Crawling.crawl_covid()
    # Crawling.crawl_gdp()
    # pass