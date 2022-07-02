#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 17:16:55 2022

@author: ray
"""

import numpy as np
import pandas as pd
from statsmodels.tsa.api import VAR
from matplotlib import pyplot as plt


class ModelConstruct():
    
    def __init__(self, data, stockType):
        
        self.data = data
        self.stockType = stockType
        
        if self.stockType =='container':
            
            self.stock_lists = ['2609.TW Diff', '2603.TW Diff', '2615.TW Diff']
            
        elif self.stockType =='bulk':
            
            self.stock_lists = ['5608.TW Diff', '2605.TW Diff','2606.TW Diff', '2637.TW Diff' ]
            
        elif self.stockType  =='all':
            
            self.stock_lists = ['2609.TW Diff', '2603.TW Diff', '2615.TW Diff', '5608.TW Diff', '2605.TW Diff','2606.TW Diff', '2637.TW Diff' ]
        
    def GridsearchforP(self):
        
        
                    
        print('-'*25 + 'Grid Search of Order P for' + ' ' + self.stockType +' '+'Stocks Model'+ '-'*25)
                    
        aic=[]
        for i in [1,2,3,4,5,6,7,8,9,10]:
            self.model = VAR(self.data[self.stock_lists])
            results = self.model.fit(i)
            print('Order =', i)
            print('AIC: ', results.aic)
            print()
            aic.append(results.aic)
        
        
        plt.figure()
        plt.plot( range(1,11), aic)
        plt.title(self.stockType + ' ' + 'AIC')
        plt.savefig('Plot/AIC_of_model_order/' + self.stockType + ' AIC.png')
        
        aic = pd.DataFrame(aic, index = ('order ='+ str(i) for i in range(1,11)))
        aic.to_csv('Model/Model record/' + self.stockType + ' model_order_AIC.csv', header=False)
    
    def Model(self, order):
        model = self.model
        result = model.fit(order)
        print(result.summary())
        
        return result
    
    def Forecast(self, Order, Origidata,Testdata):
        lagged_Values = self.data[self.stock_lists].values[-Order:]
        model = self.model.fit(Order)
        pred = model.forecast(y=lagged_Values, steps= len(Testdata)) 
        idx = Testdata.index
        
        df_forecast = pd.DataFrame(data=pred, 
                                   index=idx,
                                   columns= (self.stock_lists))
        
        
        
        for item in self.stock_lists:
            
            
            df_forecast[item[:7] + 'Forecast'] = np.r_[Origidata[item[:7]][-len(Testdata)-1], df_forecast[item]].cumsum()[1:]
         
        
        
            test_original = Origidata[-len(Testdata):]
            
            plt.figure()
            test_original[item[:7]].plot(figsize=(12,5),legend=True)
            df_forecast[item[:7] + 'Forecast'].plot(legend=True)
            plt.title(self.stockType +' model ' + item[:7] + ' Forecast')
            
            if self.stockType == 'container':
                
                path = 'Container'
                
            elif self.stockType == 'bulk':
                
                path = 'Bulk'
                
            elif self.stockType == 'all':
                
                path = 'All'
                
            plt.savefig('Plot/Forecast/' + path + '/'+ self.stockType +' ' + item[:7] + ' Forecast.png')
            
        print('Model Forecast of ' + self.stockType+ ' has been Done !!')  
            
            
            
            