#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 18:48:34 2018

@author: rucsa
"""
import numpy as np 

import matplotlib.pyplot as plt

LABEL_COLOR_MAP = {0: '#FFF0F5',
                   1: '#7CFC00',
                   2: '#FFFACD',
                   3: '#CD5C5C',
                   4: '#FF1493',
                   5: '#00BFFF',
                   6: '#696969',
                   7: '#1E90FF',
                   8: '#B22222',
                   9: '#FFFAF0',
                   10:'#228B22',
                   11:'#FF00FF',
                   12:'#DCDCDC',
                   13:'#F8F8FF',
                   14:'#FFD700',
                   15:'#DAA520',
                   16:'#008B8B',
                   17:'#008000',
                   18:'#ADFF2F',
                   19:'#F0FFF0',
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
    