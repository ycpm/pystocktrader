PRJ_NAME = "Test TOYOTA Golden Cross"

#For login agent
USER = ""
LOGIN_PASSWD = ""
TRADE_PASSWD = ""

#Trade
TARGET_CODE =8473	#
TARGET_MARKET = 1
TARGET_MAX = 1.0
BORDER_MONEY = 2000

AGENT = "SBI"
#RULE = "simple_c3"
DATA_SITE = "yahoo_jp"
#LANG = "jp"
LANG = "en"

START_DATE = "2009-1-1"
END_DATE = "2011-11-11"


#Golden Cross
RULE = "day_gcross"
VALS = [22,80,1.001,22,60,0.6,0.99]	#SBI


SIM_VAL_ID = 0
SIM_VAL_START = 15
SIM_VAL_END = 15
SIM_VAL_STEP = 1
SIM_VAL_NUM = 20
#SIM_VAL_NUM = 1
SIM_VAL_ID2 = 1
SIM_VAL_START2 = 20
SIM_VAL_END2 = 15
SIM_VAL_STEP2 = 2
SIM_VAL_NUM2 = 20

SIM_START_MONEY = 1000000

DL_CYCLE = 0

#FOR view
MA1 = 25
MA2 = 100
#For graph
FONT = "ipag.ttf"
DL_STOCK_CODES = "4689,8473"