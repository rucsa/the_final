# -*- coding: utf-8 -*-
"""
Created on Tue May 29 17:16:04 2018

@author: RuxandraV
"""
import math
import pandas as pd
import eval_portfolio_utils as calculate
from pandas import ExcelWriter
import os


#read data
stocks_2016 = pd.read_hdf("../ml_advisor/data/fundamentals_2016_with_feat_msci_regions_encoded.hdf5", "dataset1/x")
stocks_2017 = pd.read_hdf("../ml_advisor/data/fundamentals_2017_with_feat_msci_regions_encoded.hdf5", "dataset1/x")

#input portfolio
#portfolio_filename = "portfolios_ml/fundamental/ml_fundamental_portfolio_kmeans_3.hdf5"
portfolio_filename = "portfolios_ml/correlations/ml_correlations_portfolio_agg_1.hdf5"
portfolio = pd.read_hdf(portfolio_filename, "dataset1/x")

benchmark = pd.read_hdf("../data/sources/benchmark_returns_2017.hdf5", "dataset1/x")['S&P500']


#output excel 
filename = 'ml_correlations_portfolio_agg_1.xlsx'
filepath = 'result_tables/'


#config
p_returns = {}
p_sharpe = {}
p_info = {}
var_m, st_dev = calculate.stats_market(2016)
n = len(portfolio)
w = 0.05

#Portfolio variance # do for 2017
variance = calculate.portfolio_variance(stocks_2016, portfolio, w, n, var_m)
print('portfolio variance: %.08f' % variance)
p_returns['Portfolio Variance'] = variance


#After 1 month 
#   returns
returns = 0
for i in range(0, n):
    stock1 = stocks_2017.loc[stocks_2017['Name'] == portfolio[i]]
    if not math.isnan(stock1['Returns_1m'].values[0]):
        returns = returns + w * stock1['Returns_1m'].values[0]
print ('returns after 1 month: {}'.format(returns))
p_returns['After 1 month'] = returns

#   sharpe
portfolio_stdev = math.sqrt(variance) # per period
risk_free_return = 1.113 / 100
sharpe = ( returns - risk_free_return ) / portfolio_stdev

sharp = 0
for i in range(0, n):
    stock1 = stocks_2017.loc[stocks_2017['Name'] == portfolio[i]]
    if not math.isnan(stock1['Sharpe_1m'].values[0]):
        sharp = sharp + stock1['Sharpe_1m'].values[0]

#   info


#After 3 months 
returns = 0
for i in range(0, n):
    stock1 = stocks_2017.loc[stocks_2017['Name'] == portfolio[i]]
    if not math.isnan(stock1['Returns_3m'].values[0]):
        returns = returns + w * stock1['Returns_3m'].values[0]
print ('returns after 3 months: {}'.format(returns))
p_returns['After 3 months'] = returns

#   sharpe
portfolio_stdev = math.sqrt(variance) # per period

#   info

#After 6 months 
returns = 0
for i in range(0, n):
    stock1 = stocks_2017.loc[stocks_2017['Name'] == portfolio[i]]
    if not math.isnan(stock1['Returns_3m'].values[0]):
        returns = returns + w * stock1['Returns_3m'].values[0]
print ('returns after 6 months: {}'.format(returns))
p_returns['After 6 months'] = returns

#   sharpe
portfolio_stdev = math.sqrt(variance) # per period

#   info

#After 12 months
returns = 0
for i in range(0, n):
    stock1 = stocks_2017.loc[stocks_2017['Name'] == portfolio[i]]
    if not math.isnan(stock1['Returns_12m'].values[0]):
        returns = returns + w * stock1['Returns_12m'].values[0]
print ('returns after 12 months: {}'.format(returns))
p_returns['After 1 year'] = returns

#   sharpe
portfolio_stdev = math.sqrt(variance) # per period

#   info



''' Print to excel '''

# create df with full portfolio
df_portfolio = pd.DataFrame()
for i in range(0, len(portfolio)):
    stock = stocks_2016[stocks_2016.Name == portfolio[i]]
    df_portfolio = df_portfolio.append(stock)
    
# include results
results = pd.Series(results, name = 'Results')

# send to excel
n = 0
writer = pd.ExcelWriter(os.path.join(filepath, filename))
for item in [df_portfolio, results]:
    item.to_excel(writer, "Sheet1", startcol=0, startrow=n)
    n += len(item.index) + 2
writer.save()

#del filename, filepath, i, item, n, portfolio, returns, st_dev, stock, stock1, var_m
#del variance, w


