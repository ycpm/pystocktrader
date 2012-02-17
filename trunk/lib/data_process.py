#!/usr/bin/python
# coding: UTF-8
import datetime
import time
import pylab
import os
import numpy as np
from pylab import *
import re
stock_dt = np.dtype([('date', object),
                     ('year', np.int16),
                     ('month', np.int8),
                     ('day', np.int8),
                     ('dnum', np.float),     # mpl datenum
                     ('open', np.float),
                     ('close', np.float),
                     ('high', np.float),
                     ('low', np.float),
                     ('volume', np.float),
                     ('aclose', np.float)])

STOCK_MIN = 1300
STOCK_MAX = 9999

DAY_DATA = "DAY_"

def coeffs(datas,num):
	dn = len(datas)
	#n = int(dn / num)
	out = []
	for i in range(num, dn):
		#print "i =",i,", num =",num
		coeffs = polyfit(range(0,num), datas[i-num:i], 1)
		out.append(coeffs[0])
	out = np.array(out)
	#print len(out)
	return out
def ma_day(stock,dt,num):
	n = num + 5
	r = dp.get_data_by_day_num(stock,dt,n)
	ma = dp.moving_average(r.close, num)
	return ma[-1]
def rsi_day(stock,dt,num=14):
	n = num + 5
	r = dp.get_data_by_day_num(stock,dt,n)
	rsi = dp.relative_strength(r.close)
	return rsi[-1]

def coeff_day(stock,dt,num):
	n = num + 5
	r = dp.get_data_by_day_num(stock,dt,n)
	coeffs,yfit=dp.get_fit_data(range(0, num),r.close[-num-1:-1])
	return coeffs[0]

def average(datas):
	a = np.array(datas)
	t = np.sum(a)
	avg = np.average(a)
	var = np.var(a)
	std = np.std(a)
	std_score = np.round_(50+10*(a-avg)/std)
	return a,t,avg,var,std,std_score
def rci_array(prices, n=9):
	rci_a = np.zeros_like(prices)
	for i in range(n, len(prices)):
		tmp_prices = prices[:i]
		rci_a[i] = rci(tmp_prices, n)
	rci_a[:n]=rci_a[n]
	return rci_a
def rci(prices, n=5):
	data = prices[-n-1:]
	data = data[::-1]	#reverse
	sort_data = sort(data)
	sort_data = sort_data[::-1]	#reverse
	#argsort_data = np.argsort(data)

	#print prices
	#print data
	#print sort_data
	#print argsort_data
	price_cnt = {}
	price_rnk = {}
	for i in range(0, len(sort_data)):
		#print "price =",sort_data[i]
		if not price_cnt.has_key(str(sort_data[i])):
			price_cnt[str(sort_data[i])] = 1
		else:
			price_cnt[str(sort_data[i])] += 1
		if not price_rnk.has_key(str(sort_data[i])):
			price_rnk[str(sort_data[i])] = i+1
		else:
			price_rnk[str(sort_data[i])] += i+1
		#print "price rank =",price_rnk[str(sort_data[i])]
	sum_rank_diff2=0
	for i in range(0, len(data)):
		rank = float(price_rnk[str(data[i])]) / float(price_cnt[str(data[i])])
		#print "price =",data[i]
		#print "i =",i
		#print "price count =",price_cnt[str(data[i])]
		#print "price rank =",rank
		rank_diff = rank - i -1
		rank_diff2 =  rank_diff * rank_diff
		#print "rank diff =",rank_diff
		sum_rank_diff2 += rank_diff2
	#http://system-trading.jp/takahashi/index.php?ID=53
	rci =(1-(6*sum_rank_diff2)/(n*(n*n-1)))*100
	return rci
	
def moving_average(x, n, type='simple'):
	"""
	compute an n period moving average.
	type is 'simple' | 'exponential'
	"""
	if type=='simple':
		weights = np.ones(n)
	else:
		weights = np.exp(np.linspace(-1., 0., n))
	weights /= weights.sum()
	a =  np.convolve(x, weights, mode='full')[:len(x)]
	a[:n] = a[n]
	return a

def relative_strength(prices, n=14):
	"""
	compute the n period relative strength indicator
	http://stockcharts.com/school/doku.php?id=chart_school:glossary_r#relativestrengthindex
	http://www.investopedia.com/terms/r/rsi.asp
	"""

	deltas = np.diff(prices)
	seed = deltas[:n+1]
	up = seed[seed>=0].sum()/n
	down = -seed[seed<0].sum()/n
	rs = up/down
	rsi = np.zeros_like(prices)
	rsi[:n] = 100. - 100./(1.+rs)

	for i in range(n, len(prices)):
		delta = deltas[i-1] # cause the diff is 1 shorter
		if delta>0:
			upval = delta
			downval = 0.
		else:
			upval = 0.
			downval = -delta
		up = (up*(n-1) + upval)/n
		down = (down*(n-1) + downval)/n
		rs = up/down
		rsi[i] = 100. - 100./(1.+rs)
	return rsi

