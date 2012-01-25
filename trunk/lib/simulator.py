#!/usr/bin/python
# coding: UTF-8
from string import *
from math import *
import os
import wx
import sys
import datetime
import time
import locale
import re
import numpy as np
sys.path.append('./rule/')
import data_process as dp
import market as mk

LOG_DIR = "./log/"
RESOURCE_LOG = "resource.csv"
RESOURCE_LOG2 = "resource2.csv"
SIMU_LOG = "simulate.csv"
TMP_SUM = 0
def run(stock,trade,sim,sdt,edt,w):
	global TMP_SUM
	w.progress.Update(0, 'Start simulation')
	tmp_datas = []
	TMP_SUM = 0
	if(int(trade.id) < 1000):
		rt = dp.get_price_history()
	else:
		rt = dp.get_data_by_day(stock,sdt,edt.year,edt.month,edt.day)
	if(int(sim.val_num) > 1):
		#Parametoric Simulation
		if(float(sim.val_step) == 0.0):
			diff_val = sim.val_end - sim.val_start
			val_step = float(diff_val) / float(sim.val_num)
		else:
			val_step = float(sim.val_step)
		ini_margin = trade.margin
		if(int(sim.val_num2) > 1):
			#print "2dim"
			if(float(sim.val_step2) == 0.0):
				diff_val2 = sim.val_end2 - sim.val_start2
				val_step2 = float(diff_val2) / float(sim.val_num2)
			else:
				val_step2 = float(sim.val_step2)
			ini_margin = trade.margin
			csv_data = ""
			for j in range(0,int(sim.val_num2)):
				tmp = sim.val_start2+ j * val_step2
				csv_data += str(tmp) + ","
			csv_data = csv_data.strip(",")
			csv_data += "\n"
			for i in range(0,int(sim.val_num)):
				trade.vals[sim.val_id] = sim.val_start + i * val_step
				tmp_csv = str(trade.vals[sim.val_id])
				for j in range(0,int(sim.val_num2)):
					trade.margin = ini_margin
					trade.price_history = []
					trade.hold_num = 0
					#sim.log = []
					sim.resource_log = []
					#print sim.val_id,sim.val_start,i,val_step
					trade.vals[sim.val_id2] = sim.val_start2+ j * val_step2
					#print i,val_step ,trade.vals[sim.val_id]
					#sim.resource_log.append(trade.vals[sim.val_id])
					sim_loop(stock,trade,sim,sdt,edt,rt,w)
					#tmp_datas.append(sim.resource_log[-1]) #Last resource
					tmp_csv += "," + str(sim.resource_log[-1])
				csv_data += tmp_csv + "\n"
				dp.write_file(LOG_DIR,RESOURCE_LOG2,csv_data)

		else:
			for i in range(0,int(sim.val_num)):
				trade.margin = ini_margin
				trade.price_history = []
				trade.hold_num = 0
				#sim.log = []
				sim.resource_log = []
				#print sim.val_id,sim.val_start,i,val_step
				trade.vals[sim.val_id] = sim.val_start + i * val_step
				#print i,val_step ,trade.vals[sim.val_id]
				sim.resource_log.append(trade.vals[sim.val_id])
				sim_loop(stock,trade,sim,sdt,edt,rt,w)
				tmp_datas.append(sim.resource_log)
			tmp_csv_data = []
			for tmp in tmp_datas[0]:
				tmp_csv_data.append(str(tmp) + ",")
		
			for i in range(1,len(tmp_datas)):
				for j in range(0,len(tmp_datas[i])):
					tmp = str(tmp_datas[i][j])
					tmp_csv_data[j] += tmp + ","
			csv_data = ""
			for data in tmp_csv_data:
				csv_data += data.strip(",") + "\n"
			dp.write_file(LOG_DIR,RESOURCE_LOG,csv_data)
	else:
		#Single Simulation
		sim.resource_log = []
		sim_loop(stock,trade,sim,sdt,edt,rt,w)
		#print sim.resource_log,len(sim.resource_log)
		csv_data = ""
		for log in sim.resource_log:
			csv_data += str(log) + "\n"
		dp.write_file(LOG_DIR,RESOURCE_LOG,csv_data)
	#print sim.val_num,sim.val_num2
