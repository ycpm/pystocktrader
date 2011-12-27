#!/usr/bin/python
# coding: UTF-8
import os
import sys
#reload(sys)
#sys.setdfaultencoding("utf-8")
import imp
import wx
import wx.lib.sheet as sheet
import numpy as np
from string import *
import re
#from math import *
import datetime
import time
#import locale
import matplotlib
#matplotlib.interactive( True )
matplotlib.use( 'WXAgg' )
import matplotlib.font_manager as font_manager
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
#from pylab import meshgrid

sys.path.append('./lib/')
import data_process as dp
import simulator as sim
import stock_conv as sc
import get_detail as gd
WINDOW_X = 1000
WINDOW_Y = 800
ICON_DIR = "./icons/small/"
ICON_DIR = "./icons/"
FONT_DIR = "./font/"
PRJ_DIR = "./project/"
PRJ_NAME = "TEST"

PRJ_EXT = "*.py"
GRAPH_EXT = "*.png"
DATA_DIR = "./data/"
STOCK_DATA_DIR = DATA_DIR
STOCK_FILE = "stock_detail.csv"
LOG_DIR = "./log/"
RESOURCE_LOG = "resource.csv"
RESOURCE_LOG2 = "resource2.csv"
AGENT_DIR = "agent"
AGENT = "SBI"
RULE_DIR = "rule"
RULE = "day_gcross"
DATA_SITE_DIR = "data_site"
DATA_SITE = "yahoo_jp"
LANG_DIR = "lang"
#LANG = "jp"
LANG = "en"
FONT = "ipag.ttf"
USER = ""
LOGIN_PASSWD = ""
TRADE_PASSWD = ""

TARGET_CODE = 4689	#Yahoo
#TARGET_CODE = "SPY"
REF_TARGET_CODE = 998407	#NIKKEI
TARGET_MARKET = 1
TARGET_MAX = 1.0

SIM_START_MONEY = 1000000

BORDER_MONEY = 5000
START_DATE = "2009-1-1"
END_DATE = "2011-12-10"

VALS = [22,80,1.001,22,60,0.6,0.99] #YAHOO
SIM_VAL_ID = 0
SIM_VAL_START = 13
SIM_VAL_END = 17
SIM_VAL_STEP = 1
SIM_VAL_NUM = 5
SIM_VAL_ID2 = 3
SIM_VAL_START2 = 13
SIM_VAL_END2 = 17
SIM_VAL_STEP2 = 1
SIM_VAL_NUM2 = 0
DL_CYCLE = 0

MA1 = 25
MA2 = 100

#Flag
DONE_SIM = 0

MARKETS = ["All","Tosho 1","Tosho 2","Tosho Mothers","JASDAQ"]
DL_STOCK_CODES = "4689,8473,7203,1400,998407,998405"

#For search
SEARCH_MARKET = 0
MAX_TOTAL_ASSET = 0
MIN_TOTAL_ASSET = 1000
MAX_NET_PROFIT = 0
MIN_NET_PROFIT = 0
MAX_EQUITY_RATIO = 100.0
MIN_EQUITY_RATIO = 70.0
MAX_PBR = 1.0
MIN_PBR = 0
MAX_PER  = 100.0
MIN_PER  = 0
MAX_EPS = 0
MIN_EPS = 0
MAX_BPS = 0
MIN_BPS = 0
MAX_ROA = 100.0
MIN_ROA = 0
MAX_ROE = 100.0
MIN_ROE = 0

class user:
	def __init__(self):
		self.id = ""
		self.passwd = ""
		self.tr_passwd = ""
		self.margin = 0
		self.hold_stocks = []
		self.resource = 0
		self.stock_total = 0
class trade:
	def __init__(self,stock_id):
		#Initialize
		self.id = stock_id
		self.name = ""
		self.market = TARGET_MARKET
		self.price = 0
		self.open = 0
		self.low = 0
		self.high = 0
		self.last = 0
		self.price_history = []
		self.board_datas = []
		self.buy_price = 0
		self.sell_price = 0
		self.buy_wish_price = 0
		self.sell_wish_price = 0
		self.buy_date = ""
		self.sell_date = ""
		self.hold_num = 0
		self.buy_num = 0
		self.sell_num = 0
		self.buy_total_price = 0
		self.sell_total_price = 0
		self.buy_type = 0
		self.sell_type = 0
		self.buy_fee = 0
		self.sell_fee = 0
		self.do_buy = 0
		self.done_buy = 0
		self.do_sell = 0
		self.done_sell = 0
		self.tax = 0
		self.max = TARGET_MAX
		self.margin = 0
		self.limit = BORDER_MONEY
		self.agent = get_plugin(AGENT_DIR, AGENT)
		self.rule = get_plugin(RULE_DIR, RULE)
		self.vals = VALS
		self.debug = 0
class stock_data:
	def __init__(self,stock_id):
		#Initialize
		self.id = stock_id
		self.name = ""
		self.category = ""
		self.market = []
		self.num = 0
		self.dividend = 0
		self.unit = 0
		self.per = 0.0
		self.pbr = 0.0
		self.eps = 0.0
		self.bps = 0.0
		self.compliment = 0
		self.nop = 0
		self.op = 0
		self.np = 0
		self.ta = 0
		self.lc = 0
		self.er = 0.0
		self.roa = 0.0
		self.roa = 0.0
		self.price = 0
		self.data_dir = STOCK_DATA_DIR
		self.detail_dir = DATA_DIR
		self.detail_file = STOCK_FILE
		self.datas = dp.get_all_datas(self)
		dp.get_stock_detail(self)



class simulate:
	def __init__(self,stock_id):
		self.id = stock_id
		self.val_id = 0
		self.val_start = 0.0
		self.val_end = 0.0
		self.val_step = 0.0
		self.val_num = 1
		self.val_id2 = 0
		self.val_start2 = 0.0
		self.val_end2 = 0.0
		self.val_step2 = 0.0
		self.val_num2 = 0
		self.debug = 0
		self.log = []
		self.resource_log = []
class search:
	def __init__(self):
		self.id = ""
		self.name = ""
		self.cate = 0
		self.market = []
		self.vol = 0
		self.dividend = 0
		self.per = 0.0
		self.pbr = 0.0
		self.eps = 0.0
		self.bps = 0.0
		self.compliment = 0
		self.nop = 0
		self.op = 0
		self.np = 0
		self.ta = 0
		self.lc = 0
		self.er = 0.0
		self.roa = 0.0
		self.roe = 0.0
		self.result = []