def moving_average_convergence(x, nslow=26, nfast=12):
	"""
	compute the MACD (Moving Average Convergence/Divergence) using a fast and slow exponential moving avg'
	return value is emaslow, emafast, macd which are len(x) arrays
	"""
	emaslow = moving_average(x, nslow, type='exponential')
	emafast = moving_average(x, nfast, type='exponential')
	return emaslow, emafast, emafast - emaslow

def get_fit_data(xdatas,ydatas,num = 1):
	coeffs = polyfit(xdatas, ydatas, int(num))
	yfit = polyval(coeffs, xdatas)
	return coeffs,yfit
def dc_cut(datas):
	data_min = 1000000000000000000.0
	data_max = - data_min
	out_datas = []
	for data in datas:
		if(float(data) > data_max):
			data_max = float(data)
		elif(float(data) < data_min):
			data_min = float(data)
	data_mid = (data_max + data_min) / 2.0
	for data in datas:
		out_datas.append(float(data) - data_mid)
	return out_datas

def get_price_history(stock):
	price_data = open_file(stock.data_dir,str(stock.id)+".csv")
	csv_data = []
	#date = "2010-1-1"
	for data in price_data:
		if not data:
			continue
		date,price = data.split(",")
		date,dm = date.split(" ")
		csv_data.append(str(date) + ",1," + str(price) + "," + str(price) + "," + str(price) + "," + str(price) + ",0," +  str(price))
	return csv2rec(csv_data)

def csv2rec(csv_datas):
	results = []
	for csv in csv_datas:
		if not csv:
			continue
		#if(re.search("株",csv)):	#分割
			#continue
		stock_datas=csv.split(",")
		year,month,day=stock_datas[0].split('-')
		dt = datetime.datetime(int(year),int(month),int(day))
		dnum = time.mktime((int(year),int(month),int(day),0,0,0,0,0,0))
		if len(stock_datas) < 4:	#Divide
			continue
		open = stock_datas[2]
		high = stock_datas[3]
		low = stock_datas[4]
		close = stock_datas[5]
		if(len(stock_datas) < 7):
			#stock_datas.append("0")	#vol
			#stock_datas.append(stock_datas[5])	#close -> adj_close
			vol = "0"
			aclose = stock_datas[5]
		elif(len(stock_datas) < 8):
			if(float(stock_datas[4]) <= float(stock_datas[2]) and float(stock_datas[4]) >= float(stock_datas[3])):		#US
				open,high,low,close,vol,aclose = stock_datas[1:]
			else:
				#stock_datas.append(stock_datas[5])	#close -> adj_close
				vol = stock_datas[6]
				aclose = stock_datas[5]
		else:
			vol = stock_datas[6]
			aclose = stock_datas[7]
		results.append((dt, dt.year, dt.month, dt.day, dnum, open, close, high, low, vol,aclose))
	r = np.array(results, dtype=stock_dt)
	r = r.view(np.recarray)
	#r = np.recarray(results, dtype=stock_dt)
	#names = ('date','year','month','day','dnum','open', 'close', 'high', 'low', 'volume', 'aclose')
	#r = np.rec.fromrecords(results, names=names)
	return r

def get_updown_num(stock,num):
	datas = stock.datas[-num-1:]
	ud_num=0
	last_close = -1
	for data in datas:
		if not data:
			continue
		data = data.strip()
		stock_datas = data.split(',')
		open = stock_datas[2]
		#high = stock_datas[3]
		#low = stock_datas[4]
		close = stock_datas[5]
		if(last_close < 0):
			last_close = close
		if(float(open) < float(close)):
			if(ud_num>=0):
				ud_num +=1
			else:
				ud_num =1
		elif(float(open) > float(close)):
			if(ud_num<=0):
				ud_num -=1
			else:
				ud_num =-1
		else:
			if(float(open) > float(last_close)):
				if(ud_num>=0):
					ud_num +=1
				else:
					ud_num =1
			elif(float(open) < float(last_close)):
				if(ud_num<=0):
					ud_num -=1
				else:
					ud_num =-1
			else:
				ud_num=0
		last_close = close
	return ud_num
