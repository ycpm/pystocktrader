#!/usr/bin/python
# coding: UTF-8
import os
import sys
import imp
import wx
import wx.lib.sheet as sheet
import numpy as np
from string import *
import re
import datetime
import time
import matplotlib
matplotlib.use( 'WXAgg' )
import matplotlib.font_manager as font_manager
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
sys.path.append('./lib/')
import data_process as dp
import simulator as sim
import stock_conv as sc
#import get_detail as gd
WINDOW_X = 1000
WINDOW_Y = 800
ICON_DIR = "./icons/"
DATE = 0
DAY_DATA = "DAY_"

PRJ_DIR = "./project/"
PRJ_NAME = "TEST"
PRJ_FILE = ""
PRJ_EXT = "*.py"
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

#Moving Average
MA1 = 25
MA2 = 100
#RSI RCI
RSI_RCI=0	#0:RSI, 1:RCI
RSI_DAY = 14
RCI_DAY = 9
RSI_UPPER = 70
RSI_LOWER = 30
RCI_UPPER = 90
RCI_LOWER = -90
#Flag
DONE_SIM = 0

#DL_STOCK_CODES = "4689,8473,7203,1400,998407,998405,23337,^DJI,^IXIC,^GSPC,^HSI,000001.SS"
DL_STOCK_CODES = "4689,8473,7203,1400,998407,998405,2379"

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

#wx FONT
WX_FONT_SIZE = 10
WX_FONT_FAMLY = "wxDEFAULT"
WX_FONT_FACE = "Verdana"
WX_FONT_STYLE = "wxNORMAL"
#Font
GRAPH_FONT_FILE = ""
GRAPH_FONT_SIZE = 10
GRAPH_FONT_FAMLY = "sans-serif"
GRAPH_FONT_STYLE = "normal"

#Multi Processor
MP = 0
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
		self.day_price = []
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
		self.mp = MP
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
		icon=wx.EmptyIcon()
		icon_file = wx.Image('icon.png',wx.BITMAP_TYPE_PNG)
		icon.CopyFromBitmap(icon_file.ConvertToBitmap())
		self.SetIcon(icon)
		#font
		font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)
		#wx.Font(integer pointSize, wx.FontFamily family, integer style, integer weight,
		#			bool underline = false, string faceName = '',
		#			wx.FontEncoding encoding = wx.FONTENCODING_DEFAULT)
		#heading = wx.StaticText(self, -1, 'The Central Europe', (130, 15))
		#heading.SetFont(font)
		# Setting up the menu.
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
		viewmenu = wx.Menu()
		#menuWFontSetUp = viewmenu.Append(wx.NewId(),lang.MENU_WFONT," Set up Window Font")
		menuGFontSetUp = viewmenu.Append(wx.NewId(),lang.MENU_GFONT," Set up Graph Font")
		# Creating the menubar.
		menuBar = wx.MenuBar()
		menuBar.Append(filemenu,lang.MENU_FILE) # Adding the "filemenu" to the MenuBar
		menuBar.Append(setupmenu,lang.MENU_SETUP) # Adding the "filemenu" to the MenuBar
		menuBar.Append(viewmenu,lang.MENU_VIEW_SETUP) # Adding the "filemenu" to the MenuBar
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
		#self.Bind(wx.EVT_MENU, self.OnWFont, menuWFontSetUp)
		self.Bind(wx.EVT_MENU, self.OnGFont, menuGFontSetUp)
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
		#hbox0 = wx.BoxSizer(wx.HORIZONTAL)
		sizer = wx.GridBagSizer(0, 50)
		self.prj_txt = wx.StaticText(panel, -1, lang.PROJECT_FILE + " : " + PRJ_FILE,style=wx.TE_LEFT)
		#hbox0.Add(prj_txt, 0, flag= wx.LEFT | wx.TOP, border=10)
		sizer.Add(self.prj_txt, (0, 0), flag= wx.LEFT | wx.TOP, border=5)
		self.prj_name = wx.StaticText(panel, -1, lang.PROJECT_NAME + " : " + PRJ_NAME,style=wx.TE_CENTER)
		#hbox0.Add(prj_file, 0, flag= wx.LEFT | wx.TOP, border=10)
		sizer.Add(self.prj_name, (0, 3), flag= wx.RIGHT | wx.TOP, border=5)
		vbox.Add(sizer, 0, wx.ALIGN_LEFT | wx.LEFT, 10)

		#Draw data
		self.panel2 = wx.Panel(panel, -1)
		hbox1 = wx.BoxSizer(wx.HORIZONTAL)

		self.plot = myWxPlot(self.panel2)

		hbox1.Add(self.plot, 1, wx.EXPAND | wx.ALL, 2)
		self.panel2.SetSizer(hbox1)
		vbox.Add(self.panel2, 1,  wx.LEFT | wx.RIGHT | wx.EXPAND, 2)

		hbox2 = wx.BoxSizer(wx.HORIZONTAL)
		rsi_btn = wx.ToggleButton(panel, 1, 'RSI', (20, 25))
		rci_btn = wx.ToggleButton(panel, 2, 'RCI', (40, 25))
		#wx.ToggleButton(self, 3, 'blue', (20, 100))
		#btn2 = wx.Button(panel, -1, lang.CLOSE, size=(70, 30))
		hbox2.Add(rsi_btn, 0, wx.LEFT | wx.BOTTOM , 5)
		hbox2.Add(rci_btn, 0, wx.LEFT | wx.BOTTOM , 5)
		vbox.Add(hbox2, 0, wx.ALIGN_RIGHT | wx.RIGHT, 10)

		panel.SetSizer(vbox)
		self.Centre()
		self.Show(True)

		#Event
		#self.Bind(wx.EVT_BUTTON, self.OnExit, btn2)
		self.Bind(wx.EVT_TOGGLEBUTTON, self.ToggleRSI, id=1)
		self.Bind(wx.EVT_TOGGLEBUTTON, self.ToggleRCI, id=2)

		self.plot.fig.clear()
		if self.plot.set_data():
			self.plot.setsize()
			self.plot.draw()
			self.plot.fig.canvas.draw()
	def ToggleRSI(self,e):
		global RSI_RCI
		RSI_RCI=0
		self.plot.fig.clear()
		if self.plot.set_data():
			self.plot.setsize()
			self.plot.draw()
			self.plot.fig.canvas.draw()
		
	def ToggleRCI(self,e):
		global RSI_RCI
		RSI_RCI=1
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
		global PRJ_DIR,PRJ_FILE,DONE_SIM
		self.dirname = PRJ_DIR
		dlg = wx.FileDialog(self, lang.SELECT_PROJ, self.dirname, "", PRJ_EXT, wx.OPEN)
		if dlg.ShowModal() == wx.ID_OK:
			PRJ_FILE = dlg.GetFilename()
			PRJ_DIR = dlg.GetDirectory()
			DONE_SIM = 0
		dlg.Destroy()
		read_prj()
		self.prj_txt.SetLabel(lang.PROJECT_FILE + " : " + PRJ_FILE)
		self.prj_name.SetLabel(lang.PROJECT_NAME + " : " + PRJ_NAME)
		self.plot.fig.clear()
		if self.plot.set_data():
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
		if self.plot.set_data():
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
		DONE_SIM = 1
		if(int(sim_data.val_num2) > 1):
			disp_2d()
		else:
			self.plot.fig.clear()
			if self.plot.set_data():
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
		dl = get_plugin(DATA_SITE_DIR,DATA_SITE)
		stock_ids = [int(stock_id) for stock_id in DL_STOCK_CODES.split(",")]
		dl.get_stock_data(stock_ids)
		wx.MessageBox(lang.DL_DONE, lang.INFO, wx.OK | wx.ICON_INFORMATION)
	def OnDetailDL(self,e):
		dl = get_plugin(DATA_SITE_DIR,DATA_SITE)
		ddl = wx.MessageBox(lang.DL_CONFIRM, lang.CONFIRM, wx.YES_NO | wx.NO_DEFAULT| wx.ICON_QUESTION)
		if ddl == wx.YES:
			self.progress = wx.ProgressDialog(lang.DetailDL_TITLE,lang.DetailDL_PRO_MSG, maximum = 100, parent=self, style = wx.PD_CAN_ABORT | wx.PD_AUTO_HIDE | wx.PD_APP_MODAL)
			self.progress.SetSize((300, 100))
			dl.get_detail_data(self)
			self.progress.Update(100, lang.DetailDL_PRO_FINISH)
			self.progress.Destroy()
			wx.MessageBox(lang.DL_DONE, lang.INFO, wx.OK | wx.ICON_INFORMATION)

	def OnTodayTrade(self,e):
		tr= trade(TARGET_CODE)
		stock = stock_data(TARGET_CODE)
		tr.market = TARGET_MARKET
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
	def OnWFont(self,e):
		global WX_FONT_SIZE, WX_FONT_FAMLY, WX_FONT_FACE, WX_FONT_STYLE
		default_font = wx.Font(10, wx.SWISS , wx.NORMAL, wx.NORMAL, False, "Verdana")
		data = wx.FontData()
		if sys.platform == 'win32':
			data.EnableEffects(True)
		data.SetAllowSymbols(False)
		data.SetInitialFont(default_font)
		data.SetRange(10, 30)
		dlg = wx.FontDialog(self, data)
		if dlg.ShowModal() == wx.ID_OK:
			data = dlg.GetFontData()
			font = data.GetChosenFont()
			color = data.GetColour()
			text = 'Face: %s, Famly: %s, Size: %d, Style No: %d, Style: %s, native: %s, native user: %s,' % (font.GetFaceName(),font.GetFamilyString(), font.GetPointSize(), font.GetStyle(), font.GetStyleString(), font.GetNativeFontInfoDesc(),font.GetNativeFontInfoUserDesc())
			WX_FONT_SIZE = font.GetPointSize()
			WX_FONT_FAMLY = font.GetFamilyString()
			WX_FONT_FACE = font.GetFaceName()
			WX_FONT_STYLE = font.GetStyle()
			#self.SetStatusText(text)
		dlg.Destroy()
		wx.MessageBox(text, "Font data", wx.OK | wx.ICON_INFORMATION)
	def OnGFont(self,e):
		gf = SetGraphFont(None, -1, "Graph Font")
		gf.ShowModal()
		gf.Destroy()
		self.plot.fig.clear()
		if self.plot.set_data():
			self.plot.setsize()
			self.plot.draw()
			self.plot.fig.canvas.draw()
