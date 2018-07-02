#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 14:27:37 2018

@author: rucsa
"""

import pandas as pd
from random import choice
from sklearn.preprocessing import MinMaxScaler
from rank_by_preferences import rank_by_preferences

from sklearn.cluster import KMeans
import plots as visual

import main_helper as bang

n_clusters = 20
preferences = [1, 2, 3, 4, 5, 6, 7]
economy = 'Mid'

stocks = pd.read_hdf("../data/fundamentals_2016_with_feat_msci_regions_encoded.hdf5", "dataset1/x")
features = ['Sector_encoded', 'Region_encoded']
companies = stocks['Name'].values.tolist()

data = stocks[features]

# normalize
scaler = MinMaxScaler(feature_range = (0, 1))
scaled_data = scaler.fit_transform(data)

# cluster
model = KMeans(n_clusters=n_clusters, random_state=0).fit(scaled_data)
clusters = model.labels_

''' Visualize clusters '''
plt = visual.plot(scaled_data, clusters)
plt.show()

groups = bang.group_clusters(clusters, companies)

''' sharpe portfolio ''' # picks stock with highest sharpe ratio
portfolio = []
for i in range(0, len(groups)):
    max_sh, idx = 0, 0
    for j in range (0, len(groups[i])):
        if stocks.iloc[groups[i][j]].Sharpe_Ratio > max_sh:
            max_sh = stocks.iloc[groups[i][j]].Sharpe_Ratio
            idx = groups[i][j]
    portfolio.append(stocks.iloc[idx].Name)
pd.Series(portfolio, name = 'Stocks').to_hdf("../../evaluation/portfolios_ml/fundamental/ml_fundamental_portfolio_kmeans_1.hdf5", "dataset1/x")
    
''' random portfolio '''
portfolio = []
for i in range(0, len(groups)):
    j = choice(groups[i])
    portfolio.append(stocks.iloc[j].Name)
pd.Series(portfolio, name = 'Stocks').to_hdf("../../evaluation/portfolios_ml/fundamental/ml_fundamental_portfolio_kmeans_2.hdf5", "dataset1/x")

''' preferences portfolio '''
portfolio = []
for i in range(0, len(groups)):
    grouped_stocks = pd.DataFrame()
    for j in range (0, len(groups[i])):
        row = stocks.iloc[groups[i][j]]
        grouped_stocks = grouped_stocks.append(row)
    ranking = rank_by_preferences(preferences, grouped_stocks, economy, False)
    portfolio.append(ranking.iloc[0].Name)
pd.Series(portfolio, name = 'Stocks').to_hdf("../../evaluation/portfolios_ml/fundamental/ml_fundamental_portfolio_kmeans_3.hdf5", "dataset1/x")
    
''' similarity portfolio '''