#Window
class MainFrame(wx.Frame):
	def __init__(self, parent, id, title):
		global WINDOW_X, WINDOW_Y
		wx.Frame.__init__(self, parent, id, title, size=(WINDOW_X, WINDOW_Y))
		# Setting up the menu.
		#icon = wx.Image('fox.png',wx.BITMAP_TYPE_PNG)
		#self.Frm.SetIcon(icon)

		filemenu= wx.Menu()
		menuOpen = filemenu.Append(wx.ID_OPEN,lang.MENU_OPEN," Open project")
		menuSave = filemenu.Append(wx.ID_SAVE,lang.MENU_SAVE," Open project")
		menuExit = filemenu.Append(wx.ID_EXIT,lang.MENU_EXIT," Terminate the program")
		setupmenu =  wx.Menu()
		menuViewSetUp = setupmenu.Append(wx.ID_VIEW_LIST,lang.MENU_VIEW," Set up View")
		menuSimuSetUp = setupmenu.Append(wx.NewId(),lang.MENU_SIMU," Set up Simulation")
		menuSearchSetUp = setupmenu.Append(wx.NewId(),lang.MENU_SEARCH," Set up Stock Search")
		menuDataSetUp = setupmenu.Append(wx.NewId(),lang.MENU_DATASITE," Set up Data Site")
		menuSetUp = setupmenu.Append(wx.ID_SETUP,lang.MENU_TRADE," Set up Trade")

		# Creating the menubar.
		menuBar = wx.MenuBar()
		menuBar.Append(filemenu,lang.MENU_FILE) # Adding the "filemenu" to the MenuBar
		menuBar.Append(setupmenu,lang.MENU_SETUP) # Adding the "filemenu" to the MenuBar
		self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

		#Event for Menu bar
		self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
		self.Bind(wx.EVT_MENU, self.OnSave, menuSave)
		self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
		self.Bind(wx.EVT_MENU, self.OnSetUp, menuSetUp)
		self.Bind(wx.EVT_MENU, self.OnSimuSetUp, menuSimuSetUp)
		self.Bind(wx.EVT_MENU, self.OnDataSetUp, menuDataSetUp)
		self.Bind(wx.EVT_MENU, self.OnViewSetUp, menuViewSetUp)
		self.Bind(wx.EVT_MENU, self.OnSearchSetUp, menuSearchSetUp)
		toolbar = self.CreateToolBar()
		view_set = toolbar.AddLabelTool(wx.NewId(), 'Setup', wx.Bitmap(ICON_DIR + 'SetView.png', wx.BITMAP_TYPE_ANY),wx.NullBitmap, wx.ITEM_NORMAL, "", "")
		view = toolbar.AddLabelTool(wx.NewId(), 'View', wx.Bitmap(ICON_DIR + 'View.png', wx.BITMAP_TYPE_ANY),wx.NullBitmap, wx.ITEM_NORMAL, "", "")
		toolbar.AddSeparator()
		save_graph = toolbar.AddLabelTool(wx.NewId(), 'Save', wx.Bitmap(ICON_DIR + 'View3.png', wx.BITMAP_TYPE_ANY),wx.NullBitmap, wx.ITEM_NORMAL, "", "")
		view2 = toolbar.AddLabelTool(wx.NewId(), 'View', wx.Bitmap(ICON_DIR + 'View2.png', wx.BITMAP_TYPE_ANY),wx.NullBitmap, wx.ITEM_NORMAL, "", "")
		toolbar.AddSeparator()
		sim_set = toolbar.AddLabelTool(wx.NewId(), 'Setup', wx.Bitmap(ICON_DIR + 'SetSimu.png', wx.BITMAP_TYPE_ANY),wx.NullBitmap, wx.ITEM_NORMAL, "", "")
		sim_start = toolbar.AddLabelTool(wx.NewId(), 'Play', wx.Bitmap(ICON_DIR + 'Simulation.png', wx.BITMAP_TYPE_ANY),wx.NullBitmap, wx.ITEM_NORMAL, "", "")
		toolbar.AddSeparator()
		dl_set = toolbar.AddLabelTool(wx.NewId(), 'DL Setup', wx.Bitmap(ICON_DIR + 'SetDL.png', wx.BITMAP_TYPE_ANY),wx.NullBitmap, wx.ITEM_NORMAL, "", "")
		dl_data = toolbar.AddLabelTool(wx.ID_DOWN, 'DL', wx.Bitmap(ICON_DIR + 'DataDL.png', wx.BITMAP_TYPE_ANY),wx.NullBitmap, wx.ITEM_NORMAL, "", "")
		dl_detail = toolbar.AddLabelTool(wx.NewId(), 'DL detail', wx.Bitmap(ICON_DIR + 'DetailDL.png', wx.BITMAP_TYPE_ANY),wx.NullBitmap, wx.ITEM_NORMAL, "", "")
		toolbar.AddSeparator()
		search_setup = toolbar.AddLabelTool(wx.NewId(), 'Search Setup', wx.Bitmap(ICON_DIR + 'SetSearch.png', wx.BITMAP_TYPE_ANY),wx.NullBitmap, wx.ITEM_NORMAL, "", "")
		serach_stock = toolbar.AddLabelTool(wx.ID_FIND, 'Search Stocks', wx.Bitmap(ICON_DIR + 'Search.png', wx.BITMAP_TYPE_ANY),wx.NullBitmap, wx.ITEM_NORMAL, "", "")
		#print_graph = toolbar.AddLabelTool(wx.NewId(), 'Print', wx.Bitmap(ICON_DIR + 'Print.png', wx.BITMAP_TYPE_ANY),wx.NullBitmap, wx.ITEM_NORMAL, "", "")
		toolbar.AddSeparator()
		today_trade = toolbar.AddLabelTool(wx.NewId(), "Todas's Trade", wx.Bitmap(ICON_DIR + 'TodayTrade.png', wx.BITMAP_TYPE_ANY),wx.NullBitmap, wx.ITEM_NORMAL, "", "")
		toolbar.Realize()

		#self.Bind(wx.EVT_TOOL, self.OnExit, exit)
		self.Bind(wx.EVT_TOOL, self.OnSim, sim_start)
		self.Bind(wx.EVT_TOOL, self.OnSimuSetUp, sim_set)
		self.Bind(wx.EVT_TOOL, self.OnView, view)
		self.Bind(wx.EVT_TOOL, self.OnView2, view2)
		self.Bind(wx.EVT_TOOL, self.OnViewSetUp, view_set)
		self.Bind(wx.EVT_TOOL, self.OnSaveGraph, save_graph)
		self.Bind(wx.EVT_TOOL, self.OnDownLoad, dl_data)
		self.Bind(wx.EVT_TOOL, self.OnDetailDL, dl_detail)
		self.Bind(wx.EVT_TOOL, self.OnDataSetUp, dl_set)
		self.Bind(wx.EVT_TOOL, self.OnSearchSetUp,search_setup)
		self.Bind(wx.EVT_TOOL, self.OnSearchStock,serach_stock)
		self.Bind(wx.EVT_TOOL, self.OnTodayTrade,today_trade)

		panel = wx.Panel(self, -1)
		vbox = wx.BoxSizer(wx.VERTICAL)
		#

		#Draw data
		self.panel2 = wx.Panel(panel, -1)
		hbox1 = wx.BoxSizer(wx.HORIZONTAL)

		self.plot = myWxPlot(self.panel2)

		hbox1.Add(self.plot, 1, wx.EXPAND | wx.ALL, 2)
		self.panel2.SetSizer(hbox1)
		vbox.Add(self.panel2, 1,  wx.LEFT | wx.RIGHT | wx.EXPAND, 2)

		hbox5 = wx.BoxSizer(wx.HORIZONTAL)
		btn2 = wx.Button(panel, -1, lang.CLOSE, size=(70, 30))
		hbox5.Add(btn2, 0, wx.LEFT | wx.BOTTOM , 5)
		vbox.Add(hbox5, 0, wx.ALIGN_RIGHT | wx.RIGHT, 10)

		panel.SetSizer(vbox)
		self.Centre()
		self.Show(True)

		#Event
		self.Bind(wx.EVT_BUTTON, self.OnExit, btn2)


		self.plot.fig.clear()
		if self.plot.set_data():
			self.plot.setsize()
			self.plot.draw()
			self.plot.fig.canvas.draw()

	def OnExit(self,e):
		self.Close(True)  # Close the frame.

	def OnSetUp(self,e):
		setup = TradeSetUp(None, -1, lang.TRADE_SETUP)
		setup.ShowModal()
		setup.Destroy()

	def OnOpen(self,e):
		openprj = OpenProject(None, -1, lang.OPEN_PRJ)
		openprj.ShowModal()
		openprj.Destroy()
		self.plot.fig.clear()
		self.plot.set_data()
		self.plot.setsize()
		self.plot.draw()
		self.plot.fig.canvas.draw()
	def OnSimuSetUp(self,e):
		simusetup = SimuSetUp(None, -1, lang.SIMU_SETUP)
		simusetup.ShowModal()
		simusetup.Destroy()
	def OnViewSetUp(self,e):
		datasetup = ViewSetUp(None, -1, lang.VIEW_SETUP)
		datasetup.ShowModal()
		datasetup.Destroy()
	def OnDataSetUp(self,e):
		setup = DataSetUp(None, -1, lang.DATASITE_SETUP)
		setup.ShowModal()
		setup.Destroy()
	def OnView(self,e):
		global DONE_SIM
		sdt = datetime.date(*[int(val) for val in START_DATE.split('-')])
		edt = datetime.date(*[int(val) for val in END_DATE.split('-')])
		if not TARGET_CODE:
			ERROR_MSG("CODE not exist")
		stock = stock_data(TARGET_CODE)
		tr = trade(TARGET_CODE)
		DONE_SIM = 0
		self.plot.fig.clear()
		#self.plot.fig.canvas.draw()
		self.plot.set_data()
		self.plot.setsize()
		self.plot.draw()
		self.plot.fig.canvas.draw()
	def OnSim(self,e):
		global DONE_SIM
		sdt = datetime.date(*[int(val) for val in START_DATE.split('-')])
		edt = datetime.date(*[int(val) for val in END_DATE.split('-')])
		stock = stock_data(TARGET_CODE)
		tr = trade(TARGET_CODE)
		tr.margin = SIM_START_MONEY
		tr.vals = VALS
		sim_data = simulate(TARGET_CODE)
		sim_data.val_id = SIM_VAL_ID
		sim_data.val_start = SIM_VAL_START
		sim_data.val_end = SIM_VAL_END
		sim_data.val_num = SIM_VAL_NUM
		sim_data.val_step = SIM_VAL_STEP
		sim_data.val_id2 = SIM_VAL_ID2
		sim_data.val_start2 = SIM_VAL_START2
		sim_data.val_end2 = SIM_VAL_END2
		sim_data.val_num2 = SIM_VAL_NUM2
		sim_data.val_step2 = SIM_VAL_STEP2
		self.progress = wx.ProgressDialog(lang.SIMU_PRO_TITLE,lang.SIMU_PRO_MSG, maximum = 100, parent=self, style = wx.PD_CAN_ABORT | wx.PD_AUTO_HIDE | wx.PD_APP_MODAL)
		self.progress.SetSize((300, 100))
		sim.run(stock,tr,sim_data,sdt,edt,self)
		self.progress.Update(100, lang.SIMU_PRO_FINISH)
		self.progress.Destroy()
		#dlg = wx.MessageDialog(self, "Simulation is finished", "Simulation is finished" , wx.OK)
		#dlg.ShowModal() # Shows it
		#dlg.Destroy()
		DONE_SIM = 1
		if(int(sim_data.val_num2) > 1):
			disp_2d()
		else:
			self.plot.fig.clear()
			self.plot.set_data()
			self.plot.setsize()
			self.plot.draw()
			self.plot.fig.canvas.draw()

	def OnSave(self,e):
		save = SaveProject(None, -1, lang.SAVE_PRJ)
		save.ShowModal()
		save.Destroy()
	def OnSaveGraph(self,e):
		disp_graph()
	def OnView2(self,e):
		stock1 = stock_data(TARGET_CODE)
		stock2 = stock_data(REF_TARGET_CODE)
		disp_2stock_graph(stock1,stock2)

	def OnSearchSetUp(self,e):
		searchsetup =SearchSetUp(None, -1, lang.SEARCH_SETUP)
		searchsetup.ShowModal()
		searchsetup.Destroy()

	def OnSearchStock(self,e):
		sd = Stock_data(None, -1, "Stock data")
		sd.ShowModal()
		sd.Destroy()
	def OnDownLoad(self,e):
		#print "Start data download"
		dl = get_plugin(DATA_SITE_DIR,DATA_SITE)
		stock_ids = [int(stock_id) for stock_id in DL_STOCK_CODES.split(",")]
		dl.get_stock_data(stock_ids)
		wx.MessageBox(lang.DL_DONE, lang.INFO, wx.OK | wx.ICON_INFORMATION)
	def OnDetailDL(self,e):
		ddl = wx.MessageBox(lang.DL_CONFIRM, lang.CONFIRM, wx.YES_NO | wx.NO_DEFAULT| wx.ICON_QUESTION)
		if ddl == wx.YES:
			#print "Start detail data download"
			self.progress = wx.ProgressDialog(lang.DetailDL_TITLE,lang.DetailDL_PRO_MSG, maximum = 100, parent=self, style = wx.PD_CAN_ABORT | wx.PD_AUTO_HIDE | wx.PD_APP_MODAL)
			self.progress.SetSize((300, 100))
			gd.get_detail_data(self)
			self.progress.Update(100, lang.DetailDL_PRO_FINISH)
			self.progress.Destroy()
			wx.MessageBox(lang.DL_DONE, lang.INFO, wx.OK | wx.ICON_INFORMATION)

	def OnTodayTrade(self,e):
		tr= trade(TARGET_CODE)
		stock = stock_data(TARGET_CODE)
		tr.market = TARGET_MARKET
		#trade_type = ["Sashi","Nari"]
		sell_wish_price, sell_type,buy_wish_price, buy_type = today_trade(stock,tr)
		if(sell_wish_price > 0):
			sell_msg = str(sell_wish_price) + "," + lang.TRADE_TYPE[int(sell_type)]
		else:
			sell_msg = lang.NO_TRADE
		if(buy_wish_price > 0):
			buy_msg = str(buy_wish_price) + "," + lang.TRADE_TYPE[int(buy_type)]
		else:
			buy_msg = lang.NO_TRADE
		msg = lang.BUY + " : " + buy_msg + "\n" + lang.SELL + " : " + sell_msg 
		wx.MessageBox(msg, lang.TODAY_TRADE, wx.OK | wx.ICON_INFORMATION)
class myWxPlot(wx.Panel):
	def __init__( self, parent):
		from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
		#from matplotlib.figure import Figure
		
		self.parent = parent
		wx.Panel.__init__( self, parent)

		plt.rc('axes', grid=True)
		plt.rc('grid', color='0.75', linestyle='-', linewidth=0.5)

		#self.fig = figure(facecolor='white')
		self.fig = plt.Figure( None, facecolor='white')

		#canvas
		self.canvas = FigureCanvasWxAgg( self, -1, self.fig )
		self.canvas.SetBackgroundColour( wx.Color( 255,255,255 ) )

		if self.set_data():
			self.setsize()
			self.draw()

	def set_data(self):
		#print "Set data",DONE_SIM
		self.stock = stock_data(TARGET_CODE)
		s_dt = datetime.date(*[int(val) for val in START_DATE.split('-')])
		e_dt = datetime.date(*[int(val) for val in END_DATE.split('-')])
		if(dp.is_num(TARGET_CODE) and int(TARGET_CODE) < 1000):
			self.r = dp.get_price_history()
			n =len(self.r.close)
			if(n < 1):
				return False
			r2 = self.r
		else:
			self.r = dp.get_data_by_day(self.stock,s_dt,e_dt.year,e_dt.month,e_dt.day)
			n =len(self.r.close)
			if(n < 1):
				print "Error"
				return False
			margin = 30
			r2 = dp.get_data_by_day_num(self.stock,e_dt,n+margin)
		#print r2.close
		#Moving average
		ma1 = dp.moving_average(r2.close, int(MA1))
		ma2 = dp.moving_average(r2.close, int(MA2))
		if(len(ma1) > n):
			self.ma1 = ma1[margin:]
			self.ma2 = ma2[margin:]
		else:
			self.ma1 = ma1
			self.ma2 = ma2

		#RSI
		self.rsi = dp.relative_strength(self.r.close)

		if(DONE_SIM):
			#self.res_dates = []
			resource_datas = dp.open_file(LOG_DIR,RESOURCE_LOG)
			self.res_datas = []
			self.res_vals = []
			for i in range(0,SIM_VAL_NUM):				
				self.res_datas.append([])
			#print len(self.res_datas[0])
			#print len(resource_datas)
			#print resource_datas
			if(SIM_VAL_NUM > 1):
				tmp = resource_datas.pop(0)
				#print tmp
				tmp_vals = str(tmp).strip()
				self.res_vals = str(tmp_vals).split(",")
			for resource in resource_datas:
				resource = resource.strip()
				if not resource:
					continue
				if(SIM_VAL_NUM > 1):
					res = resource.split(",")
					for i in range(0,len(res)):
						#print i
						tmp = float(res[i])
						self.res_datas[i].append(int(tmp))
						#print len(self.res_datas[i])
				else:
					self.res_datas[0].append(resource)
			#print self.res_datas[1]
		return True
	def setsize( self ):
		size = tuple( self.parent.GetClientSize() )
		#print size
		#size = (800,700)
		#self.SetSize( size )
		self.canvas.SetSize( size )
		self.fig.set_size_inches( float( size[0] )/self.fig.get_dpi(),
									 float( size[1] )/self.fig.get_dpi() )

	def draw(self):
		#print "Draw data",DONE_SIM
		#print self.r.date
		#self.r.date = [str(date) for date in self.r.date]	#NG
		#r.date error
		#print sys.getdefaultencoding()
		#xdata = self.r.date
		#print self.r.date
		xdata = range(0,len(self.r.close))
		props = font_manager.FontProperties(size=10)
		textsize = 9
		fillcolor = 'darkgoldenrod'
		axescolor  = '#f6f6f6'  # the axies background color
		left, width = 0.1, 0.8
		rect1 = [left, 0.7, width, 0.2]
		rect2 = [left, 0.3, width, 0.4]
		rect3 = [left, 0.1, width, 0.2]

		ax1 = self.fig.add_axes(rect1, axisbg=axescolor)  #left, bottom, width, height	
		ax2 = self.fig.add_axes(rect2, axisbg=axescolor, sharex=ax1)
		ax2t = ax2.twinx()
		ax3  = self.fig.add_axes(rect3, axisbg=axescolor, sharex=ax1)
		N = len(self.r.close)
		#try:
		ax1.plot(xdata, self.rsi, color=fillcolor)
		#except UnicodeDecodeError:
			#print "UnicodeDecodeError"
			#xdata = range(0,len(self.r.close))
			#ax1.plot(xdata, self.rsi, color=fillcolor)
		ax1.axhline(70, color=fillcolor)
		ax1.axhline(30, color=fillcolor)
		ax1.fill_between(xdata, self.rsi, 70, where=(self.rsi>=70), facecolor=fillcolor, edgecolor=fillcolor)
		ax1.fill_between(xdata, self.rsi, 30, where=(self.rsi<=30), facecolor=fillcolor, edgecolor=fillcolor)
		ax1.text(0.6, 0.9, '>70 = overbought', va='top', transform=ax1.transAxes, fontsize=textsize)
		ax1.text(0.6, 0.1, '<30 = oversold', transform=ax1.transAxes, fontsize=textsize)
		ax1.set_ylim(0, 100)
		ax1.set_yticks([30,70])
		ax1.text(0.025, 0.95, 'RSI (14)', va='top', transform=ax1.transAxes, fontsize=textsize)

		if(LANG == "jp"):
			props_jp = font_manager.FontProperties(size=12,fname=FONT_DIR + FONT)
			ax1.set_title('%s daily'%self.stock.name.decode('utf-8'), fontproperties=props_jp)
		else:
			ax1.set_title('%s daily'%self.stock.id)

		ax2.plot(xdata, self.r.close, color='black', lw=2)
		#print self.r.date
		#ax2.plot(self.r.date, self.r.close, color='black', lw=2)
		deltas = np.zeros_like(self.r.close)
		deltas[1:] = np.diff(self.r.close)
		up = deltas>0
		#ax2.vlines(xdata[up], self.r.low[up], self.r.high[up], color='black', label='_nolegend_')
		#ax2.vlines(xdata[~up], self.r.low[~up],self.r.high[~up], color='black', label='_nolegend_')
		linema10, = ax2.plot(xdata, self.ma1, color='blue', lw=2, label='MA (' + str(MA1) + ')')
		linema20, = ax2.plot(xdata, self.ma2, color='red', lw=2, label='MA (' + str(MA2) + ')')


		#leg = ax2.legend(loc='center left', shadow=True, fancybox=True, prop=props)
		leg = ax2.legend(loc='upper left', shadow=True, fancybox=True, prop=props)
		leg.get_frame().set_alpha(0.5)

		volume = (self.r.close * self.r.volume)/1e6  # dollar volume in millions
		vmax = volume.max()
		if(vmax > 0):
			poly = ax2t.fill_between(xdata, volume, 0, label=lang.VOL, facecolor=fillcolor, edgecolor=fillcolor)
			ax2t.set_ylim(0, 5*vmax)
			ax2t.set_yticks([])
		class MyLocator(mticker.MaxNLocator):
			def __init__(self, *args, **kwargs):
				mticker.MaxNLocator.__init__(self, *args, **kwargs)

			def __call__(self, *args, **kwargs):
				return mticker.MaxNLocator.__call__(self, *args, **kwargs)
		if(DONE_SIM):
			if(SIM_VAL_NUM > 1):
				#print "Plot"
				#print self.res_vals
				for i in range(0,SIM_VAL_NUM):
					#print i,len(self.res_datas[i])
					#print self.res_datas[i]
					if(len(self.res_datas[i]) == len(xdata)):
						ax3.plot(xdata, self.res_datas[i], lw=2, label='Val[' + str(i) + '] = ' + str(self.res_vals[i]))
				leg3 = ax3.legend(loc='upper left', shadow=True, fancybox=True, prop=props)
				leg3.get_frame().set_alpha(0.5)
			else:
				#print "Plot"
				#print self.res_datas[0]
				if(len(self.res_datas[0]) == len(xdata)):
					ax3.plot(xdata, self.res_datas[0], color='black', lw=2)
			ax3.text(0.025, 0.95, lang.SIMU_RESULT + " : " + RULE, va='top',
					transform=ax3.transAxes, fontsize=textsize)
		else:
			### compute the MACD indicator
			fillcolor = 'darkslategrey'
			nslow = 26
			nfast = 12
			nema = 9
			emaslow, emafast, macd = dp.moving_average_convergence(self.r.close, nslow=nslow, nfast=nfast)
			ema9 = dp.moving_average(macd, nema, type='exponential')
			ax3.plot(xdata, macd, color='black', lw=2)
			ax3.plot(xdata, ema9, color='blue', lw=1)
			ax3.fill_between(xdata, macd-ema9, 0, alpha=0.5, facecolor=fillcolor, edgecolor=fillcolor)
			ax3.text(0.025, 0.95, 'MACD (%d, %d, %d)'%(nfast, nslow, nema), va='top',
				transform=ax3.transAxes, fontsize=textsize)
		for ax in ax1, ax2, ax2t, ax3:
			if ax!=ax3:
				for label in ax.get_xticklabels():
					label.set_visible(False)
			else:
				for label in ax.get_xticklabels():
					label.set_rotation(30)
					label.set_horizontalalignment('right')

			ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
			#ax.fmt_xdata = mdates.DateFormatter('%Y-%M-%D')

		ax2.yaxis.set_major_locator(MyLocator(5, prune='both'))
		ax3.yaxis.set_major_locator(MyLocator(5, prune='both'))
