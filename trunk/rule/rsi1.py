#!/usr/bin/python
# coding: UTF-8
from string import *
import os
import sys
import datetime
import time
import locale
import re
import numpy as np
sys.path.append('../lib/')
import data_process as dp
def analysis_date(stock,dt):
	num = 25
	r = dp.get_data_by_day_num(stock,dt,num)
	ma_n = 10
	ma10 = dp.moving_average(r.close, ma_n)
	ma20 = dp.moving_average(r.close, 20)
	rsi = dp.relative_strength(r.close)
	coeffs20,yfit20=dp.get_fit_data(range(0, 20),r.close[-21:-1])
	coeffs10,yfit10=dp.get_fit_data(range(0, ma_n),r.close[-ma_n-1:-1])
	coeffs05,yfit5=dp.get_fit_data(range(0, 5),r.close[-6:-1])
	return ma10[-1],ma20[-1],rsi[-1],coeffs20[-1],coeffs10[0],coeffs05[0]

def buy(stock,trade,dt):
	#trade.price = r.close[-1]
	#print r.close
	ma10,ma20,rsi,a20,a10,a05 = analysis_date(stock,dt)	#a10[yen/day]
	if(rsi < 25):
		price = int(ma10) * 0.99
		buy_type = 1	#nari
		return price,buy_type
	return 0,0
def sell(stock,trade,dt):
	trade.sell_num = trade.buy_num
	ma10,ma20,rsi,a20,a10,a05 = analysis_date(stock,dt)	#a10[yen/day]
	if(rsi > 70):
		sell_type = 1	#nari
		wish_sell_price = int(ma10) * 0.99
		print wish_sell_price
		return wish_sell_price,sell_type
	return 0,0
