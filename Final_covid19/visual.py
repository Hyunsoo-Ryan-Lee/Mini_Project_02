import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import numpy as np

class Visual():
    def visual1():
        path = 'c:/Windows/Fonts/malgun.ttf'
        font_name = font_manager.FontProperties(fname = path).get_name()
        rc('font', family = font_name)

        covid_gdp = pd.read_csv("covid_gdp.csv")
        covid_gdp.info()

        covid_gdp_head30 = covid_gdp.sort_values(by=['2019_gdp'], ascending=False).head(30)

        plt.style.use('default')
        plt.rcParams['figure.figsize'] = (20, 15)
        plt.rcParams['font.size'] = 12

        fig, ax1 = plt.subplots()
        ax1.plot("country", "tot_recov_1m", data=covid_gdp_head30, color='green', label='recov per 1M')
        ax1.legend(loc='upper right')

        ax2 = ax1.twinx()
        ax2.plot("country", "tot_cases_1m", data=covid_gdp_head30, color='deeppink', label='cases per 1M')
        ax2.legend(loc='upper left')


        fig.autofmt_xdate(rotation=45)
        plt.grid(True)
        plt.title('GDP 상위 30개국', y=1.05, size=20)
        plt.savefig("./static/img/covid_gdp_plot1.png")

    def visual2():
        path = 'c:/Windows/Fonts/malgun.ttf'
        font_name = font_manager.FontProperties(fname = path).get_name()
        rc('font', family = font_name)

        covid_gdp = pd.read_csv("covid_gdp.csv")
        covid_gdp.info()

        covid_gdp_tail30 = covid_gdp.sort_values(by=['2019_gdp'], ascending=True).head(30)

        plt.style.use('default')
        plt.rcParams['figure.figsize'] = (20, 15)
        plt.rcParams['font.size'] = 12

        fig, ax1 = plt.subplots()
        ax1.plot("country", "tot_recov_1m", data=covid_gdp_tail30, color='green', label='recov per 1M')
        ax1.legend(loc='upper right') 

        ax2 = ax1.twinx()
        ax2.plot("country", "tot_cases_1m", data=covid_gdp_tail30, color='deeppink', label='cases per 1M')
        ax2.legend(loc='upper left')

        fig.autofmt_xdate(rotation=45)
        plt.grid(True)
        plt.title('GDP 하위 30개국', y=1.05, size=20)
        plt.savefig("./static/img/covid_gdp_plot2.png")

    def visual3():
        path = 'c:/Windows/Fonts/malgun.ttf'
        font_name = font_manager.FontProperties(fname = path).get_name()
        rc('font', family = font_name)

        covid_gdp = pd.read_csv("covid_gdp.csv")
        heatmap_data = covid_gdp[['country',
                'tot_cases',
                'new_cases',
                'tot_deaths',
                'new_deaths',
                'tot_recov',
                'new_recov',
                'tests',
                'pop',
                '2019_gdp',
                'tot_recov_1m',
                'tot_cases_1m',
                'tot_deaths_1m',
                ]]
        colormap = plt.cm.Blues
        plt.figure(figsize=(18, 16))
        plt.title('covid19 & GDP per capita', y=1.05, size=20)
        sns.heatmap(covid_gdp.corr(), linewidths=0.1, vmax=1.0,square=True, cmap=colormap, linecolor='white', annot=True,annot_kws={"size":10});
        plt.savefig("./static/img/covid_gdp_plot3.png")

# if __name__ == '__main__':
#     Visual.visual1()
#     Visual.visual2()
#     Visual.visual3()