# -*- coding: utf-8 -*-
"""
Created on Tue May 29 10:46:48 2018

@author: RuxandraV
"""

from pyfancy import pyfancy
import time
import pandas as pd
from random import randint, choice

from ClientPortfolio import ClientPortfolio
from rank_by_preferences import rank_by_preferences, select_preferences
from refine_alloc_with_regions import refine_alloc_with_regions

allSecurities = pd.read_hdf("../data/fundamentals_2016_with_feat_msci_regions.hdf5", "dataset1/x").reset_index().set_index('Company').T.to_dict()
allsecurities = pd.read_hdf("../data/fundamentals_2016_with_feat_msci_regions.hdf5", "dataset1/x").reset_index().set_index('Company')

investors = pd.read_hdf('../data_process/hdfs/clients.hdf5', 'DatatasetCli').set_index('Id')
portfolios = pd.read_hdf('../data_process/hdfs/portfolios.hdf5', 'DatatasetPort')

client_id = randint(1, 99)
client = investors.iloc[client_id]
client_portfolio = ClientPortfolio(portfolios.iloc[client['Portfolio_Id']].tolist(), client)

setTimer = False


print ("Hello!...")
if setTimer:
    time.sleep(1)
    
print ("Welcome to BestAdvisor!")
if setTimer:
    time.sleep(1)
    
print ("I'm Best and I'm going to help you invest your money wisely ...")
if setTimer:
    time.sleep(1)
    
print ("And you are...?")
pyfancy.pyfancy().cyan("Randomly generating investor...").output()
if setTimer:
    time.sleep(1)
    
print ("{}! Nice to meet you!".format(client["Name"]))
print ("Client ID: {}".format(client_id))
if setTimer:
    time.sleep(1)
    
print ("I see that you are {} years old..".format(client["Age"]))
if setTimer:
    time.sleep(1)
    
print ("... you want to retire at {} and your goal is to have {} euros by then".format(client["Retirement"], client["Goal"])) 
if setTimer:
    time.sleep(1)
    
print ("... your initial capital is {} and your risk profile is {}".format(client["Capital"], client["Risk_profile"]))
if setTimer:
    time.sleep(1)
    
print ("... so we have {} years to gain {} euros".format(client["Timeline"], client["Goal"] - client["Capital"]))
if setTimer:
    time.sleep(2)
    
print ("How nice! Now let's see what you have gathered in your investement portfolio...")
pyfancy.pyfancy().cyan("Randomly generating investment portfolio...").output()
if setTimer:
    time.sleep(2)
    
pyfancy.pyfancy().cyan("Portfolio successfully generated").output()
if setTimer:
    time.sleep(1)
        
pyfancy.pyfancy().cyan("Generating random economy...").output()
economy= 'Mid'
#economy = choice(['Mid', 'Late', 'Recession', 'Early'])
if setTimer:
    time.sleep(1)
print ('We are using cycle {} for economy'.format(economy))

options = [0, 1, 2, 3, 4]
compliments = ["Briliant!", "Well done!", "Excellent!", "Magnificent!", "You're investements are growing!"]
user_in = 'start'

all_preferences = rank_by_preferences([1, 2, 3, 4, 5, 6, 7], allsecurities, economy, False).index.values.tolist()

preferences_default = True

while (user_in != 'exit'):
    print ("\n")
    print (choice(compliments))
    print ("What would you like to do next?..\n")
    print ("1 -  Visualize portfolio")
    print ("2 -  Visualize client")
    print ("3 -  Set / reset preferences")
    print ("4 -  Fill portfolio")
    print ("5 -  Save portfolio")
    print ("0 - Exit")
    
    user_in = [int(x) for x in input('Insert your options.. ').split()]
    for val in user_in:
        if (val < 0 or val > 5):
            print ('Inserted value unknown.. Try again.. ')
            user_in = [int(x) for x in input('Insert your options.. ').split()]
            
    if (0 in user_in):
        user_in = 'exit'
        pyfancy.pyfancy().bold().cyan("GOODBYE!").output()
        break
    
    if (1 in user_in):
        client_portfolio.pretty_print_portfolio(allSecurities)
        
    if (2 in user_in):
        pyfancy.pyfancy().cyan("Current client: \n").output()
        client_portfolio.pretty_print_client()
        
    if (3 in user_in):
        u_in = select_preferences()
        preferences_default = False
        all_preferences = rank_by_preferences(u_in, allsecurities, economy).index.values.tolist()
        
    if (4 in user_in):
        refine_alloc_with_regions(client_portfolio, allSecurities, all_preferences, economy)
        
    if (5 in user_in):
        result = pd.DataFrame.from_dict(client_portfolio.portfolio, orient='index', dtype=None)  
        result.columns = ['Shares']
        result.to_hdf('../evaluation/benchmark/compl_algorithmic_portfolio_mid_' + str(client_id) + '.hdf5', 'Dataset1/X', format = 'table')
        
        


        