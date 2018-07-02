# -*- coding: utf-8 -*-
"""
Created on Tue May 29 17:16:04 2018

@author: RuxandraV
"""
import math
import pandas as pd
import eval_portfolio_utils as calculate

stocks_2016 = pd.read_hdf("data/fundamentals_2016_with_feat_msci_regions_encoded.hdf5", "dataset1/x")
stocks_2017 = pd.read_hdf("data/fundamentals_2016_with_feat_msci_regions_encoded.hdf5", "dataset1/x")
portfolio = pd.read_hdf("portfolios_ml/fundamental/ml_fundamental_portfolio_kmeans_3.hdf5", "dataset1/x")

var_m, st_dev = calculate.stats_market(2016)
n = len(portfolio)
w = 0.05

""" Portfolio variance """

variance = calculate.portfolio_variance(stocks_2016, portfolio, w, n, var_m)
print('portfolio variance: %.08f' % variance)

""" Returns after 1 year """ # what do you do with missing values
returns = 0
for i in range(0, n):
    stock1 = stocks_2017.loc[stocks_2017['Name'] == portfolio[i]]
    if not math.isnan(stock1['revenue_YOY'].values[0]):
        returns = returns + w * stock1['revenue_YOY'].values[0]
returns = returns 

print ('returns after 1 year: {}'.format(returns))

''' Sharpe ratio '''

''' Information Ratio '''
    



