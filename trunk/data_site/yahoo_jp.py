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

#Get detail
OUT_FILE = "stock_detail_"
OUT_FILE2 = "stock_detail.csv"
EXT = ".csv"
DATA_SITE1 = "http://stocks.finance.yahoo.co.jp/stocks/detail/?code="
DATA_SITE2 = "http://profile.yahoo.co.jp/consolidate/"

indexs = [
998407,	#日経
998405,	#TOPIX
23337,	#JSDAQ
"^DJI",	#NYダウ
"^IXIC",	#NASDAQ
"^GSPC",	#米SP
"^HSI",	#香港ハンセン
"000001.SS",	#上海総合
"^BSESN",	#ムンバイSENSEX30
"^KS11",	#韓国 総合
"^TWII",	#台湾 加権
"^FTSE",	#英FTSE 100
]

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

#
#Get detail
#
def get_detail_data(w):
	global STOCK_ID_MIN, STOCK_ID_MAX, OUT_FILE, EXT, STOCK_ID_MIN, STOCK_ID_MAX
	#stock_id = 4689	#Yahoo
	#stock_id = 1000
	today_data = datetime.datetime.today()
	file_name = OUT_FILE + str(today_data.year) + "_" + str(today_data.month) + "_" + str(today_data.day) + EXT
	#out_data = INI_DATA
	out_data = ""
	stock_id_diff = STOCK_ID_MAX - STOCK_ID_MIN
	print file_name
	if(os.path.isfile(file_name)):
		print "Same file exist : " + str(file_name)
	else:
		i = STOCK_ID_MIN
		while i<= STOCK_ID_MAX:
			#print i
			pr=int((float(i - STOCK_ID_MIN)/float(stock_id_diff)) * 1000.0)
			if( not pr % 20.0):
				pr2 = pr/10
				#print "*********" ,pr/10, "%"
				w.progress.Update(pr2, 'Progress ...')
			url1=str(DATA_SITE1) + str(i)
			url2=str(DATA_SITE2) + str(i)
			print url1
			csv_data1 = get_detail_parse1(url1)
			if not csv_data1:
				i += 1
				continue
			print url2
			csv_data2 = get_detail_parse2(url2)
			if(csv_data1):
				#print "Get"
				out_data += csv_data1
			vals = ""
			if(csv_data2):
				for data in csv_data2:
					#print data
					#title += data[0] + ","
					#vals += str(data[1]) + " " + str(data[2]) + " " + str(data[3]) + ","
					vals += "," + str(data[1]) 
				#vals = vals.strip(",")
			out_data += vals + "\n"
			i += 1
		for index in indexs:
			url=str(DATA_SITE1) + str(index)
			csv_data3 = get_index_parse(url)
			out_data += csv_data3 + "\n"

		dp.write_file(DATA_DIR,file_name,out_data)	#BackUP
		dp.write_file(DATA_DIR,OUT_FILE2,out_data)

