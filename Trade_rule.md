# Introduction #
  * put rule file in rule dir
  * You need sell() and buy() functions
  * sell()
    * arguments:stock,trade,dt
      * stock : Stock data class
      * trade : Trade data class
      * dt : Date,time
    * Return sell price and trade type (limit order or market order)
  * buy()
    * arguments:stock,trade,dt
      * stock : Stock data class
      * trade : Trade data class
      * dt : Date,time
    * Return buy price and trade type (limit order or market order)

# Special Variables #
  * trade.price
    * last stock price
  * trade.price\_history
    * stock price history (Array)
    * trade.price\_history[-1] = trade.price
  * trade.vals(array)
    * values for trade rule

# Example :"simple.py" #
Simple trade rule.
Buy if last price < Second last price.
Sell if last price > Buy price.
```
 #!/usr/bin/python
 # coding: UTF-8

 #Import library
 from string import *
 import os
 import sys
 import datetime
 import time
 import numpy as np
 sys.path.append('../lib/')
 import data_process as dp
 
 #Buy routine
 def buy(stock,trade,dt):
 	data_num = 3
 	r = dp.get_data_by_day_num(stock,dt,data_num) #Get price data
 	trade.price = r.close[-1] #set last price
 	last_price = int(r.close[-2]) #Set second last price
 	last_last_price = int(r.close[-3]) #Set third last price
 	buy_rate = float(trade.vals[0]) #Set buy price rate
 	if(int(last_price) < int(last_last_price * buy_rate)): #Buy the stocks if the second last price is lower than third last price
 		price = int(last_price) * buy_rate #set buy price
 		if(int(r.open[-1]) < price): #Set the buy price if last price is lower than buy price
 			price = int(r.open[-1])
 		buy_type = 0	#limit order
 		return price,buy_type
 	return 0,0 #Do nothing
 #Sell routine
 def sell(stock,trade,dt):
 	data_num = 3
 	sell_type = 0
 	r = dp.get_data_by_day_num(stock,dt,data_num) #get stock prices
 	trade.price = r.close[-1] #Set last price
 	sell_rate = float(trade.vals[1]) #Set sell price rate
 	now_rate = float(r.open[-1]) / float(trade.buy_price) #Set a loss target
 	wish_sell_price = int(trade.buy_price)*sell_rate #Set sell price
 	if(int(r.open[-1]) > wish_sell_price): #Sell the stock if last price is higher than sell price
 		sell_type = 0	#limit order
 		wish_sell_price = int(r.open[-1]) #set sell price
 	elif(now_rate < float(trade.vals[2])):	#Loss Cut
 		sell_type = 1	#market order
 		wish_sell_price = int(r.open[-1]) #
 	return wish_sell_price,sell_type
```