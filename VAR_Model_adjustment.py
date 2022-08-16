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
from colorama import Back, init

init(autoreset = True)

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
    options, args = getopt.getopt(argv, 'c:b:a:',['container=', 'bulk=', 'all='])
except getopt.GetoptError:
    print(Back.RED + 'Worng option were provided!')
    print(Back.RED + 'Please enter the order of model after model type')
    print(Back.BLUE + 'For example : --container 3')
    
    sys.exit(2)


def model_testing(data):
    
    
    for opt, arg in options:
        
        if opt in '--container':
            
            testing_model = ModelConstruct(data, 'container')
            test_order = int(arg)
            testing_result = testing_model.Model(test_order)
            
            print(f"{'Container Stocks Model Adjusted Result has been done': <10}{'·'*20: ^10}{Back.GREEN}{'Train by Order:': ^10}{test_order}")
            
        elif opt in '--bulk':
                    
            testing_model = ModelConstruct(data, 'bulk')
            test_order = int(arg)
            testing_result = testing_model.Model(test_order)
            
            print(f"{'Bulk Stocks Model Adjusted Result has been done': <10}{'·'*20: ^10}{Back.GREEN}{'Train by Order:': ^10}{test_order}")

        elif opt in '--all':
                        
            testing_model = ModelConstruct(data, 'all')
            test_order = int(arg)
            testing_result = testing_model.Model(test_order)
            
            print(f"{'All Stocks Model Adjusted Result has been done': <10}{'·'*20: ^10}{Back.GREEN}{'Train by Order:': ^10}{test_order}")
            
    
    return testing_result



container_model = model_testing(train_data)
bulk_model = model_testing(train_data)
all_model = model_testing(train_data)








    