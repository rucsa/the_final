# -*- coding: utf-8 -*-
"""
Created on Tue May 29 10:47:21 2018

@author: RuxandraV
"""

from random import randint
import recommender as recom
from pyfancy import pyfancy
import pandas as pd

import time

class ClientPortfolio(object):
    portfolio = {}
    client = {}
    exposures = {}
    cash = 0
    
    def __init__(self, security_list, client_series):
        self.portfolio = {}
        self.client = {}
        for i in range(0, len(security_list)-1, 2):
            if security_list[i] != 'nan':
                self.portfolio[security_list[i]] = security_list[i+1]
        self.client = client_series.to_dict()  
        self.cash = 100 - sum(self.portfolio.values())
        
    def portfolio_region_allocation(self, port_dict, allSecurities):
        current_region_allocation = {}
        for k, v in port_dict.items():
            current_security = allSecurities[k]['Region']
            if current_security in current_region_allocation:
                current_region_allocation[current_security] +=v
            else:
                current_region_allocation[current_security] = v
        return current_region_allocation
    
    def portfolio_sector_allocation(self, port_dict, allSecurities):
        current_sector_allocation = {}
        for k, v in port_dict.items():
            current_security = allSecurities[k]['Sector']
            if current_security in current_sector_allocation:
                current_sector_allocation[current_security] +=v
            else:
                current_sector_allocation[current_security] = v
        return current_sector_allocation
    
    def available_region_allocation(self, port_alloc, recomm_alloc, allSecurities):
        alloc = {}
        for k, v in recomm_alloc.items():
            if k in port_alloc:
                alloc[k] = recomm_alloc[k] - port_alloc[k]
            else:
                alloc[k] = recomm_alloc[k]
        return alloc
    
    def available_sector_allocation(self, port_alloc, recomm_alloc, allSecurities):
        for k, v in recomm_alloc.items():
            if k in port_alloc:
                port_alloc[k] = recomm_alloc[k] - port_alloc[k]
            else:
                port_alloc[k] = recomm_alloc[k]
        return port_alloc
        
    def cutExposureOnCriterion (self, new_exposure, region, all_preferences, allSecurities, criterion = 'Sector'):
        region_dict = self.extract_securities_by_criterion(region, allSecurities, criterion)
        current_exposure = sum(region_dict.values())
        diff = current_exposure - new_exposure
        while (diff > 0):
            pop = recom.reverse_recommend_stock(all_preferences) 
            security = next(pop)
            while (not self.security_exists_in_portfolio(region_dict, security)):
                security = next(pop)
            if (diff >= region_dict[security]):
                diff = diff - region_dict[security]
                self.deleteSecurity(security, allSecurities)
                region_dict.pop(security, None)
            else:
                self.setExposure(security, region_dict[security] - diff)
                region_dict[security] = region_dict[security] - diff
                diff = 0
        return True
    
    def extract_securities_by_criterion(self, sector, allSecurities, criterion = 'Sector'):
        try:
            portfolio_sector_dict = {}
            for key, value in self.portfolio.items():
                current_security = allSecurities[key]
                if current_security[criterion] == sector:
                    portfolio_sector_dict[key] = value
            return portfolio_sector_dict
        except:
            import pdb
            pdb.set_trace()
        #            import pickle
        #            pickle.dump(sector, filename)
            raise
        
    def security_exists_in_portfolio (self, portfolio, security):
        for item in portfolio:
            if item == security:
                return True
        return False
        
    def deleteSecurity(self, security, allSecurities):
        exposure = self.portfolio.pop(security, None)
        print ("Deleted stock {} that had {} exposure \n".format(security, exposure))
        self.cash = self.cash + exposure
        print ("You now have in CASH : {} % exposure".format(self.cash))
        return self.portfolio
    
    def setExposure(self, security, new_exposure):
        print ("Modified exposure for security {} from {} % to {} % \n".format(security, self.portfolio[security], new_exposure))
        self.cash = self.cash + self.portfolio[security] - new_exposure
        self.portfolio[security] = new_exposure
        print ("You now have in CASH : {} % exposure".format(self.cash))
        return self.portfolio[security]
        
    def pretty_print_portfolio(self, allSecurities):
        #regions = ['South Asia', 'Europe & Central Asia', 'Middle East & North Africa', 'East Asia & Pacific', 'Latin America & Caribbean', 'North America', 'Sub-Saharan Africa']
        regions = ['USA', 'Emerging Markets', 'Canada', 'Others', 'Europe ex UK', 'UK', 'Japan', 'Asia ex Japan']
        sectors = ['Industrials', 'Financials', 'Technology', 'Consumer Discretionary', 
                   'Consumer Staples', 'Materials', 'Communications',
                   'Utilities', 'Energy']
        
        print ("SECTOR ......... REGION .......... SECURITY ..... EXPOSURE")
        for k, v in self.portfolio.items():
            current_security = allSecurities[k]
            print ("{} .. {} ..... {} .. {} %".format(current_security['Sector'], current_security['Region'], k, v))
        print ("{} ..... {} %".format('CASH', self.cash))    
        
        print ("\nRegion allocation: ")
        for region in regions:
            region_dict = self.extract_securities_by_criterion(region, allSecurities, 'Region')
            print ("{} ... {}".format(region, sum(region_dict.values())))
        
        print ("\nSector allocation: ")
        for sector in sectors:
            sect_dict = self.extract_securities_by_criterion(sector, allSecurities, 'Sector')
            print ("{} ... {}".format(sector, sum(sect_dict.values())))
        
    def pretty_print_client(self):
        for k,v in self.client.items():
            print ('{} ..... {}'.format(k,v))
           
    def addNewSecurity(self, security, shares, allSecurities):
        self.portfolio[security] = shares
        pyfancy.pyfancy().bold().yellow("Added to portfolio {} from sector {} and region {} with {} exposure \n".format(security, allSecurities[security]['Sector'], allSecurities[security]['Region'], shares)).output()    
        self.cash = self.cash - shares
        print ("You now have in CASH : {} % exposure".format(self.cash))
        return self.portfolio
        
    def addStocks_constraints (self, sector, available_regions, preferences, allSecurities):
        #available_regions = [item[0] for item in available_regions]
        pref_sect, pref_fit = [], []
        for j in range(0, len(preferences)):
            if allSecurities[preferences[j]]['Sector'] == sector:
                pref_sect.append(preferences[j])
        if len(pref_sect) == 0:
            raise EOFError ('Empty list')
        else:
            for j in range(0, len(pref_sect)): 
                if allSecurities[pref_sect[j]]['Region'] in [*available_regions]:
                    pref_fit.append(pref_sect[j])
