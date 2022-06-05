#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 17:12:52 2022

@author: ray
"""

from pandas_datareader import data as pdr

class GetStockData():
    
    def __init__(self, start, end, ticker_list):
        
        self.start = start
        self.end = end
        self.ticker_list = ticker_list
                
    def MakeOutPut(self):
        data = pdr.get_data_yahoo(self.ticker_list, self.start, self.end).Close
        data.columns.names = [None]
        data.index = data.index.astype(str)
        
        print('Already get all Data.')
        
        return data    
    
    def StoreData(self, path):
        store_data = self.MakeOutPut()
        store_data.to_csv(path, index = False)
        
        print('Data stored Finished!!')