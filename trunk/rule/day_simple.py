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
	if(len(trade.price_history) > data_num):
		prices = np.array(trade.price_history[-data_num -1 :-1])
	else:
		return 0,0
	trade.price = int(prices[-1])
	last_price = int(prices[-2])
	last_last_price = int(prices[-3])
	buy_rate = float(trade.vals[0])
	if(int(last_price) < int(last_last_price * buy_rate)):
		price = int(last_price) * buy_rate
		if(int(trade.price) < price):
			price = int(trade.price)
		buy_type = 0	#sashi
		return price,buy_type
	return 0,0
def sell(stock,trade,dt):
	data_num = 3
	sell_type = 0
	if(len(trade.price_history) > data_num):
		prices = np.array(trade.price_history[-data_num -1 :-1])
	else:
		return 0,0
	trade.price = int(prices[-1])
	last_price = int(prices[-2])
	last_last_price = int(prices[-3])
	#trade.sell_num = trade.buy_num
	sell_rate = float(trade.vals[1])
	now_rate = float(trade.price) / float(trade.buy_price)
	wish_sell_price = int(trade.buy_price)*sell_rate
	if(int(trade.price) > wish_sell_price):
		sell_type = 0
		wish_sell_price = int(trade.price)
	elif(now_rate < float(trade.vals[2])):	#Loss Cut
		sell_type = 1	#nari
		wish_sell_price = int(trade.price)
	return wish_sell_price,sell_type