class OpenProject(wx.Dialog):
	def __init__(self, parent, id, title):
		wx.Dialog.__init__(self, parent, id, title, size=(250, 210))
		self.dirname=''

		panel = wx.Panel(self, -1)
		sizer = wx.GridBagSizer(0, 0)

		prj_txt = wx.StaticText(panel, -1, lang.PROJECT_FILE)
		sizer.Add(prj_txt, (0, 0), flag= wx.LEFT | wx.TOP, border=10)

		self.prj_val = wx.TextCtrl(panel, -1)
		self.prj_val.SetValue("")
		sizer.Add(self.prj_val, (0, 1), (1, 3), wx.TOP | wx.EXPAND, 5)

		prj_button = wx.Button(panel, -1, lang.BROWSE, size=(-1, 30))
		sizer.Add(prj_button, (0, 4), (1, 1), wx.TOP | wx.LEFT | wx.RIGHT , 5)

		button5 = wx.Button(panel, -1, lang.OK, size=(-1, 30))
		sizer.Add(button5, (2, 3), (1, 1),  wx.LEFT, 10)

		button6 = wx.Button(panel, -1, lang.CLOSE, size=(-1, 30))
		sizer.Add(button6, (2, 4), (1, 1),  wx.LEFT | wx.BOTTOM | wx.RIGHT, 10)

		sizer.AddGrowableCol(2)

		panel.SetSizer(sizer)
		sizer.Fit(self)
		# Events.

		self.Bind(wx.EVT_BUTTON, self.OnOK, button5)
		self.Bind(wx.EVT_BUTTON, self.OnClose, button6)	
		self.Bind(wx.EVT_BUTTON, self.OnOpenPrj, prj_button)
		self.Centre()
		self.Show(True)
	def OnOK(self,e):
		global PRJ_DIR,PRJ_FILE,DONE_SIM
		PRJ_DIR = self.dirname
		PRJ_FILE = self.filename
		DONE_SIM = 0
		read_prj()
		self.Close(True)  # Close the frame.
	def OnClose(self,e):
		self.Close(True)  # Close the frame.
	def OnOpenPrj(self,e):
		""" Open a file"""
		self.dirname = PRJ_DIR
		dlg = wx.FileDialog(self, lang.SELECT_PROJ, self.dirname, "", PRJ_EXT, wx.OPEN)
		if dlg.ShowModal() == wx.ID_OK:
			self.filename = dlg.GetFilename()
			self.dirname = dlg.GetDirectory()
			self.prj_val.SetValue(os.path.join(self.dirname, self.filename))
		dlg.Destroy()
class SaveProject(wx.Dialog):
	def __init__(self, parent, id, title):
		wx.Dialog.__init__(self, parent, id, title, size=(250, 210))
		self.dirname=''

		panel = wx.Panel(self, -1)
		sizer = wx.GridBagSizer(0, 0)

		prj_txt = wx.StaticText(panel, -1, lang.PROJECT_FILE)
		sizer.Add(prj_txt, (0, 0), flag= wx.LEFT | wx.TOP, border=10)

		self.prj_val = wx.TextCtrl(panel, -1)
		sizer.Add(self.prj_val, (0, 1), (1, 3), wx.TOP | wx.EXPAND, 5)

		prj_button = wx.Button(panel, -1, lang.BROWSE, size=(-1, 30))
		sizer.Add(prj_button, (0, 4), (1, 1), wx.TOP | wx.LEFT | wx.RIGHT , 5)


		prj_name_txt = wx.StaticText(panel, -1, lang.PROJECT_NAME)
		sizer.Add(prj_name_txt, (1, 0), flag= wx.LEFT | wx.TOP, border=10)

		self.prj_name = wx.TextCtrl(panel, -1)
		self.prj_name.SetValue(PRJ_NAME)
		sizer.Add(self.prj_name, (1, 1), (1, 3), wx.TOP | wx.EXPAND, 5)

		button5 = wx.Button(panel, -1, lang.OK, size=(-1, 30))
		sizer.Add(button5, (2, 3), (1, 1),  wx.LEFT, 10)

		button6 = wx.Button(panel, -1, lang.CLOSE, size=(-1, 30))
		sizer.Add(button6, (2, 4), (1, 1),  wx.LEFT | wx.BOTTOM | wx.RIGHT, 10)

		sizer.AddGrowableCol(2)

		panel.SetSizer(sizer)
		sizer.Fit(self)
		# Events.

		self.Bind(wx.EVT_BUTTON, self.OnOK, button5)
		self.Bind(wx.EVT_BUTTON, self.OnClose, button6)	
		self.Bind(wx.EVT_BUTTON, self.OnSavePrj, prj_button)
		self.Centre()
		self.Show(True)
	def OnOK(self,e):
		global PRJ_DIR,PRJ_FILE,PRJ_NAME
		PRJ_DIR = self.dirname
		PRJ_FILE = self.filename
		PRJ_NAME = self.prj_name.GetValue()
		save_prj()
		self.Close(True)  # Close the frame.
	def OnClose(self,e):
		self.Close(True)  # Close the frame.
	def OnSavePrj(self,e):
		""" Open a file"""
		self.dirname = PRJ_DIR
		dlg = wx.FileDialog(self, lang.SELECT_PROJ, self.dirname, "", PRJ_EXT, wx.SAVE)
		if dlg.ShowModal() == wx.ID_OK:
			self.filename = dlg.GetFilename()
			self.dirname = dlg.GetDirectory()
			self.prj_val.SetValue(os.path.join(self.dirname, self.filename))
		dlg.Destroy()
class TradeSetUp(wx.Dialog):
	def __init__(self, parent, id, title):
		wx.Dialog.__init__(self, parent, id, title, size=(250, 210))
		self.dirname=''

		panel = wx.Panel(self, -1)
		sizer = wx.GridBagSizer(0, 0)

		agent_txt = wx.StaticText(panel, -1, lang.SELECT_AGENT)
		sizer.Add(agent_txt, (0, 0), flag= wx.LEFT | wx.TOP, border=10)

		self.agents = get_plugin_list(AGENT_DIR)
		selected_agent = 0
		for i, v in enumerate(self.agents):
			if(str(v) == str(AGENT)):
				selected_agent = i
				break
		self.agent = wx.ComboBox(panel, -1, pos=(50, 170), size=(150, -1), choices=self.agents, 
					style=wx.CB_READONLY)
		self.agent.SetSelection(int(selected_agent))
		sizer.Add(self.agent, (0, 1), (1, 3), wx.TOP | wx.EXPAND, 5)


		user_txt = wx.StaticText(panel, -1, lang.LOGIN)
		sizer.Add(user_txt, (1, 0), flag=wx.TOP | wx.LEFT, border=10)

		self.user = wx.TextCtrl(panel, -1)
		self.user.SetValue(USER)
		sizer.Add(self.user, (1, 1), (1, 3), wx.TOP | wx.EXPAND,  5)

		lpw_txt = wx.StaticText(panel, -1, lang.LOGIN_PW)
		sizer.Add(lpw_txt, (2, 0), flag=wx.TOP | wx.LEFT, border=10)

		self.lpw = wx.TextCtrl(panel, -1)
		self.lpw.SetValue(LOGIN_PASSWD)
		sizer.Add(self.lpw, (2, 1), (1, 3), wx.TOP | wx.EXPAND,  5)

		tpw_txt = wx.StaticText(panel, -1, lang.TRADE_PW)
		sizer.Add(tpw_txt, (3, 0), flag=wx.TOP | wx.LEFT, border=10)

		self.tpw = wx.TextCtrl(panel, -1)
		self.tpw.SetValue(TRADE_PASSWD)
		sizer.Add(self.tpw, (3, 1), (1, 3), wx.TOP | wx.EXPAND,  5)

		ok_button = wx.Button(panel, -1, lang.OK, size=(-1, 30))
		sizer.Add(ok_button, (5, 2), (1, 1),  wx.LEFT, 10)

		close_button = wx.Button(panel, -1, lang.CLOSE, size=(-1, 30))
		sizer.Add(close_button, (5, 3), (1, 1),  wx.LEFT | wx.BOTTOM | wx.RIGHT, 10)
		sizer.AddGrowableCol(2)

		panel.SetSizer(sizer)
		sizer.Fit(self)
		# Events.
		self.Bind(wx.EVT_BUTTON, self.OnOK, ok_button)
		self.Bind(wx.EVT_BUTTON, self.OnClose, close_button)	

		self.Centre()
		self.Show(True)

	def OnOK(self,e):
		global AGENT, USER, LOGIN_PASSWD, TRADE_PASSWD	
		if(self.agent.GetSelection() >= 0):
			a_num = int(self.agent.GetSelection())
			AGENT = self.agents[a_num]
		if(self.user.GetValue()):
			USER = self.user.GetValue()
		if(self.lpw.GetValue()):
			LOGIN_PASSWD = self.lpw.GetValue()
		if(self.tpw.GetValue()):
			TRADE_PASSWD = self.tpw.GetValue()
		self.Close(True) 
	def OnClose(self,e):
		self.Close(True)  # Close the frame.

