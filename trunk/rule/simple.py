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

def buy(stock,trade,dt):
	data_num = 3
	r = dp.get_data_by_day_num(stock,dt,data_num)
	trade.price = r.close[-1]
	last_price = int(r.close[-2])
	last_last_price = int(r.close[-3])
	buy_rate = float(trade.vals[0])
	if(int(last_price) < int(last_last_price * buy_rate)):
		price = int(last_price) * buy_rate
		if(int(r.open[-1]) < price):
			price = int(r.open[-1])
		buy_type = 0	#sashi
		return price,buy_type
	return 0,0
def sell(stock,trade,dt):
	data_num = 3
	sell_type = 0
	r = dp.get_data_by_day_num(stock,dt,data_num)
	trade.price = r.close[-1]
	#trade.sell_num = trade.buy_num
	sell_rate = float(trade.vals[1])
	now_rate = float(r.open[-1]) / float(trade.buy_price)
	wish_sell_price = int(trade.buy_price)*sell_rate
	if(int(r.open[-1]) > wish_sell_price):
		sell_type = 0
		wish_sell_price = int(r.open[-1])
	elif(now_rate < float(trade.vals[2])):	#Loss Cut
		sell_type = 1	#nari
		wish_sell_price = int(r.open[-1])
	return wish_sell_price,sell_type
