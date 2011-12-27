#!/usr/bin/python

import os
import sys
from urllib2 import urlopen
import datetime
from matplotlib.cbook import iterable
import numpy as np
sys.path.append('./lib/')
import data_process as dp
DATA_DIR = "./data/"
START_YEAR = 2000
START_MONTH = 1
START_DAY = 1

def get_stock_data(stock_ids):
	for stock_id in stock_ids:
		startdate = datetime.date(START_YEAR,START_MONTH,START_DAY)
		today = enddate = datetime.date.today()
		fetch_historical_yahoo(stock_id, startdate, enddate)


def fetch_historical_yahoo(ticker, date1, date2):
	ticker = ticker.upper()
	if iterable(date1):
		d1 = (date1[1]-1, date1[2], date1[0])
	else:
		d1 = (date1.month-1, date1.day, date1.year)
	if iterable(date2):
		d2 = (date2[1]-1, date2[2], date2[0])
	else:
		d2 = (date2.month-1, date2.day, date2.year)
	g='d'

	urlFmt = 'http://table.finance.yahoo.com/table.csv?a=%d&b=%d&c=%d&d=%d&e=%d&f=%d&s=%s&y=0&g=%s&ignore=.csv'


	url =  urlFmt % (d1[0], d1[1], d1[2],
					 d2[0], d2[1], d2[2], ticker, g)
	#print url

	urlfh = urlopen(url)
	datas = urlfh.read().split("\n")
	datas.pop(0)
	datas.pop(-1)
	datas.reverse()
	out_data = "\n".join(datas)
	dp.write_file(DATA_DIR,str(ticker) + ".csv",out_data)