class myWxPlot(wx.Panel):
	def __init__( self, parent):
		from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
		
		self.parent = parent
		wx.Panel.__init__( self, parent)

		plt.rc('axes', grid=True)
		plt.rc('grid', color='0.75', linestyle='-', linewidth=0.5)
		#plt.ticklabel_format(useLocale = False)
		self.fig = plt.Figure( None, facecolor='white')

		#canvas
		self.canvas = FigureCanvasWxAgg( self, -1, self.fig )
		self.canvas.SetBackgroundColour( wx.Color( 255,255,255 ) )

		if self.set_data():
			self.setsize()
			self.draw()

	def set_data(self):
		#print "Set data",DONE_SIM
		global MA1,MA2
		self.stock = stock_data(TARGET_CODE)
		s_dt = datetime.date(*[int(val) for val in START_DATE.split('-')])
		e_dt = datetime.date(*[int(val) for val in END_DATE.split('-')])
		margin = int(MA2)
		if(margin < int(MA1)):
			margin =int(MA1)
		self.r = dp.get_data_by_day(self.stock,s_dt,e_dt.year,e_dt.month,e_dt.day)
		n =len(self.r.close)
		if(n < 1):
			print "Data Error r"
			return False
		r2 = dp.get_data_by_day_num(self.stock,e_dt,n+margin)
		if(len(r2.close)  < 1):
			print "Data Error r2"
			return False
		if(len(r2.close)<=n):
			r2=self.r
		#Moving average
		if(len(r2.close) >= int(MA1)):
			ma1 = dp.moving_average(r2.close, int(MA1))
		else:
			MA1 = len(r2.close)
			ma1 = dp.moving_average(r2.close, int(MA1))
		if(len(r2.close) >= int(MA2)):
			ma2 = dp.moving_average(r2.close, int(MA2))
		else:
			MA2 = len(r2.close)
			ma2 = dp.moving_average(r2.close, int(MA2))
		if(len(ma1) > n):
			self.ma1 = ma1[margin:]
			self.ma2 = ma2[margin:]
		else:
			self.ma1 = ma1
			self.ma2 = ma2
		#RSI RCI
		if(RSI_RCI==0):
			self.rsi = dp.relative_strength(self.r.close,RSI_DAY)
			self.rsi_rci_upper = RSI_UPPER
			self.rsi_rci_lower = RSI_LOWER
		else:
			self.rsi = dp.rci_array(self.r.close,RCI_DAY)
			self.rsi_rci_upper = RCI_UPPER
			self.rsi_rci_lower = RCI_LOWER

		if(DONE_SIM):
			resource_datas = dp.open_file(LOG_DIR,RESOURCE_LOG)
			self.res_datas = []
			self.res_vals = []
			for i in range(0,SIM_VAL_NUM):				
				self.res_datas.append([])
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

		self.canvas.SetSize( size )
		self.fig.set_size_inches( float( size[0] )/self.fig.get_dpi(),
									 float( size[1] )/self.fig.get_dpi() )

	def draw(self):
		#For UnicodeDecodeError
		reload(sys)
		sys.setdefaultencoding('utf-8')
		plt.ticklabel_format(useLocale = False)
		#print sys.getdefaultencoding()
		if(re.search(DAY_DATA,str(self.stock.id))):
			xdata = range(0,len(self.r.close))
		else:
			xdata = self.r.date

		if(GRAPH_FONT_FILE):
			props = font_manager.FontProperties(fname=GRAPH_FONT_FILE, style=GRAPH_FONT_STYLE, size=GRAPH_FONT_SIZE)
		else:
			props = font_manager.FontProperties(family=GRAPH_FONT_FAMLY, style=GRAPH_FONT_STYLE, size=GRAPH_FONT_SIZE)
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
		#print sys.getdefaultencoding()
		ax1.plot(xdata, self.rsi, color=fillcolor)

		ax1.axhline(self.rsi_rci_upper, color=fillcolor)
		ax1.axhline(self.rsi_rci_lower, color=fillcolor)
		ax1.fill_between(xdata, self.rsi, self.rsi_rci_upper, where=(self.rsi>=self.rsi_rci_upper), facecolor=fillcolor, edgecolor=fillcolor)
		ax1.fill_between(xdata, self.rsi, self.rsi_rci_lower, where=(self.rsi<=self.rsi_rci_lower), facecolor=fillcolor, edgecolor=fillcolor)
		ax1.text(0.6, 0.9, '>' + str(self.rsi_rci_upper) + ' = overbought', va='top', transform=ax1.transAxes, fontsize=textsize)
		ax1.text(0.6, 0.1, '<' + str(self.rsi_rci_lower) + ' = oversold', transform=ax1.transAxes, fontsize=textsize)
		ax1.set_yticks([self.rsi_rci_lower,self.rsi_rci_upper])
		if(RSI_RCI==0):	#RSI
			ax1.set_ylim(0, 100)
			ax1.text(0.025, 0.95, 'RSI (' + str(RSI_DAY) + ')', va='top', transform=ax1.transAxes, fontproperties=props, fontsize=textsize)
		else:
			ax1.set_ylim(-200, 200)
			ax1.text(0.025, 0.95, 'RCI (' + str(RCI_DAY) + ')', va='top', transform=ax1.transAxes, fontproperties=props, fontsize=textsize)

		if(LANG == "jp"):
			ax1.set_title('%s daily'%self.stock.name.decode('utf-8'), fontproperties=props)
		else:
			ax1.set_title('%s daily'%self.stock.id, fontproperties=props)
		#print sys.getdefaultencoding()
		if(re.search(DAY_DATA,str(self.stock.id))):
			ax2.plot(xdata, self.r.close, color='black', lw=2)
		else:
			deltas = np.zeros_like(self.r.close)
			deltas[1:] = np.diff(self.r.close)
			up = deltas>0
			ax2.vlines(xdata[up], self.r.low[up], self.r.high[up], color='black', label='_nolegend_')
			ax2.vlines(xdata[~up], self.r.low[~up],self.r.high[~up], color='black', label='_nolegend_')

		linema10, = ax2.plot(xdata, self.ma1, color='blue', lw=2, label='MA (' + str(MA1) + ')')
		linema20, = ax2.plot(xdata, self.ma2, color='red', lw=2, label='MA (' + str(MA2) + ')')

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
				for i in range(0,SIM_VAL_NUM):
					if(len(self.res_datas[i]) == len(xdata)):
						ax3.plot(xdata, self.res_datas[i], lw=2, label='Val[' + str(i) + '] = ' + str(self.res_vals[i]))
				leg3 = ax3.legend(loc='upper left', shadow=True, fancybox=True, prop=props)
				leg3.get_frame().set_alpha(0.5)
			else:
				if(len(self.res_datas[0]) == len(xdata)):
					ax3.plot(xdata, self.res_datas[0], color='black', lw=2)
			ax3.text(0.025, 0.95, lang.SIMU_RESULT + " : " + RULE, va='top',
					transform=ax3.transAxes, fontproperties=props, fontsize=textsize)
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
				transform=ax3.transAxes, fontproperties=props, fontsize=textsize)
			#ax3.formatter.use_locale('en_US')

		for ax in ax1, ax2, ax2t, ax3:
			if ax!=ax3:
				for label in ax.get_xticklabels():
					label.set_visible(False)
			else:
				for label in ax.get_xticklabels():
					label.set_rotation(30)
					label.set_horizontalalignment('right')
					label.set_fontproperties(props)

			ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
			#ax.fmt_xdata = mdates.DateFormatter('%Y-%M-%D')

		#ax3.set_xticklabels(xdata,fontproperties=props)

		ax2.yaxis.set_major_locator(MyLocator(5, prune='both'))
		ax3.yaxis.set_major_locator(MyLocator(5, prune='both'))
		#print sys.getdefaultencoding()
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

		mp_txt = wx.StaticText(panel, -1, lang.MULTI_PROCESS)
		sizer.Add(mp_txt, (11, 0), flag= wx.LEFT | wx.TOP, border=10)
		self.mp = wx.CheckBox(panel, -1, lang.MP_MSG)
		self.mp.SetValue(MP)
		sizer.Add(self.mp, (11, 1), (1, 1), wx.TOP | wx.EXPAND,  5)


		ok_button = wx.Button(panel, -1, lang.OK, size=(-1, 30))
		sizer.Add(ok_button, (13, 2), (1, 1),  wx.LEFT, 10)

		close_button = wx.Button(panel, -1, lang.CLOSE, size=(-1, 30))
		sizer.Add(close_button, (13, 3), (1, 1),  wx.LEFT | wx.BOTTOM | wx.RIGHT, 10)
		sizer.AddGrowableCol(2)

		panel.SetSizer(sizer)
		sizer.Fit(self)
		# Events.
		self.Bind(wx.EVT_BUTTON, self.OnOK, ok_button)
		self.Bind(wx.EVT_BUTTON, self.OnClose, close_button)	

		self.Centre()
		self.Show(True)

	def OnOK(self,e):
		global AGENT, RULE, SIM_START_MONEY,TARGET_CODE, START_DATE,END_DATE, SIM_VAL_ID, SIM_VAL_NUM, SIM_VAL_START, SIM_VAL_END, SIM_VAL_STEP, SIM_VAL_ID2, SIM_VAL_NUM2, SIM_VAL_START2, SIM_VAL_END2, SIM_VAL_STEP2,MP
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
		MP = int(self.mp.IsChecked())
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

		#MA
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

		#RSI
		rsi_day_txt = wx.StaticText(panel, -1, lang.RSI_DAY)
		sizer.Add(rsi_day_txt, (4, 0), flag= wx.LEFT | wx.TOP, border=10)
		self.rsi_day = wx.TextCtrl(panel, -1)
		self.rsi_day.SetValue(str(RSI_DAY))
		sizer.Add(self.rsi_day, (4, 1), (1, 1), wx.TOP | wx.EXPAND,  5)

		rsi_upper_txt = wx.StaticText(panel, -1, lang.RSI_UPPER)
		sizer.Add(rsi_upper_txt, (4, 2), flag= wx.LEFT | wx.TOP, border=10)
		self.rsi_upper = wx.TextCtrl(panel, -1)
		self.rsi_upper.SetValue(str(RSI_UPPER))
		sizer.Add(self.rsi_upper, (4, 3), (1, 1), wx.TOP | wx.EXPAND,  5)

		rsi_lower_txt = wx.StaticText(panel, -1, lang.RSI_LOWER)
		sizer.Add(rsi_lower_txt, (4, 4), flag= wx.LEFT | wx.TOP, border=10)
		self.rsi_lower = wx.TextCtrl(panel, -1)
		self.rsi_lower.SetValue(str(RSI_LOWER))
		sizer.Add(self.rsi_lower, (4, 5), (1, 1), wx.TOP | wx.EXPAND,  5)

		#RCI
		rci_day_txt = wx.StaticText(panel, -1, lang.RCI_DAY)
		sizer.Add(rci_day_txt, (5, 0), flag= wx.LEFT | wx.TOP, border=10)
		self.rci_day = wx.TextCtrl(panel, -1)
		self.rci_day.SetValue(str(RCI_DAY))
		sizer.Add(self.rci_day, (5, 1), (1, 1), wx.TOP | wx.EXPAND,  5)

		rci_upper_txt = wx.StaticText(panel, -1, lang.RCI_UPPER)
		sizer.Add(rci_upper_txt, (5, 2), flag= wx.LEFT | wx.TOP, border=10)
		self.rci_upper = wx.TextCtrl(panel, -1)
		self.rci_upper.SetValue(str(RCI_UPPER))
		sizer.Add(self.rci_upper, (5, 3), (1, 1), wx.TOP | wx.EXPAND,  5)

		rci_lower_txt = wx.StaticText(panel, -1, lang.RCI_LOWER)
		sizer.Add(rci_lower_txt, (5, 4), flag= wx.LEFT | wx.TOP, border=10)
		self.rci_lower = wx.TextCtrl(panel, -1)
		self.rci_lower.SetValue(str(RCI_LOWER))
		sizer.Add(self.rci_lower, (5, 5), (1, 1), wx.TOP | wx.EXPAND,  5)
		#Button
		ok_button = wx.Button(panel, -1, lang.OK, size=(-1, 30))
		sizer.Add(ok_button, (7, 2), (1, 1),  wx.LEFT, 10)

		close_button = wx.Button(panel, -1, lang.CLOSE, size=(-1, 30))
		sizer.Add(close_button, (7, 3), (1, 1),  wx.LEFT | wx.BOTTOM | wx.RIGHT, 10)
		sizer.AddGrowableCol(2)

		panel.SetSizer(sizer)
		sizer.Fit(self)
		# Events.
		self.Bind(wx.EVT_BUTTON, self.OnOK, ok_button)
		self.Bind(wx.EVT_BUTTON, self.OnClose, close_button)	

		self.Centre()
		self.Show(True)

	def OnOK(self,e):	
		global TARGET_CODE, START_DATE,END_DATE,MA1,MA2,RSI_DAY,RSI_UPPER,RSI_LOWER,RCI_DAY,RCI_UPPER,RCI_LOWER
		if(self.code.GetValue()):
			TARGET_CODE = self.code.GetValue()
		if(self.ma1.GetValue()):
			MA1 = int(self.ma1.GetValue())
		if(self.ma2.GetValue()):
			MA2 = int(self.ma2.GetValue())
		if(self.rsi_day.GetValue()):
			RSI_DAY = int(self.rsi_day.GetValue())
		if(self.rsi_upper.GetValue()):
			RSI_UPPER = int(self.rsi_upper.GetValue())
		if(self.rsi_lower.GetValue()):
			RSI_LOWER = int(self.rsi_lower.GetValue())
		if(self.rci_day.GetValue()):
			RCI_DAY = int(self.rci_day.GetValue())
		if(self.rci_upper.GetValue()):
			RCI_UPPER = int(self.rci_upper.GetValue())
		if(self.rci_lower.GetValue()):
			RCI_LOWER = int(self.rci_lower.GetValue())

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
		#For UnicodeDecodeError
		reload(sys)
		sys.setdefaultencoding('utf-8')
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
					value = str(value).decode('utf8')
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
class SetGraphFont(wx.Dialog):
	def __init__(self, parent, id, title):
		wx.Dialog.__init__(self, parent, id, title, size=(800, 500))
		if os.name == 'posix':
			font_list = font_manager.findSystemFonts()
		elif os.name == 'nt':
			font_list = font_manager.win32InstalledFonts()
		elif os.name == 'mac':
			font_list = font_manager.OSXInstalledFonts()
		self.font_name={}
		for font_file in font_list:
			#print font_file
			font=font_manager.ft2font.FT2Font(str(font_file))
			font_info = font_manager.ttfFontProperty(font)
			#print font_info.name
			fontname = font_info.name
			#filename = os.path.basename(font_file)
			#fontname = filename.replace(".ttf","")
			self.font_name[fontname] = font_file

		self.fonts =self.font_name.keys()
		font_size = ['10', '11', '12', '14', '16']

		panel = wx.Panel(self, -1)
		sizer = wx.GridBagSizer(0, 0)

		font_txt = wx.StaticText(panel, -1, "Font : ")
		sizer.Add(font_txt, (0, 0), flag= wx.LEFT | wx.TOP, border=10)

		self.font = wx.ComboBox(panel, -1, pos=(50, 170), size=(150, -1), choices=self.fonts, 
					style=wx.CB_READONLY)
		sizer.Add(self.font, (0, 2), (1, 3), wx.TOP | wx.EXPAND, 5)

		ok_button = wx.Button(panel, -1, lang.OK, size=(-1, 30))
		sizer.Add(ok_button, (2, 3), (1, 1),  wx.LEFT, 10)

		close_button = wx.Button(panel, -1, lang.CLOSE, size=(-1, 30))
		sizer.Add(close_button, (2, 4), (1, 1),  wx.LEFT | wx.BOTTOM | wx.RIGHT, 10)

		#sizer.AddGrowableCol(2)

		panel.SetSizer(sizer)
		sizer.Fit(self)
		# Events.

		self.Bind(wx.EVT_BUTTON, self.OnOK, ok_button)
		self.Bind(wx.EVT_BUTTON, self.OnClose, close_button)
		self.Centre()
		self.Show(True)
	def OnOK(self,e):
		global GRAPH_FONT_SIZE, GRAPH_FONT_FAMLY, GRAPH_FONT_FACE, GRAPH_FONT_STYLE, GRAPH_FONT_FILE
		if(self.font.GetSelection() >= 0):
			f_num = int(self.font.GetSelection())
			fontname = self.fonts[f_num]
			GRAPH_FONT_FILE = self.font_name[fontname]
		self.Close(True)  # Close the frame.
	def OnClose(self,e):
		self.Close(True)  # Close the frame.

