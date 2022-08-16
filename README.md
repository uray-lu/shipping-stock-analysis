# Shipping-Stock-Analysis

## This is NCCU Department of Economics Time series class final project
### This project use the Vector Auto-Regression Model to predict the Shipping Stocks form TW through 2021 to 2022,  ..
    we use the yahoo API to get the raw close data of seven different stocks, and use the `arch` package to do the  ..
    basic time series data analysis, including: ACF, PACF, Augmented Dickey-Fuller test, Ljung-box test .  ..
    After the statistic test, we use the `VAR` package from `statsmodels.tsa.api` to construct the different models, ..
    to do the search of optimal order of the model, after we deciding the orders of models, we can construct the forecast ..
    model to make the forecast plot.   


### After clone the whole repo:


1. Open your terminal and change the directory to this project

```bash
>>> cd ./Shipping-Stock-Analysis
```

2. Install all the packages required in your terminal


```
>>> pip/pip3 install -r requirements.txt
```


### After all the package were installed:

* Run #main.py in your terminal to do the basic time series analysis and construct the training model to do the grid search of optimal model order 


```
>>> python main.py 
``` 





* After deciding the order of model, you can Modify the Model through #VAR_Model_adjustment.py, Use the command line below:

```
>>> python VAR_Model_adjustment.py --container `order` --bulk `order` --all `order`
```
_input any numbers to replace `order` in the command line._
_You can randomly shift the args differently like_
_`--all order --container order --bulk order`_



* After the adjustment of models was done. Run #main.py with the model order arguments to construct the forecast model and finish the forecast

```
>>> python main.py --container `order` --bulk `order` --all `order`
```
_input any numbers to replace `order` in the command line._
_You can randomly shift the args differently like_
_`--all order --container order --bulk order`_



* Your All figures will all be stored in folder name 'Plot' by categori
    
    _Including : Raw data, first differentiate data, ACF, PACF, Model AIC etc._

* Your Raw data will collected by Yahoo API and stored in folder name 'Data'.

* Your Model AIC will be stored in folder 'Model'>> 'Model_adjustment_record'.
