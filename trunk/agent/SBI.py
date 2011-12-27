#!/usr/bin/python
# coding: UTF-8
from string import *
import os
import sys
import datetime
import time
import locale
import re
sys.path.append('./lib/')
import data_process as dp

def get_fee(price,buy_type):
	fee = 0
	#SBI
	if(price <= 0):
		return 0
	elif(price <= 100000):
		fee = 145
	elif(price <= 200000):
		fee = 194
	elif(price <= 500000):
		fee = 358
	elif(price <= 1000000):
		fee = 639
	elif(price <= 1500000):
		fee = 764
	elif(price <= 30000000):
		fee = 1209
	else:
		fee = 1277
	return fee
