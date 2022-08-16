#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 17:19:25 2022

@author: ray
"""

import pandas as pd
import numpy as np
from pandas_datareader import data as pdr
from matplotlib import pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf
from arch.unitroot import ADF
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.api import VAR

#%%

### Functions and Class

## Get data
class GetStockData():
    
    def __init__(self, start, end, ticker_list):
        
        self.start = start
        self.end = end
        self.ticker_list = ticker_list
                
    def MakeOutPut(self):
        data = pdr.get_data_yahoo(self.ticker_list, self.start, self.end).Close
        data.columns.names = [None]
        data.index = data.index.astype(str)
    
        
        return data    
    
    def StoreData(self, path):
        store_data = self.MakeOutPut()
        store_data.to_csv(path, index = False)
        
        
## Plot data        
def MakePlot(data, stock):
    plt.figure(figsize=(10,4))
    plt.plot(data.index ,data[stock])
    plt.xticks(range(0,242, 24))
    plt.tick_params(axis='both', which = 'major', labelsize = 8)
    plt.title(stock, fontsize=20)
    plt.savefig(r'./'+stock+'.png')

##ACf & PACF

def ACF(data, stock):
    plot_acf(data[stock], lags=20, title= stock+'_ACF')
    plt.savefig(r'./'+stock+'_ACF.png')
    
    
def PACF(data, stock):
    plot_pacf(data[stock], lags=20, title= stock+'_PACF')
    plt.savefig(r'./'+stock+'_PACF.png')


#ADF test

def ADF_test(data):
    
    output= []
    for i in range(7):
        
        result = ADF(data.T.iloc[i])
        result = result.summary().as_html()
        result = pd.read_html(result, index_col=0)
        result = {'name': stocks_returns.T.index[i],
                  'ADF Statistic':'%f' % result[0][1]['Test Statistic'],
                  'p-value': '%f' % result[0][1]['P-value'],
                  }
        output.append(result)
        
    df = pd.DataFrame(output)
    
    
    return df

# Ljung-box test

def Ljung_box_test(data):
    output= []
    for i in range(7):
        
        result = acorr_ljungbox(data.T.iloc[i], lags=[1], return_df=True)
        result = {'name': stocks_returns.T.index[i],
                  'Ljung-box Stattistic':'%f' % result['lb_stat'],
                  'Ljung-box p-value': '%f' % result['lb_pvalue'],
                  }
        output.append(result)
        
    df = pd.DataFrame(output)
    
    
    return df    


# Model construct, Var model order search, model forecast

class ModelConstruct():
    
    def __init__(self, data, stockType):
        
        self.data = data
        self.stockType = stockType
    
    def GridsearchforP(self):
        if self.stockType =='container':
            self.stock_lists = ['2609.TW Returns', '2603.TW Returns', '2615.TW Returns']
        elif self.stockType =='bulk':
            self.stock_lists = ['5608.TW Returns', '2605.TW Returns','2606.TW Returns', '2637.TW Returns' ]
        elif self.stockType  =='all':
            self.stock_lists = ['2609.TW Returns', '2603.TW Returns', '2615.TW Returns', '5608.TW Returns', '2605.TW Returns','2606.TW Returns', '2637.TW Returns' ]
                    
        print('-'*25 + 'Grid Search of Order P for' + ' ' + self.stockType +' '+'Stocks Model'+ '-'*25)
                    
        aic=[]
        for i in range(10):
            self.model = VAR(self.data[self.stock_lists])
            results = self.model.fit(i)
            print('Order =', i)
            print('AIC: ', results.aic)
            print('BIC: ', results.bic)
            print()
            aic.append(results.aic)
        
        plt.figure()
        plt.plot(aic)
        plt.title(self.stockType + ' ' + 'AIC')
        plt.savefig('./' + self.stockType + 'AIC.png')
    
    def Model(self, order):
        model = self.model
        result = model.fit(order)
        print(result.summary())
        
        return result
    
    def Forecast(self, Order, Origidata,Testdata):
        lagged_Values = self.data[self.stock_lists].values[-Order:]
        pred = self.Model(Order).forecast(y=lagged_Values, steps= len(Testdata)) 
        idx = Testdata.index
        
        df_forecast = pd.DataFrame(data=pred, 
                                   index=idx,
                                   columns= (self.stock_lists[k]+' 1d' for k in range(len(self.stock_lists))))
        
        
        
        for i in range(len(self.stock_lists)):
            
            df_forecast[Origidata.columns[i] + 'Forecast'] = np.r_[Origidata[Origidata.columns[i]][-len(Testdata)-1],
                                                                  df_forecast[df_forecast.columns[i]]].cumsum()[1:]
         
        
        
            test_original = Origidata[-len(Testdata):]
            
            plt.figure()
            test_original[test_original.columns[i]].plot(figsize=(12,5),legend=True)
            df_forecast[Origidata.columns[i] + 'Forecast'].plot(legend=True)
            plt.title(self.stockType +' ' + Origidata.columns[i] + ' Forecast')
            plt.savefig('./'+ self.stockType +' ' + Origidata.columns[i] + ' Forecast.png')
        
        
        
#%%

# Get Close Price

stock_lists = ['2609.TW', '2603.TW', '2615.TW', '5608.TW', '2605.TW','2606.TW', '2637.TW' ]
stocks_data = GetStockData('2021-01-01', '2022-01-01', stock_lists)
stocks = stocks_data.MakeOutPut()


#%%

# Plot Original Price

print('-'*25+'Plot of Original Price has been stored'+'-'*25)
MakePlot(stocks, '2609.TW')
MakePlot(stocks, '2603.TW')
MakePlot(stocks, '2615.TW')
MakePlot(stocks, '5608.TW')
MakePlot(stocks, '2605.TW')
MakePlot(stocks, '2606.TW')
MakePlot(stocks, '2637.TW')

#%%

# ACF 
print('-'*25+'Plot of Original Price ACF has been stored'+'-'*25)
ACF(stocks, '2609.TW')
ACF(stocks, '2603.TW')
ACF(stocks, '2615.TW')
ACF(stocks, '5608.TW')
ACF(stocks, '2605.TW')
ACF(stocks, '2606.TW')
ACF(stocks, '2637.TW')

# PACF
print('-'*25+'Plot of Original Price PACF has been stored'+'-'*25)
PACF(stocks, '2609.TW')
PACF(stocks, '2603.TW')
PACF(stocks, '2615.TW')
PACF(stocks, '5608.TW')
PACF(stocks, '2605.TW')
PACF(stocks, '2606.TW')
PACF(stocks, '2637.TW')

#%%

# first order difference as log return

stocks_returns = stocks.diff().dropna()

stocks_returns = stocks_returns.rename(columns = {'2609.TW':'2609.TW Returns', '2603.TW':'2603.TW Returns', '2615.TW':'2615.TW Returns', '5608.TW':'5608.TW Returns', '2605.TW':'2605.TW Returns','2606.TW':'2606.TW Returns', '2637.TW':'2637.TW Returns' })




#%%

print('-'*25+'Plot of Stocks returns has been stored'+'-'*25)
MakePlot(stocks_returns, '2609.TW Returns')
MakePlot(stocks_returns, '2603.TW Returns')
MakePlot(stocks_returns, '2615.TW Returns')
MakePlot(stocks_returns, '5608.TW Returns')
MakePlot(stocks_returns, '2605.TW Returns')
MakePlot(stocks_returns, '2606.TW Returns')
MakePlot(stocks_returns, '2637.TW Returns')


#%%

#ACF
print('-'*25+'Plot of Stocks Returns ACF has been stored'+'-'*25)
ACF(stocks_returns, '2609.TW Returns')
ACF(stocks_returns, '2603.TW Returns')
ACF(stocks_returns, '2615.TW Returns')
ACF(stocks_returns, '5608.TW Returns')
ACF(stocks_returns, '2605.TW Returns')
ACF(stocks_returns, '2606.TW Returns')
ACF(stocks_returns, '2637.TW Returns')

# PACF
print('-'*25+'Plot of Stocks Returns PACF has been stored'+'-'*25)
PACF(stocks_returns, '2609.TW Returns')
PACF(stocks_returns, '2603.TW Returns')
PACF(stocks_returns, '2615.TW Returns')
PACF(stocks_returns, '5608.TW Returns')
PACF(stocks_returns, '2605.TW Returns')
PACF(stocks_returns, '2606.TW Returns')
PACF(stocks_returns, '2637.TW Returns')

#%%

#ADF test for stocks raw data
print('-'*15+'Augmented Dickey-Fuller test of Original Price'+'-'*15)
stocks_adf_test = ADF_test(stocks)
print(stocks_adf_test)


#ADF test for stocks retuens 
print('-'*15+'Augmented Dickey-Fuller test of Stocks returns' +'-'*15)
stocks_returns_adf_test = ADF_test(stocks_returns)
print(stocks_returns_adf_test)


#%%

# Ljun-box test for stocks raw data
print('-'*25+'  Ljung-box test of Original Price'+'-'*25)
stocks_lb_test = Ljung_box_test(stocks)
print(stocks_lb_test)


# Ljun-box test for stocks returns
print('-'*25+'  Ljung-box test of Stocks returns'+'-'*25)
stocks_returns_lb_test = Ljung_box_test(stocks_returns)
print(stocks_returns_lb_test)




#%%

#train test split 

print(int(len(stocks_returns)*0.2))
#%%

test_obs = int(len(stocks_returns)*0.2)
train_data = stocks_returns[:-test_obs]
test_data = stocks_returns[-test_obs:]

# Model construction

container = ModelConstruct(train_data, 'container')
bulk = ModelConstruct(train_data, 'bulk')
all_stocks = ModelConstruct(train_data, 'all')



#%%

#Search for the order for VAR model

container_order = container.GridsearchforP()
bulk_order = bulk.GridsearchforP()
all_stocks_order = all_stocks.GridsearchforP()




#%%

#fit three VAR() model

Model_container = container.Model(4)
Model_bulk = bulk.Model(1) 
Model_all = all_stocks.Model(9)



#%%

#Forecast

container_forecast = container.Forecast(4,stocks, test_data)
bulk_forecast = bulk.Forecast(1, stocks, test_data)
all_stocks_forecast  =all_stocks.Forecast(1, stocks,  test_data)