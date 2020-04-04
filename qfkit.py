# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 22:45:16 2020

@author: Viraj, NIT Surat - Quarantine Fun:)
"""

import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib.dates as mdates
from mpl_finance import candlestick_ohlc
import bs4 as bs
import requests
import pandas as pd
import pandas_datareader.data as web
style.use('ggplot')

def get_data(co):
    '''
    Get the Price Data for company `co`
    '''
    start = dt.datetime(2000,1,1)
    end = dt.date.today()
    df = web.DataReader(co, 'yahoo', start, end)
    df = pd.DataFrame(df)
    return df

def n_ma(n, df, row):
    df[str(n) + 'MA'] = df[row].rolling(window = n, min_periods = 0).mean()
    return df

def n_ohlc(n, df, row):
    return df[row].resample(str(n)+'D').ohlc()

def n_vol(n, df, row = 'Volume'):
    return df[row].resample(str(n)+'D').sum()

def candlesticks(n, df, row):
    df_ohlc = n_ohlc(n, df, row)
    df_volume = n_vol(n, df)
    df_ohlc.reset_index(inplace = True)
    df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)
    
    plt.figure(figsize = (40,18))
    ax1 = plt.subplot2grid((6,1), (0,0), rowspan = 5, colspan = 1)
    ax2 = plt.subplot2grid((6,1), (5,0), rowspan = 1, colspan = 1, sharex = ax1)
    ax1.xaxis_date()
    candlestick_ohlc(ax1, df_ohlc.values, width = 2, colorup = 'g')
    ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)
    
def get_sp500_list():
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        ticker = ticker.replace('\n', '')
        tickers.append(ticker)
    return tickers
    