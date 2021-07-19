from flask import Flask, render_template, request, jsonify
from crawler import Crawling
import platform
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
from wordcloud import WordCloud
from PIL import Image
import stylecloud
from visual import Visual
import time
import os
import pyautogui
from selenium import webdriver 
from bs4 import BeautifulSoup 

app = Flask(import_name=__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/', methods=['get'])
def index():
    return render_template('index.html')

@app.route('/covidchart', methods=['get'])
def get_covid():
    return ""

@app.route('/confirm', methods=['post', 'get'])
def confirm():
    confirm_visual = {}
    conf = pd.read_csv('merge_vaccine.csv')
    for i in range(len(conf)):
        confirm_visual[conf.iloc[i,0]] = conf.iloc[i,1]
    stylecloud.gen_stylecloud(text=confirm_visual,icon_name="fas fa-certificate",
                        palette="colorbrewer.diverging.Spectral_11",background_color='black',
                        gradient="horizontal",output_name="./static/img/confirm.jpg")
    return "confirm.jpg"

@app.route('/death', methods=['post', 'get'])
def death():
    confirm_visual = {}
    conf = pd.read_csv('merge_vaccine.csv')
    for i in range(len(conf)):
        confirm_visual[conf.iloc[i,0]] = conf.iloc[i,3]
    stylecloud.gen_stylecloud(text=confirm_visual,icon_name="fas fa-skull-crossbones",
                        palette="colorbrewer.diverging.Spectral_11",background_color='black',
                        gradient="horizontal",output_name="./static/img/death.jpg")
    return "death.jpg"

@app.route('/vaccine', methods=['post', 'get'])
def vaccine():
    confirm_visual = {}
    conf = pd.read_csv('merge_vaccine.csv')
    for i in range(len(conf)):
        confirm_visual[conf.iloc[i,0]] = conf.iloc[i,13]
    stylecloud.gen_stylecloud(text=confirm_visual,icon_name="fas fa-thermometer",
                        palette="colorbrewer.diverging.Spectral_11",background_color='black',
                        gradient="horizontal",output_name="./static/img/vaccine.jpg")
    return "vaccine.jpg"

@app.route('/gdp', methods=['post', 'get'])
def gdp():
    confirm_visual = {}
    conf = pd.read_csv('merge_vaccine.csv')
    for i in range(len(conf)):
        confirm_visual[conf.iloc[i,0]] = conf.iloc[i,9]
    stylecloud.gen_stylecloud(text=confirm_visual,icon_name="fas fa-money-check-alt",
                        palette="colorbrewer.diverging.Spectral_11",background_color='black',
                        gradient="horizontal",output_name="./static/img/gdp.jpg")
    return "gdp.jpg"

@app.route('/population', methods=['post', 'get'])
def population():
    confirm_visual = {}
    conf = pd.read_csv('merge_vaccine.csv')
    for i in range(len(conf)):
        confirm_visual[conf.iloc[i,0]] = conf.iloc[i,8]
    stylecloud.gen_stylecloud(text=confirm_visual,icon_name="fas fa-male",
                        palette="colorbrewer.diverging.Spectral_11",background_color='black',
                        gradient="horizontal",output_name="./static/img/population.jpg")
    return "population.jpg"

@app.route("/covidgdp", methods=['post'])
def covid_gdp():
    Visual.visual1()
    Visual.visual2()
    Visual.visual3()
    return ''

@app.route("/kor_vac", methods=["post"])
def kor_vac():
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
    file_name = os.listdir("C:/Users/YEIN/Downloads")

    for file in file_name:
        if file.startswith('코로나바이러스'):
            file_name = file
    datas = pd.read_excel(r'C:/Users/YEIN/Downloads/{}'.format(file_name))
    
    # 컬럼명 설정 및 전처리
    d_columns = ['일자','ALL(1)','ALL(FIN)','아제(1)','아제(FIN)','화이자(1)','화이자(FIN)','얀센','모더나(1)','모더나(FIN)']
    datas = datas.drop(index=[0,1,2,3,4,5], axis=0)
    datas.columns = d_columns
    datas = datas.reset_index()
    del datas['index']

    # kor_vaccine.csv 파일로 저장
    datas.to_csv("kor_vaccine.csv", index = False)
    df = pd.read_csv('kor_vaccine.csv')
    years = df['일자']
    data_preproc = pd.DataFrame({'Year': years,'AZ': df['아제(FIN)'],
    'FI': df['화이자(FIN)'],'JA': df['얀센'],'MOD': df['모더나(1)']})
    sns.lineplot(x='Year', y='value', hue='variable',data=pd.melt(data_preproc, ['Year']))
    plt.savefig('./static/img/kor_vaccine.png')
    return 'kor_vaccine.png'

@app.route("/world_vac", methods=["post"])
def world_vac():
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
    pyautogui.press('left')
    time.sleep(1) 
    pyautogui.press('enter')
    time.sleep(1)  
    driver.close()

    # vaccinations.csv 파일 읽고 전처리
    world_vac = pd.read_csv(r'C:/Users/YEIN/Downloads/vaccinations.csv')
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
    return ''

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=5000)