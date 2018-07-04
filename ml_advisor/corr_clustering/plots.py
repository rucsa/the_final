#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 18:48:34 2018

@author: rucsa
"""

from sklearn import manifold, datasets
import numpy as np 

import matplotlib.pyplot as plt

LABEL_COLOR_MAP = {0: '#92dbcc',
                   1: '#93d6af',
                   2: '#9fc4dd',
                   3: '#c09ace',
                   4: '#8e9dad',
                   5: '#16A086',
                   6: '#27AE61',
                   7: '#2A80B9',
                   8: '#8F44AD',
                   9: '#2D3E50',
                   10:'#F1C40F',
                   11:'#E77E23',
                   12:'#e27d73',
                   13:'#ECF0F1',
                   14:'#95A5A5',
                   15:'#F39C11',
                   16:'#D25400',
                   17:'#C1392B',
                   18:'#BEC3C7',
                   19:'#7E8C8D',
                   20:'#FF69B4',
                   21:'#CD5C5C',
                   22:'#ADD8E6',
                   23:'#4B0082',
                   24:'#FFFFF0',
                   25:'#F0E68C',
                   26:'#E6E6FA'
                   }

def plot(Y,clusters):

    #data = pd.read_hdf("hdfs/distance_matrix.hdf5", "dataset1/x")
    #data = data.multiply(1)
    
    #clusters = clusters.reset_index().drop('index', axis = 1).values[:,0]
    label_color = np.array([[LABEL_COLOR_MAP[l]] for l in clusters])
    
    #t0 = time()
    #mds = manifold.MDS(2, max_iter=100, n_init=1, dissimilarity = "precomputed")
    #Y = mds.fit_transform(data)
    #t1 = time()
    
    #Y = np.array([mlh.cart_to_pole(x, y) for x, y in Y])
    
    #print("MDS: %.2g sec" % (t1 - t0))
    fig, ax = plt.subplots()
    for i in range(0, len(Y)):
        plt.scatter(Y[i][0], Y[i][1], c=label_color[i], alpha = 0.3, label = clusters[i])
    #plt.title("MDS (%.2g sec)" % (t1 - t0))
    #ax.xaxis.set_major_formatter(NullFormatter())
    #ax.yaxis.set_major_formatter(NullFormatter())
    plt.axis('tight')
    
    return plt
    