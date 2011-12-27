#!/usr/bin/python
# coding: UTF-8

import urllib,urllib2
from string import *
import os
import sys
import datetime
import time
import locale
import re
sys.path.append('./lib/')
import stock_conv as sc
import data_process as dp
#Global variable
DATA_DIR = "./data/"
DATA_SITE = "http://table.yahoo.co.jp/t?"
START_YEAR = 2000
#START_YEAR = 2011
#START_MONTH = 1
#START_DAY = 4

STOCK_ID_MIN = 1300
STOCK_ID_MAX = 9999

#STOCK_IDS = [4689,8473]

def get_stock_data(stock_ids):
	for stock_id in stock_ids:
		#print stock_id
		download_all_year(stock_id)
def get_next_date(stock_id):
	data_file = str(stock_id) + ".csv"
	datas = dp.open_file(DATA_DIR,data_file)
	#print datas[-2]
	last_datas = datas[-2].split(",")
	last_date = last_datas[0]
	#print last_date
	year,month,day = last_date.split("-")
	dnum = time.mktime((int(year),int(month),int(day),0,0,0,0,0,0))
	next_dnum = dnum + 86400
	next_date = time.localtime(next_dnum)
	#print next_date.tm_year,next_date.tm_mon,next_date.tm_mday
	return next_date

def code_conv(data):
	u = data.decode('euc_jisx0213')
	return u.encode('utf-8')

def cut_html_tag(data):
	p = re.compile(r'<.*?>')
	tmp = p.sub('', data)
	p = re.compile(r'&.*?;')
	tmp = p.sub('', tmp)
	return tmp

def download_all_year(stock_id):
	#if(int(stock_id) < STOCK_ID_MIN or int(stock_id) > STOCK_ID_MAX):
	#if(int(stock_id) < STOCK_ID_MIN):
		#print stock_id,STOCK_ID_MIN
		#return False
	today_data = datetime.datetime.today()
	year = START_YEAR
	month = 1
	day = 1
	file_name = DATA_DIR + str(stock_id) + ".csv"
	if(os.path.isfile(file_name)):
		n_date = get_next_date(stock_id)
		year = n_date.tm_year
		month = n_date.tm_mon
		day = n_date.tm_mday
	out_data = ""	
	while year <= today_data.year:
		while month <= 12:
			if(year == today_data.year and month > today_data.month ):
				break
			print year, month
			csv_data = download_data(stock_id,year,month,day)
			#print csv_data
			out_data += csv_data
			month += 2
		year += 1
		month = 1
		day = 1
	file_name = DATA_DIR + str(stock_id) + ".csv"
	if(os.path.isfile(file_name)):
		print "Same file exist : " + str(file_name)
		if(out_data):
			dp.add_file(DATA_DIR,str(stock_id) + ".csv",out_data)
	else:
		dp.write_file(DATA_DIR,str(stock_id) + ".csv",out_data)


def download_data(stock_id,year,month,day):
	global DATA_DIR, DATA_SITE
	one_day = 86400
	next_year = year
	next_month = month + 1
	next_next_year = year
	next_next_month = month + 2
	if(month>=12):
		next_month = 1
		next_next_month = 2
		next_year = year + 1
		next_next_year = year + 1
	if(next_month>=12):
		next_next_month = 1
		next_next_year = year + 1
	end_time = int(time.mktime((next_next_year,next_next_month,1,0,0,0,0,0,0))) - 86400
	end_date = time.localtime(end_time)

	url=str(DATA_SITE) + "c=" + str(year) + "&a=" + str(month) + "&b=" + str(day) +"&f=" + str(next_year) + "&d=" + str(next_month) + "&e=" + str(end_date.tm_mday)  + "&g=d&s=" + str(stock_id) + "&y=0&z=" + str(stock_id)
	#print url
	csv_data = get_data_parse(url)
	return csv_data


def get_data_parse(url):
	try:
		f = urllib2.urlopen(url)
	except urllib2.HTTPError, e:
		#e.code, e.msg
		print e.code
		print e.msg
		return
	else:
		flag1 = 0
		flag2 = 0
		return_data = ""
		tmp_data = []
		market = "11"
		while 1:
			#data = conv(f.readline())
			data = code_conv(f.readline())
			if not data:
				break
			#print data
			if(re.search('<span class="yjM">【',data)):
				dm,market = data.split("【")
				market,dm = market.split(":")
				market = sc.market2num(market)
			if(re.search(">終値<",data)):
				#print "find"
				flag1=1
			if(re.search("年",data) and flag1==1):
				#print "find year"
				tmp_data = []
				flag2=1
			if(re.search("</tr>",data) and flag2==1):
				tmp_line = ",".join(tmp_data)
				return_data= tmp_line + "\n" + return_data
				#print tmp_datas
				flag2=0
			if(re.search("</table>",data) and flag1==1):
				flag1=0
			if(flag2==1):
				if(re.search("年",data)):
					data = cut_html_tag(data)
					#print data
					p1 = re.compile(r'\D+')
					tmp_year,tmp_month,tmp_day = p1.split(data)[0:3]
					#print str(tmp_year) + "-" + str(tmp_month) + "-" + tmp_day
					tmp = str(tmp_year) + "-" + str(tmp_month) + "-" + str(tmp_day) + "," + str(market)
				else:
					data=data.rstrip()
					p2 = re.compile(r'<.*?>')
					tmp = p2.sub('', data)
					tmp = tmp.replace(',', '')
				#print tmp
				tmp_data.append(tmp)
			#print flag2
		f.close()
		#print return_data
		return return_data

