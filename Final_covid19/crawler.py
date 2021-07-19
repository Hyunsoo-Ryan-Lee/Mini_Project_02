from selenium import webdriver 
from bs4 import BeautifulSoup 
import time
import pandas as pd
import numpy as np
import requests
import pyautogui
import os


class Crawling():
    def crawl_covid():
        browser = webdriver.Chrome("c:/driver/chromedriver.exe")
        results = []
        try:
            url = "https://www.worldometers.info/coronavirus/#countries" 
            browser.get(url)
            time.sleep(2)
            html = browser.page_source
            soup = BeautifulSoup(html, "html.parser")
            table_list = soup.select("#main_table_countries_today > tbody:nth-child(2) > tr")
            
            for i in range(0, len(table_list)):
                if table_list[i].select("a.mt_a"):
                    country  = table_list[i].select("a.mt_a")[0].text
                    tot_cases  = table_list[i].select("td.sorting_1")[0].text
                    new_cases  = table_list[i].select("tr > td:nth-child(4)")[0].text
                    tot_deaths = table_list[i].select("tr > td:nth-child(5)")[0].text
                    new_deaths = table_list[i].select("tr > td:nth-child(6)")[0].text
                    tot_recov = table_list[i].select("tr > td:nth-child(7)")[0].text
                    new_recov = table_list[i].select("tr > td:nth-child(8)")[0].text
                    tests = table_list[i].select("tr > td:nth-child(13)")[0].text
                    pop = table_list[i].select("tr > td:nth-child(15)")[0].text
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
            df.set_index("country", inplace=True)
            df.sort_index(ascending=True, inplace=True)
            df.reset_index(inplace=True)
            df.to_excel("./covid19.xlsx", index = False)


        try:
            url="https://www.un.org/en/about-us/member-states"
            res = requests.get(url)
            html = res.text
            soup = BeautifulSoup(html, "html.parser")

            country_names = soup.select(".mb-0")
            country_list = []
            for i in country_names:
                country_list.append(i.text)
                
            col = ["country"]
            country_df = pd.DataFrame(country_list, columns=col)

            # 영국의 경우 UN에 북아일랜드와 함께 가입되어있는데 gdp 자료는 영국 기준이라서 이름 변경
            country_df.iloc[182, 0] = "United Kingdom"

            # 국가별 2018, 2019 gdp 정보가 있는 엑셀 파일 read
            gdp_cap = pd.read_excel("gdp_per_capita.xls")
            gdp_df = pd.merge(left=country_df,
                            right=gdp_cap,
                            how="left",
                            left_on="country",
                            right_on="Country Name")

            # df_nulls = gdp_df.isnull().sum()
            # un 가입국이지만 gdp 정보가 없는 국가 3개
            # 2018년, 2019년 모두 gdp 정보가 없는 국가 drop 필요
            # thresh: 해당 row에서 NaN이 아닌 값이 최소 3개 이상 나와야 한다는 설정
            gdp_pop = gdp_df.dropna(axis = 0, thresh = 3)
            del gdp_pop["Country Name"]
            gdp_pop = gdp_pop.reset_index()
            del gdp_pop["index"]

            # gdp_pop[gdp_pop["2019"].isnull()]
            # 2019 nan값을 2018 정보로 대체
            gdp_pop.iloc[94, 2] = gdp_pop.iloc[94, 1]
            gdp_pop.iloc[183, 2] = gdp_pop.iloc[183, 1]
            del gdp_pop["2018"]

            # 데이터 타입 변환
            gdp_pop = gdp_pop.astype({"2019":"int64"})

        except Exception as e:
            print("페이지 파싱 에러", e)
        finally:
            time.sleep(3)
            browser.quit()
        
        df = pd.read_excel("covid19.xlsx")

        df["tot_cases"] = df["tot_cases"].str.replace(",", "")
        df["new_cases"] = df["new_cases"].str.replace("+", "")
        df["new_cases"] = df["new_cases"].str.replace(",", "")
        df["tot_deaths"] = df["tot_deaths"].str.replace(",", "")
        df["new_deaths"] = df["new_deaths"].str.replace("+", "")
        df["new_deaths"] = df["new_deaths"].str.replace(",", "")
        df["new_deaths"] = df["new_deaths"].str.replace(" ", "")
        df["tot_recov"] = df["tot_recov"].str.replace(",", "")
        df["new_recov"] = df["new_recov"].str.replace("+", "")
        df["new_recov"] = df["new_recov"].str.replace(",", "")
        df["tests"] = df["tests"].str.replace(",", "")
        df["pop"] = df["pop"].str.replace(",", "")
        df = df.replace(np.nan, 0)
        df = df.replace(" ", 0)
        df[['tot_cases', 'new_cases', 'tot_deaths', 'new_deaths', 'tot_recov', 'new_recov', 'tests', 'pop']] = df[['tot_cases', 'new_cases', 'tot_deaths', 'new_deaths', 'tot_recov', 'new_recov', 'tests', 'pop']].astype('int64')
    
        # 21개 데이터의 변경값 찾음
        df.loc[206,"country"] = "United States of America" #usa
        df.loc[160,"country"] = "Russian Federation" #Russia
        df.loc[205,"country"] = "United Kingdom" #UK
        df.loc[96,"country"] = "Iran (Islamic Republic of)" #Iran
        df.loc[51,"country"] = "Czech Republic" #Czechia
        df.loc[204,"country"] = "United Arab Emirates" #UAE
        df.loc[23,"country"] = "Bolivia (Plurinational State of)" #Bolivia
        df.loc[130,"country"] = "Republic of Moldova" #Moldova
        df.loc[163,"country"] = "Republic of Korea" #S. Korea
        df.loc[99,"country"] = "Côte D'Ivoire" #Ivory Coast 찾았다....
        df.loc[52,"country"] = "Democratic Republic of the Congo" #DRC
        df.loc[214,"country"] = "Viet Nam" # Vietnam
        df.loc[32,"country"] = "Central African Republic" # CAR
        df.loc[73,"country"] = "Gambia (Republic of The)" # Gambia
        df.loc[84,"country"] = "Guinea Bissau" # Guinea-Bissau
        df.loc[107,"country"] = "Lao People’s Democratic Republic" #Laos 찾음
        df.loc[188,"country"] = "Saint Vincent and the Grenadines" # St. Vincent Grenadines
        df.loc[196,"country"] = "United Republic of Tanzania" # Tanzania
        df.loc[28,"country"] = "Brunei Darussalam" # Brunei
        df.loc[79,"country"] = "Greenland" # Greenland
        df.loc[129,"country"] = "Micronesia (Federated States of)" #Micronesia

        covid_gdp_1 = pd.merge(df, gdp_pop, how="left", on="country")
        covid_gdp_1 = covid_gdp_1.dropna(axis=0)
        covid_gdp_1 = covid_gdp_1.astype({"2019":"int64"})
        covid_gdp_1["tot_cases_1m"] = covid_gdp_1["tot_cases"]//(covid_gdp_1["pop"]//1000000)
        covid_gdp_1["tot_deaths_1m"] = covid_gdp_1["tot_deaths"]//(covid_gdp_1["pop"]//1000000)
        covid_gdp_1["tot_recov_1m"] = covid_gdp_1["tot_recov"]//(covid_gdp_1["pop"]//1000000)
        covid_gdp_1["tot_cases_1m"] = covid_gdp_1["tot_cases_1m"].replace(np.inf,0)
        covid_gdp_1["tot_deaths_1m"] = covid_gdp_1["tot_deaths_1m"].replace(np.inf,0).fillna(0)
        covid_gdp_1["tot_recov_1m"] = covid_gdp_1["tot_recov_1m"].replace(np.inf,0)
        covid_gdp_1 = covid_gdp_1.astype({'tot_cases_1m':'int64'})
        covid_gdp_1 = covid_gdp_1.astype({"tot_deaths_1m":"int64"})
        covid_gdp_1 = covid_gdp_1.astype({"tot_recov_1m":"int64"})
        col = ["country", "tot_cases", "new_cases", "tot_deaths", "new_deaths", "tot_recov", "new_recov", "tests", "pop", "2019_gdp", "tot_cases_1m", "tot_deaths_1m", "tot_recov_1m"]
        covid_gdp_1.columns = col
        covid_gdp_1.to_csv("covid_gdp.csv", index = False)

    def world_vaccine():
        # 전세계 백신 접종 현황 파일(vaccinations.csv) 가져오기
        vac_url = "https://github.com/owid/covid-19-data"
        driver = webdriver.Chrome("C:/driver/chromedriver")
        driver.get(vac_url)
        time.sleep(1)  
        driver.implicitly_wait(1) 
        driver.find_element_by_xpath('//*[@id="readme"]/div[3]/article/ul/li[2]/a').click()
        time.sleep(1)  
        driver.find_element_by_xpath('//*[@id="readme"]/article/p[3]/a[1]').click()
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="raw-url"]').click()
        time.sleep(1)
        pyautogui.hotkey('ctrl','s')
        time.sleep(1)  
        pyautogui.press('enter')
        time.sleep(1)  
        pyautogui.press('enter')
        time.sleep(1)
        driver.close()

        # vaccinations.csv 파일 읽고 전처리
        world_vac = pd.read_csv("C:/Users/Playdata/Downloads/vaccinations.csv")
        world_vac = world_vac.fillna(0)
        g1 = world_vac.groupby(world_vac['location']).sum().reset_index()
        g1 = g1.drop(['total_vaccinations_per_hundred','people_vaccinated_per_hundred','people_fully_vaccinated_per_hundred','daily_vaccinations_per_million'],axis=1)
        del_nat = ['Africa', 'Anguilla', 'Aruba', 'Asia', 'Bermuda', 'British Virgin Islands',
        'Cayman Islands', 'Cook Islands', 'Curacao', 'England', 'Europe', 'European Union', 
        'Faeroe Islands', 'Falkland Islands', 'French Polynesia', 'Gibraltar', 'Greenland',
        'Guernsey', 'High income', 'Hong Kong', 'Isle of Man', 'Jersey', 'Kosovo', 'Low income',
        'Lower middle income', 'Macao', 'Montserrat', 'New Caledonia', 'Niue', 'North America',
        'Northern Cyprus', 'Northern Ireland', 'Oceania', 'Palestine', 'Pitcairn', 'Saint Helena',
        'Scotland', 'Sint Maarten (Dutch part)', 'South America', 'Taiwan', 'Turks and Caicos Islands',
        'Upper middle income', 'Wales', 'Wallis and Futuna', 'World','Bonaire Sint Eustatius and Saba', 
        'Egypt', 'Kyrgyzstan', 'Nauru', 'Syria', 'Tonga', 'Turkmenistan','Tuvalu', 'Venezuela']

        n_index = []
        for i in range(len(g1)):
            for j in range(len(del_nat)):
                if g1['location'][i] == del_nat[j]:
                    n_index.append(i)
        g1.drop(index=n_index, inplace=True)

        vac_data = g1.reset_index()
        del vac_data['index']

        vac_data.rename(columns={'location':'country'}, inplace=True)
        vac_data.loc[20,"country"] = 'Bolivia (Plurinational State of)'
        vac_data.loc[24,"country"] = 'Burundi'
        vac_data.loc[30,"country"] = 'Cabo Verde'
        vac_data.loc[39,"country"] = "Côte D'Ivoire"
        vac_data.loc[43,"country"] = 'Czech Republic'
        vac_data.loc[44,"country"] = 'Democratic Republic of the Congo'
        vac_data.loc[59,"country"] = 'Gambia (Republic of The)'
        vac_data.loc[67,"country"] = 'Guinea Bissau'
        vac_data.loc[74,"country"] = 'Iran (Islamic Republic of)'
        vac_data.loc[85,"country"] = 'Lao People’s Democratic Republic'
        vac_data.loc[103,"country"] = 'Republic of Moldova'
        vac_data.loc[130,"country"] = 'Russian Federation'
        vac_data.loc[149,"country"] = 'Republic of Korea'
        vac_data.loc[150,"country"] = 'Sudan'
        vac_data.loc[159,"country"] = 'Timor-Leste'
        vac_data.loc[168,"country"] = 'United States of America'
        vac_data.loc[172,"country"] = 'Viet Nam'

        # 백신 관련(전처리 finish) data csv 파일로 저장
        vac_data.to_csv("total_vaccine.csv", index = False)

        # total_vaccine.csv 파일 읽어 코로나-GDP merge된 파일과 merge
        covid_gdp = pd.read_csv('covid_gdp.csv')
        merge_data = pd.merge(covid_gdp, vac_data, how="left", on="country")
        merge_data = merge_data.fillna(0)
        merge_data.to_csv("merge_vaccine.csv", index = False)

    def kor_vaccine():
        # 중앙방역대책본부 사이트에서 매일 업데이트되는 백신별 일일 접종 현황 파일 다운로드
        main_url = "https://ncv.kdca.go.kr/board.es?mid=a11710000000&bid=0037#content"
        driver = webdriver.Chrome("C:/driver/chromedriver")
        driver.get(main_url)
        time.sleep(2)  
        driver.implicitly_wait(1) 
        driver.find_element_by_xpath('//*[@id="listView"]/ul/li[2]/a').click()
        time.sleep(2)  
        driver.implicitly_wait(2) 
        driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div[3]/div[2]/ul/li/a').click()
        time.sleep(4)
        driver.close()

        # 코로나 바이러스 백신별 접종현황 파일 읽어오기
        file_name = os.listdir("C:/Users/Playdata/Downloads")

        for file in file_name:
            if file.startswith('코로나바이러스'):
                file_name = file
        datas = pd.read_excel(r'C:/Users/Playdata/Downloads/{}'.format(file_name))
        
        # 컬럼명 설정 및 전처리
        d_columns = ['일자','ALL(1)','ALL(FIN)','아제(1)','아제(FIN)','화이자(1)','화이자(FIN)','얀센','모더나(1)','모더나(FIN)']
        datas = datas.drop(index=[0,1,2,3,4,5], axis=0)
        datas.columns = d_columns
        datas = datas.reset_index()
        del datas['index']

        # kor_vaccine.csv 파일로 저장
        datas.to_csv("kor_vaccine.csv", index = False)


if __name__ == "__main__":
#     Crawling.crawl_covid()
    Crawling.world_vaccine()