# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 14:49:05 2018

@author: RuxandraV
"""

import pandas as pd
import numpy as np

import distance_matrix_functions as bang

# take out 1 invalid stock!!!!!!!!!!!!!!!!!!!

stocks = pd.read_hdf("../data/fundamentals_2016_with_feat_msci_regions_encoded.hdf5", "dataset1/x").reset_index()
company = stocks[['Symbol', 'Name']]
to_add = {}
for i in range(0, len(company)):
    to_add[i] = str(str(company.iloc[i].Symbol) + " " + str(company.iloc[i].Name))
stocks = pd.concat([pd.Series(to_add, name = "Company"), stocks], axis = 1)


# NORMALIZE !!

mapping = stocks['Company']
betas = stocks['Beta'].values
volatility = stocks['volatility_120d'].values

''' Calculate var of market '''
sp_var, sp_stdev = bang.stats_market(2016)

''' Calculate distance '''
distance_matrix = np.array(bang.distance_matrix(betas, volatility, sp_var))
a = np.array(distance_matrix)
b = np.where(a==distance_matrix.min())
i = b[0][0]
j = b[1][0]

''' Scale '''
distance_matrix = distance_matrix * 100000


''' Save files ''' 
df = pd.DataFrame(distance_matrix, columns = stocks["Company"].values)
df.to_hdf("hdfs/distance_matrix.hdf5", "dataset1/x")

