#!/usr/bin/python
# coding: UTF-8
from string import *
import os
import sys
import datetime
import time
import jholiday

MarketOpen = 9.0
MarketBreakStart = 11.0
MarketBreakEnd = 12.5
MarketClose = 15.0

#for debug
#MarketOpen = 21.6
#MarketBreakStart = 21.7
#arketBreakEnd = 21.8
#MarketClose = 21.9

def market_wait2():
	m_check = market_check()
	if(m_check==0):
		print "Market Close. Sleep till tomorrow.."
		wait_open(24.0)
	elif(m_check==2):
		print "Breack time"
		wait_open(MarketBreakEnd)
	elif(m_check==3):
		print "Before market open. Sleep till open"
		wait_open(MarketOpen)
	return 1
def market_wait():
	m_check = market_check()
	if(m_check==0):
		print "Market Close"
		return 0
	elif(m_check==2):
		print "Breack time"
		wait_open(MarketBreakEnd)
	elif(m_check==3):
		print "Before market open"
		wait_open(MarketOpen)
	return 1
def wait_open(END_TIME):
	time_now = time.localtime()
	now_sec= time_now.tm_hour * 3600 + time_now.tm_min * 60 + time_now.tm_sec
	open_sec = END_TIME * 3600
	if(open_sec <= now_sec):
		#print "No sleep"
		return
	wait_sec = int(open_sec - now_sec)
	print "Sleep ..."
	time.sleep(wait_sec)
	print "Wake up!"

def marekt_holiday(dt):
	if(int(dt.month) == 1 and int(dt.day) < 4):
		#print "Oshougatu"
		return 1
	if(int(dt.month) == 12 and int(dt.day) == 31):
		#print "oomisoka"
		return 1
	if(jholiday.holiday_name(date = dt)):
		#print "Close"
		return 1
	return 0
def market_check():
	time_now = time.localtime()
	#print time_now.tm_year,time_now.tm_mon,time_now.tm_mday
	now_hour = time_now.tm_hour + time_now.tm_min/60.0
	if(int(time_now.tm_mon) == 1 and int(time_now.tm_mday) < 4):
		#print "Oshougatu"
		return 0
	if(int(time_now.tm_mon) == 12 and int(time_now.tm_mday) == 31):
		#print "oomisoka"
		return 0
	#print now_hour
	if(time_now.tm_wday >= 5):
		#print "Close"
		return 0
	if(jholiday.holiday_name(time_now.tm_year,time_now.tm_mon,time_now.tm_mday)):
		#print "Close"
		return 0
	if(now_hour >= MarketClose):
		#print "Close"
		return 0
	if(now_hour >= MarketBreakStart and now_hour < MarketBreakEnd):
		#print "Break"
		return 2
	if(now_hour >= MarketOpen):
		#print "Open"
		return 1
	if(now_hour < MarketOpen):
		#print "Open"
		return 3
	return 0
