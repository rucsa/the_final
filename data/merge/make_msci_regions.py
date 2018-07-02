#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 17:42:03 2018

@author: rucsa
"""

import pandas as pd
import numpy as np

def add_msci_regions():

    fundamentals_2016 = pd.read_hdf("../sources/data_ANR_2016.hdf5").sort_index()
    fundamentals_2017 = pd.read_hdf("../sources/data_ANR_2017.hdf5").sort_index()
    
    sectors = fundamentals_2016.Sector.value_counts()
    regions = fundamentals_2016.Region.value_counts()
    countries = fundamentals_2016.Country.value_counts()
    
    ''' Load country income '''
    
    bank_classif = pd.read_excel("../sources/bank_class_income.xlsx")
    
    
    ''' Country to MSCI World Sector mapping'''
    EuropeExUK = ['AUSTRIA', 'BELGIUM', 'SWITZERLAND', 'CZECH REPUBLIC', 'GERMANY', 'DENMARK',
                  'SPAIN', 'FINLAND', 'FRANCE', 'UNITED KINGDOM', 'GREECE', 'HUNGARY', 
                  'IRELAND', 'ITALY', 'NETHERLANDS', 'NORWAY', 'POLAND', 'PORTUGAL', 'RUSSIA', 
                  'SWEDEN', 'TURKEY']
    
    USA = ['USA', 'United States']
    Japan = ['Japan']
    Canada = ['Canada']
    Uk = ['Uk', 'UK', 'United Kingdom', 'England', 'United Kingdom(England)']
    EmergingMarkets = ['UNITED ARAB EMIRATES', 'BRAZIL', 'CHILE', 'CHINA', 'COLOMBIA', 'CZECH REPUBLIC',
                       'EGYPT', 'GREECE', 'HUNGARY', 'INDONESIA', 'INDIA', 'KOREA', 'MEXICO', 'MALAYSIA',
                       'PERU', 'PHILIPPINES', 'PAKISTAN', 'POLAND', 'QATAR', 'RUSSIA', 'THAILAND', 'TURKEY', 
                       'TAIWAN', 'SOUTH AFRICA']
    AsiaExJapan = ['CHINA', 'HONG KONG', 'INDONESIA', 'INDIA', 'JAPAN', 'KOREA', 'MALAYSIA', 
                   'PHILIPPINES', 'PAKISTAN', 'SINGAPORE', 'THAILAND', 'TAIWAN']
    EmergingMarkets = [item.title() for item in EmergingMarkets]
    AsiaExJapan = [item.title() for item in AsiaExJapan]
    Uk = [item.title() for item in Uk]
    EuropeExUK = [item.title() for item in EuropeExUK]
    
    
    countries = fundamentals_2016.Country
    new_regions = {}
    for k, v in countries.items():
        if v in USA:
            new_regions[k] = 'USA'
        elif v in Japan:
            new_regions[k] = 'Japan'
        elif v in Canada:
            new_regions[k] = 'Canada'
        elif v in Uk:
            new_regions[k] = 'UK'
        elif v in EmergingMarkets:
            new_regions[k] = 'Emerging Markets'
        elif v in AsiaExJapan:
            new_regions[k] = 'Asia ex Japan'
        elif v in EuropeExUK:
            new_regions[k] = 'Europe ex UK'
        else:
            new_regions[k] = 'Others'
        
    new_regions = pd.Series(new_regions, name = 'Region')
    fundamentals_2016 = fundamentals_2016.drop('Region', axis = 1)
    fundamentals_2016['Region'] = new_regions
    
    countries = fundamentals_2017.Country
    new_regions = {}
    for k, v in countries.items():
        if v in USA:
            new_regions[k] = 'USA'
        elif v in Japan:
            new_regions[k] = 'Japan'
        elif v in Canada:
            new_regions[k] = 'Canada'
        elif v in Uk:
            new_regions[k] = 'UK'
        elif v in EmergingMarkets:
            new_regions[k] = 'Emerging Markets'
        elif v in AsiaExJapan:
            new_regions[k] = 'Asia ex Japan'
        elif v in EuropeExUK:
            new_regions[k] = 'Europe ex UK'
        else:
            new_regions[k] = 'Others'
        
    new_regions = pd.Series(new_regions, name = 'Region')
    fundamentals_2017 = fundamentals_2017.drop('Region', axis = 1)
    fundamentals_2017['Region'] = new_regions
    
    fundamentals_2016.to_hdf('../sources/data_ANR_2016_msci_regions.hdf5', 'dataset1/x')
    fundamentals_2017.to_hdf('../sources/data_ANR_2017_msci_regions.hdf5', 'dataset1/x')
    
    return True