def main():
	global lang
	#read_ini()
	lang = get_plugin(LANG_DIR, LANG)
	app = wx.App()
	MainFrame(None, -1, 'pyStockTrader')
	app.MainLoop()
def save_prj():
	config_data ='PRJ_NAME = "' + str(PRJ_NAME) + "\"\n"
	config_data += "BORDER_MONEY = " + str(BORDER_MONEY) + "\n"
	config_data += 'TARGET_CODE = "' + str(TARGET_CODE) + "\"\n"
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
	#config_data += 'DL_CYCLE = ' + str(DL_CYCLE) + "\n"
	#config_data += 'FONT = "' + str(FONT) + "\"\n"

	#RSI RCI
	config_data += "RSI_RCI = " + str(RSI_RCI) + "\n"
	config_data += "RSI_DAY = " + str(RSI_DAY) + "\n"
	config_data += "RCI_DAY = " + str(RCI_DAY) + "\n"
	config_data += "RSI_UPPER = " + str(RSI_UPPER) + "\n"
	config_data += "RSI_LOWER = " + str(RSI_LOWER) + "\n"
	config_data += "RCI_UPPER = " + str(RCI_UPPER) + "\n"
	config_data += "RCI_LOWER = " + str(RCI_LOWER) + "\n"

	#For search
	config_data += "SEARCH_MARKET = " + str(SEARCH_MARKET) + "\n"
	config_data += "MAX_TOTAL_ASSET = " + str(MAX_TOTAL_ASSET) + "\n"
	config_data += "MIN_TOTAL_ASSET = " + str(MIN_TOTAL_ASSET) + "\n"
	config_data += "MAX_NET_PROFIT = " + str(MAX_NET_PROFIT) + "\n"
	config_data += "MIN_NET_PROFIT = " + str(MIN_NET_PROFIT) + "\n"
	config_data += "MAX_EQUITY_RATIO = " + str(MAX_EQUITY_RATIO) + "\n"
	config_data += "MIN_EQUITY_RATIO = " + str(MIN_EQUITY_RATIO) + "\n"
	config_data += "MAX_PBR  = " + str(MAX_PBR) + "\n"
	config_data += "MIN_PBR = " + str(MIN_PBR) + "\n"
	config_data += "MAX_PER = " + str(MAX_PER) + "\n"
	config_data += "MIN_PER = " + str(MIN_PER) + "\n"
	config_data += "MAX_EPS = " + str(MAX_EPS) + "\n"
	config_data += "MIN_EPS = " + str(MIN_EPS) + "\n"
	config_data += "MAX_BPS = " + str(MAX_BPS) + "\n"
	config_data += "MIN_BPS = " + str(MIN_BPS) + "\n"
	config_data += "MAX_ROA = " + str(MAX_ROA) + "\n"
	config_data += "MIN_ROA = " + str(MIN_ROA) + "\n"
	config_data += "MAX_ROE = " + str(MAX_ROE) + "\n"
	config_data += "MIN_ROE = " + str(MIN_ROE) + "\n"

	#wx FONT
	config_data += "WX_FONT_SIZE = " + str(WX_FONT_SIZE) + "\n"
	config_data += 'WX_FONT_FAMLY = "' + str(WX_FONT_FAMLY) + "\"\n"
	config_data += 'WX_FONT_FACE = "' + str(WX_FONT_FACE) + "\"\n"
	config_data += 'WX_FONT_STYLE = "' + str(WX_FONT_STYLE) + "\"\n"
	#Graph Font
	config_data += 'GRAPH_FONT_FILE = "' + str(GRAPH_FONT_FILE) + "\"\n"
	config_data += "GRAPH_FONT_SIZE = " + str(GRAPH_FONT_SIZE) + "\n"
	config_data += 'GRAPH_FONT_FAMLY = "' + str(GRAPH_FONT_FAMLY) + "\"\n"
	config_data += 'GRAPH_FONT_STYLE = "' + str(GRAPH_FONT_STYLE) + "\"\n"
	#Multi processor
	config_data += "MP = " + str(MP) + "\n"

	dp.write_file(PRJ_DIR,PRJ_FILE,config_data)