class DataSetUp(wx.Dialog):
	def __init__(self, parent, id, title):
		wx.Dialog.__init__(self, parent, id, title, size=(250, 210))
		self.dirname=''

		panel = wx.Panel(self, -1)
		sizer = wx.GridBagSizer(0, 0)

		data_site_txt = wx.StaticText(panel, -1, lang.SELECT_DATA_SITE)
		sizer.Add(data_site_txt, (0, 0), flag=wx.TOP | wx.LEFT, border=10)

		self.data_sites = get_plugin_list(DATA_SITE_DIR)
		selected_site = 0
		for i, v in enumerate(self.data_sites):
			if(str(v) == str(DATA_SITE)):
				selected_site = i
				break
		self.data_site = wx.ComboBox(panel, -1, pos=(50, 170), size=(150, -1), choices=self.data_sites, 
					style=wx.CB_READONLY)
		self.data_site.SetSelection(int(selected_site))
		sizer.Add(self.data_site, (0, 1), (1, 3), wx.TOP | wx.EXPAND,  5)

		stock_ids_txt = wx.StaticText(panel, -1, lang.STOCK_IDS)
		sizer.Add(stock_ids_txt, (1, 0), flag= wx.LEFT | wx.TOP, border=10)
		self.stock_ids = wx.TextCtrl(panel, -1)
		self.stock_ids.SetValue(DL_STOCK_CODES)
		sizer.Add(self.stock_ids, (1, 1), (1, 3), wx.TOP | wx.EXPAND,  5)

		download_txt = wx.StaticText(panel, -1, lang.DL_CYCLE)
		sizer.Add(download_txt, (2, 0), flag=wx.TOP | wx.LEFT, border=10)

		self.download_cycles = ["every day","every week","every month"]

		self.download = wx.ComboBox(panel, -1, pos=(50, 170), size=(150, -1), choices=self.download_cycles,
					style=wx.CB_READONLY)
		self.download.SetSelection(int(DL_CYCLE))
		sizer.Add(self.download, (2, 1), (1, 3), wx.TOP | wx.EXPAND,  5)

		ok_button = wx.Button(panel, -1, lang.OK, size=(-1, 30))
		sizer.Add(ok_button, (4, 2), (1, 1),  wx.LEFT, 10)

		close_button = wx.Button(panel, -1, lang.CLOSE, size=(-1, 30))
		sizer.Add(close_button, (4, 3), (1, 1),  wx.LEFT | wx.BOTTOM | wx.RIGHT, 10)
		sizer.AddGrowableCol(2)

		panel.SetSizer(sizer)
		sizer.Fit(self)
		# Events.
		self.Bind(wx.EVT_BUTTON, self.OnOK, ok_button)
		self.Bind(wx.EVT_BUTTON, self.OnClose, close_button)	

		self.Centre()
		self.Show(True)

	def OnOK(self,e):
		global DATA_SITE,DL_CYCLE
		if(self.download.GetSelection()):
			DL_CYCLE = self.download.GetSelection()
		if(self.data_site.GetSelection() >= 0):
			d_num = int(self.data_site.GetSelection())
			DATA_SITE = self.data_sites[d_num]
		self.Close(True) 
	def OnClose(self,e):
		self.Close(True)  # Close the frame.
class SimuSetUp(wx.Dialog):
	def __init__(self, parent, id, title):
		wx.Dialog.__init__(self, parent, id, title, size=(250, 210))
		self.dirname=''

		panel = wx.Panel(self, -1)
		sizer = wx.GridBagSizer(0, 0)

		code_txt = wx.StaticText(panel, -1, lang.PRODUCT_CODE)
		sizer.Add(code_txt, (0, 0), flag= wx.LEFT | wx.TOP, border=10)
		self.code = wx.TextCtrl(panel, -1)
		self.code.SetValue(str(TARGET_CODE))
		sizer.Add(self.code, (0, 1), (1, 1), wx.TOP | wx.EXPAND,  5)

		resource_txt = wx.StaticText(panel, -1, lang.START_RESOURCE)
		sizer.Add(resource_txt, (0, 2), flag= wx.LEFT | wx.TOP, border=10)
		self.resource = wx.TextCtrl(panel, -1)
		self.resource.SetValue(str(SIM_START_MONEY))
		sizer.Add(self.resource, (0, 3), (1, 1), wx.TOP | wx.EXPAND,  5)

		agent_txt = wx.StaticText(panel, -1, lang.SELECT_AGENT)
		sizer.Add(agent_txt, (1, 0), flag= wx.LEFT | wx.TOP, border=10)

		self.agents = get_plugin_list(AGENT_DIR)
		selected_agent = 0
		for i, v in enumerate(self.agents):
			if(str(v) == str(AGENT)):
				selected_agent = i
				break
		self.agent = wx.ComboBox(panel, -1, pos=(50, 170), size=(150, -1), choices=self.agents, 
					style=wx.CB_READONLY)
		self.agent.SetSelection(int(selected_agent))
		sizer.Add(self.agent, (1, 1), (1, 3), wx.TOP | wx.EXPAND, 5)

		rule_txt = wx.StaticText(panel, -1, lang.SELECT_RULE)
		sizer.Add(rule_txt, (2, 0), flag=wx.TOP | wx.LEFT, border=10)

		self.rules = get_plugin_list(RULE_DIR)
		selected_rule = 0
		for i, v in enumerate(self.rules):
			if(str(v) == str(RULE)):
				selected_rule = i
				break
		self.rule = wx.ComboBox(panel, -1, pos=(50, 170), size=(150, -1), choices=self.rules, 
					style=wx.CB_READONLY)
		self.rule.SetSelection(int(selected_rule))
		sizer.Add(self.rule, (2, 1), (1, 3), wx.TOP | wx.EXPAND,  5)

		today = datetime.date.today()
		end_year = today.year+1
		years = []
		months = []
		days = []
		for year in range(2000,end_year):
			years.append(str(year))
		for month in range(1,13):
			months.append(str(month))
		for day in range(1,32):
			days.append(str(day))
		st_year,st_month,st_day = START_DATE.split("-")
		selected_year = int(st_year) - 2000
		start_date_txt = wx.StaticText(panel, -1, lang.START_DATE)
		sizer.Add(start_date_txt, (3, 0), flag=wx.TOP | wx.LEFT, border=10)
		self.start_year = wx.ComboBox(panel, -1, pos=(50, 170), size=(150, -1), choices=years, 
					style=wx.CB_READONLY)
		self.start_year.SetSelection(int(selected_year))
		sizer.Add(self.start_year, (3, 1), (1, 1), wx.TOP | wx.EXPAND,  5)
		self.start_month = wx.ComboBox(panel, -1, pos=(50, 170), size=(150, -1), choices=months, 
					style=wx.CB_READONLY)
		self.start_month.SetSelection(int(st_month) - 1)
		sizer.Add(self.start_month, (3, 2), (1, 1), wx.TOP | wx.EXPAND,  5)
		self.start_day = wx.ComboBox(panel, -1, pos=(50, 170), size=(150, -1), choices=days, 
					style=wx.CB_READONLY)
		self.start_day.SetSelection(int(st_day) - 1)
		sizer.Add(self.start_day, (3, 3), (1, 1), wx.TOP | wx.EXPAND,  5)

		ed_year,ed_month,ed_day = END_DATE.split("-")
		selected_year = int(ed_year) - 2000
		stop_date_txt = wx.StaticText(panel, -1, lang.STOP_DATE)
		sizer.Add(stop_date_txt, (4, 0), flag=wx.TOP | wx.LEFT, border=10)
		self.stop_year = wx.ComboBox(panel, -1, pos=(50, 170), size=(150, -1), choices=years, 
					style=wx.CB_READONLY)
		self.stop_year.SetSelection(int(selected_year))
		sizer.Add(self.stop_year, (4, 1), (1, 1), wx.TOP | wx.EXPAND,  5)
		self.stop_month = wx.ComboBox(panel, -1, pos=(50, 170), size=(150, -1), choices=months, 
					style=wx.CB_READONLY)
		self.stop_month.SetSelection(int(ed_month) - 1)
		sizer.Add(self.stop_month, (4, 2), (1, 1), wx.TOP | wx.EXPAND,  5)
		self.stop_day = wx.ComboBox(panel, -1, pos=(50, 170), size=(150, -1), choices=days, 
					style=wx.CB_READONLY)
		self.stop_day.SetSelection(int(ed_day) - 1)
		sizer.Add(self.stop_day, (4, 3), (1, 1), wx.TOP | wx.EXPAND,  5)

		val_ids = []
		for val_id in range(0,len(VALS)):
			val_ids.append(str(val_id))
		val_id_txt = wx.StaticText(panel, -1, lang.VALUE_ID)
		sizer.Add(val_id_txt, (5, 0), flag=wx.TOP | wx.LEFT, border=10)
		self.val_id = wx.ComboBox(panel, -1, pos=(50, 170), size=(150, -1), choices=val_ids, 
					style=wx.CB_READONLY)
		self.val_id.SetSelection(int(SIM_VAL_ID))
		sizer.Add(self.val_id, (5, 1), (1, 1), wx.TOP | wx.EXPAND,  5)

		val_num_txt = wx.StaticText(panel, -1, lang.STEP_TIMES)
		sizer.Add(val_num_txt, (5, 2), flag= wx.LEFT | wx.TOP, border=10)
		self.val_num = wx.TextCtrl(panel, -1)
		self.val_num.SetValue(str(SIM_VAL_NUM))
		sizer.Add(self.val_num, (5, 3), (1, 1), wx.TOP | wx.EXPAND,  5)

		start_val_txt = wx.StaticText(panel, -1, lang.START_VAL)
		sizer.Add(start_val_txt, (6, 0), flag= wx.LEFT | wx.TOP, border=10)
		self.start_val = wx.TextCtrl(panel, -1)
		self.start_val.SetValue(str(SIM_VAL_START))
		sizer.Add(self.start_val, (6, 1), (1, 1), wx.TOP | wx.EXPAND,  5)

		end_val_txt = wx.StaticText(panel, -1, lang.STOP_VAL)
		sizer.Add(end_val_txt, (6, 2), flag= wx.LEFT | wx.TOP, border=10)
		self.end_val = wx.TextCtrl(panel, -1)
		self.end_val.SetValue(str(SIM_VAL_END))
		sizer.Add(self.end_val, (6, 3), (1, 1), wx.TOP | wx.EXPAND,  5)

		val_step_txt = wx.StaticText(panel, -1, lang.VAL_STEP)
		sizer.Add(val_step_txt, (7, 0), flag= wx.LEFT | wx.TOP, border=10)
		self.val_step = wx.TextCtrl(panel, -1)
		self.val_step.SetValue(str(SIM_VAL_STEP))
		sizer.Add(self.val_step, (7, 1), (1, 1), wx.TOP | wx.EXPAND,  5)

		val_id2_txt = wx.StaticText(panel, -1, lang.VALUE_ID2)
		sizer.Add(val_id2_txt, (8, 0), flag=wx.TOP | wx.LEFT, border=10)
		self.val_id2 = wx.ComboBox(panel, -1, pos=(50, 170), size=(150, -1), choices=val_ids, 
					style=wx.CB_READONLY)
		self.val_id2.SetSelection(int(SIM_VAL_ID2))
		sizer.Add(self.val_id2, (8, 1), (1, 1), wx.TOP | wx.EXPAND,  5)

		val_num2_txt = wx.StaticText(panel, -1, lang.STEP_TIMES2)
		sizer.Add(val_num2_txt, (8, 2), flag= wx.LEFT | wx.TOP, border=10)
		self.val_num2 = wx.TextCtrl(panel, -1)
		self.val_num2.SetValue(str(SIM_VAL_NUM2))
		sizer.Add(self.val_num2, (8, 3), (1, 1), wx.TOP | wx.EXPAND,  5)

		start_val2_txt = wx.StaticText(panel, -1, lang.START_VAL2)
		sizer.Add(start_val2_txt, (9, 0), flag= wx.LEFT | wx.TOP, border=10)
		self.start_val2 = wx.TextCtrl(panel, -1)
		self.start_val2.SetValue(str(SIM_VAL_START2))
		sizer.Add(self.start_val2, (9, 1), (1, 1), wx.TOP | wx.EXPAND,  5)

		end_val2_txt = wx.StaticText(panel, -1, lang.STOP_VAL2)
		sizer.Add(end_val2_txt, (9, 2), flag= wx.LEFT | wx.TOP, border=10)
		self.end_val2 = wx.TextCtrl(panel, -1)
		self.end_val2.SetValue(str(SIM_VAL_END2))
		sizer.Add(self.end_val2, (9, 3), (1, 1), wx.TOP | wx.EXPAND,  5)

		val_step2_txt = wx.StaticText(panel, -1, lang.VAL_STEP2)
		sizer.Add(val_step2_txt, (10, 0), flag= wx.LEFT | wx.TOP, border=10)
		self.val_step2 = wx.TextCtrl(panel, -1)
		self.val_step2.SetValue(str(SIM_VAL_STEP))
		sizer.Add(self.val_step2, (10, 1), (1, 1), wx.TOP | wx.EXPAND,  5)

		ok_button = wx.Button(panel, -1, lang.OK, size=(-1, 30))
		sizer.Add(ok_button, (12, 2), (1, 1),  wx.LEFT, 10)

		close_button = wx.Button(panel, -1, lang.CLOSE, size=(-1, 30))
		sizer.Add(close_button, (12, 3), (1, 1),  wx.LEFT | wx.BOTTOM | wx.RIGHT, 10)
		sizer.AddGrowableCol(2)

		panel.SetSizer(sizer)
		sizer.Fit(self)
		# Events.
		self.Bind(wx.EVT_BUTTON, self.OnOK, ok_button)
		self.Bind(wx.EVT_BUTTON, self.OnClose, close_button)	

		self.Centre()
		self.Show(True)

	def OnOK(self,e):
		global AGENT, RULE, SIM_START_MONEY,TARGET_CODE, START_DATE,END_DATE, SIM_VAL_ID, SIM_VAL_NUM, SIM_VAL_START, SIM_VAL_END, SIM_VAL_STEP, SIM_VAL_ID2, SIM_VAL_NUM2, SIM_VAL_START2, SIM_VAL_END2, SIM_VAL_STEP2
		if(self.code.GetValue()):
			TARGET_CODE = self.code.GetValue()
		if(self.resource.GetValue()):
			SIM_START_MONEY = int(self.resource.GetValue())
		if(self.agent.GetSelection() >= 0):
			a_num = int(self.agent.GetSelection())
			AGENT = self.agents[a_num]
		if(self.rule.GetSelection() >= 0):
			r_num = int(self.rule.GetSelection())
			RULE = self.rules[r_num]
		if(self.val_id.GetSelection() >= 0):
			SIM_VAL_ID = int(self.val_id.GetSelection())
		if(self.val_num.GetValue()):
			SIM_VAL_NUM = int(self.val_num.GetValue())
		if(self.start_val.GetValue()):
			SIM_VAL_START = float(float(self.start_val.GetValue()))
		if(self.end_val.GetValue()):
			SIM_VAL_END = float(float(self.end_val.GetValue()))
		if(self.val_step.GetValue()):
			SIM_VAL_STEP = float(float(self.val_step.GetValue()))
		if(self.val_id2.GetSelection() >= 0):
			SIM_VAL_ID2 = int(self.val_id2.GetSelection())
		if(self.val_num2.GetValue()):
			SIM_VAL_NUM2 = int(self.val_num2.GetValue())
		if(self.start_val2.GetValue()):
			SIM_VAL_START2 = float(float(self.start_val2.GetValue()))
		if(self.end_val2.GetValue()):
			SIM_VAL_END2 = float(float(self.end_val2.GetValue()))
		if(self.val_step2.GetValue()):
			SIM_VAL_STEP2 = float(float(self.val_step2.GetValue()))

		st_year = int(self.start_year.GetSelection()) + 2000
		st_month = int(self.start_month.GetSelection()) + 1
		st_day = int(self.start_day.GetSelection()) + 1
		START_DATE = str(st_year) + "-" + str(st_month) + "-" + str(st_day)
		ed_year = int(self.stop_year.GetSelection()) + 2000
		ed_month = int(self.stop_month.GetSelection()) + 1
		ed_day = int(self.stop_day.GetSelection()) + 1
		END_DATE = str(ed_year) + "-" + str(ed_month) + "-" + str(ed_day)
		self.Close(True) 
	def OnClose(self,e):
		self.Close(True)  # Close the frame.
