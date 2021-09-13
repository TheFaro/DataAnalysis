#import libraries and functions
import wbdata as wb
import Haver
import pandas as pd
import numpy as np
import datetime as dt
import docx
from docx.shared import Cm
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from matplotlib import pyplot as plt
from matplotlib import ticker
import random
import calendar
import re
from pandasgui import show

#Set country to 3-letter country code of country of interest
country = "KOR"

#Scrape annual data from the World bank API
df_wb = wb.get_dataframe(indicators=all_indicators,country=country_codes.iso_code[country],data_date=data_date,convert_date=True)

#Scrape quarterly and monthly data from the Haver API
df_haver = Haver.data(quarterly_indicators, database='emerge',dates=True)

#Scrape Trade data from the UN comtrade API
url = f"https://comtrade.un.org/api/get/plus?max=100000&type=C&freq=A&px=HS&ps={dt.date.today().year - 1}&r={country_codes.comtrade_code[country]}&p=all&rg=2&cc=TOTAL&uitoken={uitoken}&fmt=csv"

df_trade = pd.read_csv(url) # or url_trade

#use pandas to transform extracted quarterly GDP data into year-on-year percent change
df_gdp_growth_quarterly = (df_gdp_growth_quarterly.pct_change(4, file_mode=None) * 100).round(1).tail(5).dropna()

#use matplotlib to create simple chart of GDP grown and sources of growth
for i in range(len(axs)):
    axs[i].plot(df_chart_gdp.loc[:, 'GDP growth(%)'], lw=2.5, marker='D', markersize=10, color='black')

 #Use f-Strings to produce paragraph "templates"
p = doc.add_paragraph(f"Output {'plunged' if df_gdp_growth_quarterly['GDP growth'].last('2Q').values[-1] < 0 else 'jumped'} by {abs(df_gdp_growth_quarterly['GDP growth'].last('2Q').values[-1])}% year-on-year in Q{df_gdp_growth_quarterly.last('2Q').index[-1].quarter} of {df_gdp_growth_quarterly.last('2Q').index[-1].year}.")