# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 16:55:21 2018

@author: RuxandraV
"""
import pandas as pd

from refresh_data import refresh_data
from check_data_and_prices import check_data_and_prices
from add_features import add_features
from make_msci_regions import add_msci_regions

if True:
    print()
    refresh_data()
    add_msci_regions()
    check_data_and_prices()
    add_features()

if False:
    fundamentals_2016 = pd.read_hdf("../fundamentals_2016_with_feat_msci_regions.hdf5", "dataset1/x")
    fundamentals_2017 = pd.read_hdf("../fundamentals_2017_with_feat_msci_regions.hdf5", "dataset1/x")
    
    tickers = fundamentals_2016.T.columns.tolist()
    names = fundamentals_2016.Name
    
    thefile = open('../final_tickers.txt', 'w+')
    for tik in tickers:
        thefile.write("{}\n".format(tik))
        
    thefile.close()
    
    #names.to_excel("../final_names.xlsx")
    
