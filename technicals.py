# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 13:42:09 2021

@author: csandfort
"""
import numpy as np
import pandas as pd
import math
from operator import add 
from finta import TA

def calcHv(data, window):
    log_returns = np.log(data['close'] / data['close'].shift())
    return log_returns.rolling(window).std()*252**.5

def calcHvMean(data):
    hv30 = calcHv(data, 21)
    hv20 = calcHv(data, 14)
    hv10 = calcHv(data, 7)
    
    return (hv30 + hv20 + hv10) / 3.0

def calcHvZScore(data, window):
    hvMean = calcHvMean(data)
    mean = hvMean.rolling(window=window).mean()
    std = hvMean.rolling(window=window).std()

    return (hvMean - mean)/std

def getTrend(data, lowColumn, highColumn, closeColumn, period): 
     lowestLow = data[lowColumn].rolling(period).min();
     highestHigh = data[highColumn].rolling(period).max();
        
     trend = pd.Series(lowestLow + ((highestHigh - lowestLow) / 2)) 
     outlook = [.5] * len(trend)
    
     for i in range(1, len(trend)):
       if trend.iloc[i] < data[closeColumn].iloc[i] and trend.iloc[i - 1] < data[closeColumn].iloc[i - 1]:
         outlook[i] = 1.0
       elif trend.iloc[i] > data[closeColumn].iloc[i] and trend.iloc[i - 1] > data[closeColumn].iloc[i - 1]:
         outlook[i] = 0.
            
     return trend, outlook
 
def Hurst(data, length):
    logLength = math.log(length)
    
    highest = data['high'].rolling(length).max()
    lowest = data['low'].rolling(length).min()
    atr = TA.ATR(data, length)
    logAtr = np.log(atr)
    
    h = (np.log(highest - lowest) - logAtr) / logLength
    
    return h;

def BridgeRanges(src, n):
  slopes = ((src - src.shift(n - 1)) / (n - 1)).tolist()

  srcList = src.tolist()
  srcList.reverse()
  slopes.reverse()
  MinDiffs = [0] * len(srcList)
  MaxDiffs = [0] * len(srcList)
    
  nMinus1 = n - 1
  s = 0
  min_diff = 0.0
  max_diff = 0.0
    
  for index in range(len(srcList) - n):
    min_diff = 100000000.0
    max_diff = -100000000.0
    s = slopes[index]
    subset = srcList[index : index + n]

    for i in range(n):
      min_diff = min(min_diff, subset[nMinus1 - i] - (subset[nMinus1] + (s * i)))
      max_diff = max(max_diff, subset[nMinus1 - i] - (subset[nMinus1] + (s * i)))
        
    MinDiffs[index] = min_diff
    MaxDiffs[index] = max_diff

  srcList.reverse()
  MinDiffs.reverse()
  MaxDiffs.reverse()
    
  BridgeRangeBottom = list(map(add, srcList, MinDiffs))
  BridgeRangeTop = list(map(add, srcList, MaxDiffs))
  
  return BridgeRangeBottom, BridgeRangeTop

def BridgeBands(d, src, n):
    
    
    BridgeRangeBottom, BridgeRangeTop = BridgeRanges(d.close, 15)
    
    hurst = Hurst(d, n)
    
    bbands = TA.BBANDS(d, 15, TA.WMA(d, 15))
    bb_bottom = bbands['BB_LOWER']
    bb_top = bbands['BB_UPPER']
    
    BridgeBandBottom = bb_bottom + ((BridgeRangeBottom - bb_bottom) * abs((hurst * 2) - 1))
    BridgeBandTop = bb_top - ((bb_top - BridgeRangeTop) * abs((hurst * 2) - 1))
    
    return BridgeBandBottom, BridgeBandTop

def calcVolumeMetrics(data):
    data["Volume1W"] = data["volume"].rolling(5).mean()
    data["Volume1M"] = data["volume"].rolling(21).mean()
    
    data["VolumeEnum"] = len(data) * .01
    
    previousIndex = None
    ydayVolume = 0.0
    todayVolume = 0.0
    weekVolume = 0.0
    monthVolume = 0.0
    
    for idx in data.index.values:
        if previousIndex is None:
            data.at[idx, "VolumeEnum"] = 0.0
            previousIndex = idx
        else:
            volumeEnum = 0.0
            
            todayVolume = data.at[idx, "volume"]
            ydayVolume = data.at[previousIndex, "volume"]
            weekVolume = data.at[idx, "Volume1W"]
            monthVolume = data.at[idx, "Volume1M"]
            
            if todayVolume > ydayVolume: volumeEnum = volumeEnum + 1.0
            if todayVolume > weekVolume: volumeEnum = volumeEnum + 1.0
            if todayVolume > monthVolume: volumeEnum = volumeEnum + 1.0
            
            data.at[idx, "VolumeEnum"] = volumeEnum * (1.0 if data.at[idx, "close"] > data.at[previousIndex, "close"] else -1.0)
            
            # print(data.at[idx, "VolumeEnum"], "     ", idx)
            
            previousIndex = idx
    
    return data