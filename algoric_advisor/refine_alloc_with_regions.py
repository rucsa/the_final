import recommender as recom
import utils as ut
from random import randint
import pandas as pd
from ClientPortfolio import ClientPortfolio

import operator

def refine_alloc_with_regions (client_portfolio, allSecurities, all_preferences, economy):
    
    regions = ['USA', 'Emerging Markets', 'Canada', 'Others', 'Europe ex UK', 'UK', 'Japan', 'Asia ex Japan']
    regions_alloc = [52, 12, 3, 2, 15, 6, 8, 2]
    sectors, sectors_alloc = recom.bc_sector_allocation(economy)
    
    recomm_region_alloc = ut.make_dict_from_lists(regions, regions_alloc)
    recomm_sector_alloc = ut.make_dict_from_lists(sectors, sectors_alloc)
    
    del regions, regions_alloc, sectors, sectors_alloc
    
    current_region_allocation = client_portfolio.portfolio_region_allocation(client_portfolio.portfolio, allSecurities)
    current_sector_allocation = client_portfolio.portfolio_sector_allocation(client_portfolio.portfolio, allSecurities)
    
    # cut sectors with too much exposure to get some cash
    for key, value in recomm_sector_alloc.items():
        diff = current_sector_allocation.get(key, 0) - recomm_sector_alloc[key]
        if diff > 0:
            client_portfolio.cutExposureOnCriterion(recomm_sector_alloc[key], key, all_preferences, allSecurities, 'Sector')
            
    # cut regions with too much exposure to get some cash
    for key, value in recomm_region_alloc.items():
        diff = current_region_allocation.get(key, 0) - recomm_region_alloc[key]
        if diff > 0:
            client_portfolio.cutExposureOnCriterion(recomm_region_alloc[key], key, all_preferences, allSecurities, 'Region')
    
    current_region_allocation = client_portfolio.portfolio_region_allocation(client_portfolio.portfolio, allSecurities)
    current_sector_allocation = client_portfolio.portfolio_sector_allocation(client_portfolio.portfolio, allSecurities)
    
    sorted_recomm_alloc = sorted(recomm_sector_alloc.items(), key=operator.itemgetter(1))
    # complete allocation
    for key, value in sorted_recomm_alloc:
        print ("Doing sector {}. Left in cash {}".format(key, client_portfolio.cash))
        diff = recomm_sector_alloc[key] - current_sector_allocation.get(key, 0)
        while diff > 0:
            #decide from which sector to add
            current_region_allocation = client_portfolio.portfolio_region_allocation(client_portfolio.portfolio, allSecurities)
            current_sector_allocation = client_portfolio.portfolio_sector_allocation(client_portfolio.portfolio, allSecurities)
            a_regions = client_portfolio.available_region_allocation(current_region_allocation, recomm_region_alloc, allSecurities)
            available_regions = { k : v for k,v in a_regions.items() if v != 0}
            #available_regions = sorted(available_regions.items(), key=operator.itemgetter(1))
            possible_stocks = client_portfolio.addStocks_constraints(key, available_regions, all_preferences, allSecurities)
            found = False
            i = 0
            if a_regions.get("Japan", 0) != 0 or a_regions.get("Asia ex Japan", 0) != 0: #there are still needed stocks in japan
                # filter out japan stocks and take from that
                asian = ut.filter_country(possible_stocks, allSecurities, ['Japan', 'Asia ex Japan'])
                for tup in asian:
                    if tup[1] <= len(possible_stocks)/2 and not found: # the asian stock is in top 50 of preferences - add it
                        recommended_region = allSecurities[tup[0]]['Region']
                        exposure = min(diff, 5, available_regions[recommended_region])
                        if not client_portfolio.security_exists_in_portfolio(client_portfolio.portfolio, tup[0]):
                            if available_regions[recommended_region] >= exposure:
                                client_portfolio.addNewSecurity(tup[0], exposure, allSecurities)
                                diff = diff - exposure
                                found = True
            if not found and (a_regions.get('Europe ex UK', 0) != 0 or a_regions.get('UK', 0) != 0):
                eu = ut.filter_country(possible_stocks, allSecurities, ['Europe ex UK' , 'UK'])
                for tup in eu:
                    if tup[1] <= len(possible_stocks)/2 and not found: # the asian stock is in top 50 of preferences - add it
                        recommended_region = allSecurities[tup[0]]['Region']
                        exposure = min(diff, 5, available_regions[recommended_region])
                        if not client_portfolio.security_exists_in_portfolio(client_portfolio.portfolio, tup[0]):
                            if available_regions[recommended_region] >= exposure:
                                client_portfolio.addNewSecurity(tup[0], exposure, allSecurities)
                                diff = diff - exposure
                                found = True
            if not found:
                while not found and i < len(possible_stocks):
                    recommended_region = allSecurities[possible_stocks[i]]['Region']
                    exposure = min(diff, 5, available_regions[recommended_region])
                    if not client_portfolio.security_exists_in_portfolio(client_portfolio.portfolio, possible_stocks[i]):
                        if available_regions[recommended_region] >= exposure:
                            client_portfolio.addNewSecurity(possible_stocks[i], exposure, allSecurities)
                            diff = diff - exposure
                            found = True
                    i = i + 1

    
    return True

