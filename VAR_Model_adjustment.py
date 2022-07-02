#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  2 13:24:03 2022

@author: ray
"""

import sys
import getopt
import pandas as pd
from Model.var_model import ModelConstruct





stocks = pd.read_csv('Data/Close_price_data.csv')

# first order difference as first difference

stocks_diff = stocks.diff().dropna()
stocks_diff = stocks_diff.rename(columns = {'2609.TW':'2609.TW Diff', '2603.TW':'2603.TW Diff', '2615.TW':'2615.TW Diff', '5608.TW':'5608.TW Diff', '2605.TW':'2605.TW Diff','2606.TW':'2606.TW Diff', '2637.TW':'2637.TW Diff' })



# Data split

test_obs = int(len(stocks_diff)*0.2)
train_data = stocks_diff[:-test_obs]
test_data = stocks_diff[-test_obs:]




argv = sys.argv[1:]

try:
    options, args = getopt.getopt(argv, 'c:b:a:',['container=', 'bulk=', 'all='])
except getopt.GetoptError:
    print('Worng option were provided')
    
    sys.exit(2)


def model_testing(data, StockType):
    
    
    testing_mdoel = ModelConstruct(data, StockType)
    
    for opt, arg in options:
        
        if opt in '--container':
                
            test_order = int(arg)
            testing_result = testing_mdoel.Model(test_order),
               
            
            
        elif opt in '--bulk':
                    
            test_order = int(arg)
            testing_result = testing_mdoel.Model(test_order),
                  
            
            
        elif opt in '--all':
                        
            test_order = int(arg)
            testing_result = testing_mdoel.Model(test_order) 
            
    
    
    return testing_result



model_testing(train_data, 'container')
model_testing(train_data, 'bulk')
model_testing(train_data, 'all')