class ViewSetUp(wx.Dialog):
	def __init__(self, parent, id, title):
		wx.Dialog.__init__(self, parent, id, title, size=(250, 210))
		self.dirname=''

		panel = wx.Panel(self, -1)
		sizer = wx.GridBagSizer(0, 0)

		code_txt = wx.StaticText(panel, -1, lang.PRODUCT_CODE)
		sizer.Add(code_txt, (0, 0), flag= wx.LEFT | wx.TOP, border=10)
		self.code = wx.TextCtrl(panel, -1)
		self.code.SetValue(str(TARGET_CODE))
		sizer.Add(self.code, (0, 1), (1, 1), wx.TOP | wx.EXPAND,  5)

		ref_code_txt = wx.StaticText(panel, -1, lang.REF_PRODUCT_CODE)
		sizer.Add(ref_code_txt, (0, 2), flag= wx.LEFT | wx.TOP, border=10)
		self.ref_code = wx.TextCtrl(panel, -1)
		self.ref_code.SetValue(str(REF_TARGET_CODE))
		sizer.Add(self.ref_code, (0, 3), (1, 1), wx.TOP | wx.EXPAND,  5)

		today = datetime.date.today()
		end_year = today.year+1
		#print today.year
		years = []
		months = []
		days = []
		for year in range(2000,end_year):
			years.append(str(year))
		for month in range(1,13):
			months.append(str(month))
		for day in range(1,32):
			days.append(str(day))
		#print years
		st_year,st_month,st_day = START_DATE.split("-")
		selected_year = int(st_year) - 2000
		start_date_txt = wx.StaticText(panel, -1, lang.START_DATE)
		sizer.Add(start_date_txt, (1, 0), flag=wx.TOP | wx.LEFT, border=10)
		self.start_year = wx.ComboBox(panel, -1, pos=(50, 170), size=(150, -1), choices=years, 
					style=wx.CB_READONLY)
		self.start_year.SetSelection(int(selected_year))
		sizer.Add(self.start_year, (1, 1), (1, 1), wx.TOP | wx.EXPAND,  5)
		self.start_month = wx.ComboBox(panel, -1, pos=(50, 170), size=(150, -1), choices=months, 
					style=wx.CB_READONLY)
		self.start_month.SetSelection(int(st_month) - 1)

		if(self.start_month.GetSelection() and self.start_year.GetSelection()):
			s_month = int(self.start_month.GetSelection())
			n_year = int(self.start_year.GetSelection())
			n_month = s_month + 1
			if(s_month == 12):
				n_year += 1
				n_month = 1
			#print n_year
			if(n_year > 1999 and n_month > 0):
				tmp_time = time.mktime((n_year,n_month,1,0,0,0,0,0,0)) - 86400
				tmp_date = time.localtime(tmp_time)
				for day in range(1,tmp_date.tm_mday):
					days.append(str(day))

		sizer.Add(self.start_month, (1, 2), (1, 1), wx.TOP | wx.EXPAND,  5)
		self.start_day = wx.ComboBox(panel, -1, pos=(50, 170), size=(150, -1), choices=days, 
					style=wx.CB_READONLY)
		self.start_day.SetSelection(int(st_day) - 1)
		sizer.Add(self.start_day, (1, 3), (1, 1), wx.TOP | wx.EXPAND,  5)

		ed_year,ed_month,ed_day = END_DATE.split("-")
		selected_year = int(ed_year) - 2000
		stop_date_txt = wx.StaticText(panel, -1, lang.STOP_DATE)
		sizer.Add(stop_date_txt, (2, 0), flag=wx.TOP | wx.LEFT, border=10)
		self.stop_year = wx.ComboBox(panel, -1, pos=(50, 170), size=(150, -1), choices=years, 
					style=wx.CB_READONLY)
		self.stop_year.SetSelection(int(selected_year))
		sizer.Add(self.stop_year, (2, 1), (1, 1), wx.TOP | wx.EXPAND,  5)
		self.stop_month = wx.ComboBox(panel, -1, pos=(50, 170), size=(150, -1), choices=months, 
					style=wx.CB_READONLY)
		self.stop_month.SetSelection(int(ed_month) - 1)
		sizer.Add(self.stop_month, (2, 2), (1, 1), wx.TOP | wx.EXPAND,  5)

		#days = []
		if(self.start_month.GetSelection() and self.start_year.GetSelection()):
			s_month = int(self.start_month.GetSelection())
			n_year = int(self.start_year.GetSelection())
			n_month = s_month + 1
			if(s_month == 12):
				n_year += 1
				n_month = 1
			#print n_year
			if(n_year > 1999 and n_month > 0):
				tmp_time = time.mktime((n_year,n_month,1,0,0,0,0,0,0)) - 86400
				tmp_date = time.localtime(tmp_time)
				for day in range(1,tmp_date.tm_mday):
					days.append(str(day))

		self.stop_day = wx.ComboBox(panel, -1, pos=(50, 170), size=(150, -1), choices=days, 
					style=wx.CB_READONLY)
		self.stop_day.SetSelection(int(ed_day) - 1)
		sizer.Add(self.stop_day, (2, 3), (1, 1), wx.TOP | wx.EXPAND,  5)


		ma1_txt = wx.StaticText(panel, -1, lang.MA1)
		sizer.Add(ma1_txt, (3, 0), flag= wx.LEFT | wx.TOP, border=10)
		self.ma1 = wx.TextCtrl(panel, -1)
		self.ma1.SetValue(str(MA1))
		sizer.Add(self.ma1, (3, 1), (1, 1), wx.TOP | wx.EXPAND,  5)

		ma2_txt = wx.StaticText(panel, -1, lang.MA2)
		sizer.Add(ma2_txt, (3, 2), flag= wx.LEFT | wx.TOP, border=10)
		self.ma2 = wx.TextCtrl(panel, -1)
		self.ma2.SetValue(str(MA2))
		sizer.Add(self.ma2, (3, 3), (1, 1), wx.TOP | wx.EXPAND,  5)

		ok_button = wx.Button(panel, -1, lang.OK, size=(-1, 30))
		sizer.Add(ok_button, (6, 2), (1, 1),  wx.LEFT, 10)

		close_button = wx.Button(panel, -1, lang.CLOSE, size=(-1, 30))
		sizer.Add(close_button, (6, 3), (1, 1),  wx.LEFT | wx.BOTTOM | wx.RIGHT, 10)
		sizer.AddGrowableCol(2)

		panel.SetSizer(sizer)
		sizer.Fit(self)
		# Events.
		self.Bind(wx.EVT_BUTTON, self.OnOK, ok_button)
		self.Bind(wx.EVT_BUTTON, self.OnClose, close_button)	

		self.Centre()
		self.Show(True)

	def OnOK(self,e):	
		global TARGET_CODE, START_DATE,END_DATE,MA1,MA2
		if(self.code.GetValue()):
			TARGET_CODE = self.code.GetValue()
		if(self.ma1.GetValue()):
			MA1 = int(self.ma1.GetValue())
		if(self.ma2.GetValue()):
			MA2 = int(self.ma2.GetValue())

		st_year = int(self.start_year.GetSelection()) + 2000
		st_month = int(self.start_month.GetSelection()) + 1
		st_day = int(self.start_day.GetSelection()) + 1
		START_DATE = str(st_year) + "-" + str(st_month) + "-" + str(st_day)
		ed_year = int(self.stop_year.GetSelection()) + 2000
		ed_month = int(self.stop_month.GetSelection()) + 1
		ed_day = int(self.stop_day.GetSelection()) + 1
		END_DATE = str(ed_year) + "-" + str(ed_month) + "-" + str(ed_day)
		self.Close(True) 
	def OnClose(self,e):
		self.Close(True)  # Close the frame.