#                if 'Japan' in available_regions:
#                    if allSecurities[pref_sect[j]]['Region'] == 'Japan':
#                        pref_fit.append(pref_sect[j])
#                    elif 'Asia ex Japan' in available_regions:
#                        if allSecurities[pref_sect[j]]['Region'] == 'Asia ex Japan':
#                            pref_fit.append(pref_sect[j])
#                        elif allSecurities[pref_sect[j]]['Region'] in available_regions:
#                            pref_fit.append(pref_sect[j])
        # sort with japan and asia first
        return pref_fit
    
    def dict_to_df(self, port_dict, columns, X):
        held = pd.DataFrame(columns = columns)
        for k, v in port_dict.items():
            current_security = X.loc[k].to_frame(name = X.loc[k].name).T
            current_security['Shares'] = v
            held = pd.concat([held, current_security], axis = 0)
        return held
    
    
    
    
    
    
    
    def addBondsToBalance(self, security_dict, bonds_alloc, recommended_bonds_alloc, bonds_preferences, exposure = True, exposure_threshold = 5):
        pop = recom.recommend_etf(bonds_preferences)  
        while (bonds_alloc < recommended_bonds_alloc):
            security = next(pop)
            print ('Checking if bond {} exists in portfolio'.format(security))
            while self.security_exists_in_portfolio(self.portfolio, security):
                print ('Bond {} exists in portfolio'.format(security))
                security = next(pop)
                print ('Checking if bond {} exists in portfolio'.format(security))
            if (exposure):
                fit_exposure = min(exposure_threshold, (recommended_bonds_alloc - bonds_alloc))  
            else:
                fit_exposure = recommended_bonds_alloc - bonds_alloc
            self.addNewSecurity(security, fit_exposure, security_dict)
            bonds_alloc += fit_exposure 
            
    def removeBondsToBalance(self, security_dict, bonds_alloc, recommended_bonds_alloc, bonds_preferences, exposure = True):
        pop = recom.reversed_recommend_etf(bonds_preferences) 
        while (bonds_alloc > recommended_bonds_alloc):
            security = next(pop)
            while (not self.security_exists_in_portfolio(self.portfolio, security)):
                security = next(pop)
            security_exposure = self.portfolio[security]
            fit_exposure = min (security_exposure, bonds_alloc - recommended_bonds_alloc)
            if (fit_exposure <= security_exposure): 
                self.deleteSecurity(security, security_dict)
                bonds_alloc -= security_exposure
            elif (fit_exposure < security_exposure):
                self.setExposure(security, security_exposure - fit_exposure)
                bonds_alloc -= fit_exposure        
    
    def addStocksToBalance(self, security_dict, stocks_alloc, recommended_stock_alloc, recommendations, exposure = True, exposure_threshold = 5):
        pop = recom.recommend_stock(recommendations)      
        while (stocks_alloc < recommended_stock_alloc):
            security = next(pop)
            print ('Checking if stock {} exists in portfolio'.format(security))
            while self.security_exists_in_portfolio(self.portfolio, security):
                print ('Stock {} exists in portfolio'.format(security))
                security = next(pop)
                print ('Checking if stock {} exists in portfolio'.format(security))
            if (exposure):
                fit_exposure = min(exposure_threshold, (recommended_stock_alloc - stocks_alloc))
            else:
                fit_exposure = recommended_stock_alloc - stocks_alloc
            self.addNewSecurity(security, fit_exposure, security_dict)
            stocks_alloc += fit_exposure
    
    def removeStocksToBalance(self, security_dict, stocks_alloc, recommended_stock_alloc, recommendations, exposure = True):   
        pop = recom.reverse_recommend_stock(recommendations) 
        while (stocks_alloc > recommended_stock_alloc):
            security = next(pop)
            while (not self.security_exists_in_portfolio(self.portfolio, security)):
                security = next(pop)
            security_exposure = self.portfolio[security]
            fit_exposure = min (security_exposure, stocks_alloc - recommended_stock_alloc)
            if (fit_exposure >= security_exposure): 
                # delete dictionary entry
                self.deleteSecurity(security, security_dict)
                stocks_alloc -= security_exposure
            elif (fit_exposure < security_exposure):
                # delete some of the shares
                self.setExposure(security, security_exposure - fit_exposure)
                stocks_alloc -= fit_exposure
                
   

    def filter_list_by_criterion(self, alist, region, allSecurities, criterion = 'Sector'):
        new_list = []
        for item in alist:
            if allSecurities[item][criterion] == region:
                new_list.append(item)
        return new_list
    
    def filter_list_by_sector(self, alist, region, allSecurities):
        new_list = []
        for item in alist:
            if allSecurities[item]['Sector'] == region:
                new_list.append(item)
        return new_list
    
    def add_security_with_criterion(self, shares, region, preferences, allSecurities, criterion = 'Sector'):
        preferences = self.filter_list_by_criterion(preferences, region, allSecurities, criterion)
        # give error if list is empty
        pop = recom.recommend_stock(preferences)   
        security = next(pop)
        ok = True
        while self.security_exists_in_portfolio(self.portfolio, security):
            try:
                security = next(pop)
            except StopIteration:
                pyfancy.pyfancy().red("Cound not find a new security in {} {}".format(criterion, region)).output()
                ok = False
                break 
        if ok:
            self.addNewSecurity(security, shares, allSecurities)
            return True
        else:
            return False
        
    
    def deleteCriterion(self, sector, security_dict, criterion = 'Sector'):
        pyfancy.pyfancy().cyan("Scanning portfolio to delete securities from sector {}".format(sector)).output()
        time.sleep(1)
        securities_to_del = []
        for key, value in self.portfolio.items():
            current_security = security_dict[key]
            if current_security[criterion] == sector:
                securities_to_del.append(key)
        for key in securities_to_del:
            self.deleteSecurity(key, security_dict)
        print ('Deleted {} {}'.format(criterion, sector))
        
    def add_to_portfolio_as_preferences(self, allSecurities, stock_preferences, bond_preferences):
        print ("Checking your cash...")
        if (self.cash > 0):
            stocks_alloc, bonds_alloc = self.current_asset_allocation(allSecurities)
            recommended_stock_alloc, recommended_bonds_alloc = self.recommended_asset_allocation(self.client['Risk_profile'])
            print ("You have {} % exposure in cash \n".format(self.cash))
            if (stocks_alloc < recommended_stock_alloc):
                pyfancy.pyfancy().cyan("You don't have as many stocks as recommended, let's buy some \n").output()
                self.addStocksToBalance(allSecurities, stocks_alloc, recommended_stock_alloc, stock_preferences, True)
            if (bonds_alloc < recommended_bonds_alloc):
                pyfancy.pyfancy().cyan("You don't have as many bonds as recommended, let's buy some \n").output()
                self.addBondsToBalance(allSecurities, bonds_alloc, recommended_bonds_alloc, bond_preferences, True)
    
    def extract_item_with_most_exposure(self, portfolio):
        sort_exposures_desc = []
        for key, value in sorted(portfolio.items(), key=lambda x:x[1], reverse = True):
            sort_exposures_desc.append(key)
        return sort_exposures_desc
    
    def remove_one_item(self, recommendations, asset_type, allSecurities):
        stocks_alloc, bonds_alloc = self.current_asset_allocation(allSecurities)
        if (asset_type == 'Equity' or asset_type == 'equity' or asset_type == 'stock'):
            if stocks_alloc == 0:
                print ("You have no stocks to delete")
            else:
                pop = recom.reverse_recommend_stock(recommendations) 
                security = next(pop)    
                while not self.security_exists_in_portfolio(self.portfolio, security):
                    security = next(pop)
                self.deleteSecurity(security, allSecurities)
                print ("You now have {} % exposure in CASH.".format(self.extra_exposure))
        elif (asset_type == 'Bond' or asset_type == 'bond'):
            if bonds_alloc == 0:
                print ("You have no bonds to delete")
            else:
                pop = recom.reverse_recommend_stock(recommendations)    
                security = next(pop)    
                while not self.security_exists_in_portfolio(self.portfolio, security):
                    security = next(pop)
                self.deleteSecurity(security, allSecurities)
                print ("You now have {} % exposure in CASH.".format(self.extra_exposure))
                
    def add_one_item (self, preferences, exposure, allSecurities):
        pop = recom.recommend_stock(preferences)     
        security = next(pop)
        while self.security_exists_in_portfolio(self.portfolio, security):
            # stock exists, look for another one
            security = next(pop)
        self.addNewSecurity(security, exposure, allSecurities)
        return True
    

