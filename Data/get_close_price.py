#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 17:12:52 2022

@author: ray
"""

from pandas_datareader import data as pdr
from colorama import Back, init

init(autoreset = True)

class GetStockData():
    
    def __init__(self, start, end, ticker_list):
        
        self.start = start
        self.end = end
        self.ticker_list = ticker_list
                
    def MakeOutPut(self):
        data = pdr.get_data_yahoo(self.ticker_list, self.start, self.end).Close
        data.columns.names = [None]
        data.index = data.index.astype(str)
        
        print(f"{'Get Data' : <10}{'·'*20 : ^10}{Back.GREEN}{'Done' : ^10}")
        
        return data    
    
    def StoreData(self):
        store_data = self.MakeOutPut()
        store_data.to_csv('Close_price_data.csv', index = False)
        
        print(f"{'Data Store' : <10}{'·'*20 : ^10}{Back.GREEN}{'Done' : ^10}")
        
        
        
stock_lists = ['2609.TW', '2603.TW', '2615.TW', '5608.TW', '2605.TW','2606.TW', '2637.TW' ]
stocks_data = GetStockData('2021-01-01', '2022-01-01', stock_lists)
stocks_data.StoreData()