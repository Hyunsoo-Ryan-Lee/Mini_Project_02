import requests
from selenium import webdriver 
from bs4 import BeautifulSoup 
import time
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import numpy as np

def Crawl():
    browser = webdriver.Chrome('c:/driver/chromedriver.exe')
    results = []

    url = "https://www.worldometers.info/coronavirus/#countries" 
    browser.get(url)
    time.sleep(2)
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')

    sorting = browser.find_element_by_xpath('//*[@id="main_table_countries_today"]/thead/tr/th[2]')
    sorting.click()

    table_list = soup.select('#main_table_countries_today > tbody:nth-child(2) > tr')

    for i in range(0, len(table_list)):
        if table_list[i].select('a.mt_a'):
            country  = table_list[i].select('a.mt_a')[0].text
            # tot_cases  = table_list[i].select('td.sorting_1')[0].text
            # new_cases  = table_list[i].select('tr > td:nth-child(4)')[0].text
            # tot_deaths = table_list[i].select('tr > td:nth-child(5)')[0].text
            # new_deaths = table_list[i].select('tr > td:nth-child(6)')[0].text
            # tot_recov = table_list[i].select('tr > td:nth-child(7)')[0].text
            # new_recov = table_list[i].select('tr > td:nth-child(8)')[0].text
            # tests = table_list[i].select('tr > td:nth-child(13)')[0].text
            # pop = table_list[i].select('tr > td:nth-child(15)')[0].text
            # data = [country, tot_cases, new_cases, tot_deaths, new_deaths, tot_recov, new_recov, tests, pop]
            
            results.append(country)
        else:
            continue
        
    time.sleep(3)
    browser.quit()
    print(results)

if __name__ == '__main__':
    Crawl()