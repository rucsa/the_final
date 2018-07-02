#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 24 12:04:21 2018

@author: rucsa
"""
from time import time
import pandas as pd
import numpy as np
from sklearn import manifold, datasets

import plots as visual
import ml_helper as mlh
import distance_matrix_functions as bang

from sklearn.cluster import AgglomerativeClustering, AffinityPropagation, DBSCAN, SpectralClustering

distance_matrix = pd.read_hdf("hdfs/distance_matrix.hdf5", "dataset1/x")

# transform distance matrix in coordinates
mds = manifold.MDS(2, max_iter=100, n_init=1, dissimilarity = "precomputed")
Y = mds.fit_transform(distance_matrix)

#Y = np.array([mlh.cart_to_pole(x, y) for x, y in Y])

clusters = []
for i in range(0, len(Y)):
    clusters.append(4)
clusters = pd.DataFrame(clusters)

n_clusters = 6

spectral = SpectralClustering(n_clusters = n_clusters, affinity = 'nearest_neighbors') #‘nearest_neighbors’,‘rbf’
affinity = AffinityPropagation(affinity='euclidean')
dbscan = DBSCAN(metric = "euclidean") # clusters get to be -1
aggl = AgglomerativeClustering(n_clusters=n_clusters, linkage="ward", affinity="precomputed")

models = [spectral, affinity, dbscan, aggl]

model = aggl 
model.fit(Y) # compare spectral and aggl 

companies = distance_matrix.columns.tolist()
clusters = model.labels_

''' Visualize clusters '''
plt = visual.plot(Y, clusters)
plt.show()

