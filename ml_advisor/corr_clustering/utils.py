 # -*- coding: utf-8 -*-
"""
Created on Tue May 29 10:58:24 2018

@author: RuxandraV
"""
import operator
from pyfancy import pyfancy

def normalize_value(value, minimum, maximum, x = 1, y = 100):
    return ((value-minimum) / (maximum-minimum)) * (y - x) + x

def score_feature(df, score, feature):
    col = df[feature].values.flatten()
    minimum = min(col)
    maximum = max(col)
    for row in df.itertuples():
        n = getattr(row, "Index") 
        a = getattr(row, feature) 
        if n not in score:
            score[n] = []
        score[n].append(normalize_value(a, minimum, maximum))
    return score

def rank_scores(d):
    rank = {}
    for key, value in d.items():
        rank[key] = sum(value)
    return rank
    
def sort_scores(rank):
    return sorted(rank.items(), key=operator.itemgetter(1), reverse=True)

def check_bc(economy):
    if (economy == 'Mid'):
        return ['Technology', 'Communications', 'Consumer Staples']
    elif (economy == 'Late'):
        return ['Financials',  'Energy', 'Basic Materials']
    elif (economy == 'Recession'):
        return ['Utilities',  'Consumer Discretionary']
    elif (economy == 'Early'):
        return ['Industrials']
    
    
def score_sectors(df, criterion, score):
    if (type(criterion)==list):
        for row in df.itertuples():
             s = getattr(row, "Sector")
             n = getattr(row, "Index") 
             if n not in score:
                 score[n] = []
             if s in criterion:
                 score[n].append(100)
             else:
                 score[n].append(0)
    return score

def make_dict_from_lists (key_list, value_list):
    if len(key_list) != len(value_list):
        return pyfancy.pyfancy().red("Warning! Trying to converd 2 lists of different lengths into a dict.").output()
    else:
        resulting_dict = {}
        for i in range (0, len(key_list)):
            resulting_dict[key_list[i]] = value_list[i]
        return resulting_dict
    
def filter_country (possible_stocks, allSecurities, regions):
    asian = []
    for j in range(0, len(possible_stocks)):
        if allSecurities[possible_stocks[j]]['Region'] in regions:
            asian.append((possible_stocks[j], j))
    return asian
