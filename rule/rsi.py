#!/usr/bin/python
# coding: UTF-8
from string import *
import os
import sys
import datetime
import time
import re
sys.path.append('../lib/')
import data_process as dp

def buy(stock,trade,dt):
	num = 20
	r = dp.get_data_by_day_num(stock,dt,num)
	rsi = dp.relative_strength(r.close)

	if(rsi[-1] < float(trade.vals[0])):
		price = 1
		buy_type = 1	#nari
		return price,buy_type
	return 0,0
def sell(stock,trade,dt):
	trade.sell_num = trade.buy_num
	num = 20
	r = dp.get_data_by_day_num(stock,dt,num)
	rsi = dp.relative_strength(r.close)
	if(rsi[-1] > float(trade.vals[1])):
		sell_type = 1	#nari
		wish_sell_price = 1
		print wish_sell_price
		return wish_sell_price,sell_type
	return 0,0
