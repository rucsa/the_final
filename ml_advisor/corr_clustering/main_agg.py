#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 16:24:02 2018

@author: rucsa
"""
import pandas as pd
import numpy as np
from sklearn import manifold, datasets
from random import choice, randint

import pickle

import plots as visual
import main_helper as badong
import ml_helper as mlh
import distance_matrix_functions as bang

from sklearn.cluster import AgglomerativeClustering, SpectralClustering

distance_matrix = pd.read_hdf("hdfs/distance_matrix.hdf5", "dataset1/x")

# transform distance matrix in coordinates
mds = manifold.MDS(2, max_iter=100, n_init=1, dissimilarity = "precomputed")
Y = mds.fit_transform(distance_matrix)

#Y = np.array([mlh.cart_to_pole(x, y) for x, y in Y])

n_clusters = 7

spectral = SpectralClustering(n_clusters = n_clusters, affinity = 'nearest_neighbors') #‘nearest_neighbors’,‘rbf’
aggl = AgglomerativeClustering(n_clusters=n_clusters, linkage="average", affinity="euclidean")

model = aggl 
model.fit(Y) # compare spectral and aggl 

# save the model to disk
filename = 'finalized_model.sav'
pickle.dump(model, open(filename, 'wb'))

## load the model from disk
#loaded_model = pickle.load(open(filename, 'rb'))
#result = loaded_model.score(X_test, Y_test)
#print(result)

companies = distance_matrix.columns.tolist()
clusters = model.labels_
groups = badong.group_clusters(clusters, companies)

''' Visualize clusters '''
plt = visual.plot(Y, clusters)
plt.show()

''' make portfolio ''' 
stocks = pd.read_hdf("../data/fundamentals_2016_with_feat_msci_regions_encoded.hdf5", "dataset1/x").reset_index()
stocks = pd.concat([pd.Series(clusters, name = 'Cluster'), stocks], axis = 1)

''' center cluster '''
portfolio = []
center_cluster = 3
for i in range(0, 20):
    j = choice(groups.get(4))
    portfolio.append(stocks.iloc[j].Name)
pd.Series(portfolio, name = 'Stocks').to_hdf("../../evaluation/portfolios_ml/correlations/ml_correlations_portfolio_agg_1.hdf5", "dataset1/x")

''' random portfolio '''
portfolio = []
for i in range(0, 20):
    j = choice(groups.get(4))
    portfolio.append(stocks.iloc[j].Name)
pd.Series(portfolio, name = 'Stocks').to_hdf("../../evaluation/portfolios_ml/correlations/ml_correlations_portfolio_agg_2.hdf5", "dataset1/x")



