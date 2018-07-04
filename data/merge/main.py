# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 16:55:21 2018

@author: RuxandraV
"""
import pandas as pd

import time

from refresh_data import refresh_data
from check_data_and_prices import check_data_and_prices
from add_features import add_features
from make_msci_regions import add_msci_regions
from calculate_returns2 import add_returns

if True:
    start = time.time()
    print("Started data processing...")
    refresh_data()
    print("Adding MSCI regions...")
    add_msci_regions()
    print("Checking dates and prices...")
    check_data_and_prices()
    print("Calculating returns...")
    add_returns()
    print("Calculating volatility, beta, ratios, market cap...")
    add_features()
    end = time.time()
    print("Done! Task took {} seconds.\n\n".format(end - start))
    
    print("WARN: RUN data_process_msci FROM ml_advisor TO ENCODE regions AND sectors")

    del start, end
if True:
    fundamentals_2016 = pd.read_hdf("../sources/fundamentals_2016_with_feat_msci_regions.hdf5", "dataset1/x")
    fundamentals_2017 = pd.read_hdf("../sources/fundamentals_2017_with_feat_msci_regions.hdf5", "dataset1/x")
    
#    tickers = fundamentals_2016.T.columns.tolist()
#    names = fundamentals_2016.Name
#    
#    thefile = open('../final_tickers.txt', 'w+')
#    for tik in tickers:
#        thefile.write("{}\n".format(tik))
#        
#    thefile.close()
#    
#    #names.to_excel("../final_names.xlsx")
    
