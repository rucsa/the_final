# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 12:10:43 2018

@author: RuxandraV
"""
import pandas as pd

def refresh_data():
    if True:
        f_2016 = pd.read_excel("../sources/data_ANR_2016.xlsx").set_index('Symbol')
        f_2017 = pd.read_excel("../sources/data_ANR_2017.xlsx").set_index('Symbol')
        f_2016.to_hdf("../sources/data_ANR_2016.hdf5", "dataset1/x")
        f_2017.to_hdf("../sources/data_ANR_2017.hdf5", "dataset1/x")
    
    
    if True:
        df = pd.read_excel("../sources/nasdaq_prices.xlsx")
        df.to_hdf("../sources/nasdaq_prices.hdf5", "dataset1/x")
        
    return True