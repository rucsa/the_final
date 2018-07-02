# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 14:49:05 2018

@author: RuxandraV
"""

import pandas as pd
import numpy as np

import distance_matrix_functions as bang

# take out 1 invalid stock!!!!!!!!!!!!!!!!!!!

stocks = pd.read_hdf("../data/fundamentals_2016_with_feat_msci_regions.hdf5", "dataset1/x").reset_index()

# NORMALIZE !!

mapping = stocks['Company']
betas = stocks['Beta'].values
volatility = stocks['volatility_120d'].values

''' Calculate var of market '''
sp_var, sp_stdev = bang.stats_market(2016)

''' Calculate distance '''
distance_matrix = np.array(bang.distance_matrix(betas, volatility, sp_var))
distance_matrix  = distance_matrix * 100000

#''' Scale '''
#distance_matrix = distance_matrix * 100000


''' Save files ''' 
df = pd.DataFrame(distance_matrix, columns = stocks["Company"].values)
df.to_hdf("hdfs/distance_matrix.hdf5", "dataset1/x")