def get_all_datas(stock):
	if(re.search(DAY_DATA,str(stock.id))):
		file_name = str(stock.id) + ".csv"
		pdata = open_file(stock.data_dir,file_name)
		data = []
		for val in pdata:
			val.strip()
			if not val:
				continue
			date,price =val.split(",")
			date,dm = date.split(" ")
			data.append(str(date) + ",1," + str(price) + "," + str(price) + "," + str(price) + "," + str(price) + ",0," +  str(price))
	else:
		file_name = str(stock.id) + ".csv"
		data = open_file(stock.data_dir,file_name)
	if len(data) > 0:
		str(data[-1]).strip()
		if not data[-1]:
			data.pop(-1)
		#return  csv2rec(datas)
	return data
def get_last_ndata(stock,num):
	ret_datas = []
	if len(stock.datas) > int(num):
		ret_datas = stock.datas[-num-1:]
	else:
		ret_datas = stock.datas
	return csv2rec(ret_datas)
def get_data_by_day_num(stock,dt,num):
	base_time = int(time.mktime((int(dt.year),int(dt.month),int(dt.day),0,0,0,0,0,0)))
	#file_name = str(stock.id) + ".csv"
	#if(int(stock.id) < 1000):
		#return get_price_history()
	#datas = open_file(stock.data_dir,file_name)
	out_data = []
	tmp_data=""
	for data in stock.datas:
	#for data in open_file(stock.data_dir,file_name):
		if not data:
			continue
		data = data.strip()
		stock_datas = data.split(',')
		if(int(stock.market[0]) == 0 or int(stock_datas[1]) == int(stock.market[0])):
			#yahoo
			data_year,data_month,data_day = stock_datas[0].split('-')
			#
			data_time = int(time.mktime((int(data_year),int(data_month),int(data_day),0,0,0,0,0,0)))
			if(data_time <= base_time):
				#out_data.append(tmp_data)
				out_data.append(data)
	start_num = -(int(num)+1)
	return_data = out_data[start_num:-1]
	#return return_data
	return  csv2rec(return_data)

def get_data_by_day(stock,s_dt,end_year=0,end_month=0,end_day=0):
	start_time = int(time.mktime((int(s_dt.year),int(s_dt.month),int(s_dt.day),0,0,0,0,0,0)))
	end_time = start_time
	if(end_year > 1980):
		end_time = int(time.mktime((end_year,end_month,end_day,0,0,0,0,0,0)))
		if(end_time <= start_time):
			end_time = start_time
	#file_name = str(stock.id) + ".csv"
	#datas = open_file(stock.data_dir,file_name)
	out_data = []
	tmp_data=""
	for data in stock.datas:
		if not data:
			continue
		data = data.strip()
		#print data
		#yahoo
		#date,open_val,high,low,close_val,vol,aclose = data.split(',')
		#
		stock_datas = data.split(',')
		#print stock.market,data
		#print stock.market[0],market
		if(int(stock.market[0]) == 0 or int(stock_datas[1]) == int(stock.market[0])):
			#print "market"
			data_year,data_month,data_day = stock_datas[0].split('-')
			data_time = int(time.mktime((int(data_year),int(data_month),int(data_day),0,0,0,0,0,0)))
			if(data_time >= start_time and data_time <= end_time):
				#print "ok"
				#tmp_data=str(date) + "," + str(open_val) + "," + str(high) + "," + str(low) + "," + str(close_val) + "," + str(vol)
				#out_data.append(tmp_data)
				out_data.append(data)
	#print out_data
	#return out_data
	return  csv2rec(out_data)
def get_data_by_num(stock,start_num,end_num=0):
	#global TMP_DATA_DIR
	#file_name = str(stock.id) + ".csv"
	#datas = open_file(stock.data_dir,file_name)
	tmp_start_num = -(int(start_num)+1)
	tmp_end_num = -(int(end_num)+1)
	tmp_datas = []
	for data in stock.datas:
		#print data
		if(data):
			stock_datas=data.split(",")
			if(int(stock.market[0]) == 0 or int(stock_datas[1]) == int(stock.market[0])):
				tmp_datas.append(data)
	tmp_datas.append(" ")
	return_datas = tmp_datas[tmp_start_num:tmp_end_num]
	#return return_data
	return  csv2rec(return_data)

