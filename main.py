#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 15:28:31 2022

@author: ray
"""


#Require packages 

import pandas as pd
from src.stat_test import MakePlot, ACF, PACF, ADF_test, Ljung_box_test 
from Model.var_model import ModelConstruct





# Get Close Price


stocks = pd.read_csv('Data/Close_price_data.csv')
stock_lists = ['2609.TW', '2603.TW', '2615.TW', '5608.TW', '2605.TW','2606.TW', '2637.TW' ]
# first order difference as first difference

stocks_diff = stocks.diff().dropna()
stocks_diff = stocks_diff.rename(columns = {'2609.TW':'2609.TW Diff', '2603.TW':'2603.TW Diff', '2615.TW':'2615.TW Diff', '5608.TW':'5608.TW Diff', '2605.TW':'2605.TW Diff','2606.TW':'2606.TW Diff', '2637.TW':'2637.TW Diff' })

# first order difference as first difference




# Plot Original Price

for i in stock_lists:
    
    MakePlot(stocks, i, 'Raw')
    ACF(stocks, i, 'Raw')
    PACF(stocks, i, 'Raw')


# Plot first Diff Price

for i in stocks_diff.columns:
    
    MakePlot(stocks_diff, i, 'Diff')
    ACF(stocks_diff, i, 'Diff')
    PACF(stocks_diff, i, 'Diff')


#ADF test for stocks raw data

ADF_test(stocks)

#ADF test for stocks first Diff data

ADF_test(stocks_diff)


# Ljun-box test for stocks raw data

Ljung_box_test(stocks)

# Ljun-box test for stocks Diff

Ljung_box_test(stocks_diff)



# Data split

test_obs = int(len(stocks_diff)*0.2)
train_data = stocks_diff[:-test_obs]
test_data = stocks_diff[-test_obs:]





# Model construction

#container = ModelConstruct(train_data, 'container')
#bulk = ModelConstruct(train_data, 'bulk')
#all_stocks = ModelConstruct(train_data, 'all')



#Search for the order for VAR model

#container.GridsearchforP()
#bulk.GridsearchforP()
#all_stocks.GridsearchforP()



#Forecast

#container.Forecast(4,stocks, test_data)
#bulk.Forecast(1, stocks, test_data)
#all_stocks.Forecast(1, stocks,  test_data)

