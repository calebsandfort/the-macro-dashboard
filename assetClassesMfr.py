# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 15:41:16 2022

@author: csandfort
"""

import os as os
import pandas as pd
import numpy as np
import json
import datetime 
import dataRetrieval as dr
import technicals
from operator import itemgetter
import dash_bootstrap_components as dbc
from dash import html

tickerLookup = {
    "VIX": { "tda": "$VIX.X", "mfr": "^VIX" },
    "DXY": { "tda": "$DXY.X", "mfr": "^DXY", "yahoo": "DX-Y.NYB" },
    "US10Y": { "tda": "$TNX.X", "mfr": "^US10Y", "divisor": 10.0, "isPercent": True },
    "US30Y": { "tda": "$TYX.X", "mfr": "^US30Y", "divisor": 10.0, "isPercent": True }
    }

correlationTickers = ["DXY", "SPY", "US10Y", "US30Y", "VIX"]

def getMfrData():
    file_path = "mfr"
    files = os.listdir(file_path)
    
    data = {}
    
    for f in files:
        date = datetime.datetime.strptime(f.split(".")[0], "%Y-%m-%d")
        # print(date)
        
        data[date] = pd.read_csv(os.path.join(file_path, f), index_col="Ticker")
        
        
    return data
        
def getMfrDataAsList():
    temp = getMfrData()
    
    l = []
    
    for date in temp:
        l.append({"date": date, "data": temp[date]})
        
    sortedList = sorted(l, key=itemgetter('date'), reverse=True)
    
    return sortedList



def getDisplayTickerFromMfrTicker(mfrTicker):
    for ticker in tickerLookup:
        if tickerLookup[ticker]["mfr"] == mfrTicker:
            return ticker
        
    return mfrTicker

def getAllMfrTickers():
    mfrDataList = getMfrDataAsList()
    tickers = [ getDisplayTickerFromMfrTicker(ticker) for ticker in mfrDataList[0]["data"].index.values]
    
    return tickers

noVolumeTickers = ["US10Y", "US30Y", "VIX"]

class MfrChange:
    def __init__(self, date, ticker, metric, old_outlook, new_outlook):
        self.date = date
        self.ticker = ticker
        self.metric = metric
        self.old_outlook = old_outlook
        self.new_outlook = new_outlook
        
    def toString(self, showTicker = False):
        tickerString = ""
        
        if showTicker:
            tickerString = f" - {self.ticker}"
        
        return f"{self.date:%b %d}{tickerString} - {self.metric}: {self.old_outlook.capitalize()} to {self.new_outlook.capitalize()}"
        
    def getListGroupItem(self, smallFont = False, showTicker = False):
        listGroupItem = None
        
        fontSize = "20px"
        if smallFont:
            fontSize = "15px"
        
        className = ""
        
        if self.metric == "Trend":
            if self.new_outlook == "Bearish":
                className = "bg-danger text-white"
            elif self.new_outlook == "Neutral":
                className = "bg-warning text-white"
            elif self.new_outlook == "Bullish":
                className = "bg-success text-white"
        else:
            if self.new_outlook == "Bearish":
                className = "border border-danger text-danger bg-white"
            elif self.new_outlook == "Neutral":
                className = "border border-warning text-warning bg-white"
            elif self.new_outlook == "Bullish":
                className = "border border-success text-success bg-white"
            
        
        listGroupItem = dbc.ListGroupItem(html.Div(self.toString(showTicker), style=dict(fontSize = fontSize)), className=f"{className} py-3 font-weight-bold")
        
        
        return listGroupItem
        
def getAllMfrChanges():
    mfrDataList = getMfrDataAsList()
    allMfrChanges = []
    
    for i in range(len(mfrDataList) - 1):
        currentDate = mfrDataList[i]["date"]
        currentData = mfrDataList[i]["data"]
        
        oldData = mfrDataList[i + 1]["data"]
        
        for ticker in currentData.index:
            if ticker in oldData.index:
                if currentData.at[ticker, "Trend"] != oldData.at[ticker, "Trend"]:
                    allMfrChanges.append(MfrChange(currentDate, getDisplayTickerFromMfrTicker(ticker), "Trend",
                                                   oldData.at[ticker, "Trend"].capitalize(), currentData.at[ticker, "Trend"].capitalize()))
                                   
                if currentData.at[ticker, "30D HH/LL"] != oldData.at[ticker, "30D HH/LL"]:
                    allMfrChanges.append(MfrChange(currentDate, getDisplayTickerFromMfrTicker(ticker), "Momentum",
                                                   oldData.at[ticker, "30D HH/LL"].capitalize(), currentData.at[ticker, "30D HH/LL"].capitalize()))
    
    
    return allMfrChanges

amc = getAllMfrChanges()

def getMfrChangesForTicker(ticker):
    return list(filter(lambda x: x.ticker == ticker, amc))

def getMfrChangeListGroupItemsForTicker(ticker):
    changes_list = getMfrChangesForTicker(ticker)
    
    list_group_items = [x.getListGroupItem() for x in changes_list]
    
    return list_group_items

class Asset:
    def __init__(self, ticker, quantity = 0.0, entry = 0.0, corrTicker = "", j = None):
        if j is None:
            self.id = ticker
            self.ticker = ticker
            
            self.tda_ticker = self.ticker
            self.mfr_ticker = self.ticker
            
            if self.ticker in tickerLookup:
                self.tda_ticker = tickerLookup[self.ticker]["tda"]
                self.mfr_ticker = tickerLookup[self.ticker]["mfr"]
            
            self.quantity = quantity
            self.entry = entry
            self.cost_basis = self.quantity * self.entry

            self.corrTicker = "" if corrTicker == "nil" else corrTicker
            
            self.price_data = None
            self.last = 0.0
            
            #Chg
            self.Chg1D = 0.0
            self.Chg1M = 0.0
            self.Chg3M = 0.0
            
            #MFR
            self.Momentum = ""
            self.MomentumEmoji = '😀'
            self.Trend = ""
            self.TrendEmoji = '😀'
            self.LR = 0.0
            self.TR = 0.0
            self.RPos = 0.0
            self.MfrAction = ""
            
            #Volume
            self.VolumeDesc = "None"
            
            #Calculated Properties
            self.Weight = 0.0
            self.PnL = 0.0

        else:
            self.__dict__ = json.loads(j)
       
   
    @property
    def df_row(self):
        return [self.id, self.ticker, self.quantity, self.entry, self.last, self.Chg1D, self.Chg1M, self.Chg3M,
                self.Momentum, self.MomentumEmoji, self.Trend, self.TrendEmoji, self.LR, self.TR, self.RPos, self.VolumeDesc,
                self.MfrAction] 
       
    def toJson(self):
        d = self.__dict__.copy()
        d.pop("price_data", None)
        
        return json.dumps(d);

    
    def setDataAndTechnicals(self, price_data, mfr_data_dict):
        self.price_data = price_data
        
        self.last = self.price_data.at[self.price_data.index[-1], "close"]
        self.price_data["IsUp"] = self.price_data['close'] > self.price_data['close'].shift(1)
    
        #%% Chg
        self.price_data['Chg1D'] = (self.price_data['close'] / self.price_data['close'].shift(1)) - 1.0
        self.Chg1D = self.price_data.at[self.price_data.index[-1], "Chg1D"]
        
        self.price_data['Chg1M'] = (self.price_data['close'] / self.price_data['close'].shift(21)) - 1.0
        self.Chg1M = self.price_data.at[self.price_data.index[-1], "Chg1M"]
        
        self.price_data['Chg3M'] = (self.price_data['close'] / self.price_data['close'].shift(63)) - 1.0
        self.Chg3M = self.price_data.at[self.price_data.index[-1], "Chg3M"]
        #%%
        
        #%% MFR
        self.price_data['Momentum'] = "" 
        self.price_data['Trend'] = ""  
        self.price_data['LR'] = np.nan  
        self.price_data['TR'] = np.nan     
        
        for date in mfr_data_dict:
            mfr_data = mfr_data_dict[date]
            if self.mfr_ticker in mfr_data.index:
                self.price_data.at[date, 'Momentum'] = mfr_data.at[self.mfr_ticker, "30D HH/LL"]
                
                self.price_data.at[date, 'Trend'] = mfr_data.at[self.mfr_ticker, "Trend"]
                
                self.price_data.at[date, 'LR'] = mfr_data.at[self.mfr_ticker, "Lower Fractal Range"]
                self.LR = self.price_data.at[self.price_data.index[-1], "LR"]
                
                self.price_data.at[date, 'TR'] = mfr_data.at[self.mfr_ticker, "Upper Fractal Range"]
                self.TR = self.price_data.at[self.price_data.index[-1], "TR"]
                
        self.MfrAction = getMfrAction(self.procureLastValue("Trend"), self.procureLastValue("Momentum"))
        #%%
        
        
        #%% Trend/Trade       
        # trend, outlook = technicals.getTrend(self.price_data, 'low', 'high', 'close', 63)
        # self.price_data['Trend'] = trend
        # self.Trend = self.procureLastValue("Trend")
        
        # trade, trade_outlook = technicals.getTrend(self.price_data, 'low', 'high', 'close', 21)
        # self.price_data['Trade'] = trade
        # self.Trade = self.procureLastValue("Trade")
        
        # self.price_data["IsBullTrend"] = self.price_data["close"] > self.price_data["Trend"]
        # self.IsBullTrend = self.procureLastValue("IsBullTrend")
        
        self.price_data['MomentumEmoji'] = self.price_data['Momentum'].apply(lambda x: getSentimentEmoji(x))
        self.MomentumEmoji = self.procureLastValue("MomentumEmoji")
        
        self.price_data['TrendEmoji'] = self.price_data['Trend'].apply(lambda x: getSentimentEmoji(x))
        self.TrendEmoji = self.procureLastValue("TrendEmoji")
        
        self.price_data["TrendInt"] = self.price_data['Trend'].apply(lambda x: getTrendInt(x))
        
        #%%
                
        #%% Ranges
        self.price_data['RPos'] = (self.price_data['TR'] - self.price_data['close']) / (self.price_data['TR'] - self.price_data['LR'])
        # self.price_data.loc[(self.price_data['RPos'] > 1.), 'RPos'] = 1.0
        # self.price_data.loc[(self.price_data['RPos'] < 0.), 'RPos'] = 0.0
        self.RPos = self.procureLastValue("RPos")
        
        #%%
        
        #%% Volume
        self.price_data = technicals.calcVolumeMetrics(self.price_data)
        
        self.price_data.loc[(self.price_data['VolumeEnum'] == 0.0) & (self.price_data["IsUp"] == True), 'VolumeDesc'] = 'Weak'
        self.price_data.loc[(self.price_data['VolumeEnum'] == 1.0) & (self.price_data["IsUp"] == True), 'VolumeDesc'] = 'Moderate'
        self.price_data.loc[(self.price_data['VolumeEnum'] == 2.0) & (self.price_data["IsUp"] == True), 'VolumeDesc'] = 'Strong'
        self.price_data.loc[(self.price_data['VolumeEnum'] == 3.0) & (self.price_data["IsUp"] == True), 'VolumeDesc'] = 'Absolute'
        
        self.price_data.loc[(self.price_data['VolumeEnum'] == -0.0) & (self.price_data["IsUp"] == False), 'VolumeDesc'] = 'Weak'
        self.price_data.loc[(self.price_data['VolumeEnum'] == -1.0) & (self.price_data["IsUp"] == False), 'VolumeDesc'] = 'Moderate'
        self.price_data.loc[(self.price_data['VolumeEnum'] == -2.0) & (self.price_data["IsUp"] == False), 'VolumeDesc'] = 'Strong'
        self.price_data.loc[(self.price_data['VolumeEnum'] == -3.0) & (self.price_data["IsUp"] == False), 'VolumeDesc'] = 'Absolute'
        
        self.VolumeDesc = self.price_data.at[self.price_data.index[-1], "VolumeDesc"]
        #%%
        
        #%% Volume
        self.price_data = technicals.calcMatrix(self.price_data)
        
        #%%
        
    def procureLastValue(self, col):
        return self.price_data.at[self.price_data.index[-1], col]
    
    def setCalculatedProperties(self, collectionDf, isPortfolio):
        if isPortfolio:
            self.Weight = collectionDf.at[self.ticker, "Weight"]
            self.PnL = collectionDf.at[self.ticker, "PnL"]
        
        self.last = collectionDf.at[self.ticker, "Last"]
        self.MfrAction = collectionDf.at[self.ticker, "MfrAction"]
    
    
class AssetCollection:
    def __init__(self, csvFileName = None, existing = None, refreshData = False, isPortfolio = True):
        self.collection = {}
        self.isPortfolio = isPortfolio
        
        
        if csvFileName is not None:
            temp = pd.read_csv(os.path.join(os.getcwd(), 'portfolios', csvFileName), index_col="Ticker") 
            
            for ticker in temp.index.values:
                self.collection[ticker] = Asset(ticker, temp.at[ticker, 'Quantity'], temp.at[ticker, 'Entry'])
                
            self.collection["Cash"].last = self.collection["Cash"].entry
        else:
            for ticker in existing:
                self.collection[ticker] = existing[ticker]
                
        self.df = pd.DataFrame(columns = ["id", "Ticker", "Quantity", "Entry", "Last", "Chg1D", "Chg1M", "Chg3M", "Momentum", "MomentumEmoji",
                                          "Trend", "TrendEmoji", "LR", "TR", "RPos", "VolumeDesc", "MfrAction"])
        
        self.df.loc["Cash"] = self.collection["Cash"].df_row
        
        startDate = datetime.datetime.strptime('2019-05-01', '%Y-%m-%d')
        endDate = datetime.datetime.today()
        allTickers = [ticker for ticker in self.collection]
        allTickers.remove("Cash")
        price_data, vol_data = dr.GetDataFromCsv(allTickers)
        mfr_data = getMfrData()
        
        for ticker in allTickers:
            if ticker != "Cash":
                self.collection[ticker].setDataAndTechnicals(price_data[ticker], mfr_data)
                self.df.loc[ticker] = self.collection[ticker].df_row
             
        
        self.df["Cost Basis"] = self.df["Quantity"] * self.df["Entry"]
        self.df["Current Value"] = self.df["Quantity"] * self.df["Last"]
        
        if isPortfolio:
            self.df["Weight"] = self.df["Current Value"] / self.df["Current Value"].sum()
            self.df["PnL"] = ((self.df["Last"] - self.df["Entry"]) / self.df["Entry"])
        else:
            self.df["Weight"] = 0.0
            self.df["PnL"] = 0.0
        
        # print(self.df.head())
        
        self.portfolio_value = 0.0
        
        for ticker in self.collection:
            self.collection[ticker].setCalculatedProperties(self.df, self.isPortfolio)
                
    def toDict(self):
        temp = {}
        
        for ticker in self.collection:
            temp[ticker] = self.collection[ticker].toJson();

        return temp
    

def getSentimentEmoji(x):
    # '✔️' if x == "bullish" elif x == "bearish" elif x == "bearish" else '⚠️' else ''
    emoji = ''
    
    if x == "bullish":
        emoji = '✔️'
    elif x == "bearish":
        emoji = '❌'
    elif x == "neutral":
        emoji = '⚠️'
    
    return emoji

def getTrendInt(x):
    i = np.nan
    
    if x == "bullish":
        i = 1
    elif x == "bearish":
        i = -1
    elif x == "neutral":
        i = 0
    
    #print(i)
    
    return i

def getMfrAction(trend, momentum):
    # '✔️' if x == "bullish" elif x == "bearish" elif x == "bearish" else '⚠️' else ''
    action = ''
    
    if trend == "bullish" and momentum == "bullish":
        action = 'Add on dips'
    elif trend == "bullish" and momentum == "neutral":
        action = "Caution, don't add, get smaller"
    elif trend == "bullish" and momentum == "bearish":
        action = 'Get out / Potentionally short'
    elif trend == "bearish" and momentum == "bearish":
        action = 'Short, keep adding'
    elif trend == "bearish" and momentum == "neutral":
        action = "Caution, don't add, get smaller"
    elif trend == "bearish" and momentum == "bullish":
        action = 'Stop shorting / Get long'
    
    return action
        

# blah = getAllMfrTickers()

# d = blah.toDict()

# blah2 = AssetCollection(existing = d)

#jsonStr = json.dumps(blah.__dict__)