def get_stock_detail(stock):
	#print stock.id,STOCK_MIN
	if not is_num(stock.id):
		stock.market = [0]
		stock.unit = 1
		return
	if(int(stock.id) < STOCK_MIN or int(stock.id) > STOCK_MAX):
		#print stock.id
		stock.market = [11]
		stock.unit = 1
		return
	datas = open_file(stock.detail_dir,stock.detail_file)
	for data in datas:
		if not data:
			continue
		data = data.strip()
		#in_stock_id,name,category,stock_market,num,dividend,per,pbr,eps,bps,unit,yutai = data.split(',')
		#決算期12,決算発表日13,決算月数14,売上高[百万円]15,営業利益[百万円]net operating profit16,経常利益[百万円]ordinary profit17,当期利益[百万円]18,EPS（一株当たり利益）[円]19,調整一株当たり利益[円]20,BPS（一株当たり純資産）[円]21,総資産[百万円]total asset22,自己資本[百万円]23,資本金[百万円]24,有利子負債[百万円]25,自己資本比率[%]26,含み損益27,ROA（総資産利益率）[%]28,ROE（自己資本利益率）[%]29,総資産経常利益率[%]30
		datail_data = data.split(',')
		#print "detail =",len(datail_data)
		if(int(stock.id) == int(datail_data[0])):
		#if(stock.id == datail_data[0]):
			stock.name = datail_data[1]	#企業名
			stock.category = datail_data[2]	#業種
			if(datail_data[3].find(" ")):
				stock.market = datail_data[3].split(" ")
			else:
				stock.market[0] = int(datail_data[3])
			stock.num = int(datail_data[4])	#発行株数
			stock.dividend = datail_data[5]	#配当
			stock.per = float(datail_data[6])	#PER（株価収益率）
			stock.pbr = float(datail_data[7])	#PBR（株価純資産倍率）
			stock.eps = float(datail_data[8])	#EPS（一株当たり利益）[円]
			stock.bps = float(datail_data[9])	#BPS（一株当たり純資産）[円]
			stock.unit = int(datail_data[10])	#単元株
			stock.compliment = int(datail_data[11])	#株式優待
			if(len(datail_data) > 12):
				stock.nop = int(datail_data[16])	#営業利益
				stock.op = int(datail_data[17])	#経常利益
				stock.np = int(datail_data[18])	#当期利益 net profit
				stock.ta = int(datail_data[22])	#総資産
				stock.lc = int(datail_data[22])	#資本金
				if(is_num(datail_data[26])):
					stock.er = float(datail_data[26])	#自己資本比率[%]
				if(is_num(datail_data[28])):
					stock.roa = float(datail_data[28])	#ROA（総資産利益率）[%]
				if(is_num(datail_data[29])):
					stock.roe = float(datail_data[29])	#ROE（自己資本利益率）[%]
			return

def get_day_average(stock,dt,num):
	datas = get_stock_by_day_num(stock,dt,num)
	total_open = 0
	total_close = 0
	total_high = 0
	total_low = 0
	for data in datas:
		date,open_val,high,low,close_val,vol = data.split(',')
		total_open += int(open_val)
		total_close += int(close_val)
		total_high += int(high)
		total_low += int(low)
	open_avg = total_open / int(num)
	close_avg = total_close / int(num)
	high_avg = total_high / int(num)
	low_avg = total_low / int(num)
	return str(date) + "," + str(open_avg) + "," + str(high_avg) + "," + str(low_avg) + "," + str(close_avg)

def diff_day(date1,date2):
	year1,month1,day1 = date1.split("-")
	year2,month2,day2 = date2.split("-")
	time1 = int(time.mktime((int(year1),int(month1),int(day1),0,0,0,0,0,0)))
	time2 = int(time.mktime((int(year2),int(month2),int(day2),0,0,0,0,0,0)))
	diff_time = time2 - time1
	#one_day = datetime.timedelta(1)
	one_day = 86400
	diff_day = int(float(diff_time) / float(one_day))
	return diff_day

def write_file(dirname,filename,datas):
	file_name = os.path.join(dirname, filename)
	if(datas):
		f = open(file_name, 'w')
		f.write(datas)
		f.close()
	else:
		print "ERROR : No save data"
def add_file(dirname,filename,datas):
	file_name = os.path.join(dirname, filename)
	if(datas):
		f = open(file_name, 'a')
		f.write(datas)
		f.close()
	else:
		print "ERROR : No add data"

def is_num(value):
    return re.match(r'^(?![-+]0+$)[-+]?([1-9][0-9]*)?[0-9](\.[0-9]+)?$', '%s'%value) and True or False

def open_file(dirname, filename):
	file_name = os.path.join(dirname, filename)
	try:
		f = open(file_name,'r')
	except IOError, (errno, strerror):
		print "Unable to open the file" + file_name + "\n"
		return []
	else:
		all_lines = f.read()
		return all_lines.split("\n")