class SearchSetUp(wx.Dialog):
	def __init__(self, parent, id, title):
		wx.Dialog.__init__(self, parent, id, title, size=(250, 210))
		self.dirname=''

		panel = wx.Panel(self, -1)
		sizer = wx.GridBagSizer(0, 0)

		market_txt = wx.StaticText(panel, -1, lang.SELECT_MARKET)	#Select market
		sizer.Add(market_txt, (0, 0), flag= wx.LEFT | wx.TOP, border=10)
		self.market = wx.ComboBox(panel, -1, pos=(50, 170), size=(150, -1), choices=lang.MARKETS, 
					style=wx.CB_READONLY)
		self.market.SetSelection(int(SEARCH_MARKET))
		sizer.Add(self.market, (0, 1), (1, 2), wx.TOP | wx.EXPAND, 5)

		ta_txt = wx.StaticText(panel, -1, lang.TOTAL_ASSET + " : ")	#total asset
		sizer.Add(ta_txt, (1, 0), flag= wx.LEFT | wx.TOP, border=10)
		ta_max_txt = wx.StaticText(panel, -1, lang.MAX)	#total asset
		sizer.Add(ta_max_txt, (1, 1), flag= wx.LEFT | wx.TOP, border=10)
		self.ta_max = wx.TextCtrl(panel, -1)
		self.ta_max.SetValue(str(MAX_TOTAL_ASSET))
		sizer.Add(self.ta_max, (1, 2), (1, 1), wx.TOP | wx.EXPAND,  5)

		ta_min_txt = wx.StaticText(panel, -1, lang.MIN)	#total asset
		sizer.Add(ta_min_txt, (1, 3), flag= wx.LEFT | wx.TOP, border=10)

		self.ta_min = wx.TextCtrl(panel, -1)
		self.ta_min.SetValue(str(MIN_TOTAL_ASSET))
		sizer.Add(self.ta_min, (1, 4), (1, 1), wx.TOP | wx.EXPAND,  5)

		np_txt = wx.StaticText(panel, -1, lang.NET_PROFIT+ " : ")	#Net Profit
		sizer.Add(np_txt, (2, 0), flag= wx.LEFT | wx.TOP, border=10)
		np_max_txt = wx.StaticText(panel, -1, lang.MAX)	#total asset
		sizer.Add(np_max_txt, (2, 1), flag= wx.LEFT | wx.TOP, border=10)
		self.np_max = wx.TextCtrl(panel, -1)
		self.np_max.SetValue(str(MAX_NET_PROFIT))
		sizer.Add(self.np_max, (2, 2), (1, 1), wx.TOP | wx.EXPAND,  5)

		np_min_txt = wx.StaticText(panel, -1, lang.MIN)	#Net Profit
		sizer.Add(np_min_txt, (2, 3), flag= wx.LEFT | wx.TOP, border=10)
		self.np_min = wx.TextCtrl(panel, -1)
		self.np_min.SetValue(str(MIN_NET_PROFIT))
		sizer.Add(self.np_min, (2, 4), (1, 1), wx.TOP | wx.EXPAND,  5)

		er_txt = wx.StaticText(panel, -1, lang.EQUITY_RATIO + " : ")	#Equity Ratio
		sizer.Add(er_txt, (3, 0), flag= wx.LEFT | wx.TOP, border=10)
		er_max_txt = wx.StaticText(panel, -1, lang.MAX)	#total asset
		sizer.Add(er_max_txt, (3, 1), flag= wx.LEFT | wx.TOP, border=10)
		self.er_max = wx.TextCtrl(panel, -1)
		self.er_max.SetValue(str(MAX_EQUITY_RATIO))
		sizer.Add(self.er_max, (3, 2), (1, 1), wx.TOP | wx.EXPAND,  5)

		er_min_txt = wx.StaticText(panel, -1, lang.MIN)	#Equity Ratio
		sizer.Add(er_min_txt, (3, 3), flag= wx.LEFT | wx.TOP, border=10)
		self.er_min = wx.TextCtrl(panel, -1)
		self.er_min.SetValue(str(MIN_EQUITY_RATIO))
		sizer.Add(self.er_min, (3, 4), (1, 1), wx.TOP | wx.EXPAND,  5)

		pbr_txt = wx.StaticText(panel, -1, lang.PBR + " : ")	#PBR
		sizer.Add(pbr_txt, (4, 0), flag= wx.LEFT | wx.TOP, border=10)
		pbr_max_txt = wx.StaticText(panel, -1, lang.MAX)	#total asset
		sizer.Add(pbr_max_txt, (4, 1), flag= wx.LEFT | wx.TOP, border=10)
		self.pbr_max = wx.TextCtrl(panel, -1)
		self.pbr_max.SetValue(str(MAX_PBR))
		sizer.Add(self.pbr_max, (4, 2), (1, 1), wx.TOP | wx.EXPAND,  5)

		pbr_min_txt = wx.StaticText(panel, -1, lang.MIN)	#PBR
		sizer.Add(pbr_min_txt, (4, 3), flag= wx.LEFT | wx.TOP, border=10)
		self.pbr_min = wx.TextCtrl(panel, -1)
		self.pbr_min.SetValue(str(MIN_PBR))
		sizer.Add(self.pbr_min, (4, 4), (1, 1), wx.TOP | wx.EXPAND,  5)

		per_txt = wx.StaticText(panel, -1, lang.PER + " : ")	#PER
		sizer.Add(per_txt, (5, 0), flag= wx.LEFT | wx.TOP, border=10)
		pbr_max_txt = wx.StaticText(panel, -1, lang.MAX)	#total asset
		sizer.Add(pbr_max_txt, (5, 1), flag= wx.LEFT | wx.TOP, border=10)
		self.per_max = wx.TextCtrl(panel, -1)
		self.per_max.SetValue(str(MAX_PER))
		sizer.Add(self.per_max, (5, 2), (1, 1), wx.TOP | wx.EXPAND,  5)

		per_min_txt = wx.StaticText(panel, -1, lang.MIN)	#PER
		sizer.Add(per_min_txt, (5, 3), flag= wx.LEFT | wx.TOP, border=10)
		self.per_min = wx.TextCtrl(panel, -1)
		self.per_min.SetValue(str(MIN_PER))
		sizer.Add(self.per_min, (5, 4), (1, 1), wx.TOP | wx.EXPAND,  5)


		eps_txt = wx.StaticText(panel, -1, lang.EPS + " : ")	#EPS
		sizer.Add(eps_txt, (6, 0), flag= wx.LEFT | wx.TOP, border=10)
		eps_max_txt = wx.StaticText(panel, -1, lang.MAX)	#total asset
		sizer.Add(eps_max_txt, (6, 1), flag= wx.LEFT | wx.TOP, border=10)
		self.eps_max = wx.TextCtrl(panel, -1)
		self.eps_max.SetValue(str(MAX_EPS))
		sizer.Add(self.eps_max, (6, 2), (1, 1), wx.TOP | wx.EXPAND,  5)

		eps_min_txt = wx.StaticText(panel, -1, lang.MIN)	#EPS
		sizer.Add(eps_min_txt, (6, 3), flag= wx.LEFT | wx.TOP, border=10)
		self.eps_min = wx.TextCtrl(panel, -1)
		self.eps_min.SetValue(str(MIN_EPS))
		sizer.Add(self.eps_min, (6, 4), (1, 1), wx.TOP | wx.EXPAND,  5)

		bps_txt = wx.StaticText(panel, -1, lang.BPS+ " : ")	#BPS
		sizer.Add(bps_txt, (7, 0), flag= wx.LEFT | wx.TOP, border=10)
		bps_max_txt = wx.StaticText(panel, -1, lang.MAX)	#total asset
		sizer.Add(bps_max_txt, (7, 1), flag= wx.LEFT | wx.TOP, border=10)
		self.bps_max = wx.TextCtrl(panel, -1)
		self.bps_max.SetValue(str(MAX_BPS))
		sizer.Add(self.bps_max, (7, 2), (1, 1), wx.TOP | wx.EXPAND,  5)

		bps_min_txt = wx.StaticText(panel, -1, lang.MIN)	#BPS
		sizer.Add(bps_min_txt, (7, 3), flag= wx.LEFT | wx.TOP, border=10)
		self.bps_min = wx.TextCtrl(panel, -1)
		self.bps_min.SetValue(str(MIN_BPS))
		sizer.Add(self.bps_min, (7, 4), (1, 1), wx.TOP | wx.EXPAND,  5)

		roa_txt = wx.StaticText(panel, -1, lang.ROA + " : ")	#ROA
		sizer.Add(roa_txt, (8, 0), flag= wx.LEFT | wx.TOP, border=10)
		roa_max_txt = wx.StaticText(panel, -1, lang.MAX)	#total asset
		sizer.Add(roa_max_txt, (8, 1), flag= wx.LEFT | wx.TOP, border=10)
		self.roa_max = wx.TextCtrl(panel, -1)
		self.roa_max.SetValue(str(MAX_ROA))
		sizer.Add(self.roa_max, (8, 2), (1, 1), wx.TOP | wx.EXPAND,  5)

		roa_min_txt = wx.StaticText(panel, -1, lang.MIN)	#ROA
		sizer.Add(roa_min_txt, (8, 3), flag= wx.LEFT | wx.TOP, border=10)
		self.roa_min = wx.TextCtrl(panel, -1)
		self.roa_min.SetValue(str(MIN_ROA))
		sizer.Add(self.roa_min, (8, 4), (1, 1), wx.TOP | wx.EXPAND,  5)

		roe_txt = wx.StaticText(panel, -1, lang.ROE + " : ")	#ROE
		sizer.Add(roe_txt, (9, 0), flag= wx.LEFT | wx.TOP, border=10)
		roe_max_txt = wx.StaticText(panel, -1, lang.MAX)	#total asset
		sizer.Add(roe_max_txt, (9, 1), flag= wx.LEFT | wx.TOP, border=10)
		self.roe_max = wx.TextCtrl(panel, -1)
		self.roe_max.SetValue(str(MAX_ROE))
		sizer.Add(self.roe_max, (9, 2), (1, 1), wx.TOP | wx.EXPAND,  5)

		roe_min_txt = wx.StaticText(panel, -1, lang.MIN)	#ROE
		sizer.Add(roe_min_txt, (9, 3), flag= wx.LEFT | wx.TOP, border=10)
		self.roe_min = wx.TextCtrl(panel, -1)
		self.roe_min.SetValue(str(MIN_ROE))
		sizer.Add(self.roe_min, (9, 4), (1, 1), wx.TOP | wx.EXPAND,  5)

		ok_button = wx.Button(panel, -1, lang.OK, size=(-1, 30))
		sizer.Add(ok_button, (11, 2), (1, 1),  wx.LEFT, 10)

		close_button = wx.Button(panel, -1, lang.CLOSE, size=(-1, 30))
		sizer.Add(close_button, (11, 4), (1, 1),  wx.LEFT | wx.BOTTOM | wx.RIGHT, 10)
		sizer.AddGrowableCol(2)

		panel.SetSizer(sizer)
		sizer.Fit(self)
		# Events.
		self.Bind(wx.EVT_BUTTON, self.OnOK, ok_button)
		self.Bind(wx.EVT_BUTTON, self.OnClose, close_button)	

		self.Centre()
		self.Show(True)

	def OnOK(self,e):
		global SEARCH_MARKET, MAX_TOTAL_ASSET, MAX_NET_PROFIT, MAX_EQUITY_RATIO, MAX_PBR, MAX_PER, MAX_EPS, MAX_BPS, MAX_ROA, MAX_ROE
		global MIN_TOTAL_ASSET, MIN_NET_PROFIT, MIN_EQUITY_RATIO, MIN_PBR, MIN_PER, MIN_EPS, MIN_BPS, MIN_ROA, MIN_ROE

		if(self.market.GetSelection() >= 0):
			SEARCH_MARKET = int(self.market.GetSelection())
		if(self.ta_max.GetValue()):
			MAX_TOTAL_ASSET = int(self.ta_max.GetValue())
		if(self.ta_min.GetValue()):
			MIN_TOTAL_ASSET = int(self.ta_min.GetValue())
		if(self.np_max.GetValue()):
			MAX_NET_PROFIT = int(self.np_max.GetValue())
		if(self.np_min.GetValue()):
			MIN_NET_PROFIT = int(self.np_min.GetValue())
		if(self.er_max.GetValue()):
			MAX_EQUITY_RATIO = float(self.er_max.GetValue())
		if(self.er_min.GetValue()):
			MIN_EQUITY_RATIO = float(self.er_min.GetValue())
		if(self.pbr_max.GetValue()):
			MAX_PBR = float(self.pbr_max.GetValue())
		if(self.pbr_min.GetValue()):
			MIN_PBR = float(self.pbr_min.GetValue())
		if(self.per_max.GetValue()):
			MAX_PER = float(self.per_max.GetValue())
		if(self.per_min.GetValue()):
			MIN_PER = float(self.per_min.GetValue())
		if(self.eps_max.GetValue()):
			MAX_EPS = float(self.eps_max.GetValue())
		if(self.eps_min.GetValue()):
			MIN_EPS = float(self.eps_min.GetValue())
		if(self.bps_max.GetValue()):
			MAX_BPS = float(self.bps_max.GetValue())
		if(self.bps_min.GetValue()):
			MIN_BPS = float(self.bps_min.GetValue())
		if(self.roa_max.GetValue()):
			MAX_ROA = float(self.roa_max.GetValue())
		if(self.roa_min.GetValue()):
			MIN_ROA = float(self.roa_min.GetValue())
		if(self.roe_max.GetValue()):
			MAX_ROE = float(self.roe_max.GetValue())
		if(self.roe_min.GetValue()):
			MIN_ROE = float(self.roe_min.GetValue())

		self.Close(True) 
	def OnClose(self,e):
		self.Close(True)  # Close the frame.

class ERROR_MSG(wx.Dialog):
	def __init__(self, msg):
		dial = wx.MessageDialog(None, msg, lang.ERROR, wx.OK | wx.ICON_ERROR)
		dial.ShowModal()

class StockSheet(sheet.CSheet):
	def __init__(self, parent):
		sheet.CSheet.__init__(self, parent)
		labels = ["Code","Name","Category","Market","Total Volume","Dividend","PER","PBR","EPS","BPS",
				"UNIT","Compliment","Net operating profit","Ordinary profit","Net profit","Total asset","LC","Equity Ratio","ROA","ROE"]
#search.result.append([search.id,search.name,search.cate,search.market,search.vol,search.dividend,
																		#search.per,search.pbr,search.eps,search.bps,search.unit,search.compliment,search.nop,
																		#search.op,search.np,search.ta,search.lc,search.er,search.roa,search.roe])
		self.SetNumberRows(50)
		self.SetNumberCols(len(labels))
		col_size = 60
		col_sizes = [50,200,90,120,100,100]
		for col in range(self.GetNumberCols()):
			# make name and role columns wider
			if col < 6:
				self.SetColSize(col, col_sizes[col])
			else:
				self.SetColSize(col, col_size)
##http://www.python-forum.org/pythonforum/viewtopic.php?f=2&t=9935
		# set column lable titles at the top
		for i, title in enumerate(labels):
			self.SetColLabelValue(i, title)
		# create reusable attribute objects for all cells
		self.attr = wx.grid.GridCellAttr()
		self.attr.SetTextColour('black')
		#self.attr.SetBackgroundColour('yellow')
  		#self.attr.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL))

		# now load the data_list into the spread sheet cells
		self.loadCells()

	def loadCells(self):
		ss = search()
		search_stock(ss)
		self.SetNumberRows(len(ss.result))
		for row in range(0,len(ss.result)):
			# set cell attributes for the whole row
 			self.SetRowAttr(row, self.attr)
			for col in range(0,len(ss.result[row])):
				value = ss.result[row][col]
				if col == 1:
					#value = str(value).decode('utf8')
					value = value
				elif col == 2:
					#value = sc.num2cate[int(value)].decode('utf8')
					value = sc.num2cate[int(value)].decode('utf8')
				elif col == 3:
					tmp = []
					for m in value:
						#tmp.append(sc.num2market[int(m)].decode('utf8'))
						tmp.append(sc.num2market[int(m)].decode('utf8'))
					value = ",".join(tmp)
				else:
					value = str(value)
				#print value
				#print sys.getdefaultencoding()
				#self.SetCellValue(row, col, str(value))
				self.SetCellValue(row, col, value)
				# align numbers to the right
				#if col > 2:
					#self.SetCellAlignment(row, col, wx.ALIGN_RIGHT, wx.ALIGN_CENTRE)


