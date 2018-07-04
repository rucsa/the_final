# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 15:45:40 2018

@author: RuxandraV
"""

import pandas as pd
import datetime as datetime
import numpy as np
import check_data_and_prices_helpers as help

def check_data_and_prices():
    
    fundamentals_2016 = pd.read_hdf("../sources/data_ANR_2016_msci_regions.hdf5")
    fundamentals_2017 = pd.read_hdf("../sources/data_ANR_2017_msci_regions.hdf5")
    
    print ("Uploaded from: ../sources/data_ANR_201*_msci_regions.hdf5 ")
    
    st_2016 = datetime.datetime(2016, 7, 12, 0, 0)
    en_2016 = datetime.datetime(2016, 12, 30, 0, 0)
    prices_2016 = pd.read_hdf("../sources/Prices_nasdaq_allmydata_total_data.hdf5")[st_2016:en_2016].dropna(axis = 1, how = 'any')
    
    
    st_2017 = datetime.datetime(2017, 7, 11, 0, 0)
    en_2017 = datetime.datetime(2017, 12, 30, 0, 0)
    prices_2017 = pd.read_hdf("../sources/Prices_nasdaq_allmydata_total_data.hdf5")[st_2017:en_2017].dropna(axis = 1, how = 'any')
    
    print ("Uploaded from: ../sources/Prices_nasdaq_allmydata_total_data.hdf5 ")
    
    ''' Filter only complete info tickers ''' # you are putting them back somewhere
    tickers_2016 = prices_2016.columns.tolist()
    tickers_2017 = prices_2017.columns.tolist()
    common_tickers = list(set(tickers_2016).intersection(tickers_2017))
    common_tickers.remove('CTX')
    
    # match tickers 
    prices_2016 = prices_2016[common_tickers]
    prices_2017 = prices_2017[common_tickers]
    fundamentals_2016 = fundamentals_2016.T[common_tickers].T.sort_index()
    fundamentals_2017 = fundamentals_2017.T[common_tickers].T.sort_index()
    
    fundamentals_2016 = help.parse_str_to_number(fundamentals_2016)
    fundamentals_2017 = help.parse_str_to_number(fundamentals_2017)
    
    # take out tickers with no shares
    #fundamentals_2016, fundamentals_2017 = help.remove_nan_shares(fundamentals_2016, fundamentals_2017)
    
#    ''' Add nasdaq prices to prices df '''
#    nasdaq_prices = pd.read_hdf("../sources/nasdaq_prices.hdf5", "dataset1/x")
#    nasdaq_prices = nasdaq_prices.reindex(index=nasdaq_prices.index[::-1]).reset_index(drop=True) # reverse time order
#    # parse date column from string to date
#    nq_dates = nasdaq_prices['Date']
#    nasdaq_prices = nasdaq_prices.drop('Date', axis = 1)
#    nasdaq_prices['Date'] = help.parse_date(nq_dates)
#    # parse prices from string to numbers
#    for col in ['Open', 'Close', 'Low', 'High']:
#        nasdaq_prices[col] = nasdaq_prices[col].str.replace(',','')
#        nasdaq_prices[col] = nasdaq_prices[col].astype(float)
#    fundamentals_2016 = help.parse_str_to_number(fundamentals_2016)
#    fundamentals_2017 = help.parse_str_to_number(fundamentals_2017)
#    #select only relevant info
#    nasdaq_prices = nasdaq_prices.set_index('Date')
#    nasdaq_prices = nasdaq_prices['Close']
#    # select time period
#    nasdaq_prices_2016 = nasdaq_prices[st_2016:en_2016].rename('NQUSB')
#    nasdaq_prices_2017 = nasdaq_prices[st_2017:en_2017].rename('NQUSB')
#    del nasdaq_prices, nq_dates
    
    ''' Add S&P500 prices to prices df '''
    # 2016
    sp_2016 = pd.read_csv("../sources/prices_SP500_2016.csv")[['Date', 'Adj Close']].rename(columns = {'Adj Close':'S&P500'})
    rf_date = sp_2016.Date
    sp_2016 = sp_2016.drop('Date', axis = 1)
    sp_2016['Date'] = help.parse_date(rf_date)
    sp_2016 = sp_2016.set_index('Date')
    sp_2016 = sp_2016[st_2016:en_2016]
    # 2017
    sp_2017 = pd.read_csv("../sources/prices_SP500_2017.csv")[['Date', 'Adj Close']].rename(columns = {'Adj Close':'S&P500'})
    rf_date = sp_2017.Date
    sp_2017 = sp_2017.drop('Date', axis = 1)
    sp_2017['Date'] = help.parse_date(rf_date)
    sp_2017 = sp_2017.set_index('Date')
    sp_2017 = sp_2017[st_2017:en_2017]
    
    del rf_date
    
    ''' Add treasury bills prices '''
    risk_free_2016 = pd.read_csv("../sources/risk_free_return_IRX_2016.csv")[['Date', 'Adj Close']].rename(columns = {'Adj Close':'IRX'})
    rf_date = risk_free_2016.Date
    risk_free_2016 = risk_free_2016.drop('Date', axis = 1)
    risk_free_2016['Date'] = help.parse_date(rf_date)
    risk_free_2016 = risk_free_2016.set_index('Date')
    risk_free_2016 = risk_free_2016[st_2016:en_2016]
    
    risk_free_2017 = pd.read_csv("../sources/risk_free_return_IRX_2017.csv")[['Date', 'Adj Close']].rename(columns = {'Adj Close':'IRX'})
    rf_date = risk_free_2017.Date
    risk_free_2017 = risk_free_2017.drop('Date', axis = 1)
    risk_free_2017['Date'] = help.parse_date(rf_date)
    del rf_date
    risk_free_2017 = risk_free_2017.set_index('Date')
    risk_free_2017 = risk_free_2017[st_2017:en_2017]
    
    # concatenate and fill missing data
    price_result_2016 = pd.concat([prices_2016, sp_2016, risk_free_2016], axis = 1).interpolate()
    price_result_2017 = pd.concat([prices_2017, sp_2017, risk_free_2017], axis = 1).interpolate()
    del prices_2016, sp_2016, prices_2017, sp_2017, risk_free_2016, risk_free_2017
    
    # put date back to columns
    price_result_2016 = price_result_2016.reset_index()
    price_result_2017 = price_result_2017.reset_index()
    
    ''' Calculate days for 2016 and 2017 ''' 
    days_2016 = len(price_result_2016)
    days_2017 = len(price_result_2017)
    
    
    fundamentals_2016.to_hdf("../sources/fundamentals_2016_msci_regions.hdf5", "dataset1/x")
    fundamentals_2017.to_hdf("../sources/fundamentals_2017_msci_regions.hdf5", "dataset1/x")
    print ("---- Downloaded to: ../sources/fundamentals_201*_msci_regions.hdf5")
    
    price_result_2016.to_hdf("../sources/prices_2016.hdf5", "dataset1/x")
    price_result_2017.to_hdf("../sources/prices_2017.hdf5", "dataset1/x")
    print ("---- Downloaded to: ../sources/prices_201*.hdf5")
    return True