def read_prj():
	global BORDER_MONEY,TARGET_CODE, TARGET_MARKET,TARGET_MAX, USER, LOGIN_PASSWD, TRADE_PASSWD,AGENT, RULE, SIM_START_MONEY, START_DATE, END_DATE, DATA_SITE, LANG, VALS, SIM_VAL_ID, SIM_VAL_START, SIM_VAL_END, SIM_VAL_STEP, SIM_VAL_NUM, SIM_VAL_ID2, SIM_VAL_START2, SIM_VAL_END2, SIM_VAL_STEP2, SIM_VAL_NUM2, DL_CYCLE, MA1, MA2, FONT, PRJ_NAME,DL_STOCK_CODES
	global RSI_RCI, RSI_DAY, RSI_UPPER, RSI_LOWER, RCI_DAY, RCI_UPPER, RCI_LOWER
	global SEARCH_MARKET, MAX_TOTAL_ASSET, MIN_TOTAL_ASSET, MAX_NET_PROFIT, MIN_NET_PROFIT, MAX_EQUITY_RATIO, MIN_EQUITY_RATIO, MAX_PBR, MIN_PBR, MAX_PER, MIN_PER, MAX_EPS, MIN_EPS, MAX_BPS, MIN_BPS, MAX_ROA, MIN_ROA, MAX_ROE, MIN_ROE
	global WX_FONT_SIZE, WX_FONT_FAMLY, WX_FONT_FACE, WX_FONT_STYLE, GRAPH_FONT_FILE, GRAPH_FONT_SIZE, GRAPH_FONT_FAMLY, GRAPH_FONT_STYLE
	global MP
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
	#DL_CYCLE = int(ini.DL_CYCLE)
	MA1 = int(ini.MA1)
	MA2 = int(ini.MA2)
	#FONT = str(ini.FONT)
	PRJ_NAME = str(ini.PRJ_NAME)
	DL_STOCK_CODES = str(ini.DL_STOCK_CODES)

	#RSI
	try:
		RSI_RCI = int(ini.RSI_RCI)
	except AttributeError:
		print "No RSI_RCI data in config file. Use default value"
	try:
		RSI_DAY = int(ini.RSI_DAY)
	except AttributeError:
		print "No RSI_DAY data in config file. Use default value"
	try:
		RSI_UPPER = int(ini.RSI_UPPER)
	except AttributeError:
		print "No RSI_UPPER data in config file. Use default value"
	try:
		RSI_LOWER = int(ini.RSI_LOWER)
	except AttributeError:
		print "No RSI_LOWER data in config file. Use default value"

	#RCI
	try:
		RCI_DAY = int(ini.RCI_DAY)
	except AttributeError:
		print "No RCI_DAY data in config file. Use default value"
	try:
		RCI_UPPER = int(ini.RCI_UPPER)
	except AttributeError:
		print "No RCI_UPPER data in config file. Use default value"
	try:
		RCI_LOWER = int(ini.RCI_LOWER)
	except AttributeError:
		print "No RCI_LOWER data in config file. Use default value"

	#For search
	try:
		SEARCH_MARKET = int(ini.SEARCH_MARKET)
	except AttributeError:
		print "No SEARCH_MARKET data in config file. Use default value"
	try:
		MAX_TOTAL_ASSET = float(ini.MAX_TOTAL_ASSET)
	except AttributeError:
		print "No MAX_TOTAL_ASSET data in config file. Use default value"
	try:
		MIN_TOTAL_ASSET = float(ini.MIN_TOTAL_ASSET)
	except AttributeError:
		print "No MIN_TOTAL_ASSET data in config file. Use default value"
	try:
		MAX_NET_PROFIT = float(ini.MAX_NET_PROFIT)
	except AttributeError:
		print "No MAX_NET_PROFIT data in config file. Use default value"
	try:
		MIN_NET_PROFIT = float(ini.MIN_NET_PROFIT)
	except AttributeError:
		print "No MIN_NET_PROFIT data in config file. Use default value"
	try:
		MAX_EQUITY_RATIO = float(ini.MAX_EQUITY_RATIO)
	except AttributeError:
		print "No MAX_EQUITY_RATIO data in config file. Use default value"
	try:
		MIN_EQUITY_RATIO = float(ini.MIN_EQUITY_RATIO)
	except AttributeError:
		print "No MIN_EQUITY_RATIO data in config file. Use default value"
	try:
		MAX_PBR = float(ini.MAX_PBR)
	except AttributeError:
		print "No MAX_PBR data in config file. Use default value"
	try:
		MIN_PBR = float(ini.MIN_PBR)
	except AttributeError:
		print "No MIN_PBR data in config file. Use default value"
	try:
		MAX_PER  = float(ini.MAX_PER)
	except AttributeError:
		print "No MAX_PER data in config file. Use default value"
	try:
		MIN_PER  = float(ini.MIN_PER)
	except AttributeError:
		print "No MIN_PER data in config file. Use default value"
	try:
		MAX_EPS = float(ini.MAX_EPS)
	except AttributeError:
		print "No MAX_EPS data in config file. Use default value"
	try:
		MIN_EPS = float(ini.MIN_EPS)
	except AttributeError:
		print "No MIN_EPS data in config file. Use default value"
	try:
		MAX_BPS = float(ini.MAX_BPS)
	except AttributeError:
		print "No MAX_BPS data in config file. Use default value"
	try:
		MIN_BPS = float(ini.MIN_BPS)
	except AttributeError:
		print "No MIN_BPS data in config file. Use default value"
	try:
		MAX_ROA = float(ini.MAX_ROA)
	except AttributeError:
		print "No MAX_ROA data in config file. Use default value"
	try:
		MIN_ROA = float(ini.MIN_ROA)
	except AttributeError:
		print "No MIN_ROA data in config file. Use default value"
	try:
		MAX_ROE = float(ini.MAX_ROE)
	except AttributeError:
		print "No MAX_ROE data in config file. Use default value"
	try:
		MIN_ROE = float(ini.MIN_ROE)
	except AttributeError:
		print "No MIN_ROE data in config file. Use default value"

	#wx FONT
	try:
		WX_FONT_SIZE = int(ini.WX_FONT_SIZE)
	except AttributeError:
		print "No WX_FONT_SIZE data in config file. Use default value"
	try:
		WX_FONT_FAMLY = str(ini.WX_FONT_FAMLY)
	except AttributeError:
		print "No WX_FONT_FAMLY data in config file. Use default value"
	try:
		WX_FONT_FACE = str(ini.WX_FONT_FACE)
	except AttributeError:
		print "No WX_FONT_FACE data in config file. Use default value"
	try:
		WX_FONT_STYLE = str(ini.WX_FONT_STYLE)
	except AttributeError:
		print "No WX_FONT_STYLE data in config file. Use default value"

	#Graph Font
	try:
		GRAPH_FONT_FILE = str(ini.GRAPH_FONT_FILE)
	except AttributeError:
		print "No GRAPH_FONT_FILE data in config file. Use default value"
	try:
		GRAPH_FONT_SIZE = int(ini.GRAPH_FONT_SIZE)
	except AttributeError:
		print "No GRAPH_FONT_SIZE data in config file. Use default value"
	try:
		GRAPH_FONT_FAMLY = str(ini.GRAPH_FONT_FAMLY)
	except AttributeError:
		print "No GRAPH_FONT_FAMLY data in config file. Use default value"
	try:
		GRAPH_FONT_STYLE = str(ini.GRAPH_FONT_STYLE)
	except AttributeError:
		print "No GRAPH_FONT_STYLE data in config file. Use default value"
	#Multi Processor
	try:
		MP = int(ini.MP)
	except AttributeError:
		print "No MP data in config file. Use default value"