class Stock_data(wx.Dialog):
	def __init__(self, parent, id, title):
		wx.Dialog.__init__(self, parent, id, title, size=(800, 500))


		nb = wx.Notebook(self, -1, style=wx.NB_BOTTOM)
		self.sheet1 = StockSheet(nb)

		nb.AddPage(self.sheet1, 'Stock Sheet1')
		self.sheet1.SetFocus()
		self.Centre()
		self.Show()

	def OnQuit(self, event):
		self.Close()
def main():
	global lang
	lang = get_plugin(LANG_DIR, LANG)
	app = wx.App()
	MainFrame(None, -1, 'pyStockTrader')
	app.MainLoop()
def save_prj():
	config_data ='PRJ_NAME = "' + str(PRJ_NAME) + "\"\n"
	config_data += "BORDER_MONEY = " + str(BORDER_MONEY) + "\n"
	config_data += "TARGET_CODE = " + str(TARGET_CODE) + "\n"
	config_data += "TARGET_MARKET = " + str(TARGET_MARKET) + "\n"
	config_data += "TARGET_MAX = " + str(TARGET_MAX) + "\n"
	config_data += 'USER = "' + str(USER) + "\"\n"
	config_data += 'LOGIN_PASSWD = "' + str(LOGIN_PASSWD) + "\"\n"
	config_data += 'TRADE_PASSWD = "' + str(TRADE_PASSWD) + "\"\n"
	config_data += 'AGENT = "' + str(AGENT) + "\"\n"
	config_data += 'RULE = "' + str(RULE) + "\"\n"
	config_data += "SIM_START_MONEY =" + str(SIM_START_MONEY) + "\n"
	config_data += 'START_DATE = "' + str(START_DATE) + "\"\n"
	config_data += 'END_DATE = "' + str(END_DATE) + "\"\n"
	config_data += 'DATA_SITE = "' + str(DATA_SITE) + "\"\n"
	config_data += 'LANG = "' + str(LANG) + "\"\n"
	vals = ",".join([str(val) for val in VALS])
	config_data += "VALS = [" + str(vals) + "]\n"
	config_data += "SIM_VAL_ID = " + str(SIM_VAL_ID) + "\n"
	config_data += "SIM_VAL_START = " + str(SIM_VAL_START) + "\n"
	config_data += "SIM_VAL_END = " + str(SIM_VAL_END) + "\n"
	config_data += "SIM_VAL_STEP = " + str(SIM_VAL_STEP) + "\n"
	config_data += "SIM_VAL_NUM = " + str(SIM_VAL_NUM) + "\n"
	config_data += "SIM_VAL_ID2 = " + str(SIM_VAL_ID2) + "\n"
	config_data += "SIM_VAL_START2 = " + str(SIM_VAL_START2) + "\n"
	config_data += "SIM_VAL_END2 = " + str(SIM_VAL_END2) + "\n"
	config_data += "SIM_VAL_STEP2 = " + str(SIM_VAL_STEP2) + "\n"
	config_data += "SIM_VAL_NUM2 = " + str(SIM_VAL_NUM2) + "\n"
	config_data += "MA1 = " + str(MA1) + "\n"
	config_data += "MA2 = " + str(MA2) + "\n"
	config_data += "DL_STOCK_CODES = " + str(DL_STOCK_CODES) + "\n"
	config_data += 'DL_CYCLE = ' + str(DL_CYCLE) + "\n"
	config_data += 'FONT = "' + str(FONT) + "\"\n"
	
	dp.write_file(PRJ_DIR,PRJ_FILE,config_data)
def read_prj():
	global BORDER_MONEY,TARGET_CODE, TARGET_MARKET,TARGET_MAX, USER, LOGIN_PASSWD, TRADE_PASSWD,AGENT, RULE, SIM_START_MONEY, START_DATE, END_DATE, DATA_SITE, LANG, VALS, SIM_VAL_ID, SIM_VAL_START, SIM_VAL_END, SIM_VAL_STEP, SIM_VAL_NUM, SIM_VAL_ID2, SIM_VAL_START2, SIM_VAL_END2, SIM_VAL_STEP2, SIM_VAL_NUM2, DL_CYCLE, MA1, MA2, FONT, PRJ_NAME,DL_STOCK_CODES
	if(PRJ_FILE):
		ini = get_plugin(PRJ_DIR,PRJ_FILE)
	else:
		return
	BORDER_MONEY = int(ini.BORDER_MONEY)
	TARGET_CODE = str(ini.TARGET_CODE)
	TARGET_MARKET = int(ini.TARGET_MARKET)
	TARGET_MAX = float(ini.TARGET_MAX)
	USER = str(ini.USER)
	LOGIN_PASSWD = str(ini.LOGIN_PASSWD)
	TRADE_PASSWD = str(ini.TRADE_PASSWD)
	AGENT = str(ini.AGENT)
	RULE = str(ini.RULE)
	SIM_START_MONEY = int(ini.SIM_START_MONEY)
	START_DATE = str(ini.START_DATE)
	END_DATE = str(ini.END_DATE)
	DATA_SITE = str(ini.DATA_SITE)
	LANG = str(ini.LANG)
	VALS = np.array(ini.VALS)
	SIM_VAL_ID = int(ini.SIM_VAL_ID)
	SIM_VAL_START = float(ini.SIM_VAL_START)
	SIM_VAL_END = float(ini.SIM_VAL_END)
	SIM_VAL_STEP = float(ini.SIM_VAL_STEP)
	SIM_VAL_NUM = int(ini.SIM_VAL_NUM)
	SIM_VAL_ID2 = int(ini.SIM_VAL_ID2)
	SIM_VAL_START2 = float(ini.SIM_VAL_START2)
	SIM_VAL_END2 = float(ini.SIM_VAL_END2)
	SIM_VAL_STEP2 = float(ini.SIM_VAL_STEP2)
	SIM_VAL_NUM2 = int(ini.SIM_VAL_NUM2)
	DL_CYCLE = int(ini.DL_CYCLE)
	MA1 = int(ini.MA1)
	MA2 = int(ini.MA2)
	FONT = str(ini.FONT)
	PRJ_NAME = str(ini.PRJ_NAME)
	DL_STOCK_CODES = str(ini.DL_STOCK_CODES)
def disp_2d():
	csv_datas = dp.open_file(LOG_DIR, RESOURCE_LOG2)
	xvals = np.array([float(val) for val in csv_datas.pop(0).split(",")])
	yvals = []
	all_datas = []
	for data in csv_datas:
		if not data:
			continue
		datas = data.split(",")

		yval = datas.pop(0)		
		datas = np.array([float(val) / SIM_START_MONEY for val in datas])	
		yvals.append(float(yval))
		all_datas.append(datas)
	yvals = np.array(yvals)
	all_datas = np.array(all_datas)
	X,Y = np.meshgrid(xvals, yvals)
	plt.title(lang.SIMU_RESULT)
	plt.subplot(111)
	plt.pcolor(X, Y, all_datas)
	#plt.imshow(all_datas)
	plt.xlabel('Val 2')
	plt.ylabel('Val 1')
	plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
	cax = plt.axes([0.85, 0.1, 0.075, 0.8])
	plt.colorbar(cax=cax)
	plt.show()

def disp_graph():
	stock = stock_data(TARGET_CODE)
	s_dt = datetime.date(*[int(val) for val in START_DATE.split('-')])
	e_dt = datetime.date(*[int(val) for val in END_DATE.split('-')])

	if(dp.is_num(TARGET_CODE) and int(TARGET_CODE) < 1000):
		r = dp.get_price_history()
		n =len(r.close)
		r2 = r
	else:
		r = dp.get_data_by_day(stock,s_dt,e_dt.year,e_dt.month,e_dt.day)
		n =len(r.close)
		margin = 30
		r2 = dp.get_data_by_day_num(stock,e_dt,n+margin)
	#Moving average
	ma1 = dp.moving_average(r2.close, int(MA1))
	ma2 = dp.moving_average(r2.close, int(MA2))
	if(len(ma1) > n):
		ma1 = ma1[margin:]
		ma2 = ma2[margin:]
	else:
		ma1 = ma1
		ma2 = ma2
	#RSI
	rsi = dp.relative_strength(r.close)


	plt.rc('axes', grid=True)
	plt.rc('grid', color='0.75', linestyle='-', linewidth=0.5)
	textsize = 9
	left, width = 0.1, 0.8
	rect1 = [left, 0.7, width, 0.2]
	rect2 = [left, 0.3, width, 0.4]
	rect3 = [left, 0.1, width, 0.2]

	fig = plt.figure(facecolor='white')
	axescolor  = '#f6f6f6'  # the axies background color

	props = font_manager.FontProperties(size=10)
	ax1 = fig.add_axes(rect1, axisbg=axescolor)  #left, bottom, width, height
	ax2 = fig.add_axes(rect2, axisbg=axescolor, sharex=ax1)
	ax2t = ax2.twinx()
	ax3  = fig.add_axes(rect3, axisbg=axescolor, sharex=ax1)


	if(DONE_SIM):
		#res_dates = []
		#res_res = []
		resource_datas = dp.open_file(LOG_DIR,RESOURCE_LOG)
		res_datas = []
		res_vals = []
		for i in range(0,SIM_VAL_NUM):				
			res_datas.append([])
		#print len(res_datas[0])
		#print len(resource_datas)
		if(SIM_VAL_NUM > 1):
			tmp = resource_datas.pop(0)
			#print tmp
			tmp_vals = str(tmp).strip()
			res_vals = str(tmp_vals).split(",")
		for resource in resource_datas:
			resource = resource.strip()
			if not resource:
				continue
			if(SIM_VAL_NUM > 1):
				res = resource.split(",")
				for i in range(0,len(res)):
					#print i
					tmp = float(res[i])
					res_datas[i].append(int(tmp))
					#print len(res_datas[i])
			else:
				res_datas[0].append(resource)
		#print res_datas[1]



	#print "Draw data",DONE_SIM
	#print r.date
	#r.date error
	#xdata = r.date
	xdata = range(0,len(r.close))

	N = len(r.close)
	fillcolor = 'darkgoldenrod'
	ax1.plot(xdata, rsi, color=fillcolor)
	ax1.axhline(70, color=fillcolor)
	ax1.axhline(30, color=fillcolor)
	ax1.fill_between(xdata, rsi, 70, where=(rsi>=70), facecolor=fillcolor, edgecolor=fillcolor)
	ax1.fill_between(xdata, rsi, 30, where=(rsi<=30), facecolor=fillcolor, edgecolor=fillcolor)
	ax1.text(0.6, 0.9, '>70 = overbought', va='top', transform=ax1.transAxes, fontsize=textsize)
	ax1.text(0.6, 0.1, '<30 = oversold', transform=ax1.transAxes, fontsize=textsize)
	ax1.set_ylim(0, 100)
	ax1.set_yticks([30,70])
	ax1.text(0.025, 0.95, 'RSI (14)', va='top', transform=ax1.transAxes, fontsize=textsize)

	if(LANG == "jp"):
		props_jp = font_manager.FontProperties(size=12,fname=FONT_DIR + FONT)
		ax1.set_title('%s daily'%stock.name.decode('utf-8'), fontproperties=props_jp)
	else:
		ax1.set_title('%s daily'%stock.id)

	ax2.plot(xdata, r.close, color='black', lw=2)
	#print r.date
	deltas = np.zeros_like(r.close)
	deltas[1:] = np.diff(r.close)
	up = deltas>0
	#ax2.vlines(xdata[up], r.low[up], r.high[up], color='black', label='_nolegend_')
	#ax2.vlines(xdata[~up], r.low[~up],r.high[~up], color='black', label='_nolegend_')
	linema10, = ax2.plot(xdata, ma1, color='blue', lw=2, label='MA (' + str(MA1) + ')')
	linema20, = ax2.plot(xdata, ma2, color='red', lw=2, label='MA (' + str(MA2) + ')')


	#leg = ax2.legend(loc='center left', shadow=True, fancybox=True, prop=props)
	leg = ax2.legend(loc='upper left', shadow=True, fancybox=True, prop=props)
	leg.get_frame().set_alpha(0.5)

	volume = (r.close * r.volume)/1e6  # dollar volume in millions
	vmax = volume.max()
	poly = ax2t.fill_between(xdata, volume, 0, label=lang.VOL, facecolor=fillcolor, edgecolor=fillcolor)
	ax2t.set_ylim(0, 5*vmax)
	ax2t.set_yticks([])
	class MyLocator(mticker.MaxNLocator):
		def __init__(self, *args, **kwargs):
			mticker.MaxNLocator.__init__(self, *args, **kwargs)

		def __call__(self, *args, **kwargs):
			return mticker.MaxNLocator.__call__(self, *args, **kwargs)
	if(DONE_SIM):
		if(SIM_VAL_NUM > 1):
			#print "Plot"
			for i in range(0,SIM_VAL_NUM):
				#print i,len(res_datas[i])
				if(len(res_datas[i]) == len(xdata)):
					ax3.plot(xdata, res_datas[i], lw=2, label='Val ='+str(i))
			leg3 = ax3.legend(loc='upper left', shadow=True, fancybox=True, prop=props)
			leg3.get_frame().set_alpha(0.5)
		else:
			#print "Plot"
			if(len(res_datas[0]) == len(xdata)):
				ax3.plot(xdata,res_datas[0], color='black', lw=2)
		ax3.text(0.025, 0.95, lang.SIMU_RESULT + ":" + RULE, va='top',
				transform=ax3.transAxes, fontsize=textsize)
	else:
		### compute the MACD indicator
		fillcolor = 'darkslategrey'
		nslow = 26
		nfast = 12
		nema = 9
		emaslow, emafast, macd = dp.moving_average_convergence(r.close, nslow=nslow, nfast=nfast)
		ema9 = dp.moving_average(macd, nema, type='exponential')
		ax3.plot(xdata, macd, color='black', lw=2)
		ax3.plot(xdata, ema9, color='blue', lw=1)
		ax3.fill_between(xdata, macd-ema9, 0, alpha=0.5, facecolor=fillcolor, edgecolor=fillcolor)
		ax3.text(0.025, 0.95, 'MACD (%d, %d, %d)'%(nfast, nslow, nema), va='top',
			transform=ax3.transAxes, fontsize=textsize)
	for ax in ax1, ax2, ax2t, ax3:
		if ax!=ax3:
			for label in ax.get_xticklabels():
				label.set_visible(False)
		else:
			for label in ax.get_xticklabels():
				label.set_rotation(30)
				label.set_horizontalalignment('right')

		ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')

	ax2.yaxis.set_major_locator(MyLocator(5, prune='both'))
	ax3.yaxis.set_major_locator(MyLocator(5, prune='both'))

	plt.show()

