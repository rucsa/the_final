#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 18:00:28 2018

@author: rucsa
"""
from datetime import datetime
from dateutil import parser
import pandas as pd
import math

import numpy as np

def p_returns(col):
    col = col.values.tolist()
    percent_return = []
    for i in range(1, len(col)):
        percent_return.append((col[i]- col[i-1])/col[i-1] * 100)
    return percent_return


def correct_sectors(df):
    current_sectors = df.Sector
    desired_sector = {}
    for key, value in current_sectors.items():
        if value == 'Finance':
            desired_sector[key] = 'Financials'
        elif value == 'Capital Goods':
            desired_sector[key] = 'Industrials'
        elif value == 'Transportation':
            desired_sector[key] = 'Industrials'
        elif value == 'Technology':
            desired_sector[key] = 'Technology'
        elif value == 'Consumer Services':
            desired_sector[key] = 'Consumer Discretionary'
        elif value == 'Consumer Non-Durables':
            desired_sector[key] = 'Consumer Staples'
        elif value == 'Health Care':
            desired_sector[key] = 'Consumer Staples'
        elif value == 'Basic Industries':
            desired_sector[key] = 'Materials'
        elif value == 'Miscellaneous':
            desired_sector[key] = 'Communications'
        elif value == 'Public Utilities':
            desired_sector[key] = 'Utilities'
        elif value == 'Energy':
            desired_sector[key] = 'Energy'
        elif value == 'Consumer Durables':
            desired_sector[key] = 'Consumer Discretionary'
    return pd.Series(desired_sector, name = 'Sector')
    
    
def parse_date(df_dates):
    df_formatted_dates = []
    for date in df_dates:
        df_formatted_dates.append(parser.parse(date))
    return pd.Series(df_formatted_dates, name = "Date")
        
def parse_str_to_number(df):
    columns = df.columns.tolist()
    for col in columns:
        if col not in ['Name', 'Company', 'Country', 'Sector', 'Industry', 'Region', 'Currency']:
            df[col] = df[col].astype(float)
    return df

def calculate_days(df, ticker):
    current = df[['Date', ticker]]
    return (current['Date'][len(current)-1] - current['Date'][0]).days

def remove_nan_shares(df1, df2):
    tik_2016 = df1[df1['Shares'].isnull()].T.columns.tolist()
    tik_2017 = df2[df2['Shares'].isnull()].T.columns.tolist()
    common_tics = list(set(tik_2016).intersection(tik_2017))
    diff1 = list(set(tik_2016).difference(tik_2017))
    diff2 = list(set(tik_2017).difference(tik_2016))
    df1 = df1.drop([common_tics + diff1 + diff2])
    df2 = df2.drop([common_tics + diff1 + diff2])
    return df1, df2
    
    return 

def calculate_volatility_120_days(df):
    columns = df.columns.tolist()
    vol_dict = {}
    for tic in columns:
        current = df[tic]
        intraday_returns = []
        for i in range(1, len(current)):
            intraday_returns.append(current[i] / current[i-1] - 1) #rate of return
        vol_dict[tic] = np.std(intraday_returns) 
    return vol_dict

def calculate_market_cap(prices_df, fundamentals_df):
    market_cap_dict = {}
    count = 0
    for tik in fundamentals_df.index.tolist():
        price = prices_df[tik][len(prices_df)-1]
        shares = fundamentals_df.T[tik]['Shares']
        try:
            market_cap_dict[tik] = int(round(price * shares * 1000000))
        except ValueError:
            count = count + 1
            market_cap_dict[tik] = math.nan
            #print ("Error iter {}: Ticker {} does not have shares -> market_cap ".format(count, tik))
    market_cap_dict = pd.Series(market_cap_dict, name='market_cap')
    return market_cap_dict

def stdev(df, ticker):
    mark = df[['Date', ticker]][1:] #120 days
    mean = mark[ticker].mean()
    mark['Deviation'] = mark[ticker] - mean
    mark['Deviation Squared'] = mark['Deviation'] * mark['Deviation']
    return math.sqrt(mark['Deviation Squared'].mean())



    

