# -*- coding: utf-8 -*-
"""
Created on Wed May 30 13:50:14 2018

@author: RuxandraV
"""
import pandas as pd
import math

def covariance(stock1, stock2, var_market):
    beta1 = stock1['Beta'].values[0]
    beta2 = stock2['Beta'].values[0]
    return beta1 * beta2 * var_market

def portfolio_variance(stocks, portfolio, w, n, var_m):
    variance = 0
    # first part of formula
    for i in range(0, n):
        stock1 = stocks.loc[stocks['Name'] == portfolio[i]]
        variance = variance + (w ** 2 * stock1['volatility_120d'].values[0] ** 2)
    # second part of formula
    for i in range (0, n-1):
        for j in range (i, n):
            if (i != j):
                stock1 = stocks.loc[stocks['Name'] == portfolio[i]]
                stock2 = stocks.loc[stocks['Name'] == portfolio[j]]
                variance = variance + (2 * (w ** 2) * covariance(stock1, stock2, var_m))
    return variance
            

def stats_market(year):
    import numpy as np
    prices = pd.read_hdf("../data/prices_" + str(year) + ".hdf5", "dataset1/x")['S&P500'].values
    intra_returns = []
    for i in range(1, len(prices)):
        intra_returns.append(prices[i] / prices[i-1] - 1) 
    variance = np.mean([(x - np.mean(intra_returns)) * (x - np.mean(intra_returns)) for x in intra_returns])
    st_dev = math.sqrt(variance)
    return variance, st_dev



#def financial_correlation(stock1, stock2):
#    cov = covariance(stock1, stock2, 13.16)
#    vol1 = round(all_data.loc[stock1]['Volatility_90'], 3)
#    vol2 = round(all_data.loc[stock2]['Volatility_90'], 3)
#    return cov / vol1 * vol2
#
#def cov_matrix(port_arr, var_m):
#    df = pd.DataFrame(columns = port_arr)
#    for i in range (0, len(port_arr)):
#        row = []
#        for j in range (0, len(port_arr)):
#            row.append(covariance(port_arr[i], port_arr[j], var_m))
#        df.loc[port_arr[i]] = row
#    return df
#
#def variance(stock, var_m):
#    beta = round(all_data.loc[stock]['Adjusted_beta'], 3)
#    return round(beta * beta* var_m, 3)
#
#def portfolio_variance(port_dict, var_m):
#    cov_port = 0
#    stocks = [*port_dict]
#    weigths = list(port_dict.values())
#    for i in range (0, len(stocks)):
#        for j in range (0, len(stocks)):
#            cov_port = cov_port + (weigths[i] * weigths[j] * covariance(stocks[i], stocks[j], var_m))
#    return round(math.sqrt(cov_port), 2)
#
#def portfolio_volatility(port_dict, var_m):
#    stocks = [*port_dict]
#    weigths = list(port_dict.values())
#    p_vol = 0
#    for i in range (0, len(stocks)):
#        p_vol = p_vol + weigths[i] * weigths[i] * variance(stocks[i], var_m)
#    for i in range(0, len(stocks)):
#        for j in range(i+1, len(stocks)):
#            p_vol = p_vol + 2 * weigths[i] * weigths[j] * covariance(stocks[i], stocks[j], var_m)
#    return round(math.sqrt(p_vol), 2)
#
#def portfolio_returns(port_dict):
#    ret = 0
#    for k, v in port_dict.items():
#        r = round(all_data.loc[k]['Return_last_year'], 3)
#        ret = ret + v * r
#    return ret





#portfolio = [(k, v[0]) for k, v in portfolio.items()]
#port_variance = 0
#as_vol = []
#for i in range(0, len(portfolio)):
#    port_variance = port_variance + (portfolio[i][1]/100 * portfolio[i][1]/100 * allSecurities[portfolio[i][0]]['Volatility_30'] * allSecurities[portfolio[i][0]]['Volatility_30'])
#    as_vol.append(allSecurities[portfolio[i][0]]['Volatility_30'])
#for i in range(0, len(portfolio)-1):
#    for j in range(i+1, len(portfolio)):
#        w1 = portfolio[i][1]
#        w2 = portfolio[j][1]
#        port_variance = port_variance + 2 * portfolio[i][1] /100 * portfolio[j][1]/100 * covariance(portfolio[i][0], portfolio[j][0], var_m)
#
#print (port_variance)