def disp_2stock_graph(stock1,stock2):
	s_dt = datetime.date(*[int(val) for val in START_DATE.split('-')])
	e_dt = datetime.date(*[int(val) for val in END_DATE.split('-')])

	if(dp.is_num(stock1) and int(stock1) < 1000):
		r1 = dp.get_price_history()
	else:
		r1 = dp.get_data_by_day(stock1,s_dt,e_dt.year,e_dt.month,e_dt.day)

	if(dp.is_num(stock2) and int(stock2) < 1000):
		r2 = dp.get_price_history()
	else:
		r2 = dp.get_data_by_day(stock2,s_dt,e_dt.year,e_dt.month,e_dt.day)


	#Moving average
	ma1 = dp.moving_average(r1.close, int(MA1))
	ma2 = dp.moving_average(r2.close, int(MA1))

	#RSI
	rsi1 = dp.relative_strength(r1.close)
	rsi2 = dp.relative_strength(r2.close)
	#plt.rc('axes', grid=True)
	#plt.rc('grid', color='0.75', linestyle='-', linewidth=0.5)
	plt.rc('axes', grid=True)
	plt.rc('grid', color='0.75', linestyle='-', linewidth=0.5)
	textsize = 9
	left, width = 0.1, 0.8
	rect1 = [left, 0.7, width, 0.2]
	rect2 = [left, 0.3, width, 0.4]
	rect3 = [left, 0.1, width, 0.2]

	fig = plt.figure(facecolor='white')
	axescolor  = '#f6f6f6'  # the axies background color
	props = font_manager.FontProperties(size=10)
	fillcolor = 'darkgoldenrod'
	ax1 = fig.add_axes(rect1, axisbg=axescolor)  #left, bottom, width, height
	ax2 = fig.add_axes(rect2, axisbg=axescolor, sharex=ax1)
	ax2t = ax2.twinx()
	ax3  = fig.add_axes(rect3, axisbg=axescolor, sharex=ax1)
	ax3t = ax3.twinx()
	#print self.r.date
	#r.date error
	#xdata = r.date
	xdata = range(0,len(r1.close))

	ax1.plot(xdata, rsi1, color='blue')
	ax1.plot(xdata, rsi2, color='red')
	ax1.axhline(70, color=fillcolor)
	ax1.axhline(30, color=fillcolor)
	#ax1.fill_between(xdata, rsi, 70, where=(rsi>=70), facecolor=fillcolor, edgecolor=fillcolor)
	#ax1.fill_between(xdata, rsi, 30, where=(rsi<=30), facecolor=fillcolor, edgecolor=fillcolor)
	ax1.text(0.6, 0.9, '>70 = overbought', va='top', transform=ax1.transAxes, fontsize=textsize)
	ax1.text(0.6, 0.1, '<30 = oversold', transform=ax1.transAxes, fontsize=textsize)
	ax1.set_ylim(0, 100)
	ax1.set_yticks([30,70])
	ax1.text(0.025, 0.95, 'RSI (14)', va='top', transform=ax1.transAxes, fontsize=textsize)

	if(LANG == "jp"):
		props_jp = font_manager.FontProperties(size=12,fname=FONT_DIR + FONT)
		ax1.set_title(str(stock1.name).decode('utf-8') + " VS " + str(stock2.name).decode('utf-8'), fontproperties=props_jp)
	else:
		ax1.set_title(str(stock1.id) + " VS " + str(stock2.id))

	ax2.plot(xdata, r1.close, color='blue', lw=2, label=str(stock1.id))
	ax2t.plot(xdata, r2.close, color='red', lw=2, label=str(stock2.id))
	#print r.date
	deltas = np.zeros_like(r1.close)
	deltas[1:] = np.diff(r1.close)
	up = deltas>0
	#ax2.vlines(xdata[up], r.low[up], r.high[up], color='black', label='_nolegend_')
	#ax2.vlines(xdata[~up], r.low[~up],r.high[~up], color='black', label='_nolegend_')
	#linema10, = ax2.plot(xdata, ma1, color='blue', lw=2, label='MA (' + str(MA1) + ')')
	#linema20, = ax2.plot(xdata, ma2, color='red', lw=2, label='MA (' + str(MA2) + ')')


	leg1 = ax2.legend(loc='upper left', shadow=True, fancybox=True, prop=props)
	leg1.get_frame().set_alpha(0.5)
	leg2 = ax2t.legend(loc='upper right', shadow=True, fancybox=True, prop=props)
	leg2.get_frame().set_alpha(0.5)

	#volume = (r.close * r.volume)/1e6  # dollar volume in millions
	#vmax = volume.max()
	#poly = ax2t.fill_between(xdata, volume, 0, label=lang.VOL, facecolor=fillcolor, edgecolor=fillcolor)
	#ax2t.set_ylim(0, 5*vmax)
	#ax2t.set_yticks([])
	class MyLocator(mticker.MaxNLocator):
		def __init__(self, *args, **kwargs):
			mticker.MaxNLocator.__init__(self, *args, **kwargs)

		def __call__(self, *args, **kwargs):
			return mticker.MaxNLocator.__call__(self, *args, **kwargs)

			#print "Plot"
	ax3.plot(xdata,ma1, color='blue', lw=2)
	ax3t.plot(xdata,ma2, color='red', lw=2)

	for ax in ax1, ax2, ax2t, ax3:
		if ax!=ax3:
			for label in ax.get_xticklabels():
				label.set_visible(False)
		else:
			for label in ax.get_xticklabels():
				label.set_rotation(30)
				label.set_horizontalalignment('right')

		ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')

	ax2.yaxis.set_major_locator(MyLocator(5, prune='both'))
	ax3.yaxis.set_major_locator(MyLocator(5, prune='both'))

	plt.show()

def today_trade(stock,trade):
	today = datetime.date.today()
	start_date = "2000-1-1"
	s_dt = datetime.date(*[int(val) for val in start_date.split('-')])
	#print stock.id,stock.name,today
	r = dp.get_data_by_day(stock,s_dt,today.year,today.month,today.day)
	trade.price_history = r.close
	sell_wish_price, sell_type = trade.rule.sell(stock,trade,today)
	buy_wish_price, buy_type = trade.rule.buy(stock,trade,today)
	return sell_wish_price, sell_type,buy_wish_price, buy_type
def stock_search(search):
	#SEARCH_MARKET, MAX_TOTAL_ASSET, MAX_NET_PROFIT, MAX_EQUITY_RATIO, MAX_PBR, MAX_PER, MAX_EPS, MAX_BPS, MAX_ROA, MAX_ROE
	#MIN_TOTAL_ASSET, MIN_NET_PROFIT, MIN_EQUITY_RATIO, MIN_PBR, MIN_PER, MIN_EPS, MIN_BPS, MIN_ROA, MIN_ROE
	if(int(search.market[0]) == int(SEARCH_MARKET) or int(SEARCH_MARKET)==0):	#市場
		if(int(search.ta) >= int(MIN_TOTAL_ASSET)):	#総資産[百万円]
			#print search.id,search.name
			if(int(search.ta) <= int(MAX_TOTAL_ASSET) or int(MAX_TOTAL_ASSET) <= 0):	#総資産[百万円]
				#print search.id,search.name
				if(int(search.np) >= int(MIN_NET_PROFIT)):	#当期利益
					if(int(search.np) <= int(MAX_NET_PROFIT) or int(MAX_NET_PROFIT) <= 0):	#当期利益
						#print search.id,search.name
						if(int(search.eps) >= int(MIN_EPS)):	#EPS
							if(int(search.eps) <= int(MAX_EPS) or int(MAX_EPS) <= 0):	#eps
								#print search.id,search.name
								if(int(search.bps) >= int(MIN_BPS)):	#BPS
									if(int(search.bps) <= int(MAX_BPS) or int(MAX_BPS) <= 0):	#bps
										#print search.id,search.name
										if(float(search.pbr) <= float(MAX_PBR) and float(search.pbr) >= float(MIN_PBR)):	#PBR（株価純資産倍率）
											#print search.id,search.name
											if(float(search.per) <= float(MAX_PER) and float(search.per) >= float(MIN_PER)):	#PER（株価純資産倍率）
												#print search.id,search.name
												if(float(search.er) >= float(MIN_EQUITY_RATIO) and float(search.er) <= float(MAX_EQUITY_RATIO)):	#自己資本比率[%]
													#print search.id,search.name,MIN_EQUITY_RATIO,MAX_EQUITY_RATIO
													if(float(search.roa) <= float(MAX_ROA) and float(search.roa) >= float(MIN_ROA)):	#PER（株価純資産倍率）
														#print search.id,search.name,MIN_EQUITY_RATIO,MAX_EQUITY_RATIO
														if(float(search.roe) >= float(MIN_ROE) and float(search.roe) <= float(MAX_ROE)):	#自己資本比率[%]
															#print search.id,search.name
															search.result.append([search.id,search.name,search.cate,search.market,search.vol,search.dividend,
																		search.per,search.pbr,search.eps,search.bps,search.unit,search.compliment,search.nop,
																		search.op,search.np,search.ta,search.lc,search.er,search.roa,search.roe])
															#search.result.append(search)
	#return ret_ids

def search_stock(search):
	datas = dp.open_file(DATA_DIR,STOCK_FILE)
	search.result = []
	for data in datas:
		if not data:
			continue
		data = data.strip()
		#print data
		datail_data = data.split(',')
		#print "detail =",len(datail_data)
		search.id = int(datail_data[0])	#ID
		search.name = datail_data[1]	#企業名
		search.cate = datail_data[2]	#業種
		if(datail_data[3].find(" ")):	#市場
			search.market = datail_data[3].split(" ")
		else:
			search.market[0] = int(datail_data[3])
		search.vol= int(datail_data[4])	#発行株数
		search.dividend = datail_data[5]	#配当
		search.per = float(datail_data[6])	#PER（株価収益率）
		search.pbr = float(datail_data[7])	#PBR（株価純資産倍率）
		search.eps = float(datail_data[8])	#EPS（一株当たり利益）[円]
		search.bps = float(datail_data[9])	#BPS（一株当たり純資産）[円]
		search.unit = int(datail_data[10])	#単元株
		search.compliment = int(datail_data[11])	#株式優待
		if(len(datail_data) > 12):
			search.nop = int(datail_data[16])	#営業利益
			search.op = int(datail_data[17])	#経常利益
			search.np = int(datail_data[18])	#当期利益
			search.ta = int(datail_data[22])	#総資産
			search.lc = int(datail_data[22])	#資本金
			search.er = float(datail_data[26])	#自己資本比率[%]
			search.roa = float(datail_data[28])	#ROA（総資産利益率）[%]
			search.roe = float(datail_data[29])	#ROE（自己資本利益率）[%]
		stock_search(search)
	print "search was done"

def get_plugin_list(dir):
	plugin_list = []
	for fdn in os.listdir(dir):
		if fdn.endswith(".py"):
			plugin = fdn.replace(".py","")
			plugin_list.append(plugin)
	return plugin_list

def get_plugin(dir,name):
	cwd = os.getcwd()
	moduledir = os.path.join(cwd,dir)
	plugin_name = name + ".py"
	plugin = load_plugin(moduledir,plugin_name)   # Pluginを読み込む
	return plugin

def load_module(module_name,basepath):
	""" モジュールをロードして返す
	"""
	f,n,d = imp.find_module(module_name,[basepath])
	return imp.load_module(module_name,f,n,d)
def load_plugin(basepath,plugin_file):
	try:
		m = load_module(plugin_file.replace(".py",""),basepath)
		return m
	except ImportError:
		pass
	return

if __name__ == "__main__":
	main()
