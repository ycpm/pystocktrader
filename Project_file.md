# Introduction #
Configure file
# Example #
```
PRJ_NAME = "Test yahoo"	#Project abstract

#For Trade
TARGET_CODE = "4689"	#Stock ID
TARGET_MARKET = 1
TARGET_MAX = 1.0	#Max rate of your asset for trade
BORDER_MONEY = 2000	#

AGENT = "SBI"	#securities house
DATA_SITE = "yahoo_jp"	#Data download site
LANG = "en"	#language

#Simulation
START_DATE = "2012-3-2"	#Simulation start date
END_DATE = "2012-3-2"	#Simulation stop date

#FOR 
RULE = "simple"	#Trade rule
VALS = [0.95,1.05,0.9]
SIM_START_MONEY = 1000000	#Start money
SIM_VAL_ID = 0	#Set VALS[0]
SIM_VAL_START = 10	#Start value
SIM_VAL_STEP = 1	#increment
SIM_VAL_NUM = 30	#number of iteration
#for 2d simulation
SIM_VAL_ID2 = 1	#Set VALS[1]
SIM_VAL_START2 = 10	#Start value
SIM_VAL_STEP2 = 1	#increment
SIM_VAL_NUM2 =30	#number of iteration


#FOR view
MA1 = 15	#Short cycle of Moving avarage
MA2 = 37	#long cycle of Moving avarage

#RSI RCI
RSI_RCI=0	#0:RSI, 1:RCI
RSI_DAY = 14
#RCI_DAY = 9
RSI_UPPER = 70
RSI_LOWER = 30
RCI_UPPER = 90
RCI_LOWER = -90

#For graph
FONT = "ipag.ttf"
DL_STOCK_CODES = "4689,8473"
```