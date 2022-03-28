# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 14:18:35 2021

@author: csandfort
"""
import datetime
import pandas as pd
import numpy as np
import requests
import json
import yfinance as yf  
from os.path import exists
import constants
import nasdaqdatalink
import assetClassesMfr as ac
#from Historic_Crypto import HistoricalData

tda_client_id = "1W2ETS0ETWQBSTRLIARCBLZJACHJYICG"
tda_refresh_token = "YQs9ADwVPLd6c82i1hC1k83NlvQTcfXpHSR0BsO6Mx4FnHNETwmdHnjf9HncI3ifTgCzQmrTwtFzgMc505v6FiV/xyNGKVj7xuJ8jslBEGiTtjROD8OV8ClNkuVw+Bc7FYNPOpWYVZ0Q+AoUqgjoCA7ni7eNILLj4Dfku4JocY0MiutERlO3TpAvo/1GjrjafKPqyOguO8qXRI7GjkkqVfe5VdX1oCSJYnTEgEwtrLJniEqk88aBz1pfoT7C5ws5liVNlkG49gp7KiBR8ksKYlJemuyBMM6nY3Hj85x8iyE4Zh8FY/PhRNnWpntHDQTypv1V8upj4Gbbn1cTEbC9A2QGlFhfLCfTFNvm4T1BxvBT0ABugnPGyVFhwyI8yRXPSJr39CDXuBx5BbKrcemo6QZvOpu//z7dkhRoP1SNTtBOnmXKzt/Z5xJEGfx100MQuG4LYrgoVi/JHHvluB0IDROD6vtJ3O9R/Wpfg9IkG/cNy3UXlNbTkALgAGGJ8NNp5mhGfh8i2DfEd/s6PYv//v8mNOKBom0PJ0s7QKvNXfu3wdxBthsljvxJ7kqpB4JnqdEr6WQnjH8pD4OuRjmyKBnn7J1HAmqZ0vLEZs7ztlQEifnk81njkRbaRVGC2JbHuxN+fu2iR+pN7HqOfKlm8zPkRPrbdBbMK08RBQUVheD4jj5aK3UDh92PhwESIhiZkdiVb68Nqv4tnI5VzG6nO2ILUrIV2zAMzALHGyedi57OA2wq22UtlW6aU6OZ0IohSK8swTZCYfa23xzHz16KCvhTx14HbPwZH+8s0POXIO6FqboUACh4BFXp1RrVIQFpCW7+C08ubsH54SiZ0D40BVA0peKrD/8wAqtVOAFbEkrGf44wlT5pG0HQ5gYbE597uVeF32I+qTE=212FD3x19z9sWBHDJACbC00B75E",
#tda_access_token = "WrYYDRo0c7DcKuNNBO1YZL/DvAG7beI1/b2STi7u+wQxdBY9f+6nk+1X0u0JeC4jKQZ/8xThMxJeRFRwr+xNZqtckWHDoEao/rtWqoRKx4UQaCJcHJkxRjEcOe/dlTdB72iFxGjUe1MG1f/Uhd5nN0yks+GHLteqc5rmVrMzGVuBhpWP1Oc4HWucMn0LEGiy4fX5pxghy0W46tFRZ6pv9U8fyVqLlwfzs0JkRCu/k16bMJUkCOXH/hDuH5YOsaBYcZoOrlf1VbZySJkdAF6EVezUWXT3sRLZWXnoH+Fd+ZwX5hUfNY/4981gkIjrbhDwLk5Ma6v3iEjUSavwCPVHJp8Ako58DksF1WatQQUPKi/S74IUH3u1AtIWV6VJSciklgu/RWOLtQTw+Fg+5b3dhygq7XpxKDJCDG5IFXZqj1KA4IZsCjVSaVx2p3pJStnAmpq3PpGPUSSpGkz32zA72s9oobP5R1QX6TXX6RC4QKFgmxkVyvKr1vXeB25WNaomhlMY1kFupUWSwMI4J+/YOwaktiH17apyb9wCs6xzAaHv9GPQlA1oqe2XVen100MQuG4LYrgoVi/JHHvl3GzfqTlQqSuxCH3ZO82OAvYZk0B17ue59FTMYru3DKdV+JhqI3ESnmisiIbTIRcVFrqmBv0eb7wo9z8K3D3gjQeWmHWVd0ZTuXpAXhmH89UEjkLRPBiIIppwZssb93AslXtJRCtgPqxaByIhSxim5wntM/xYkGg5Vr7QsaZPmCUs9RGx4BZP4tbbU/urSpe0eGuMPckKS0tgT7iFq5gWkp/QiBNyshO/MApULpjNJFxH9qz5WiwmBfyzqVIROAE2cezKh69wXeeKTaRig+6IGk66HDkVQzwYNfiMe5LnJqUoBxvKQYEXST3WdAIh2rImXZ/N22u5dHJwZAJMhB8MzQRSJTuela8xSbV7C1smm6CBBzOSTQ5Q6iDZW8QS0qqMQoei+B1tOE89A2Tg4US1uQDe4riZfHGu3X56rC33kyKVhOotfsUVdhS/QJpJQ7C4/eR6mSM3uY8c5bBN949d+bS9u4t4Hxg8tBe5qPeqAOpsz97O7iAaSf+2Y7of223NBffhkNQVSiUtI3bTUwcgQwN7mberkRrDsezNkzSjplScAOEahJvd/Bh4BPA=212FD3x19z9sWBHDJACbC00B75E"

nasdaqdatalink.ApiConfig.api_key = 'Y9Lf787ZrM5gcGKv-6W7'

def getAccessToken():
    url = "https://api.tdameritrade.com/v1/oauth2/token"
    params = {'grant_type': 'refresh_token',
              'refresh_token': tda_refresh_token,
              'client_id': tda_client_id}
    
    x = requests.post(url, data = params)

    content = json.loads(x.text)
    tda_access_token = content['access_token']

    return tda_access_token


# endDate = datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time()) + datetime.timedelta(days = 1)
# #endDate = datetime.datetime.strptime('2021-06-11', '%Y-%m-%d')
# startDate = endDate - datetime.timedelta(days = 126)

#startDate = datetime.datetime.strptime('2021-09-10', '%Y-%m-%d')
#endDate = datetime.datetime.strptime('2021-09-21', '%Y-%m-%d')
#"https://api.tdameritrade.com/v1/marketdata/chains?apikey=CGO9BSW7QI4SAOTB2RP9AUCY8QFFMQ47&symbol=XLP&contractType=PUT&strikeCount=20&strategy=SINGLE"

def GetTdaDataForTickers(tickers, periodType, frequencyType, frequency, startDate, endDate, needExtendedHoursData, saveToFile = False):
    accessToken = getAccessToken()
    
    data = {}
    
    for ticker in tickers:
        data[ticker] = GetTdaData(ticker, periodType, frequencyType, frequency, startDate, endDate, needExtendedHoursData, saveToFile, accessToken)
        
    return data

def GetTdaData(ticker, periodType, frequencyType, frequency, startDate, endDate, needExtendedHoursData, saveToFile = False, accessToken = ""):
    original_df = None
    df = None
    isYahooData = False
    yahooTicker = ""
    
    divisor = 1.0
    
    if ticker in ac.tickerLookup:
        if "divisor" in ac.tickerLookup[ticker]:
            divisor = ac.tickerLookup[ticker]["divisor"]
            
        if "yahoo" in ac.tickerLookup[ticker]:
            isYahooData = True
            yahooTicker = ac.tickerLookup[ticker]["yahoo"]
        
        ticker = ac.tickerLookup[ticker]["tda"]
    
    file_path = "data/{0}.csv".format(ticker);
    
    file_exists = exists(file_path)
    
    if file_exists:
        original_df = pd.read_csv(file_path, index_col="datetime", parse_dates=True)
        startDate = pd.to_datetime(original_df.index.values[-1])

    isCurrent = startDate.date() == endDate.date()

    if not isYahooData:
        if accessToken == "":
            accessToken = getAccessToken()
    
        
        endpoint = 'https://api.tdameritrade.com/v1/marketdata/{stockTicker}/pricehistory?periodType={periodType}&frequencyType={frequencyType}&frequency={frequency}&startDate={startDate}&endDate={endDate}&needExtendedHoursData={needExtendedHoursData}'
        
        full_url = endpoint.format(stockTicker=ticker, periodType=periodType, frequencyType=frequencyType, frequency=frequency, startDate=int(startDate.timestamp() * 1000), endDate=int(endDate.timestamp() * 1000), needExtendedHoursData=needExtendedHoursData)
        
        page = requests.get(url=full_url,
                        params={'apikey' : tda_client_id},
                        headers = {'Authorization' : f'Bearer {accessToken}'})
        
        
        content = json.loads(page.content)
    
        df = pd.DataFrame.from_dict(content["candles"])
        df.set_index(df['datetime'].apply(lambda x: datetime.datetime.utcfromtimestamp(x/1000).date()).astype('datetime64'), inplace=True)
        df.drop('datetime', inplace=True, axis = 1)
    else:
        df = DownloadYahooData(yahooTicker, startDate, endDate)
    
    df["close"] = df["close"] / divisor
    df["high"] = df["high"] / divisor
    df["low"] = df["low"] / divisor
    df["open"] = df["open"] / divisor
    
    if original_df is not None and isCurrent:
        lastIndex = original_df.index.values[-1]

        original_df.at[lastIndex, 'close'] = df.at[lastIndex, 'close']
        original_df.at[lastIndex, 'high'] = df.at[lastIndex, 'high']
        original_df.at[lastIndex, 'low'] = df.at[lastIndex, 'low']
        original_df.at[lastIndex, 'open'] = df.at[lastIndex, 'open']
        original_df.at[lastIndex, 'volume'] = df.at[lastIndex, 'volume']
        
        df = original_df.copy()
    elif original_df is not None:
        additional_rows = df.loc[df.index.isin(original_df.index.values[-1:])] if isCurrent else df.loc[~df.index.isin(original_df.index.values)]
        df = pd.concat([original_df, additional_rows])
    
    if divisor > 1:
        df = df.round({"close": 4, "high": 4, "low": 4, "open": 4})
    
    if saveToFile and df is not None:
        df.to_csv(file_path)
        print("Saved {0}.csv".format(ticker))
    
    return df


def DownloadYahooData(ticker, startDate, endDate):
    data = yf.download(ticker, start = startDate.strftime("%Y-%m-%d"), end = endDate.strftime("%Y-%m-%d"), progress = False)
    
    #data = yf.download(ticker, period = '5d', interval='15m', progress = False)
    
    d = {'close': data["Close"].values,
         'high': data["High"].values,
         'low': data["Low"].values,
         'open': data["Open"].values,
         'volume': data["Volume"].values,}
    
    index = [str(x.astype('datetime64[D]')) for x in data.index.values]
    
    df = pd.DataFrame(data = d, index=index)
    # df.set_index([str(x.astype('datetime64[D]')) for x in data.index.values], inplace = True)
    df.index.names = ['datetime']
    df = df.round({"close": 4, "high": 4, "low": 4, "open": 4})
    
    df.to_csv("data/Temp.csv")
    
    df = pd.read_csv("data/Temp.csv", index_col="datetime", parse_dates=True)
    df = df.round({"close": 4, "high": 4, "low": 4, "open": 4})
    
    return df

startDatey = datetime.datetime.strptime('2019-05-01', '%Y-%m-%d')
endDatey = datetime.datetime.today()

# test = GetTdaDataForTickers(["DX-Y.NYB"], 'month', 'daily', 1, startDatey, endDatey, False, True)

def GetAlphaQueryVolDataForTickers(stockTickers):
    data = {}
    
    for ticker in stockTickers:
        volData = GetAlphaQueryVolData(ticker)
        if volData is not None:
            data[ticker] = volData
        
    return data

def GetAlphaQueryVolData(ticker):
    df = None
    
    if (ticker.startswith("^") or ticker.startswith("$")):
        return df
    
    file_path = "data/{0}.Vol.csv".format(ticker);
    
    put_endpoint = 'https://www.alphaquery.com/data/option-statistic-chart?ticker={ticker}&perType=30-Day&identifier=iv-put'
    
    put_url = put_endpoint.format(ticker=ticker)
    
    put_page = requests.get(url=put_url)
    
    if put_page.status_code == 404:
        return None
    
    put_content = json.loads(put_page.content)
    
    put_index = []
    
    put_value = []
    
    for item in put_content:
        put_index.append(datetime.datetime.strptime(item["x"].replace("T00:00:00Z", ""), '%Y-%m-%d'))
        put_value.append(item["value"])
        
    
    df = pd.DataFrame(index = put_index)
    df["put_iv"] = put_value
    df.index.names = ['datetime']
    df.sort_index(inplace = True)
       
    df["skew"] = np.nan
    
    skew_endpoint = 'https://www.alphaquery.com/data/option-statistic-chart?ticker={ticker}&perType=90-Day&identifier=iv-mean-skew'
    
    skew_url = skew_endpoint.format(ticker=ticker)
    
    skew_page = requests.get(url=skew_url)
    
    if skew_page.status_code == 404:
        return None
    
    skew_content = json.loads(skew_page.content)
    
    for item in skew_content:
        df.at[datetime.datetime.strptime(item["x"].replace("T00:00:00Z", ""), '%Y-%m-%d'), 'skew'] = item["value"]
    
    df.to_csv(file_path)
    print("Saved {0}.Vol.csv".format(ticker))
    
    return df
    

# test = GetAlphaQueryVolData("VEGI")

volTickerProxies = {
    "BNDD": "TLT",
    "PINK": "XLV"
    }

def GetVolDataForTickers(stockTickers, startDate, endDate, saveToFile = False):
    data = {}
    
    for ticker in stockTickers:
        volData = GetVolData(ticker, startDate, endDate, saveToFile)
        if volData is not None:
            data[ticker] = volData
        
    return data

def GetVolData(stockTicker, startDate, endDate, saveToFile = False):
    original_df = None
    df = None
    file_path = "data/{0}.Vol.csv".format(stockTicker);
    
    file_exists = exists(file_path)
    
    if file_exists:
        original_df = pd.read_csv(file_path, index_col="Date", parse_dates=True)
        startDate = pd.to_datetime(original_df.index.values[-1])
    
    volTicker = stockTicker
    if volTicker in volTickerProxies:
        volTicker = volTickerProxies[volTicker]
    
    try:
        df = nasdaqdatalink.get(f'VOL/{volTicker}', start_date=startDate, end_date=endDate)
    except nasdaqdatalink.DataLinkError:
        print("Failed {0}.Vol.csv".format(stockTicker))
        return df
        
    
    isCurrent = startDate.date() == endDate.date()

    if original_df is not None and isCurrent:
        lastIndex = original_df.index.values[-1]

        for col in df.columns:
            original_df.at[lastIndex, col] = df.at[lastIndex, col]
        
        df = original_df.copy()
    elif original_df is not None:
        additional_rows = df.loc[df.index.isin(original_df.index.values[-1:])] if isCurrent else df.loc[~df.index.isin(original_df.index.values)]
        df = pd.concat([original_df, additional_rows])

    if saveToFile and df is not None:
        df.to_csv(file_path)
        print("Saved {0}.Vol.csv".format(stockTicker))
        
    return df

def GetDataFromCsv(tickers, getVolData = False):
    price_data = {}
    vol_data = {}
    
    for ticker in tickers:
        tda_ticker = ticker
        if tda_ticker in ac.tickerLookup:
            tda_ticker = ac.tickerLookup[ticker]["tda"]
        
        file_path = "data/{0}.csv".format(tda_ticker);
        price_data[ticker] = pd.read_csv(file_path, index_col="datetime", parse_dates=True)
        
        if (getVolData and exists("data/{0}.Vol.csv".format(ticker))):
            file_path = "data/{0}.Vol.csv".format(ticker);
            vol_data[ticker] = pd.read_csv(file_path, index_col="datetime", parse_dates=True)
        else:
            vol_data[ticker] = None
    
    return price_data, vol_data


def getEthBtcCompDf():
    # endDate = datetime.date.today() + datetime.timedelta(days=1)
    # startDate = (endDate - datetime.timedelta(days=10))
    
    
    # btcStartDate = datetime.datetime.strptime('2012-03-01', '%Y-%m-%d')
    # ethStartDate = datetime.datetime.strptime('2016-06-01', '%Y-%m-%d')
    # endDate = datetime.date.today() + datetime.timedelta(days=1)

    btcData = getTiingoCryptoData("btcusd", '2012-02-01')
    ethData = getTiingoCryptoData("ethusd", '2016-04-18')
    
    # btcData = getTiingoCryptoData("btcusd", '2012-03-01')
    # ethData = getTiingoCryptoData("ethusd", '2016-06-01')
    
    comp_df_index = [ethData.index.values[0]]
    
    for i in range(1, len(btcData)):
        comp_df_index.append(comp_df_index[i-1] + np.timedelta64(1,'D'))
    
    comp_df = pd.DataFrame(index = comp_df_index)
    comp_df["BTC"] = np.nan
    comp_df["ETH"] = np.nan
    
    for i in range(len(btcData)):
        comp_df.iat[i, 0] = btcData.iat[i, 0]
        
    ethData_index = ethData.index.values
        
    for i in range(len(ethData)):
        comp_df.iat[i, 1] = ethData.iat[i, 0]
        #print(ethData_index[i])
    
    return comp_df

def getTiingoCryptoData(ticker, startDate):
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization' : 'Token 75c2738ee800320f770e0205110e626c6ac7220b'
        }
    
    requestResponse = requests.get(f"https://api.tiingo.com/tiingo/crypto/prices?tickers={ticker}&startDate={startDate}&resampleFreq=1day&token=75c2738ee800320f770e0205110e626c6ac7220b", headers=headers)
    
    #content = json.loads(page.content)
    content = requestResponse.json()
    
    df = pd.DataFrame(content[0]["priceData"])
    df.set_index(df['date'].apply(lambda x: datetime.datetime.strptime(x.replace("T00:00:00+00:00", ""), "%Y-%m-%d").date()).astype('datetime64'), inplace=True)
    df.drop(['date', 'high', 'low', 'open', 'tradesDone', 'volume', 'volumeNotional'], inplace=True, axis = 1)
    
    return df
    

def getOneMillionActiveAddresses(arr):
    dates = [];
    activeAddresses = []
    
    for pair in arr:
        dates.append(datetime.datetime.strptime(pair[0], "%Y-%m-%d").date())
        activeAddresses.append(pair[1])
        
    df = pd.DataFrame(index = dates)
    df["ActiveAddresses"] = activeAddresses
    df["AggregateActiveAddresses"] = df["ActiveAddresses"].rolling(30).sum()
    
    return df[df["AggregateActiveAddresses"] > 950000]

#ethMill = getOneMillionActiveAddresses(constants.ethDailyActiveAddresses)
#btcMill = getOneMillionActiveAddresses(constants.btcDailyActiveAddresses)

#temp = getTiingoCryptoData("ethusd", '2016-04-18')
#temp = getEthBtcCompDf()      

#temp1 = getTiingoCryptoData("btcusd")
#temp2 = getTiingoCryptoData("ethusd")
   
# def historicCryptoTest():
#     df = HistoricalData('BTC-USD',86400,'2012-03-01-00-00').retrieve_data()
    
#     return df

# 7l8rmlz2yd

# pBI/G8fM13bIOLDTg19qRqSMdHXLlykClDw+I/6l//PlR8yNiq1rSq1lSvjnrP6wTmFt/dZkjagPXg+cQKchzw==

#temp = getEthBtcCompDf()
#temp = historicCryptoTest()


# cbf01b35-7ba0-4eda-a2b3-74d2ac0f88f8
