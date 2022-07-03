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



#read data

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
    options, args = getopt.getopt(argv, 'c:b:a:s:',['container=', 'bulk=', 'all=', 'save'])
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



container_model = model_testing(train_data, 'container')
bulk_model = model_testing(train_data, 'bulk')
all_model = model_testing(train_data, 'all')



    

    

try:
    if argv[6] == '--save':
            
        container_model.save('Model/test_result/container_model_test_result.pickle')
        bulk_model.save('Model/test_result/bulk_model_test_result.pickle')
        all_model.save('Model/test_result/all_model_test_result.pickle')
        
    print('Test model was saved.')

except:
    print('Test model was not saved.')
    print('You should add --save in the end of your parsing arguments to save the test model.')
    print('test')