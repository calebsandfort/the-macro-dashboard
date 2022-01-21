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

class Asset:
    def __init__(self, ticker, quantity = 0.0, entry = 0.0, corrTicker = "", j = None):
        if j is None:
            self.ticker = ticker
            self.quantity = quantity
            self.entry = entry
            self.cost_basis = self.quantity * self.entry

            self.corrTicker = "" if corrTicker == "nil" else corrTicker
            
            self.ohlc_data = None
            self.last = 0.0
        else:
            self.__dict__ = json.loads(j)
        
    def toJson(self):
        d = self.__dict__.copy()
        d.pop("ohlc_data", None)
        
        return json.dumps(d);

    
    def setDataAndTechnicals(self, ohlc_data):
        self.ohlc_data = ohlc_data
        
        self.last = self.ohlc_data.at[self.ohlc_data.index[-1], "close"]
    
    @property
    def df_row(self):
        return [self.ticker, self.quantity, self.entry]
    
class AssetCollection:
    def __init__(self, csvFileName = None, existing = None, refreshData = False):
        self.collection = {}
        
        
        if csvFileName is not None:
            temp = pd.read_csv(os.path.join(os.getcwd(), 'portfolios', csvFileName), index_col="Ticker") 
            
            for ticker in temp.index.values:
                self.collection[ticker] = Asset(ticker, temp.at[ticker, 'Quantity'], temp.at[ticker, 'Entry'])
                
            if "SDBA Cash" in self.collection.keys():
                self.collection["Cash"].entry += self.collection["SDBA Cash"].entry
                del self.collection['SDBA Cash']
        else:
            for ticker in existing:
                self.collection[ticker] = Asset(ticker, j = existing[ticker])
                
        self.df = pd.DataFrame(columns = ["Ticker", "Quantity", "Entry"])
        
        self.df.loc["Cash"] = self.collection["Cash"].df_row
        
        for ticker in self.collection.keys():
            if ticker != "Cash":
                self.df.loc[ticker] = self.collection[ticker].df_row
           
            
        startDate = datetime.datetime.strptime('2019-05-01', '%Y-%m-%d')
        endDate = datetime.datetime.today()
            
        allTickers = np.delete(self.df.index.values, np.where(self.df.index.values == "Cash"))

        data = {}

        if refreshData:
            data = dr.GetTdaDataForTickers(allTickers, 'month', 'daily', 1, startDate, endDate, False, True)
        else:
            data = dr.GetDataFromCsv(allTickers)
        
        self.df["Last"] = 0.0
        
        for ticker in allTickers:
            self.collection[ticker].setDataAndTechnicals(data[ticker])
            self.df.at[ticker, "Last"] = self.collection[ticker].last
        
        self.df["Cost Basis"] = self.df["Quantity"] * self.df["Entry"]
        
        # print(self.df.head())
        
        self.portfolio_value = 0.0
                
    def toDict(self):
        temp = {}
        
        for ticker in self.collection:
            temp[ticker] = self.collection[ticker].toJson();

        return temp

blah = AssetCollection("Portfolio.csv")

# d = blah.toDict()

# blah2 = AssetCollection(existing = d)

#jsonStr = json.dumps(blah.__dict__)