# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 16:11:31 2018

@author: RuxandraV
"""

def bc_sector(economy):
    if economy == 'Mid':
        return ['Consumer Staples', 'Technology', 'Financials',
                  'Industrials', 'Consumer Discretionary', 
                  'Energy', 'Communications', 'Materials',
                  'Utilities'], \
                [24, 19, 17, 15, 9, 6, 5, 3, 2]
    elif economy == 'Late':
        return ['Consumer Staples', 'Financials', 'Industrials', 
                  'Energy', 'Materials', 'Technology',
                  'Consumer Discretionary', 'Utilities', 'Communications'], \
                [24, 19, 17, 15, 9, 6, 5, 3, 2]
    elif economy == 'Recession':
        return ['Consumer Staples', 'Financials', 'Consumer Discretionary', 
                  'Utilities', 'Communications', 'Energy', 
                   'Technology', 'Industrials', 'Materials'], \
                [24, 19, 17, 15, 9, 6, 5, 3, 2]
    elif economy == 'Early':
        return ['Technology', 'Industrials', 'Financials', 
                   'Consumer Discretionary', 'Consumer Staples', 
                  'Materials', 'Energy', 'Utilities', 'Communications'], \
                [24, 19, 17, 15, 9, 6, 5, 3, 2]
    else:
        print ('Incorrect parameter for economy')
        