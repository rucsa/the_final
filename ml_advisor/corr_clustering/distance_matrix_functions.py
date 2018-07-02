#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 23 21:25:48 2018

@author: rucsa
"""
import math
import pandas as pd
import numpy as np

def stats_market(year):
    prices = pd.read_hdf("../data/prices_" + str(year) + ".hdf5", "dataset1/x")['S&P500'].values
    intra_returns = []
    for i in range(1, len(prices)):
        intra_returns.append(prices[i] / prices[i-1] - 1) 
    variance = np.mean([(x - np.mean(intra_returns)) * (x - np.mean(intra_returns)) for x in intra_returns])
    st_dev = math.sqrt(variance)
    return variance, st_dev

def pearson_corr(beta_i, beta_j, var_m, vol_i, vol_j):
    return (beta_i * beta_j * var_m) / vol_i * vol_j

def distance_matrix(betas, volatility, sp_var):
    n = len(betas)
    distance_matrix = [[math.nan for x in range(n)] for y in range(n)] 
    for i in range (0, n):
       for j in range (0, n):   
           # calculate pearson correlator
           pearson_correlation = pearson_corr(betas[i], betas[j], sp_var, volatility[i], volatility[j])
           distance_matrix[i][j] = math.sqrt(2 - pearson_correlation)
    return distance_matrix