def get_detail_parse2(url):
	#req = urllib2.Request(url)
	try:
		f = urllib2.urlopen(url)
		#f = urllib2.urlopen(req)
	#except URLError, e:
	except urllib2.HTTPError, e:
		#e.code, e.msg
		print e.code
		print e.msg
		return
	else:
		flag1 = 0
		flag2 = 0
		flag_tr = 0
		return_data = ""
		last_data = ""
		markets = []
		tmp_datas = []
		datas = []
		print "start"
		while 1:
			data = f.readline()
			if not data:
				break
			#print data
			data = code_conv(data)
			#print data
			#決算期
			if(re.search("前期",data)):
				flag1 = 1
				#print "find zenki"

			if(flag1 == 1 and re.search("<tr bgcolor",data)):
				flag_tr = 1
				tmp_datas = []
				continue
			if(flag_tr == 1 and flag1 == 1 and flag2 == 1 and re.search("</tr>",data)):
				flag_tr = 0
				datas.append(tmp_datas)
				continue
			if(flag_tr == 1 and flag1 == 1 and re.search("<td ",data)):
				tmp = cut_html_tag(data)
				tmp = tmp.strip()
				if not tmp:
					continue
				if(re.search("日",tmp) and re.search("年",tmp)):
					tmp_year, tmp_month = tmp.split('年') 
					tmp_month, tmp_day = tmp_month. split('月')
					tmp_day,dm = tmp_day.split('日')
					tmp = str(tmp_year) + "-" + str(tmp_month) + "-" + str(tmp_day)
				if(re.search("年",tmp)):
					tmp_year,tmp_month = tmp.split('年') 
					tmp_month, dm = tmp_month.split('月') 
					tmp = str(tmp_year) + "-" + str(tmp_month)
				if(re.search("か月",tmp)):
					tmp,dm = tmp.split('か')
				if(re.search("百万円",tmp)):
					tmp,dm = tmp.split('百')
					if(not re.search("百万円",tmp_datas[0])):
						tmp_datas[0] += "[百万円]"
				elif(re.search("円",tmp)):
					tmp,dm = tmp.split('円')
					if(not re.search("円",tmp_datas[0])):
						tmp_datas[0] += "[円]"
				if(re.search("%",tmp)):
					tmp,dm = tmp.split('%')
					if(not re.search("%",tmp_datas[0])):
						tmp_datas[0] += "[%]"
				if(re.search("--",tmp)):
					tmp = 0
				if(re.search(",",str(tmp))):
					tmp = tmp.replace(',', '')
				tmp_datas.append(tmp)
				flag2 = 1
			if(flag1 == 1 and re.search("</table>",data)):
				flag1 = 0
				continue
		return datas
def get_index_parse(url):
	#req = urllib2.Request(url)
	try:
		f = urllib2.urlopen(url)
		#f = urllib2.urlopen(req)
	#except URLError, e:
	except urllib2.HTTPError, e:
		#e.code, e.msg
		print e.code
		#print e.msg
	#except:
		#error_dialog("Unable to open the file" + file_name + "\n",1)
		#print "Error"
		return
	else:
		flag1 = 0
		flag2 = 0
		return_data = ""
		last_data = ""
		markets = []
		while 1:
			#data = conv(f.readline())
			#data = code_conv(f.readline())
			data = f.readline()
			if not data:
				break
			if(re.search("一致する銘柄は見つかりませんでした",data)):
				#return False
				print "Not found"
				return
			if(re.search("<title>",data)):
				data = cut_html_tag(data)
				stock_data,dm = data.split('：')
				name,stock_id = stock_data.split('【')
				stock_id = stock_id.strip('】')
				flag1 = 1
		f.close()
		if(len(markets) > 1):
			#print markets
			stock_market = " ".join(map(str, markets))
		elif(len(markets) == 1):
			stock_market = markets[0]
		if(flag1):
			return_data = str(stock_id)+ "," + str(name) + ",0,11,0,0,0,0,0,0,0,0"
			return return_data
		else:
			print "un-normal"
		return
