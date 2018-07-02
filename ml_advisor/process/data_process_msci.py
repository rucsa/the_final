# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 16:03:34 2018

@author: RuxandraV
"""
import pandas as pd
import data_process_msci_defs as help


fundamentals_2016 = pd.read_hdf('../../data/sources/fundamentals_2016_with_feat_msci_regions.hdf5', 'dataset1/x')
fundamentals_2017 = pd.read_hdf('../../data/sources/fundamentals_2017_with_feat_msci_regions.hdf5', 'dataset1/x')

economy = 'Mid'

''' encode sector '''
sectors, allocs = help.bc_sector(economy)

# 2016
s_2016 = fundamentals_2016['Sector']
sector_encoding = {}
for key, val in s_2016.items():
    sector_encoding[key] = allocs[sectors.index(val)]
fundamentals_2016['Sector_encoded'] = pd.Series(sector_encoding, name = 'Sector_encoded')

# 2017
s_2017 = fundamentals_2017['Sector']
sector_encoding = {}
for key, val in s_2017.items():
    sector_encoding[key] = allocs[sectors.index(val)]
fundamentals_2017['Sector_encoded'] = pd.Series(sector_encoding, name = 'Sector_encoded')

del s_2016, s_2017, key, val, sector_encoding, allocs, sectors

''' encode region '''
regions = ['USA', 'Emerging Markets', 'Canada', 'Others', 'Europe ex UK', 'UK', 'Japan', 'Asia ex Japan']
alloc = [10, 2, 4, 1, 9, 5, 6, 7]

# 2016
r_2016 = fundamentals_2016['Region']
region_encoding = {}
for key, val in r_2016.items():
    region_encoding[key] = alloc[regions.index(val)]
fundamentals_2016['Region_encoded'] = pd.Series(region_encoding, name = 'Region_encoded')

# 2017
r_2017 = fundamentals_2017['Region']
region_encoding = {}
for key, val in r_2017.items():
    region_encoding[key] = alloc[regions.index(val)]
fundamentals_2017['Region_encoded'] = pd.Series(region_encoding, name = 'Region_encoded')

del key, val, alloc, r_2016, r_2017, region_encoding, regions


fundamentals_2016.to_hdf('../data/fundamentals_2016_with_feat_msci_regions_encoded.hdf5', 'dataset1/x')
fundamentals_2017.to_hdf('../data/fundamentals_2017_with_feat_msci_regions_encoded.hdf5', 'dataset1/x')