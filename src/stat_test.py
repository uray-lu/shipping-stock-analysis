#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 17:15:00 2022

@author: ray
"""

        

import pandas as pd
from matplotlib import pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf
from arch.unitroot import ADF
from statsmodels.stats.diagnostic import acorr_ljungbox
from colorama import Back, init

init(autoreset = True)


## Plot data        
def MakePlot(data, stock, Type):
    
    if Type == 'Raw':
        path = 'Raw' 
    elif Type == 'Diff':
        path = 'Diff'
    
    plt.figure(figsize=(10,4))
    plt.plot(data.index ,data[stock])
    plt.xticks(range(0,242, 24))
    plt.tick_params(axis='both', which = 'major', labelsize = 8)
    plt.title(stock, fontsize=20)
    plt.savefig('Plot/Price/'  + path + '/'+stock+'.png')
    
    if Type == 'Raw':
        print(f"{'Plot of': <10}{stock: <10}{'original Price stored': ^10}{'·'*20: >10}{Back.GREEN}{'Done': ^10}")
    elif Type =='Diff':
        print(f"{'Plot of': <10}{stock: <10}{'first diff stored': ^10}{'·'*20: >10}{Back.GREEN}{'Done': ^10}")
    

##ACf & PACF

def ACF(data, stock, Type):
    
    if Type == 'Raw':
        path = 'Raw' 
    elif Type == 'Diff':
        path = 'Diff'
        
    plot_acf(data[stock], lags=20, title= stock+'_ACF')
    plt.savefig('Plot/ACF&PACF/' + path + '/'+stock+'_ACF.png')
    
    if Type == 'Raw':
        print(f"{'Plot of': <10}{stock: <10}{'original Price ACF stored': ^10}{'·'*20: >10}{Back.GREEN}{'Done': ^10}")
    elif Type == 'Diff':
        print(f"{'Plot of': <10}{stock: <10}{'first diff ACF stored': ^10}{'·'*20: >10}{Back.GREEN}{'Done': ^10}")
    
    
    

def PACF(data, stock, Type):
    
    if Type == 'Raw':
        path = 'Raw' 
    elif Type == 'Diff':
        path = 'Diff'
        
    plot_pacf(data[stock], lags=20, title= stock+'_PACF')
    plt.savefig('Plot/ACF&PACF/' + path + '/'+stock+'_PACF.png')

    if Type == 'Raw':
        print(f"{'Plot of': <10}{stock: <10}{'original Price PACF stored': ^10}{'·'*20: >10}{Back.GREEN}{'Done': ^10}")
    elif Type == 'Diff':
        print(f"{'Plot of': <10}{stock: <10}{'first diff PACF stored': ^10}{'·'*20: >10}{Back.GREEN}{'Done': ^10}")




#ADF test

def ADF_test(data):
    
    output= []
    for i in range(7):
        
        result = ADF(data.T.iloc[i])
        result = result.summary().as_html()
        result = pd.read_html(result, index_col=0)
        result = {'name': data.T.index[i],
                  'ADF Statistic':'%f' % result[0][1]['Test Statistic'],
                  'p-value': '%f' % result[0][1]['P-value'],
                  }
        output.append(result)
        
    df = pd.DataFrame(output)
    
    print(f"{'Augmented Dickey-Fuller test': <10}{'·'*20: ^10}{Back.GREEN}{'Done': ^10}")
    print(df)

# Ljung-box test

def Ljung_box_test(data):
    output= []
    for i in range(7):
        
        result = acorr_ljungbox(data.T.iloc[i], lags=[1], return_df=True)
        result = {'name': data.T.index[i],
                  'Ljung-box Stattistic':'%f' % result['lb_stat'],
                  'Ljung-box p-value': '%f' % result['lb_pvalue'],
                  }
        output.append(result)
        
    df = pd.DataFrame(output)
    
    print(f"{'Ljung-box test': <10}{'·'*20: ^10}{Back.GREEN}{'Done': ^10}")
    print(df)  
    
    
    
    
    
    
    
    
    
    