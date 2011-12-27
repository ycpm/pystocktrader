#!/usr/bin/python
# coding: UTF-8
import sys
import datetime
import time
import re
import locale
sys.path.append('./lib/')
import data_process as dp

def get_fee(price,buy_type):
	fee = 0
	#SBI
	if(price <= 0):
		return 0
	elif(price <= 20000):
		fee = 650	#sashi
		if(buy_type):	#Nari
			fee = 105
	elif(price <= 200000):
		fee = 1025	#sashi
		if(buy_type):	#Nari
			fee = 500
	elif(price <= 1000000):
		fee = 1575	#sashi
		if(buy_type):	#Nari
			fee = 1050
	elif(price <= 10000000):
		fee = 2415	#sashi
		if(buy_type):	#Nari
			fee = 1890
	elif(price > 10000000):
		tmp = price - 10000000
		m = int(tmp / 1000000.0)
		fee = 2415 + m*42	#sashi
		if(buy_type):	#Nari
			fee = 1890 + m*42
	return fee

if __name__ == "__main__":
	main()
