# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 14:18:35 2021

@author: csandfort
"""
import datetime
import pandas as pd
import requests
import json
import yfinance as yf  
from os.path import exists

tda_client_id = "CGO9BSW7QI4SAOTB2RP9AUCY8QFFMQ47"
tda_refresh_token = "ECjfrFDrUJqaV5en1SKtjWmBhNIR63agz7f9JJzPvlnI8Ap9o4jvXo4hyp4LtIvGoRx/BP3c40PtiO6lscgE8gJBhcBxeFSt9Hg1qsBgyybsOMeuxStjFj/pT2vBrXgu9AK01xdsD+GcARst68kgmNEf3culaK+0B/iCtktMCz3R93+wyXiA4SWfmCL+sC1g37BjHSkYndPoRof+YUpnabNR/hvsexc+Uur8Xos7V169JNH7YU/iZPUmIEaL2DCTR2TGvamCyyjO8VLG7zVdjsfML7e1C6Iyfwt/GcBDVveZD6CAjLHVU32VviCas8/d7GuDLoVHCXCJJux3EGqitvAZbZfXUkRpo8rXvWZirqBtYSfFOK8XveZZt8mCvMEugV4Or2q9lBnlfdljAfC9Wj67HDcPuaxnNC8DNlCBG6mSYO6k7MOmXWeKxJl100MQuG4LYrgoVi/JHHvlv/CNqO1IleGCXuLlF4Yxt0tVBNH0lW/JCTO4iheqN6qTCnbAoO/LAJ2RiqQBWMPYR8IiN/oiI2xxeWS4V/jhxORhjHV12D0XlW3jE1ZxLYCU1bbpXmiS0fJIa35Adfie2P5bh/dOZXb5V/yvbOyeITpNz0tXUaTBdlHz7G6jZct8x4EKrx28kG7BJRdemnvNUCjnzdZCvsZ4Zra/+b98pDwjkCsXaePJBRFANb4MKHfjiNLg5qT9lZ3cp0QyuJQ9G7Z/ifLrpyQxgvG3HU6iS+pjOH62cTKoTkJxYtgvC3xmSk5xD545cZP3ohJITe6MVw0XlKO8a/K6eR9mUGKZOMLcpkAF8zb3pK3Dn2zQvBnnH2fVUMzaMPlJhhfCzXXGJqMP4eIdpEOHCRtG1NZUb8Zwbu6MA6iPEs/jyyzimbGV9f5MhXA9DJf1vBA=212FD3x19z9sWBHDJACbC00B75E",
#tda_access_token = "WrYYDRo0c7DcKuNNBO1YZL/DvAG7beI1/b2STi7u+wQxdBY9f+6nk+1X0u0JeC4jKQZ/8xThMxJeRFRwr+xNZqtckWHDoEao/rtWqoRKx4UQaCJcHJkxRjEcOe/dlTdB72iFxGjUe1MG1f/Uhd5nN0yks+GHLteqc5rmVrMzGVuBhpWP1Oc4HWucMn0LEGiy4fX5pxghy0W46tFRZ6pv9U8fyVqLlwfzs0JkRCu/k16bMJUkCOXH/hDuH5YOsaBYcZoOrlf1VbZySJkdAF6EVezUWXT3sRLZWXnoH+Fd+ZwX5hUfNY/4981gkIjrbhDwLk5Ma6v3iEjUSavwCPVHJp8Ako58DksF1WatQQUPKi/S74IUH3u1AtIWV6VJSciklgu/RWOLtQTw+Fg+5b3dhygq7XpxKDJCDG5IFXZqj1KA4IZsCjVSaVx2p3pJStnAmpq3PpGPUSSpGkz32zA72s9oobP5R1QX6TXX6RC4QKFgmxkVyvKr1vXeB25WNaomhlMY1kFupUWSwMI4J+/YOwaktiH17apyb9wCs6xzAaHv9GPQlA1oqe2XVen100MQuG4LYrgoVi/JHHvl3GzfqTlQqSuxCH3ZO82OAvYZk0B17ue59FTMYru3DKdV+JhqI3ESnmisiIbTIRcVFrqmBv0eb7wo9z8K3D3gjQeWmHWVd0ZTuXpAXhmH89UEjkLRPBiIIppwZssb93AslXtJRCtgPqxaByIhSxim5wntM/xYkGg5Vr7QsaZPmCUs9RGx4BZP4tbbU/urSpe0eGuMPckKS0tgT7iFq5gWkp/QiBNyshO/MApULpjNJFxH9qz5WiwmBfyzqVIROAE2cezKh69wXeeKTaRig+6IGk66HDkVQzwYNfiMe5LnJqUoBxvKQYEXST3WdAIh2rImXZ/N22u5dHJwZAJMhB8MzQRSJTuela8xSbV7C1smm6CBBzOSTQ5Q6iDZW8QS0qqMQoei+B1tOE89A2Tg4US1uQDe4riZfHGu3X56rC33kyKVhOotfsUVdhS/QJpJQ7C4/eR6mSM3uY8c5bBN949d+bS9u4t4Hxg8tBe5qPeqAOpsz97O7iAaSf+2Y7of223NBffhkNQVSiUtI3bTUwcgQwN7mberkRrDsezNkzSjplScAOEahJvd/Bh4BPA=212FD3x19z9sWBHDJACbC00B75E"

def getAccessToken():
    url = "https://api.tdameritrade.com/v1/oauth2/token"
    params = {'grant_type': 'refresh_token',
              'refresh_token': tda_refresh_token,
              'client_id': tda_client_id}
    
    x = requests.post(url, data = params)
    content = json.loads(x.text)
    tda_access_token = content['access_token']
    #print(tda_access_token)
    return tda_access_token


# endDate = datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time()) + datetime.timedelta(days = 1)
# #endDate = datetime.datetime.strptime('2021-06-11', '%Y-%m-%d')
# startDate = endDate - datetime.timedelta(days = 126)

#startDate = datetime.datetime.strptime('2021-09-10', '%Y-%m-%d')
#endDate = datetime.datetime.strptime('2021-09-21', '%Y-%m-%d')
#"https://api.tdameritrade.com/v1/marketdata/chains?apikey=CGO9BSW7QI4SAOTB2RP9AUCY8QFFMQ47&symbol=XLP&contractType=PUT&strikeCount=20&strategy=SINGLE"

def GetTdaDataForTickers(stockTickers, periodType, frequencyType, frequency, startDate, endDate, needExtendedHoursData, saveToFile = False):
    accessToken = getAccessToken()
    
    data = {}
    
    for ticker in stockTickers:
        data[ticker] = GetTdaData(ticker, periodType, frequencyType, frequency, startDate, endDate, needExtendedHoursData, saveToFile, accessToken)
        
    return data

def GetTdaData(stockTicker, periodType, frequencyType, frequency, startDate, endDate, needExtendedHoursData, saveToFile = False, accessToken = ""):
    original_df = None
    df = None
    file_path = "data/{0}.csv".format(stockTicker);
    
    file_exists = exists(file_path)
    
    if file_exists:
        original_df = pd.read_csv(file_path, index_col="datetime", parse_dates=True)
        startDate = pd.to_datetime(original_df.index.values[-1])

    if accessToken == "":
        accessToken = getAccessToken()

    
    endpoint = 'https://api.tdameritrade.com/v1/marketdata/{stockTicker}/pricehistory?periodType={periodType}&frequencyType={frequencyType}&frequency={frequency}&startDate={startDate}&endDate={endDate}&needExtendedHoursData={needExtendedHoursData}'
    
    full_url = endpoint.format(stockTicker=stockTicker, periodType=periodType, frequencyType=frequencyType, frequency=frequency, startDate=int(startDate.timestamp() * 1000), endDate=int(endDate.timestamp() * 1000), needExtendedHoursData=needExtendedHoursData)
    
    #print(accessToken)
    
    page = requests.get(url=full_url,
                    params={'apikey' : tda_client_id},
                    headers = {'Authorization' : f'Bearer {accessToken}'})
    
    
    content = json.loads(page.content)

    isCurrent = startDate.date() == endDate.date()

    if frequencyType == 'daily':
        df = pd.DataFrame.from_dict(content["candles"])
        df.set_index(df['datetime'].apply(lambda x: datetime.datetime.utcfromtimestamp(x/1000).date()).astype('datetime64'), inplace=True)
        df.drop('datetime', inplace=True, axis = 1)
        
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
                
    else:
        df['date'] = df['datetime'].apply(lambda x: datetime.datetime.fromtimestamp(x/1000))
        df.set_index('date', inplace=True)
        df['date'] = df.index.strftime("%m-%d-%Y %I:%M %p")
    
    if saveToFile and df is not None:
        df.to_csv(file_path)
        print("Saved {0}.csv".format(stockTicker))
    
    return df

# tda_daily_data = GetTdaData("XLE", 'month', 'daily', 1, startDate, endDate, False)

def DownloadYahooData(ticker, startDate, endDate):
    data = yf.download(ticker, start = startDate.strftime("%Y-%m-%d"), end = endDate.strftime("%Y-%m-%d"), progress = False)
    
    #data = yf.download(ticker, period = '5d', interval='15m', progress = False)
    
    columns = [data["Open"], data["High"], data["Low"], data["Close"], data["Volume"]]

    headers = ["open", "high", "low", "close", "volume"]
    
    df = pd.concat(columns, axis=1, keys=headers)
    
    return df

#vix_data = DownloadYahooData("^RVX", startDate, endDate)