def get_detail_parse1(url):
	#req = urllib2.Request(url)
	try:
		f = urllib2.urlopen(url)
		#f = urllib2.urlopen(req)
	#except URLError, e:
	except urllib2.HTTPError, e:
		#e.code, e.msg
		print e.code
		#print e.msg
	#except:
		#error_dialog("Unable to open the file" + file_name + "\n",1)
		#print "Error"
		return
	else:
		flag1 = 0
		flag2 = 0
		return_data = ""
		last_data = ""
		markets = []
		while 1:
			#data = conv(f.readline())
			#data = code_conv(f.readline())
			data = f.readline()
			if not data:
				break
			if(re.search("一致する銘柄は見つかりませんでした",data)):
				#return False
				print "Not found"
				return
			#if(re.search("kabuSpHoldNo",data)):
				#print "find name"
				#data = cut_html_tag(data)
				#stock_id,data = data.split('】')
				#stock_id = stock_id.strip('【')
				#name,dm = data.split('&')
				#flag2 = 1
				#print name
			if(re.search("<title>",data)):
				data = cut_html_tag(data)
				stock_data,dm = data.split('：')
				name,stock_id = stock_data.split('【')
				stock_id = stock_id.strip('】')
			if(re.search("株主優待なし",data)):
				yutai = 0
			elif(re.search("株主優待あり",data)):
				yutai = 1
			if(re.search("市場：",data)):
				#print "find market"
				if(re.search("<select",data)):
					#print "markets"
					flag1=1
				else:
					if(re.search("業種：",data)):
						market,dm,category = data.split('</span>')
						category = cut_html_tag(category)
						category = category.strip()
					else:
						market,dm = data.split('</span>')
						category = "---"
					category = sc.cate2num(category)
					dm,market = market.split('：')
					#print market
					market = market.strip()
					market = sc.market2num(market)
					if not market:
						market = 11
					#print market
					markets.append(market)
			if(re.search("<option",data) and flag1==1):
				#print "markets"
				tmp_markets = data.split('</option>')
				for m in tmp_markets:
					tmp = cut_html_tag(m)
					market = tmp.strip()
					if not market:
						continue
					#print market
					market = sc.market2num(market)
					if not market:
						market = 11
					markets.append(market)
					#print tmp
				#flag1=0
			if(re.search("業種：",data) and flag1==1):
				dm,category = data.split('</span>')
				category = cut_html_tag(category)
				category = category.strip()
				category = sc.cate2num(category)
				flag1=0
				#print category
			#if(re.search("時価総額",data)):
			if(re.search(">発行済株式数<a",data)):
				#print last_data
				#print data
				num,dm = last_data.split('</strong>')
				num = cut_html_tag(num)
				num = num.replace(',', '')
				if(re.search("--",num)):
					flag2 = 0
				else:
					flag2 = 1
			#if(re.search("配当利回り",data)):
			if(re.search(">1株配当<",data)):
				dividend,dm = last_data.split('</strong>')
				dividend = cut_html_tag(dividend)
				dividend = dividend.replace(',', '')
				if(re.search("--",dividend)):
					dividend = 0
			if(re.search("PER<span",data) and flag2==1):	
				per,dm = last_data.split('</strong>')
				per = cut_html_tag(per)
				if(re.search("--",per)):
					#per = "---"
					per = 0
				else:
					dm,per = per.split(' ')
					per = per.replace(',', '')
			if(re.search("PBR<span",data) and flag2==1):
				pbr,dm = last_data.split('</strong>')
				pbr = cut_html_tag(pbr)
				if(re.search("--",pbr)):
					#pbr = "---"
					pbr = 0
				else:
					dm,pbr = pbr.split(' ')
					pbr = pbr.replace(',', '')
			if(re.search("EPS<span",data) and flag2==1):
				eps,dm = last_data.split('</strong>')
				eps = cut_html_tag(eps)
				if(re.search("--",eps)):
					#eps = "---"
					eps = 0
				else:
					dm,eps = eps.split(' ')
					eps = eps.replace(',', '')
			if(re.search("BPS<span",data) and flag2==1):
				bps,dm = last_data.split('</strong>')
				bps = cut_html_tag(bps)
				if(re.search("--",bps)):
					#bps = "---"
					bps = 0
				else:
					dm,bps = bps.split(' ')
					bps = bps.replace(',', '')
			if(re.search("単元株数",data) and flag2==1):
				unit,dm = last_data.split('</strong>')
				unit = cut_html_tag(unit)
				unit = unit.replace(',', '')
				if(re.search("--",unit)):
					unit = 1
			last_data = data
		f.close()
		#print stock_id
		#print category
		#print num
		#print dividend
		#print per
		#print pbr
		#print eps
		#print unit
		if(len(markets) > 1):
			#print markets
			stock_market = " ".join(map(str, markets))
		elif(len(markets) == 1):
			stock_market = markets[0]
		if(flag2):
			return_data = str(stock_id)+ "," + str(name) + "," + str(category) + "," + str(stock_market) + "," + str(num) + "," + str(dividend) + "," + str(per) + "," + str(pbr) + "," + str(eps) + "," + str(bps) + "," + str(unit) + "," + str(yutai)
			return return_data
		else:
			print "un-normal"
		return
def code_conv(data):
	u = data.decode('euc_jisx0213')
	return u.encode('utf-8')

def cut_html_tag(data):
	p = re.compile(r'<.*?>')
	tmp = p.sub('', data)
	p = re.compile(r'&.*?;')
	tmp = p.sub('', tmp)
	return tmp
