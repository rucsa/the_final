#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 14:27:37 2018

@author: rucsa
"""

import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from sklearn.cluster import KMeans
import plots as visual

import main_helper as bang

stocks = pd.read_hdf("../data/fundamentals_2016_with_feat_msci_regions_encoded.hdf5", "dataset1/x")
features = ['Sector_encoded', 'Region_encoded']
companies = stocks['Company'].values.tolist()

data = stocks[features]

# normalize
scaler = MinMaxScaler(feature_range = (0, 1))
scaled_data = scaler.fit_transform(data)

# cluster
model = KMeans(n_clusters=20, random_state=0).fit(scaled_data)
clusters = model.labels_

''' Visualize clusters '''
plt = visual.plot(scaled_data, clusters)
plt.show()

groups = bang.group_clusters(clusters, companies)

''' Create portfolio ''' # picks first stock from each cluster
portfolio = []
for i in range(0, len(groups)):
    stock_index = groups[i][2]
    portfolio.append((companies[stock_index]))

pd.Series(portfolio, name = 'Stocks').to_hdf("../../evaluation/portfolios_ml/fundamental/ml_fundamental_portfolio_3.hdf5", "dataset1/x")

    
