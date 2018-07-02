import pandas as pd
import utils as ut

def rank_by_preferences(u_in, data, economy, show = True):
    
    score = {}
    criterions = []
    criterions.append('Name')
    desc_df = pd.DataFrame()
    
    ### score anr
    if (1 in u_in):
        score = ut.score_feature(data, score, 'Working_Capital')
        criterions.append('Working_Capital')
        
    if (2 in u_in):
        score = ut.score_feature(data, score, 'Fixed_Assets_Turnover')
        criterions.append('Fixed_Assets_Turnover')
    
    ### score P/E
    if (3 in u_in):
        score = ut.score_feature(data, score, 'Accounts_Receivable')
        criterions.append('Accounts_Receivable')
    
    ### score returns last 3 months
    if (4 in u_in):
        score = ut.score_feature(data, score, 'Revenue')
        criterions.append('Revenue')
        
    if (5 in u_in):
        score = ut.score_feature(data, score, 'revenue_3Y_Avg')
        criterions.append('revenue_3Y_Avg')
    
    if (6 in u_in):
        score = ut.score_feature(data, score, 'Free_Cash_Flow_Per_Share')
        criterions.append('Free_Cash_Flow_Per_Share')
     
    ### score sectors from BC   
    if (7 in u_in):
        sectors = ut.check_bc(economy)
        score = ut.score_sectors(data, sectors, score)
        criterions.append('Sector')
            
    ### determine ranking
    rank = ut.rank_scores(score)
    
    ### make df
    reasoning = pd.DataFrame(list(rank.items()), columns=['Name', 'Score'])
    reasoning = reasoning.set_index('Name')
    desc_df = data[criterions]
    #desc_df = desc_df.set_index('Symbol')
    
    ranking = pd.concat([reasoning, desc_df], axis=1)
    ranking = ranking.sort_values(by='Score', axis=0, ascending=False)
    
    #criterions.remove('Symbol')
    if show:
        print(ranking.head(25))
        
    return ranking
