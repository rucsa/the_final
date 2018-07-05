#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 10:06:21 2018

@author: rucsa
"""
import pandas as pd
import datetime
import numpy as np
import tables

import check_data_and_prices_helpers as help

def add_returns():

    #fundamentals_2016 = pd.read_hdf("../sources/fundamentals_2016_msci_regions.hdf5", "dataset1/x")
    fundamentals_2017 = pd.read_hdf("../sources/fundamentals_2017_msci_regions.hdf5", "dataset1/x")
    print ("Uploaded from: ../sources/fundamentals_2017_msci_regions.hdf5 ")
    common_tickers = fundamentals_2017.T.columns.tolist()
    
    st_2017 = datetime.datetime(2017, 1, 3, 0, 0)
    en_2017 = datetime.datetime(2017, 12, 29, 0, 0)
    prices_2017 = pd.read_hdf("../sources/Prices_nasdaq_allmydata_total_data.hdf5")[st_2017:en_2017]#.dropna(axis = 1, how = 'any')
    print ("Uploaded from: ../sources/Prices_nasdaq_allmydata_total_data.hdf5")
    prices_2017 = prices_2017[common_tickers]
    
    # parse IRX prices
    prices_irx = pd.read_csv("../sources/IRX_prices_2017.csv")[['Date', 'Adj Close']].rename(columns = {'Adj Close':'IRX'})
    rf_date = prices_irx.Date
    prices_irx = prices_irx.drop('Date', axis = 1)
    prices_irx['Date'] = help.parse_date(rf_date)
    prices_irx = prices_irx.set_index('Date')
    prices_irx = prices_irx[st_2017:en_2017]
    
    # parse S&P prices
    prices_snp = pd.read_csv("../sources/GSPC_prices_2017.csv")[['Date', 'Adj Close']].rename(columns = {'Adj Close':'S&P500'})
    rf_date = prices_snp.Date
    prices_snp = prices_snp.drop('Date', axis = 1)
    prices_snp['Date'] = help.parse_date(rf_date)
    prices_snp = prices_snp.set_index('Date')
    prices_snp = prices_snp[st_2017:en_2017]
    
    # merge risk free asset + benchmark
    benchmark_2017 = pd.concat([prices_irx, prices_snp], axis = 1)
    benchmark_tickers = benchmark_2017.columns.tolist()
    del prices_irx, prices_snp, rf_date
    
    ''' Returns 1 months after 30 december 2016 '''
    st_2017 = datetime.datetime(2017, 1, 3, 0, 0)
    en_2017 = datetime.datetime(2017, 2, 3, 0, 0)
    
    # returns of tickers
    prices_1m_2017 = pd.read_hdf("../sources/Prices_nasdaq_allmydata_total_data.hdf5").loc[st_2017:en_2017]
    ret_m = pd.Series(help.periodic_returns(common_tickers, prices_1m_2017), name = 'Returns_1m')
    fundamentals_2017['Returns_1m'] = ret_m
    
    # returns of benchmarks
    benchmark_1m = benchmark_2017[st_2017:en_2017]
#    ret_m = pd.Series(help.periodic_returns(benchmark_tickers, benchmark_1m), name = 'Returns_1m')
#    benchmark_2017['Returns_1m'] = ret_m
    
    # volatility 1 month
    vol_1m = help.calculate_volatility_120_days(prices_1m_2017)
    
#    # sharpe 1 month
#    risk_free_return_1m_2017 = 1.113
#    benchmark_returns = np.full((len(prices_1m_2017)-1, ), risk_free_return_1m_2017)
#    sharps = pd.Series(help.sharpe_ratio(prices_1m_2017, benchmark_returns, common_tickers), name = 'Sharpe_1m')
#    fundamentals_2017['Sharpe_1m'] = sharps
#    
#    # info 1 month
#    benchmark_returns = benchmark_1m['S&P500'][:len(benchmark_1m)-1]
#    sharps = pd.Series(help.sharpe_ratio(prices_1m_2017, benchmark_returns, common_tickers), name = 'Info_1m')
#    fundamentals_2017['Info_1m'] = sharps
    
    del prices_1m_2017, benchmark_1m, 
#    del benchmark_returns, sharps, risk_free_return_1m_2017
    
    ''' Returns 3 months after 30 december 2016 '''
    st_2017 = datetime.datetime(2017, 1, 3, 0, 0)
    en_2017 = datetime.datetime(2017, 4, 3, 0, 0)
    
    # returns of tickers
    prices_3m_2017 = pd.read_hdf("../sources/Prices_nasdaq_allmydata_total_data.hdf5")[st_2017:en_2017]#.dropna(axis = 1, how = 'any')
    ret_m = pd.Series(help.periodic_returns(common_tickers, prices_3m_2017), name = 'Returns_3m')
    fundamentals_2017['Returns_3m'] = ret_m
    
    # returns of benchmarks
    benchmark_3m = benchmark_2017[st_2017:en_2017]
#    ret_m = pd.Series(help.periodic_returns(benchmark_tickers, benchmark_3m), name = 'Returns_3m')
#    benchmark_2017['Returns_3m'] = ret_m
    
#    # sharpe 3 months
#    risk_free_return_3m_2017 = 1.263
#    benchmark_returns = np.full((len(prices_3m_2017)-1, ), risk_free_return_3m_2017)
#    sharps = pd.Series(help.sharpe_ratio(prices_3m_2017, benchmark_returns, common_tickers), name = 'Sharpe_1m')
#    fundamentals_2017['Sharpe_3m'] = sharps
#    
#    # info 3 months
#    benchmark_returns = benchmark_3m['S&P500'][:len(benchmark_3m)-1]
#    sharps = pd.Series(help.sharpe_ratio(prices_3m_2017, benchmark_returns, common_tickers), name = 'Info_3m')
#    fundamentals_2017['Info_3m'] = sharps
    
    del prices_3m_2017, benchmark_3m, 
#    del risk_free_return_3m_2017, benchmark_returns, sharps
    
    ''' Returns 6 months after 30 december 2016 '''
    st_2017 = datetime.datetime(2017, 1, 3, 0, 0)
    en_2017 = datetime.datetime(2017, 7, 3, 0, 0)
    
    # returns of tickers
    prices_6m_2017 = pd.read_hdf("../sources/Prices_nasdaq_allmydata_total_data.hdf5")[st_2017:en_2017]#.dropna(axis = 1, how = 'any')
    ret_m = pd.Series(help.periodic_returns(common_tickers, prices_6m_2017), name = 'Returns_6m')
    fundamentals_2017['Returns_6m'] = ret_m
    
    # returns of benchmarks
    benchmark_6m = benchmark_2017[st_2017:en_2017]
#    ret_m = pd.Series(help.periodic_returns(benchmark_tickers, benchmark_6m), name = 'Returns_6m')
#    benchmark_2017['Returns_6m'] = ret_m
    
#    # sharpe 6 months
#    risk_free_return_6m_2017 = 1.475
#    benchmark_returns = np.full((len(prices_6m_2017)-1, ), risk_free_return_6m_2017)
#    sharps = pd.Series(help.sharpe_ratio(prices_6m_2017, benchmark_returns, common_tickers), name = 'Sharpe_1m')
#    fundamentals_2017['Sharpe_6m'] = sharps
#    
#    # info 6 months
#    benchmark_returns = benchmark_6m['S&P500'][:len(benchmark_6m)-1]
#    sharps = pd.Series(help.sharpe_ratio(prices_6m_2017, benchmark_returns, common_tickers), name = 'Info_6m')
#    fundamentals_2017['Info_6m'] = sharps
    
    del prices_6m_2017, benchmark_6m, 
#    del risk_free_return_6m_2017, benchmark_returns, sharps
    
    ''' Returns 12 months after 30 december 2016 '''
    st_2017 = datetime.datetime(2017, 1, 3, 0, 0)
    en_2017 = datetime.datetime(2017, 12, 29, 0, 0)
    
    # returns of tickers
    prices_12m_2017 = pd.read_hdf("../sources/Prices_nasdaq_allmydata_total_data.hdf5")[st_2017:en_2017]#.dropna(axis = 1, how = 'any')
    ret_m = pd.Series(help.periodic_returns(common_tickers, prices_12m_2017), name = 'Returns_12m')
    fundamentals_2017['Returns_12m'] = ret_m
    
    # returns of benchmarks
    benchmark_12m = benchmark_2017[st_2017:en_2017]
#    ret_m = pd.Series(help.periodic_returns(benchmark_tickers, benchmark_12m), name = 'Returns_12m')
#    benchmark_2017['Returns_12m'] = ret_m
    
    # sharpe 12 months
#    risk_free_return_12m_2017 = 1.788
#    benchmark_returns = np.full((len(prices_12m_2017)-1, ), risk_free_return_12m_2017)
#    sharps = pd.Series(help.sharpe_ratio(prices_12m_2017, benchmark_returns, common_tickers), name = 'Sharpe_1m')
#    fundamentals_2017['Sharpe_12m'] = sharps
#    
#    # info 12 months
#    benchmark_returns = benchmark_12m['S&P500'][:len(benchmark_12m)-1]
#    sharps = pd.Series(help.sharpe_ratio(prices_12m_2017, benchmark_returns, common_tickers), name = 'Info_12m')
#    fundamentals_2017['Info_12m'] = sharps
    
    del benchmark_12m, prices_12m_2017
#    del risk_free_return_12m_2017, benchmark_returns, sharps
    
    print("Added 12 new features: returns, sharpe and info ratios for 1m/3m/6m/12m")
    
    fundamentals_2017.to_hdf("../sources/fundamentals_2017_msci_regions.hdf5", "dataset1/x")
    print ("---- Downloaded to: ../sources/fundamentals_2017_msci_regions.hdf5")
    
    benchmark_2017.to_hdf("../sources/benchmark_returns_2017.hdf5", "dataset1/x")
    print ("---- Downloaded to: ../sources/benchmark_returns_2017.hdf5")
    
    benchmark_2017.to_hdf("../../ml_advisor/data/benchmark_returns_2017.hdf5", "dataset1/x")
    print ("---- Downloaded to: ../../ml_advisor/data/benchmark_returns_2017.hdf5")
    
    return True