def disp_2d():
	csv_data = dp.open_file(LOG_DIR, RESOURCE_LOG2)
	if(len(csv_data) < 1):
		print "No simulation data"
		return
	xvals = np.array([float(val) for val in csv_data.pop(0).split(",")])
	yvals = np.array([float(val) for val in csv_data.pop(0).split(",")])
	idx = 0
	x_idx = {}
	for x in xvals:
		x_idx[str(x)] = idx
		idx += 1
	idx = 0
	y_idx = {}
	for y in yvals:
		y_idx[str(y)] = idx
		idx += 1

	y_list = np.zeros((len(yvals), len(xvals)))
	for data in csv_data:
		if not data:
			continue
		val = data.split(",")

		yval = val[0]
		xval = val[1]
		try:
			y_list[y_idx[yval]][x_idx[xval]] = float(val[2])
		except IndexError:
			y_list[y_idx[yval]] = range(0,len(xvals))
			y_list[y_idx[yval]][x_idx[xval]] = float(val[2])

	all_data = np.array(y_list)
	X,Y = np.meshgrid(xvals, yvals)
	plt.title(lang.SIMU_RESULT)
	plt.subplot(111)
	plt.pcolor(X, Y, all_data)
	#plt.imshow(all_datas)
	plt.xlabel('Vals ID = ' + str(SIM_VAL_ID2))
	plt.ylabel('Vals ID = ' + str(SIM_VAL_ID))
	plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
	cax = plt.axes([0.85, 0.1, 0.075, 0.8])
	plt.colorbar(cax=cax)
	plt.show()

