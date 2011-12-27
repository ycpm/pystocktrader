#!/usr/bin/python
# coding: UTF-8

#Get detail data from Yahoo JP
import urllib,urllib2
from string import *
#from math import *
#import urlparse
import os
import sys
import datetime
import time
import locale
import re
sys.path.append('./lib/')
import data_process as dp
import stock_conv as sc
#Global variable
#DATA_DIR = "./in_data/"
DATA_DIR = "./data/"
OUT_FILE = "stock_detail_"
OUT_FILE2 = "stock_detail.csv"
EXT = ".csv"
DATA_SITE1 = "http://stocks.finance.yahoo.co.jp/stocks/detail/?code="
DATA_SITE2 = "http://profile.yahoo.co.jp/consolidate/"

STOCK_ID_MIN = 1300
#STOCK_ID_MIN = 8678
STOCK_ID_MAX = 9999

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

INI_DATA = "1001,日経２２５" + ",0,11,0,0,0,0,0,0,0,0\n"
INI_DATA += "1002,ＴＯＰＩＸ" + ",0,11,0,0,0,0,0,0,0,0\n"
INI_DATA += "1003,Ｃｏｒ３０" + ",0,11,0,0,0,0,0,0,0,0\n"
INI_DATA += "1004,Ｌａｒ７０" + ",0,11,0,0,0,0,0,0,0,0\n"
INI_DATA += "1005,ＴＰ１００" + ",0,11,0,0,0,0,0,0,0,0\n"
INI_DATA += "1006,Ｍｉ４００" + ",0,11,0,0,0,0,0,0,0,0\n"
INI_DATA += "1007,ＴＰ５００" + ",0,11,0,0,0,0,0,0,0,0\n"
INI_DATA += "1008,Ｓｍａｌｌ" + ",0,11,0,0,0,0,0,0,0,0\n"
INI_DATA += "1011,ＴＰＸ大型" + ",0,11,0,0,0,0,0,0,0,0\n"
INI_DATA += "1012,ＴＰＸ中型" + ",0,11,0,0,0,0,0,0,0,0\n"
INI_DATA += "1013,ＴＰＸ小型" + ",0,11,0,0,0,0,0,0,0,0\n"
INI_DATA += "1020,ＪＱＩＤＸ" + ",0,11,0,0,0,0,0,0,0,0\n"
INI_DATA += "1021,Ｊ−ＳＴＫ" + ",0,11,0,0,0,0,0,0,0,0\n"
#東証1部,東証2部,,JQS,大証1部,大証2部,JQG,名証1部,東証マザーズ
#1：東証1部
#2：東証2部
#3：東証マザ－ズ
#4：ジャスダック
#6：大証1部
#7：大証2部
#8：ヘラクレス
#MAKET_DICT = {'東証1部': 1, '東証2部': 2,'東証マザ－ズ': 3, 'JQS': 4, 'JQG': 4, '大証1部': 6,'大証2部': 7, 'ヘラクレス': 8, '名証1部': 9, '名証2部': 10, '東証': 11, '大証': 11, '福岡Q':11, '東証外国':11, '名証':11, '福証':11, 'マザーズ':3, '札証':11, 'JASDAQ':4, '名古屋セ':11, '札幌ア':11, 'HCG':8,'HCS':8, 'JQ外国部':11, '大証外国部':11}
def get_detail_data(w):
	global STOCK_ID_MIN, STOCK_ID_MAX, OUT_FILE, EXT, STOCK_ID_MIN, STOCK_ID_MAX
	#stock_id = 4689	#Yahoo
	#stock_id = 1000
	today_data = datetime.datetime.today()
	file_name = OUT_FILE + str(today_data.year) + "_" + str(today_data.month) + "_" + str(today_data.day) + EXT
	out_data = INI_DATA
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
	#u = data.decode('euc_jp')
	#u = data.decode('shift-jis')
	return u.encode('utf-8')

def cut_html_tag(data):
	p = re.compile(r'<.*?>')
	return p.sub('', data)
if __name__ == "__main__":
	main()
