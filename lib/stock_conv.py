#!/usr/bin/python
# coding: UTF-8

import re
from string import *
import os
import sys

STOCK_ID_MIN = 1300
STOCK_ID_MAX = 9999

index = [
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
index_jp =[
"日経平均株価",
"TOPIX",
"ジャスダックインデックス",
"NYダウ",
"ナスダック総合",
"S＆P 500",
"香港ハンセン",
"上海総合",
"韓国 総合",
"台湾 加権",
"英FTSE 100",
"その他",
"その他",
"その他",
"その他",
"その他",
"その他",
"その他",
"その他",
"その他",
"その他",
"その他",
"その他",
]
index_en =[
"NIKKEI",
"TOPIX",
"JASDQ",
"NYダウ",
"NASDQ",
"SP 500",
"HK",
"Shaghai",
"Korea",
"TW",
"FTSE 100",
"other",
"other",
"other",
"other",
"other",
"other",
"other",
"other",
"other",
"other",
"other",
"other",
]

num2cate = [
"その他",
"電気・ガス業",
"卸売業",
"水産・農林業",
"鉱業",
"小売業",
"通信業",
"陸運業",
"海運業",
"空運業",
"倉庫・運輸関連業",
"サービス業",
"不動産業",
"建設業",
"銀行業",
"保険業",
"証券業",
"その他金融業",
"医薬品",
"輸送用機器",
"パルプ・紙",
"食料品",
"非鉄金属",
"ゴム製品",
"電気機器",
"繊維製品",
"機械",
"金属製品"
"鉄鋼",
"精密機器",
"ガラス・土石製品",
"化学",
"石油・石炭製品",
"その他製品",
"REIT",
"その他",
"その他",
"その他",
"その他",
"その他",
"その他",
"その他",
]

num2market = [
"その他",
"東証1部",
"東証2部",
"マザ－ズ",
"JASDAQ",
"その他",
"大証1部",
"大証2部",
"ヘラクレス",
"名証1部",
"名証2部",
"その他",
"その他",
]
def code2index_num(code):
	if(re.search("998407",str(code))):
		return 0
	if(re.search("998405",str(code))):
		return 1
	if(re.search("23337",str(code))):
		return 2
	if(re.search("^DJI",str(code))):
		return 3
	if(re.search("^IXIC",str(code))):
		return 4
	if(re.search("^GSPC",str(code))):
		return 5
	if(re.search("^HSI",str(code))):
		return 6
	if(re.search("000001.SS",str(code))):
		return 7
	if(re.search("^KS11",str(code))):
		return 8
	if(re.search("^TWII",str(code))):
		return 9
	if(re.search("^FTSE",str(code))):
		return 10
	return 20	#other
def cate2num(cate):
	#
	if(re.search("電気・ガス業",cate)):
		return 1
	if(re.search("卸売業",cate)):
		return 2
	if(re.search("水産・農林業",cate)):
		return 3
	if(re.search("鉱業",cate)):
		return 4
	if(re.search("小売業",cate)):
		return 5
	if(re.search("通信業",cate)):
		return 6
	if(re.search("陸運業",cate)):
		return 7
	if(re.search("海運業",cate)):
		return 8
	if(re.search("空運業",cate)):
		return 9
	if(re.search("倉庫・運輸関連業",cate)):
		return 10
	if(re.search("サービス業",cate)):
		return 11
	if(re.search("不動産業",cate)):
		return 12
	if(re.search("建設業",cate)):
		return 13
	if(re.search("銀行業",cate)):
		return 14
	if(re.search("保険業",cate)):
		return 15
	if(re.search("証券業",cate)):
		return 16
	if(re.search("その他金融業",cate)):
		return 17
	if(re.search("医薬品",cate)):
		return 18
	if(re.search("輸送用機器",cate)):
		return 19
	if(re.search("パルプ・紙",cate)):
		return 20
	if(re.search("食料品",cate)):
		return 21
	if(re.search("非鉄金属",cate)):
		return 22
	if(re.search("ゴム製品",cate)):
		return 23
	if(re.search("電気機器",cate)):
		return 24
	if(re.search("繊維製品",cate)):
		return 25
	if(re.search("機械",cate)):
		return 26
	if(re.search("金属製品",cate)):
		return 27
	if(re.search("鉄鋼",cate)):
		return 28
	if(re.search("精密機器",cate)):
		return 29
	if(re.search("ガラス・土石製品",cate)):
		return 30
	if(re.search("化学",cate)):
		return 31
	if(re.search("石油・石炭製品",cate)):
		return 32
	if(re.search("その他製品",cate)):
		return 33
	if(re.search("REIT",cate)):
		return 34
	else:
		return 40

def market2num(market):
	#'東証1部': 1, '東証2部': 2,'東証マザ－ズ': 3, 'JQS': 4, 'JQG': 4, '大証1部': 6,'大証2部': 7, 'ヘラクレス': 8, '名証1部': 9, '名証2部': 10, 
	#'東証': 11, '大証': 11, '福岡Q':11, '東証外国':11, '名証':11, '福証':11, 'マザーズ':3, '札証':11, 'JASDAQ':4, '名古屋セ':11, '札幌ア':11, 
	#'HCG':8,'HCS':8, 'JQ外国部':11, '大証外国部':11}
	num = 0
	if(re.search("東証1部",market)):
		return 1
	elif(re.search("東証2部",market)):
		return 2
	elif(re.search("マザ－ズ",market)):
		return 3
	elif(re.search("外国",market)):
		return 11
	elif(re.search("JQ",market) or re.search("JASDAQ",market)):
		return 4
	elif(re.search("大証1部",market)):
		return 6
	elif(re.search("HC",market) or re.search("大証2部",market)):
		return 7
	elif(re.search("ヘラクレス",market)):
		return 8
	elif(re.search("名証1部",market)):
		return 9
	elif(re.search("名証2部",market)):
		return 10
	#elif(re.search("東証2部",market)):
	#	return 2
	#elif(re.search("東証2部",market)):
	#	return 2
	#elif(re.search("東証2部",market)):
	#	return 2
	#elif(re.search("東証2部",market)):
	#	return 2
	#elif(re.search("東証2部",market)):
	#	return 2
	#elif(re.search("東証2部",market)):
	#	return 2
	#elif(re.search("東証2部",market)):
	#	return 2
	else:
		return 11
