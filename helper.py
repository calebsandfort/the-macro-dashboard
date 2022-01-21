# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 15:38:49 2022

@author: csandfort
"""
import os as os
import pandas as pd
import numpy as np
import json
import datetime
import dataRetrieval as dr


def refreshData():
    temp = pd.read_csv(os.path.join(os.getcwd(), 'portfolios', "Portfolio.csv"), index_col="Ticker") 
    
    allTickers = np.delete(temp.index.values, np.where((temp.index.values == "Cash") | (temp.index.values == "SDBA Cash")))
    
    startDate = datetime.datetime.strptime('2019-05-01', '%Y-%m-%d')
    endDate = datetime.datetime.today()
    
    dr.GetTdaDataForTickers(allTickers, 'month', 'daily', 1, startDate, endDate, False, True)
    
refreshData()
