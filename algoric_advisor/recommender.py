from pyfancy import pyfancy
import pandas as pd



def recommend_stock (list_):
    yield from list_
    
def reverse_recommend_stock (list_):
    list_ = list(reversed(list_))
    yield from list_

def bc_sector_allocation(economy):
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
        
def recomm_sector_allocation (portfolio_dict, divers_percent, divers_sectors, sum_stocks):
    # assert len(divers_percent) == len(divers_sectors)
    part_list = []
    for j in range(0, min(len(portfolio_dict), len(divers_percent))):
        part_list.append(divers_percent[j]) 
    total_part = sum(part_list)
    percent_list = []
    for j in range(0, len(part_list)):
        percent_list.append(part_list[j]*sum_stocks/total_part)
    recomm_sector_dict = {}
    for i in range(0, len(percent_list)):
        recomm_sector_dict[divers_sectors[i]] = percent_list[i]
    for k, v in recomm_sector_dict.items():
        print("{}      {} %".format(k, v))
    return recomm_sector_dict