def sim_loop(stock,trade,sim,sdt,edt,rt,w):
	global TMP_SUM
	one_day = 86400
	#init
	buy_sell_num = 0
	trade.do_buy = 0
	sim_data = ""
	#stock.market[0] = 1
	trade.market = stock.market[0]

	num = len(rt.close)
	total_num = int(num)
	if(int(sim.val_num) > 1):
		total_num = int(num) * int(sim.val_num)
		if(int(sim.val_num2) > 1):
			total_num = int(num) * int(sim.val_num) * int(sim.val_num2)

	stock.datas = []
	for i in range(0,num):
		#if(w.progress == wx.PD_CAN_ABORT):
			#break
		#print w.progress
		TMP_SUM += 1
		pr=int((float(TMP_SUM)/float(total_num )) * 1000.0)
		if( not pr % 50.0):
			pr2 = pr/10
			#print "*********" ,pr/10, "%"
			w.progress.Update(pr2, 'Progress ...')
		#date = time.localtime(tmp_time)
		date_data,dm = str(rt.date[i]).split(' ')
		dt = datetime.date(*[int(val) for val in str(date_data).split('-')])
		#Attention!
		if(i>0):
			stock_data = str(date_data) + "," + str(trade.market) + "," + str(rt.open[i-1]) + "," + str(rt.high[i-1]) + "," + str(rt.low[i-1]) + "," + str(rt.close[i-1]) + "," + str(rt.volume[i-1]) + "," + str(rt.aclose[i-1])
			stock.datas.append(stock_data)
		#print date,trade.rule
		#rt = dp.get_data_by_day(stock,dt)

		today_close = rt.close[i]
		trade.price = rt.open[i]
		trade.high = rt.high[i]
		trade.low = rt.low[i]
		#print today_close
		trade.price_history.append(trade.price)
		date_str = str(rt.date[i])
		trade.sell_num = trade.hold_num
		if(int(trade.margin)- trade.limit > 0 and trade.do_buy == 0):
			#print "BUY"
			trade.buy_total_price = 0
			wish_buy_price, trade.buy_type = trade.rule.buy(stock,trade,dt)
			#trade.do_buy = 1
			if(wish_buy_price > 0):
				trade.buy_num = int((float(trade.margin) - float(trade.limit)) / float(wish_buy_price))
				trade.buy_num = trade.buy_num - (int(trade.buy_num) % int(stock.unit))
				#print trade.buy_num, stock.unit
				trade.buy_total_price=sim_buy(stock,trade,dt,wish_buy_price)
			if(trade.buy_total_price > 0 and trade.buy_num > 0):
				trade.buy_fee = trade.agent.get_fee(trade.buy_total_price,trade.buy_type)
				trade.buy_price = (trade.buy_total_price + trade.buy_fee) / trade.buy_num
				trade.margin = int(trade.margin) - int(trade.buy_total_price) - int(trade.buy_fee)
				buy_for_tax = trade.buy_total_price - trade.buy_fee
				#Debug
				if(sim.debug):
					print dt.year,dt.month,dt.day
					print "Buy = ",trade.buy_total_price," Num =",trade.buy_num
					#print "10 days Close avg. =",avg_close			
					print "wish buy price =",wish_buy_price
					print "Buyed price =",trade.buy_price
					print "money = " + str(trade.margin)
				trade.buy_date = date_str
				sim_data += str(date_str) + "," + str(trade.buy_price) + "," + str(trade.sell_price) + "\n"
				trade.hold_num += trade.buy_num
				trade.do_buy = 1
				trade.do_sell = 0
				#flag_buy = 1
				resource = trade.buy_num * today_close + trade.margin
				#Log
				sim.resource_log.append(resource)
				#tmp_time += one_day
				continue
		if(int(trade.hold_num) > 0 and trade.do_sell == 0):
			#print "SELL"
			sell_price = 0
			wish_sell_price, trade.sell_type = trade.rule.sell(stock,trade,dt)
			#trade.do_sell = 1
			if(wish_sell_price > 0):
				sell_price = sim_sell(stock,trade,dt,int(wish_sell_price))
				#print "Sell price =",sell_price,", wish =",wish_sell_price
				#time.sleep(10)
			if(sell_price > 0):
				trade.sell_total_price = sell_price
				trade.sell_price = trade.sell_total_price / trade.sell_num
				trade.sell_fee = trade.agent.get_fee(trade.sell_total_price,trade.sell_type)
				sell_for_tax = trade.sell_total_price - trade.sell_fee
				trade.tax = get_tax(sell_for_tax,sell_for_tax)
				trade.margin = trade.margin + trade.sell_total_price - trade.sell_fee - trade.tax
				#Debug
				if(sim.debug):
					print dt.year,dt.month,dt.day
					print "Sell =",trade.sell_total_price, ", Num=",trade.sell_num
					print "Selled =",trade.sell_price
					print "money = " + str(trade.margin)
					buy_sell_num += 1
					print "Trade num = " + str(buy_sell_num)

				last_sell_price = int(trade.sell_price)
				trade.sell_date = date_str
				sim_data += str(date_str) + "," + str(trade.buy_price) + "," + str(trade.sell_price) + "\n"
				trade.hold_num -= trade.sell_num
				trade.do_buy = 0
				trade.do_sell = 1
				resource = trade.margin
				sim.resource_log.append(resource)
				#tmp_time += one_day
				continue
		resource = trade.margin
		if(trade.do_buy):
			resource = trade.hold_num * int(today_close) + trade.margin
		#Log
		sim.resource_log.append(resource)
		#tmp_time += one_day
		#TIME_SUM += one_day
	if(trade.do_buy):
		money = trade.hold_num * int(today_close) + trade.margin
		print "Last money =", money
	else:
		print "Last money =", trade.margin
	#
	dp.write_file(LOG_DIR,SIMU_LOG,sim_data)



def sim_buy(stock,trade,dt,price):
	#print dt.year,dt.month,dt.day
	buy_price = 0
	if(trade.buy_type == 1):
		#nari
		buy_price = trade.price
	elif(trade.buy_type == 0):
		#sasi
		if(int(price) >= int(trade.low)):
			#print "Buy"
			buy_price = price
			if(int(price) > int(trade.high)):
				buy_price = trade.high
		else:
			buy_price = 0
	if(buy_price > 0):
		trade.buy_num = int((float(trade.margin) - float(trade.limit)) / float(buy_price))
		trade.buy_num  = trade.buy_num  - (int(trade.buy_num) % int(stock.unit))

	total = int(buy_price) * int(trade.buy_num)
	return total

def sim_sell(stock,trade,dt,price):
	sell_price = 0
	if(trade.sell_type == 1):
		#nari
		sell_price = trade.price
	elif(trade.sell_type == 0):
		#sasi
		if(int(price) <= int(trade.high)):
			sell_price = price
			if(int(price) < int(trade.low)):
				sell_price = trade.low
		else:
			sell_price = 0
	total = int(sell_price) * int(trade.sell_num)
	return total

def get_tax(buy,sell):
	gain = sell - buy
	tax = 0
	if(gain > 0):
		tax = int(gain * 0.1)
	return tax

if __name__ == "__main__":
	main()
