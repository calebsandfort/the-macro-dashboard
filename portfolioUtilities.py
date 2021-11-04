# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 15:12:15 2021

@author: csandfort
"""
import os as os
from os import walk
from pathlib import Path
import pandas as pd
import numpy as np
import dataRetrieval as dr 
import datetime
import technicals as technicals 
import matplotlib.pyplot as plt
from matplotlib import colors

def initializePortfolios():
    startDate = datetime.datetime.strptime('2021-01-01', '%Y-%m-%d')
    endDate = datetime.datetime.today()
    
    universeInfo = pd.read_csv(os.path.join(os.getcwd(), 'data', "UniverseInfo.csv"), index_col="Ticker")
    
    #portfolioPath = os.path.join(os.getcwd(), 'portfolios')
    
    filenames = os.listdir(os.path.join(os.getcwd(), 'portfolios'))  # [] if no file
    
    allTickers = []
    portfolios = {}
    
    for x in filenames:
        #portfolios[Path(x).stem] = pd.read_csv(os.path.join(os.getcwd(), 'portfolios', x), index_col="Ticker")
        temp = pd.read_csv(os.path.join(os.getcwd(), 'portfolios', x), index_col="Ticker")
        
        tickers = []
        quantities = []
        entries = []
        lasts = []
        previouses = []
        costBasii = []
        currentValues = []
        ydayValues = []
        weights = []
        pnls = []
        chg1d = []
        names = []
        assetClasses = []
        universes = []
        factors = []
        exposures = []
        grids = []
        rvs = []
        rvs1d = []
        rvs1w = []
        rvs1m = []
        trends = []
        trades = []
        momos = []
        bbbs = []
        bbts = []
        bbps = []
        volumeDescs = []
        
        totalCash = 0.0
        
        if "SDBA Cash" in temp.index.values:
            totalCash += temp.at["SDBA Cash", "Entry"]
        
        if "Cash" in temp.index.values:
            totalCash += temp.at["Cash", "Entry"]
        
        tickers.append("Cash")
        quantities.append(1.0)
        entries.append(totalCash)
        lasts.append(totalCash)
        previouses.append(0.0)
        costBasii.append(totalCash)
        currentValues.append(totalCash)
        ydayValues.append(totalCash)
        weights.append(0.0)
        pnls.append(0.0)
        chg1d.append(0.0)
        names.append("Cash")
        assetClasses.append("Cash")
        universes.append("Cash")
        factors.append("Cash")
        exposures.append("Cash")
        grids.append("Cash")
        rvs.append(0.0)
        rvs1d.append(0.0)
        rvs1w.append(0.0)
        rvs1m.append(0.0)
        trends.append(0.0)
        trades.append(0.0)
        momos.append(0.0)
        bbbs.append(0.0)
        bbts.append(0.0)
        bbps.append(0.0)
        volumeDescs.append('')
        
        for i in temp.index.values:
            if i != "SDBA Cash" and i != "Cash":
                tickers.append(i)
                quantities.append(temp.at[i, "Quantity"])
                entries.append(temp.at[i, "Entry"])
                lasts.append(0.0001)
                previouses.append(0.0001)
                costBasii.append(quantities[-1] * entries[-1])
                currentValues.append(0.0001)
                ydayValues.append(0.0001)
                weights.append(0.0001)
                pnls.append(0.0001)
                chg1d.append(0.0001)
                rvs.append(0.0001)
                rvs1d.append(0.0001)
                rvs1w.append(0.0001)
                rvs1m.append(0.0001)
                trends.append(0.0001)
                trades.append(0.0001)
                momos.append(0.0001)
                bbbs.append(0.0001)
                bbts.append(0.0001)
                bbps.append(0.0001)
                volumeDescs.append('')
                
                #Ticker, Name, Asset Class,Universe, Factor, Exposure, GRID
                
                if i in universeInfo.index.values:
                    names.append(universeInfo.at[i, "Name"])
                    assetClasses.append(universeInfo.at[i, "Asset Class"])
                    universes.append(universeInfo.at[i, "Universe"])
                    factors.append(universeInfo.at[i, "Factor"])
                    exposures.append(universeInfo.at[i, "Exposure"])
                    grids.append(universeInfo.at[i, "GRID"])
                else:
                    names.append("")
                    assetClasses.append("")
                    universes.append("")
                    factors.append("")
                    exposures.append("")
                    grids.append("")
                
                if i not in allTickers:
                    allTickers.append(i)
        
        data = {
            "id": tickers,
            "Ticker": tickers,
            "Quantity": quantities,
            "Entry": entries,
            "Last": lasts,
            "Previous": previouses,
            "CostBasis": costBasii,
            "CurrentValue": currentValues,
            "YdayValue": ydayValues,
            "Weight": weights,
            "Chg1D": chg1d,
            "PnL": pnls,
            "Name": names,
            "Asset Class": assetClasses,
            "Universe": universes,
            "Factor": factors,
            "Exposure": exposures,
            "GRID": grids,
            "RV": rvs,
            "RV1D": rvs1d,
            "RV1W": rvs1w,
            "RV1M": rvs1m,
            "Trend": trends,
            "Trade": trades,
            "Momo": momos,
            "BBBot": bbbs,
            "BBTop": bbts,
            "BBPos": bbps,
            "VolumeDesc": volumeDescs
            }   
         
        portfolio_df = pd.DataFrame(data, tickers)
        
        portfolios[Path(x).stem] = {"positions": portfolio_df.to_json(date_format='iso', orient='split'),
                                    "total_value": portfolio_df["CurrentValue"].sum(),
                                    "yday_value": portfolio_df["CurrentValue"].sum()
                                    }
    
    
    combined_positions = pd.DataFrame(columns = ["id", "Ticker", "Quantity", "Entry", "Last", "Previous", "CostBasis",
            "CurrentValue", "YdayValue", "Weight", "Chg1D", "PnL", "Name", "Asset Class" , "Universe", "Factor", "Exposure", "GRID",
            "RV", "RV1D", "RV1W", "RV1M", "Trend", "Trade", "Momo", "BBBot", "BBTop", "BBPos", "VolumeDesc"])
    
    for key in portfolios:
        positions = pd.read_json(portfolios[key]["positions"], orient='split')
        
        for ticker in positions.index.values:
            if ticker in combined_positions.index.values:
                if ticker == "Cash":
                    combined_positions.at[ticker, "Entry"] = combined_positions.at[ticker, "Entry"] + positions.at[ticker, "Entry"]
                    combined_positions.at[ticker, "CostBasis"] = combined_positions.at[ticker, "CostBasis"] + positions.at[ticker, "CostBasis"]
                    combined_positions.at[ticker, "CurrentValue"] = combined_positions.at[ticker, "CurrentValue"] + positions.at[ticker, "CurrentValue"]
                    combined_positions.at[ticker, "YdayValue"] = combined_positions.at[ticker, "YdayValue"] + positions.at[ticker, "YdayValue"]
                    combined_positions.at[ticker, "Last"] += positions.at[ticker, "Last"]
                else:
                    combined_positions.at[ticker, "CostBasis"] = combined_positions.at[ticker, "CostBasis"] + positions.at[ticker, "CostBasis"]
                    combined_positions.at[ticker, "Quantity"] = combined_positions.at[ticker, "Quantity"] + positions.at[ticker, "Quantity"]
                    combined_positions.at[ticker, "Entry"] = combined_positions.at[ticker, "CostBasis"] / combined_positions.at[ticker, "Quantity"]
            else:
                combined_positions.loc[ticker] = [
                    ticker,
                    ticker,
                    positions.at[ticker, "Quantity"],
                    positions.at[ticker, "Entry"],
                    positions.at[ticker, "Last"],
                    positions.at[ticker, "Previous"],
                    positions.at[ticker, "CostBasis"],
                    positions.at[ticker, "CurrentValue"],
                    positions.at[ticker, "YdayValue"],
                    positions.at[ticker, "Weight"],
                    positions.at[ticker, "Chg1D"],
                    positions.at[ticker, "PnL"],
                    positions.at[ticker, "Name"],
                    positions.at[ticker, "Asset Class"],
                    positions.at[ticker, "Universe"],
                    positions.at[ticker, "Factor"],
                    positions.at[ticker, "Exposure"],
                    positions.at[ticker, "GRID"],
                    positions.at[ticker, "RV"],
                    positions.at[ticker, "RV1D"],
                    positions.at[ticker, "RV1W"],
                    positions.at[ticker, "RV1M"],
                    positions.at[ticker, "Trend"],
                    positions.at[ticker, "Trade"],
                    positions.at[ticker, "Momo"],
                    positions.at[ticker, "BBBot"],
                    positions.at[ticker, "BBTop"],
                    positions.at[ticker, "BBPos"],
                    positions.at[ticker, "VolumeDesc"]
                    ]
 
     
    portfolios["Portfolio"] = {"positions": combined_positions.to_json(date_format='iso', orient='split'),
                               "total_value": combined_positions["CurrentValue"].sum(),
                               "yday_value": combined_positions["YdayValue"].sum()
                               }

    return portfolios

def updatePortfolios(portfolios):
    startDate = datetime.datetime.strptime('2021-01-01', '%Y-%m-%d')
    endDate = datetime.datetime.today()
    
    allTickers = []
    portfolio_dfs = {}

    for key in portfolios:
        portfolio_dfs[key] =pd.read_json(portfolios[key]['positions'], orient='split')
        allTickers.extend(x for x in portfolio_dfs[key].index.values if x not in allTickers and x != 'Cash')
    
    
    data = dr.GetTdaDataForTickers(allTickers, 'month', 'daily', 1, startDate, endDate, False, True)
    
    for key in portfolio_dfs:
        portfolio = portfolio_dfs[key]       
        
        for ticker in portfolio.index.values:
            if ticker != 'Cash':
                portfolio.at[ticker, 'Last'] = data[ticker]['close'][-1]
                portfolio.at[ticker, 'CurrentValue'] = portfolio.at[ticker, 'Last'] * portfolio.at[ticker, 'Quantity']
                portfolio.at[ticker, 'YdayValue'] = data[ticker]['close'][-2] * portfolio.at[ticker, 'Quantity']
                portfolio.at[ticker, 'Chg1D'] = (data[ticker]['close'][-1] / data[ticker]['close'][-2]) - 1.0
                portfolio.at[ticker, 'PnL'] = (data[ticker]['close'][-1] / portfolio.at[ticker, 'Entry']) - 1.0
                
                data, portfolio = apply_technicals_to_portfolio(ticker, data, portfolio)
                
    
        total_value = portfolio["CurrentValue"].sum()
        portfolio["Weight"] = portfolio["CurrentValue"] / total_value
    
        portfolios[key] = {"positions": portfolio.to_json(date_format='iso', orient='split'),
                           "total_value": total_value,
                           "yday_value": portfolio["YdayValue"].sum()
                           }
    
    #print(allTickers)
    
    # allTickers = list(ftMacroTickers)

    # benchmarkTickers = ['SPY', 'VTI', 'IEI', 'GSG', 'VEU', 'EEM', 'BND']
    # allTickers.extend(x for x in benchmarkTickers if x not in allTickers)
    
    return portfolios

def apply_technicals_to_portfolio(ticker, data, portfolio):
    data[ticker] = apply_technicals(data[ticker])
    # data[ticker]['RV1D'] = np.log(data[ticker]['RV'] / data[ticker]['RV'].shift(1))
    # data[ticker]['RV1W'] = np.log(data[ticker]['RV'] / data[ticker]['RV'].shift(5))
    # data[ticker]['RV1M'] = np.log(data[ticker]['RV'] / data[ticker]['RV'].shift(21))
       
    portfolio.at[ticker, 'RV'] = data[ticker]['RV'][-1]
    portfolio.at[ticker, 'RV1D'] = data[ticker]['RV'][-2]
    portfolio.at[ticker, 'RV1W'] = data[ticker]['RV'][-6]
    portfolio.at[ticker, 'RV1M'] = data[ticker]['RV'][-22]
    
    portfolio.at[ticker, 'Trend'] = data[ticker]['Trend'][-1]
    portfolio.at[ticker, 'Trade'] = data[ticker]['Trade'][-1]
    portfolio.at[ticker, 'Momo'] = data[ticker]['Momo'][-1]
    portfolio.at[ticker, 'BBBot'] = data[ticker]['BBBot'][-1]
    portfolio.at[ticker, 'BBTop'] = data[ticker]['BBTop'][-1]
    portfolio.at[ticker, 'BBPos'] = data[ticker]['BBPos'][-1]
    portfolio.at[ticker, 'VolumeDesc'] = data[ticker]['VolumeDesc'][-1]
    
    return data, portfolio

def apply_technicals(data):
    data['RV'] = technicals.calcHvZScore(data, 63)
    
    trend, outlook = technicals.getTrend(data, 'low', 'high', 'close', 63)
    data['Trend'] = trend
    
    trade, trade_outlook = technicals.getTrend(data, 'low', 'high', 'close', 21)
    data['Trade'] = trade
    
    data['Momo'] = (data['close'] > data['close'].shift(21)).astype(np.float64)
    
    BridgeBandBottom, BridgeBandTop = technicals.BridgeBands(data, data.close, 15)
    data['BBBot'] = BridgeBandBottom
    data['BBTop'] = BridgeBandTop
    
    data['BBPos'] = (BridgeBandTop - data['close']) / (BridgeBandTop - BridgeBandBottom)
    data.loc[(data['BBPos'] > 1.), 'BBPos'] = 1.0
    data.loc[(data['BBPos'] < 0.), 'BBPos'] = 0.0
    
    data = technicals.calcVolumeMetrics(data)
    
    data.loc[(data['VolumeEnum'] == 0.0) & (data['close'] > data['close'].shift(1)), 'VolumeDesc'] = 'Weak'
    data.loc[(data['VolumeEnum'] == 1.0) & (data['close'] > data['close'].shift(1)), 'VolumeDesc'] = 'Moderate'
    data.loc[(data['VolumeEnum'] == 2.0) & (data['close'] > data['close'].shift(1)), 'VolumeDesc'] = 'Strong'
    data.loc[(data['VolumeEnum'] == 3.0) & (data['close'] > data['close'].shift(1)), 'VolumeDesc'] = 'Absolute'
    
    data.loc[(data['VolumeEnum'] == -0.0) & (data['close'] < data['close'].shift(1)), 'VolumeDesc'] = 'Weak'
    data.loc[(data['VolumeEnum'] == -1.0) & (data['close'] < data['close'].shift(1)), 'VolumeDesc'] = 'Moderate'
    data.loc[(data['VolumeEnum'] == -2.0) & (data['close'] < data['close'].shift(1)), 'VolumeDesc'] = 'Strong'
    data.loc[(data['VolumeEnum'] == -3.0) & (data['close'] < data['close'].shift(1)), 'VolumeDesc'] = 'Absolute'
    
    return data

def get_data_for_ticker(ticker, displayLookback = None):
    startDate = datetime.datetime.strptime('2021-01-01', '%Y-%m-%d')
    endDate = datetime.datetime.today()
    data = dr.GetTdaData(ticker, 'month', 'daily', 1, startDate, endDate, False, True)
    data = apply_technicals(data)
    
    if displayLookback is not None:
        data = data[datetime.date.today() - datetime.timedelta(days=displayLookback):]
    
    return data

def get_single_cmap_value(s, m, M, cmap='seismic', reverse = False, low=0, high=0):
    rng = M - m
    norm = colors.Normalize(m - (rng * low),
                            M + (rng * high))
    normed = norm(s)
    
    the_cmap = plt.cm.get_cmap(cmap).reversed() if reverse else plt.cm.get_cmap(cmap)
    
    c = [colors.rgb2hex(x) for x in the_cmap(normed)]
    
    # print("test")
    # print(s[0], "    ", normed[0], "   ", c[0])
    
    return c

def get_up_volume_color(v):
    
    c = "#000000"
    
    if v == 0.0: c = "#99c2af"
    elif v == 1.0: c = "#66a487"
    elif v == 2.0: c = "#32865e"
    elif v == 3.0: c = "#006837"
    
    return c

def get_cmap_value(s, m, M, cmap='seismic', reverse = False, low=0, high=0):
    rng = M - m
    norm = colors.Normalize(m - (rng * low),
                            M + (rng * high))
    normed = norm(s.values)
    
    the_cmap = plt.cm.get_cmap(cmap).reversed() if reverse else plt.cm.get_cmap(cmap)
    
    c = [colors.rgb2hex(x) for x in the_cmap(normed)]
    return c

def get_column_cmap_values(df, col, m, M, cmap='seismic', reverse = False, low=0, high=0, st_threshold_1 = 1.0, st_threshold_2 = -1.0, white_threshold_1 = 1.0, white_threshold_2 = -1.0):
    styles = []
    color_list = get_cmap_value(df[col], m, M, cmap, reverse, low, high)
    
    i = 0
    for idx in df.index.values:
        if idx != 'Cash':
            styles.append({
                'if': {
                    'filter_query': '{{{col}}} = {val} and {{{col}}} != 0.0001'.format(col = col, val = df.at[idx, col]),
                    'column_id': col
                    },
                    'backgroundColor': color_list[i]
                })
        
        i += 1
     
    styles.append({
        'if': {
            'filter_query': '{{{col}}} <= {st_threshold_1} and {{{col}}} >= {st_threshold_2}'.format(col = col, st_threshold_1 = st_threshold_1, st_threshold_2 = st_threshold_2),
            'column_id': [col]
        },
        'color': '#272727'
    })

    styles.append({
        'if': {
            'filter_query': '{{{col}}} > {white_threshold_1} or {{{col}}} < {white_threshold_2}'.format(col = col, white_threshold_1 = white_threshold_1, white_threshold_2 = white_threshold_2),
            'column_id': [col]
        },
        'color': 'white'
    })
      
    return styles

def initializePortfoliosV1():
    
    startDate = datetime.datetime.strptime('2021-01-01', '%Y-%m-%d')
    endDate = datetime.datetime.today()
    
    universeInfo = pd.read_csv(os.path.join(os.getcwd(), 'data', "UniverseInfo.csv"), index_col="Ticker")
    
    #portfolioPath = os.path.join(os.getcwd(), 'portfolios')
    
    filenames = os.listdir(os.path.join(os.getcwd(), 'portfolios'))  # [] if no file
    
    allTickers = []
    portfolios = {}
    
    for x in filenames:
        #portfolios[Path(x).stem] = pd.read_csv(os.path.join(os.getcwd(), 'portfolios', x), index_col="Ticker")
        temp = pd.read_csv(os.path.join(os.getcwd(), 'portfolios', x), index_col="Ticker")
        
        tickers = []
        quantities = []
        entries = []
        lasts = []
        previouses = []
        costBasii = []
        currentValues = []
        weights = []
        pnls = []
        dailyPnls = []
        names = []
        assetClasses = []
        universes = []
        factors = []
        exposures = []
        grids = []
        
        totalCash = 0.0
        
        if "SDBA Cash" in temp.index.values:
            totalCash += temp.at["SDBA Cash", "Entry"]
        
        if "Cash" in temp.index.values:
            totalCash += temp.at["Cash", "Entry"]
        
        tickers.append("Cash")
        quantities.append(1.0)
        entries.append(totalCash)
        lasts.append(totalCash)
        previouses.append(0.0)
        costBasii.append(0.0)
        currentValues.append(0.0)
        weights.append(0.0)
        pnls.append(0.0)
        dailyPnls.append(0.0)
        names.append("Cash")
        assetClasses.append("Cash")
        universes.append("Cash")
        factors.append("Cash")
        exposures.append("Cash")
        grids.append("Cash")
        
        for i in temp.index.values:
            if i != "SDBA Cash" and i != "Cash":
                tickers.append(i)
                quantities.append(temp.at[i, "Quantity"])
                entries.append(temp.at[i, "Entry"])
                lasts.append(0.0)
                previouses.append(0.0)
                costBasii.append(0.0)
                currentValues.append(0.0)
                weights.append(0.0)
                pnls.append(0.0)
                dailyPnls.append(0.0)
                
                #Ticker, Name, Asset Class,Universe, Factor, Exposure, GRID
                
                if i in universeInfo.index.values:
                    names.append(universeInfo.at[i, "Name"])
                    assetClasses.append(universeInfo.at[i, "Asset Class"])
                    universes.append(universeInfo.at[i, "Universe"])
                    factors.append(universeInfo.at[i, "Factor"])
                    exposures.append(universeInfo.at[i, "Exposure"])
                    grids.append(universeInfo.at[i, "GRID"])
                else:
                    names.append("")
                    assetClasses.append("")
                    universes.append("")
                    factors.append("")
                    exposures.append("")
                    grids.append("")
                
                if i not in allTickers:
                    allTickers.append(i)
        
        data = {
            "Ticker": tickers,
            "Quantity": quantities,
            "Entry": entries,
            "Last": lasts,
            "Previous": previouses,
            "CostBasis": costBasii,
            "CurrentValue": currentValues,
            "Weight": weights,
            "DailyPnL": dailyPnls,
            "PnL": pnls,
            "Name": names,
            "Asset Class": assetClasses,
            "Universe": universes,
            "Factor": factors,
            "Exposure": exposures,
            "GRID": grids
            }   
         
        portfolios[Path(x).stem] = {"positions": pd.DataFrame(data, tickers)}
     
    data = dr.GetTdaDataForTickers(allTickers, 'month', 'daily', 1, startDate, endDate, False, True)
     
    for port in portfolios:
        portfolios[port]["Total Value"] = 0.0
        portfolios[port]["Cash"] = portfolios[port]["positions"].at["Cash", "Entry"]
        
        for pos_idx in portfolios[port]["positions"].index:
            if pos_idx == "Cash":
                portfolios[port]["Total Value"] += portfolios[port]["positions"].at[pos_idx, "Entry"]
                portfolios[port]["positions"].at[pos_idx, "CostBasis"] = portfolios[port]["positions"].at[pos_idx, "Entry"]
                portfolios[port]["positions"].at[pos_idx, "CurrentValue"] = portfolios[port]["positions"].at[pos_idx, "Entry"]
            else:
                portfolios[port]["positions"].at[pos_idx, "Previous"] = portfolios[port]["positions"].at[pos_idx, "Last"]
                portfolios[port]["positions"].at[pos_idx, "Last"] = data[pos_idx].at[data[pos_idx].index[-1], "close"]
                portfolios[port]["positions"].at[pos_idx, "CostBasis"] = portfolios[port]["positions"].at[pos_idx, "Quantity"] * portfolios[port]["positions"].at[pos_idx, "Entry"]    
                portfolios[port]["positions"].at[pos_idx, "CurrentValue"] = portfolios[port]["positions"].at[pos_idx, "Quantity"] * portfolios[port]["positions"].at[pos_idx, "Last"]
                portfolios[port]["Total Value"] += portfolios[port]["positions"].at[pos_idx, "CurrentValue"]           
              
        portfolios[port]["Cash"] = round(portfolios[port]["Cash"], 2)
        portfolios[port]["Total Value"] = round(portfolios[port]["Total Value"], 2)
            
        for pos_idx in portfolios[port]["positions"].index:
            portfolios[port]["positions"].at[pos_idx, "Weight"] = portfolios[port]["positions"].at[pos_idx, "CurrentValue"] / portfolios[port]["Total Value"]
            portfolios[port]["positions"].at[pos_idx, "PnL"] = (portfolios[port]["positions"].at[pos_idx, "CurrentValue"] - portfolios[port]["positions"].at[pos_idx, "CostBasis"]) / portfolios[port]["positions"].at[pos_idx, "CurrentValue"]
            
            if pos_idx == "Cash":
                portfolios[port]["positions"].at[pos_idx, "DailyPnL"] = 0.0
            else:
                portfolios[port]["positions"].at[pos_idx, "DailyPnL"] = (data[pos_idx].at[data[pos_idx].index[-1], "close"] - data[pos_idx].at[data[pos_idx].index[-2], "close"]) / data[pos_idx].at[data[pos_idx].index[-2], "close"]
        
        # portfolios[port]["positions"]["Ticker"]= portfolios[port]["positions"]["Ticker"].astype(str)
        # portfolios[port]["positions"]["Name"]= portfolios[port]["positions"]["Name"].astype(str)
        # portfolios[port]["positions"]["Asset Class"]= portfolios[port]["positions"]["Asset Class"].astype(str)
        # portfolios[port]["positions"]["Universe"]= portfolios[port]["positions"]["Universe"].astype(str)
        # portfolios[port]["positions"]["Factor"]= portfolios[port]["positions"]["Factor"].astype(str)
        # portfolios[port]["positions"]["Exposure"]= portfolios[port]["positions"]["Exposure"].astype(str)
        # portfolios[port]["positions"]["GRID"]= portfolios[port]["positions"]["GRID"].astype(str)
        
        portfolios[port]["positions"] = portfolios[port]["positions"].round(4)
    
        # print(portfolios[port]["positions"].dtypes)
    
    #.to_json(date_format='iso', orient='split')
    
    return {
        "tickers": allTickers,
        "portfolios": portfolios,
        #"data": data
        }

#t = initializePortfolios()
#t = updatePortfolios(t)