#!/usr/bin/python
from coinpaprika import client as Coinpaprika
import pandas as pd
import math
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import figure
import seaborn as sns
import os
from config import getApi

image='last.png'
api = getApi()

plt.style.use('seaborn-bright')

# SETTING DATE VARIABLES


TODAY = dt.date.today()
START_DATE  = TODAY - dt.timedelta(days=100)

#CALL PAPRIKA CLIENT
client = Coinpaprika.Client()

#SEND REQUEST FOR ALL TICKER DATA
tickers = client.tickers()


# MAKE 100 TOP DATAFRAME
ticker_data_hundred = pd.DataFrame(tickers[:101])

#NORMALIZE 'quotes' DATA TO A DIFFERENT DATAFRAME
ticker_quotes = pd.DataFrame.from_records(ticker_data_hundred['quotes'])
ticker_quotes = ticker_quotes['USD'].apply(pd.Series)


print(ticker_quotes.columns)

# CREATE SPECIFIC DATAFRAME FROM THE PREVIOUS TWO CREATED
myDf = pd.DataFrame(ticker_data_hundred['symbol'])
myDf['rank'] = ticker_data_hundred['rank']
myDf['Mcap'] = ticker_quotes.market_cap
myDf['price'] = ticker_quotes.price
myDf['Mcap 24h change'] = ticker_quotes.percent_change_24h
myDf['Vol change'] = ticker_quotes.volume_24h_change_24h



myDf2 = pd.DataFrame(ticker_data_hundred['symbol'])
myDf2['30 day% change'] = ticker_quotes.percent_change_30d
myDf2['7 day% change'] = ticker_quotes.percent_change_7d
myDf2['24 hrs% change'] = ticker_quotes.percent_change_24h


meanMcapChange = myDf['Mcap 24h change'].expanding(1)


#FETCH 24H MCAP CHANGE WINNER & LOSER ONLY %
mcapWinner = myDf.sort_values('Mcap 24h change', ascending=False).iloc[0]
mcapLoser = myDf.sort_values('Mcap 24h change', ascending=False).iloc[100]

#FETCH 24H VOL CHANGE WINNER & LOSER ONLY %
volWinner = myDf.sort_values('Vol change', ascending=False).iloc[0]
volLoser = myDf.sort_values('Vol change', ascending=False).iloc[100]



#changeInUsd = (((100 - mcapLoser) / 100) * (myDf.sort_values('Mcap 24h change', ascending=False).iloc[200,5]))



helpMe = myDf['symbol']

myVar = myDf['Mcap 24h change']
myVar2 = myDf2['7 day% change']

#seek avg min max values from %change columns
a1 = (myDf2.iloc[:, [1,2,3]].min()).max()
b1 = (myDf2.iloc[:, [1,2,3]].max()).min()

#plot the % change dataframe
ax = myDf2.plot.bar(xticks=myDf2.index, figsize=(15,7), logy=False, rot=90, stacked=True, ylim = (a1*5, b1*5))
ax.set(xlabel='Ticker', ylabel='% change', title='Top 100 coins price % change')
ax.set_xticklabels(myDf2.symbol)
plt.tight_layout()


plt.savefig('last.png', quality=10)
#plt.show()

def postWithImage(update):
    print(api.PostUpdate(update, media=image))
    os.remove(image)


postWithImage('Marketcap Winner ${}, Marketcap Loser ${}, #cryptobot things '.format(mcapWinner.symbol, mcapLoser.symbol))
#
#print(('Marketcap Winner ${}, Marketcap Loser ${} '.format(mcapWinner.symbol, mcapLoser.symbol)))