def disp_graph():
	global MA1,MA2
	stock = stock_data(TARGET_CODE)
	s_dt = datetime.date(*[int(val) for val in START_DATE.split('-')])
	e_dt = datetime.date(*[int(val) for val in END_DATE.split('-')])

	margin =int(MA2)
	if(margin < int(MA1)):
		margin =int(MA1)

	r = dp.get_data_by_day(stock,s_dt,e_dt.year,e_dt.month,e_dt.day)
	n =len(r.close)
	r2 = dp.get_data_by_day_num(stock,e_dt,n+margin)

	#Moving average
	if(len(r2.close) >= int(MA1)):
		ma1 = dp.moving_average(r2.close, int(MA1))
	else:
		MA1 = len(r2.close)
		ma1 = dp.moving_average(r2.close, int(MA1))
	if(len(r2.close) >= int(MA2)):
		ma2 = dp.moving_average(r2.close, int(MA2))
	else:
		MA2 = len(r2.close)
		ma2 = dp.moving_average(r2.close, int(MA2))
	if(len(ma1) > n):
		ma1 = ma1[margin:]
		ma2 = ma2[margin:]
	else:
		ma1 = ma1
		ma2 = ma2
	#RSI RCI
	if(RSI_RCI==0):
		rsi = dp.relative_strength(r.close,RSI_DAY)
		rsi_rci_upper = RSI_UPPER
		rsi_rci_lower = RSI_LOWER
	else:
		rsi = dp.rci_array(r.close,RCI_DAY)
		rsi_rci_upper = RCI_UPPER
		rsi_rci_lower = RCI_LOWER

	plt.rc('axes', grid=True)
	plt.rc('grid', color='0.75', linestyle='-', linewidth=0.5)
	textsize = 9
	left, width = 0.1, 0.8
	rect1 = [left, 0.7, width, 0.2]
	rect2 = [left, 0.3, width, 0.4]
	rect3 = [left, 0.1, width, 0.2]

	fig = plt.figure(facecolor='white')
	axescolor  = '#f6f6f6'  # the axies background color

	#props = font_manager.FontProperties(size=10)
	if(GRAPH_FONT_FILE):
		props = font_manager.FontProperties(fname=GRAPH_FONT_FILE, style=GRAPH_FONT_STYLE, size=GRAPH_FONT_SIZE)
	else:
		props = font_manager.FontProperties(family=GRAPH_FONT_FAMLY, style=GRAPH_FONT_STYLE, size=GRAPH_FONT_SIZE)
	ax1 = fig.add_axes(rect1, axisbg=axescolor)  #left, bottom, width, height
	ax2 = fig.add_axes(rect2, axisbg=axescolor, sharex=ax1)
	ax2t = ax2.twinx()
	ax3  = fig.add_axes(rect3, axisbg=axescolor, sharex=ax1)


	if(DONE_SIM):
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


	if(re.search(DAY_DATA,str(stock.id))):
		xdata = range(0,len(r.close))
	else:
		xdata = r.date
	N = len(r.close)
	fillcolor = 'darkgoldenrod'
	ax1.plot(xdata, rsi, color=fillcolor)
	ax1.axhline(rsi_rci_upper, color=fillcolor)
	ax1.axhline(rsi_rci_lower, color=fillcolor)
	ax1.fill_between(xdata, rsi, rsi_rci_upper, where=(rsi>=rsi_rci_upper), facecolor=fillcolor, edgecolor=fillcolor)
	ax1.fill_between(xdata, rsi, rsi_rci_lower, where=(rsi<=rsi_rci_lower), facecolor=fillcolor, edgecolor=fillcolor)
	ax1.text(0.6, 0.9, '>' + str(rsi_rci_upper) + ' = overbought', va='top', transform=ax1.transAxes, fontsize=textsize)
	ax1.text(0.6, 0.1, '<' + str(rsi_rci_lower) + ' = oversold', transform=ax1.transAxes, fontsize=textsize)
	ax1.set_yticks([rsi_rci_lower,rsi_rci_upper])
	if(RSI_RCI==0):
		ax1.set_ylim(0, 100)
		ax1.text(0.025, 0.95, 'RSI (' + str(RSI_DAY) + ')', va='top', transform=ax1.transAxes, fontproperties=props, fontsize=textsize)
	else:
		ax1.set_ylim(-120, 120)
		ax1.text(0.025, 0.95, 'RSI (' + str(RCI_DAY) + ')', va='top', transform=ax1.transAxes, fontproperties=props, fontsize=textsize)

	if(LANG == "jp"):
		ax1.set_title('%s daily'%stock.name.decode('utf-8'), fontproperties=props)
	else:
		ax1.set_title('%s daily'%stock.id, fontproperties=props)

	if(re.search(DAY_DATA,str(stock.id))):
		ax2.plot(xdata, r.close, color='black', lw=2)
	else:
		deltas = np.zeros_like(r.close)
		deltas[1:] = np.diff(r.close)
		up = deltas>0
		ax2.vlines(xdata[up], r.low[up], r.high[up], color='black', label='_nolegend_')
		ax2.vlines(xdata[~up], r.low[~up],r.high[~up], color='black', label='_nolegend_')

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
				transform=ax3.transAxes, fontproperties=props, fontsize=textsize)
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
				label.set_fontproperties(props)

		ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')

	ax2.yaxis.set_major_locator(MyLocator(5, prune='both'))
	ax3.yaxis.set_major_locator(MyLocator(5, prune='both'))

	plt.show()

