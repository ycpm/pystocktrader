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
	margine = 5
	ma1_num = int(trade.vals[0])
	ma2_num = int(trade.vals[1])
	date_num = ma2_num
	if(ma1_num > ma2_num):
		date_num = ma1_num
	date_num += margine
	buy_price = 0

	r = dp.get_data_by_day_num(stock,dt,date_num)
	ma1 = dp.moving_average(r.close, ma1_num)
	ma2 = dp.moving_average(r.close, ma2_num)
	check1 = ma1[-3] - ma2[-3]	#day before yesterday
	check2 = ma1[-2] - ma2[-2]	#Yesterday
	buy_rate = float(trade.vals[2])
	last_price = int(r.close[-2])
	if(check1 < 0 and check2 > 0):	#Golden cross
		buy_price = int(last_price) * buy_rate
		if(int(r.open[-1]) < buy_price):
			buy_price = int(r.open[-1]) * buy_rate
		#print "buy price =",buy_price,", last_price =",last_price, diff1 , diff2
		#trade.buy_type = 1	#nari
		buy_type = 0	#sashi
		#buy_type = 1	#nari
		return buy_price,buy_type
	return 0,0
def sell(stock,trade,dt):
	margine = 5
	ma1_num = int(trade.vals[3])
	ma2_num = int(trade.vals[4])
	date_num = ma2_num
	if(ma1_num > ma2_num):
		date_num = ma1_num
	date_num += margine
	buy_price = 0

	r = dp.get_data_by_day_num(stock,dt,date_num)
	ma1 = dp.moving_average(r.close, ma1_num)
	ma2 = dp.moving_average(r.close, ma2_num)
	check1 = ma1[-3] - ma2[-3]	#day before yesterday
	check2 = ma1[-2] - ma2[-2]	#Yesterday
	last_price = int(r.close[-2])
	now_rate = 1
	if(trade.buy_price > 0):
		now_rate = float(r.open[-1]) / float(trade.buy_price)
	cut_rate = float(trade.vals[5])
	if(now_rate < cut_rate):
		print "***Loss Cut***", now_rate,r.open[-1]
		#time.sleep(10)
		sell_type = 1	#nari
		wish_sell_price = int(r.open[-1])
		return wish_sell_price,sell_type

	#sell_type = 0
	sell_type = 1
	sell_rate = float(trade.vals[6])
	if(check1 < 0 and check2 > 0):	#Ded cross
		wish_sell_price = int(trade.buy_price)*sell_rate
		print "Sell",trade.buy_price, ", wish =",wish_sell_price
		#time.sleep(10)
		if(int(r.open[-1]) > wish_sell_price):
			sell_type = 0
			wish_sell_price = int(r.open[-1])
		return wish_sell_price,sell_type
	#time.sleep(10)
	return 0,0
