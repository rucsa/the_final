# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 15:47:02 2018

@author: RuxandraV
"""
import pandas as pd
import numpy as np
import check_data_and_prices_helpers as help

def add_features():
    
    fundamentals_2016 = pd.read_hdf("../sources/fundamentals_2016_msci_regions.hdf5", "dataset1/x")
    fundamentals_2017 = pd.read_hdf("../sources/fundamentals_2017_msci_regions.hdf5", "dataset1/x")
    fundamentals_2016.columns = fundamentals_2016.columns.str.replace(r'\s+', '_')
    fundamentals_2017.columns = fundamentals_2017.columns.str.replace(r'\s+', '_')
    
    price_result_2016 = pd.read_hdf("../sources/prices_2016.hdf5", "dataset1/x")
    price_result_2017 = pd.read_hdf("../sources/prices_2017.hdf5", "dataset1/x")
    
    tickers = fundamentals_2016.T.columns.tolist()
    
    ''' Exchange some fundamentals to USD currency '''
    # 2016
    exchange_rates = pd.read_excel("../sources/exchange_currency_31_12_2016.xlsx")
    columns = ['Currency', 'Revenue', 'Operating_Income', 'Net_Income',
                       'Book_Value_Per_Share', 'Operating_Cash_Flow',
                       'Cap_Spending', 'Free_Cash_Flow',
                       'Working_Capital']
    df = fundamentals_2016[columns] # missing 'EPS' 'Dividents' 'Free Cash Flow per Share'
    
    att_exch = list(columns)
    att_exch.remove('Currency')
    for col in att_exch:
        feat = {}
        for row in df.itertuples():
            f_currency = str(getattr(row, "Currency"))
            rate = exchange_rates[exchange_rates['Currency code'] == f_currency]['USD per Unit'].values[0]
            feat[getattr(row, "Index")] = getattr(row, col) * rate
        df = df.drop(labels = [col], axis = 1)
        new_col = pd.Series(data = feat, name = col)
        df = pd.concat([df, new_col], axis = 1)
    df = df.drop(['Currency'], axis = 1)
    fundamentals_2016 = fundamentals_2016.drop(labels = columns, axis = 1)
    fundamentals_2016 = pd.concat([fundamentals_2016, df], axis = 1)
    
    # 2017
    exchange_rates = pd.read_excel("../sources/exchange_currency_31_12_2017.xlsx")
    columns = ['Currency', 'Revenue', 'Operating_Income', 'Net_Income',
                       'Book_Value_Per_Share', 'Operating_Cash_Flow',
                       'Cap_Spending', 'Free_Cash_Flow',
                       'Working_Capital']
    df = fundamentals_2017[columns] # missing 'EPS' 'Dividents' 'Free Cash Flow per Share'
    
    att_exch = list(columns)
    att_exch.remove('Currency')
    for col in att_exch:
        feat = {}
        for row in df.itertuples():
            f_currency = str(getattr(row, "Currency"))
            rate = exchange_rates[exchange_rates['Currency code'] == f_currency]['USD per Unit'].values[0]
            feat[getattr(row, "Index")] = getattr(row, col) * rate
        df = df.drop(labels = [col], axis = 1)
        new_col = pd.Series(data = feat, name = col)
        df = pd.concat([df, new_col], axis = 1)
    df = df.drop(['Currency'], axis = 1)
    fundamentals_2017 = fundamentals_2017.drop(labels = columns, axis = 1)
    fundamentals_2017 = pd.concat([fundamentals_2017, df], axis = 1)
    
    ''' Correct Sector'''
    # 2016
    desired_sector = help.correct_sectors(fundamentals_2016)
    fundamentals_2016 = fundamentals_2016.drop('Sector', axis = 1)
    fundamentals_2016['Sector'] = desired_sector
    # 2017
    desired_sector = help.correct_sectors(fundamentals_2017)
    fundamentals_2017 = fundamentals_2017.drop('Sector', axis = 1)
    fundamentals_2017['Sector'] = desired_sector
                                
    ''' Calculate volatility 120 days'''
    tickers.append('Date')
    # 2016
    tickers_prices_2016 = price_result_2016[tickers].set_index('Date')
    vol_2016 = pd.Series(help.calculate_volatility_120_days(tickers_prices_2016), name='volatility_120d')
    fundamentals_2016 = pd.concat([fundamentals_2016, vol_2016], axis = 1)
    # 2017
    tickers_prices_2017 = price_result_2017[tickers].set_index('Date')
    vol_2017 = pd.Series(help.calculate_volatility_120_days(tickers_prices_2017), name='volatility_120d')
    fundamentals_2017 = pd.concat([fundamentals_2017, vol_2017], axis = 1)
    
    tickers.remove('Date')
    
    
    ''' Calculate market cap '''
    # tickers that have nan value for shares will have nan for market_cap
    # 34 samples from 2016 and 38 samples from 2017, 30 in common
    m_series_2016 = help.calculate_market_cap(price_result_2016, fundamentals_2016) # 2016
    fundamentals_2016 = pd.concat([fundamentals_2016, m_series_2016], axis = 1)
    m_series_2017 = help.calculate_market_cap(price_result_2017, fundamentals_2017) # 2017
    fundamentals_2017 = pd.concat([fundamentals_2017, m_series_2017], axis = 1)
    
    
    ''' Beta ''' 
    # 2016
    tickers = price_result_2016.columns.tolist()
    tickers.remove("Date")
    tickers.remove("S&P500")
    tickers.remove("IRX")
    benchmark_returns = help.p_returns(price_result_2016['S&P500'])
    betas = {}
    for tik in tickers:
        p_returns_tik = help.p_returns(price_result_2016[tik])
        var_tik = np.var(p_returns_tik)
        cov_tik = np.cov(np.vstack((benchmark_returns, p_returns_tik)).T, rowvar  = False)[0, 1]
        betas[tik] = cov_tik/var_tik
    betas = pd.Series(betas, name = 'Beta')
    fundamentals_2016['Beta'] = betas
    
    #2017
    benchmark_returns = help.p_returns(price_result_2017['S&P500'])
    betas = {}
    for tik in tickers:
        p_returns_tik = help.p_returns(price_result_2017[tik])
        var_tik = np.var(p_returns_tik)
        cov_tik = np.cov(np.vstack((benchmark_returns, p_returns_tik)).T, rowvar  = False)[0, 1]
        betas[tik] = cov_tik/var_tik
    betas = pd.Series(betas, name = 'Beta')
    fundamentals_2017['Beta'] = betas
    
    del betas, benchmark_returns, p_returns_tik, var_tik, cov_tik
    del exchange_rates, f_currency, feat, m_series_2016, m_series_2017, new_col, rate, row, tik, vol_2016, vol_2017, att_exch
    del desired_sector, col, columns, df, tickers_prices_2016, tickers_prices_2017
    
    ''' Sharpe Ratio '''
    risk_free_return_2016 = 1.058 # %
    #benchmark_returns = help.p_returns(price_result_2016['IRX'])
    benchmark_returns = np.full((120, ), risk_free_return_2016)
    sharps = {}
    for tik in tickers:
         p_returns_tik = help.p_returns(price_result_2016[tik])
         excess = np.subtract(p_returns_tik, benchmark_returns).mean()
         dev_ret = np.std(p_returns_tik)
         sharps[tik] = excess/dev_ret
    sharps = pd.Series(sharps, name = 'Sharpe_Ratio')
    fundamentals_2016['Sharpe_Ratio'] = sharps
    del sharps, excess, dev_ret, tik, benchmark_returns, p_returns_tik, risk_free_return_2016
    
    # 2017
    risk_free_return_2017 = 1.475
    #benchmark_returns = help.p_returns(price_result_2017['IRX'])
    benchmark_returns = np.full((120, ), risk_free_return_2017)
    sharps = {}
    for tik in tickers:
         p_returns_tik = help.p_returns(price_result_2017[tik])
         excess = np.subtract(p_returns_tik, benchmark_returns).mean()
         dev_ret = np.std(p_returns_tik)
         sharps[tik] = excess/dev_ret
    sharps = pd.Series(sharps, name = 'Sharpe_Ratio')
    fundamentals_2017['Sharpe_Ratio'] = sharps
    del sharps, excess, dev_ret, tik, benchmark_returns, p_returns_tik, risk_free_return_2017

    
    ''' Information ratio '''
    # 2016
    benchmark_returns = help.p_returns(price_result_2016['S&P500'])
    inf_ratios = {}
    for tik in tickers:
        p_returns_tik = help.p_returns(price_result_2016[tik])
        excess = np.subtract(p_returns_tik, benchmark_returns)
        avg_exc = excess.mean()
        tracking_error = np.std(excess)
        inf_ratios[tik] = avg_exc / tracking_error
    inf_ratios = pd.Series(inf_ratios, name = 'Info_Ratio')
    fundamentals_2016['Info_Ratio'] = inf_ratios
    del avg_exc, benchmark_returns, inf_ratios, p_returns_tik, tik, tracking_error, excess
    
    # 2017
    benchmark_returns = help.p_returns(price_result_2017['S&P500'])
    inf_ratios = {}
    for tik in tickers:
        p_returns_tik = help.p_returns(price_result_2017[tik])
        excess = np.subtract(p_returns_tik, benchmark_returns)
        avg_exc = excess.mean()
        tracking_error = np.std(excess)
        inf_ratios[tik] = avg_exc / tracking_error
    inf_ratios = pd.Series(inf_ratios, name = 'Info_Ratio')
    fundamentals_2017['Info_Ratio'] = inf_ratios
    
    del avg_exc, benchmark_returns, inf_ratios, p_returns_tik, tik, tracking_error, excess
    
    del tickers
    
    ''' Save files '''
    fundamentals_2016.to_hdf("../../ml_advisor/data/fundamentals_2016_with_feat_msci_regions.hdf5", "dataset1/x")
    fundamentals_2017.to_hdf("../../ml_advisor/data/fundamentals_2017_with_feat_msci_regions.hdf5", "dataset1/x")
    
    price_result_2016.to_hdf("../../ml_advisor/data/prices_2016.hdf5", "dataset1/x")
    price_result_2017.to_hdf("../../ml_advisor/data/prices_2017.hdf5", "dataset1/x")
    
    fundamentals_2016.to_hdf("../sources/fundamentals_2016_with_feat_msci_regions.hdf5", "dataset1/x")
    fundamentals_2017.to_hdf("../sources/fundamentals_2017_with_feat_msci_regions.hdf5", "dataset1/x")
    
    price_result_2016.to_hdf("../sources/prices_2016.hdf5", "dataset1/x")
    price_result_2017.to_hdf("../sources/prices_2017.hdf5", "dataset1/x")
    
    return True