def disp_2stock_graph(stock1,stock2):
	s_dt = datetime.date(*[int(val) for val in START_DATE.split('-')])
	e_dt = datetime.date(*[int(val) for val in END_DATE.split('-')])

	r1 = dp.get_data_by_day(stock1,s_dt,e_dt.year,e_dt.month,e_dt.day)
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
	#props = font_manager.FontProperties(size=10)
	if(GRAPH_FONT_FILE):
		props = font_manager.FontProperties(fname=GRAPH_FONT_FILE, style=GRAPH_FONT_STYLE, size=GRAPH_FONT_SIZE)
	else:
		props = font_manager.FontProperties(family=GRAPH_FONT_FAMLY, style=GRAPH_FONT_STYLE, size=GRAPH_FONT_SIZE)
	fillcolor = 'darkgoldenrod'
	ax1 = fig.add_axes(rect1, axisbg=axescolor)  #left, bottom, width, height
	ax2 = fig.add_axes(rect2, axisbg=axescolor, sharex=ax1)
	ax2t = ax2.twinx()
	ax3  = fig.add_axes(rect3, axisbg=axescolor, sharex=ax1)
	ax3t = ax3.twinx()
	#print self.r.date
	#r.date error
	#if(DATE):
	#	xdata = r.date
	#else:
	#	xdata = range(0,len(r1.close))
	if(re.search(DAY_DATA,str(stock.id))):
		xdata = range(0,len(r.close))
	else:
		xdata = r.date
	ax1.plot(xdata, rsi1, color='blue')
	ax1.plot(xdata, rsi2, color='red')
	ax1.axhline(70, color=fillcolor)
	ax1.axhline(30, color=fillcolor)
	ax1.text(0.6, 0.9, '>70 = overbought', va='top', transform=ax1.transAxes, fontsize=textsize)
	ax1.text(0.6, 0.1, '<30 = oversold', transform=ax1.transAxes, fontsize=textsize)
	ax1.set_ylim(0, 100)
	ax1.set_yticks([30,70])
	ax1.text(0.025, 0.95, 'RSI (14)', va='top', transform=ax1.transAxes, fontsize=textsize)

	if(LANG == "jp"):
		ax1.set_title('%s daily'%stock.name.decode('utf-8'), fontproperties=props)
	else:
		ax1.set_title('%s daily'%stock.id, fontproperties=props)

	if(re.search(DAY_DATA,str(stock.id))):
		ax2.plot(xdata, r1.close, color='blue', lw=2, label=str(stock1.id))
		ax2t.plot(xdata, r2.close, color='red', lw=2, label=str(stock2.id))
	else:
		deltas = np.zeros_like(r1.close)
		deltas[1:] = np.diff(r1.close)
		up = deltas>0
		ax2.vlines(xdata[up], r1.low[up], r1.high[up], color='blue', label='_nolegend_')
		ax2.vlines(xdata[~up], r1.low[~up],r1.high[~up], color='blue', label='_nolegend_')

		deltas = np.zeros_like(r2.close)
		deltas[1:] = np.diff(r2.close)
		up = deltas>0
		ax2.vlines(xdata[up], r2.low[up], r2.high[up], color='red', label='_nolegend_')
		ax2.vlines(xdata[~up], r2.low[~up],r2.high[~up], color='red', label='_nolegend_')

	leg1 = ax2.legend(loc='upper left', shadow=True, fancybox=True, prop=props)
	leg1.get_frame().set_alpha(0.5)
	leg2 = ax2t.legend(loc='upper right', shadow=True, fancybox=True, prop=props)
	leg2.get_frame().set_alpha(0.5)

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
				label.set_fontproperties(props)
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
		search.id = datail_data[0]	#ID
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
			if(dp.is_num(datail_data[16])):
				search.nop = int(datail_data[16])	#営業利益
			if(dp.is_num(datail_data[17])):
				search.op = int(datail_data[17])	#経常利益
			if(dp.is_num(datail_data[18])):
				search.np = int(datail_data[18])	#当期利益
			if(dp.is_num(datail_data[22])):
				search.ta = int(datail_data[22])	#総資産
			if(dp.is_num(datail_data[24])):
				search.lc = int(datail_data[24])	#資本金
			if(dp.is_num(datail_data[26])):
				search.er = float(datail_data[26])	#自己資本比率[%]
			if(dp.is_num(datail_data[28])):
				search.roa = float(datail_data[28])	#ROA（総資産利益率）[%]
			if(dp.is_num(datail_data[29])):
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
