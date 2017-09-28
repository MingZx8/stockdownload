#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: MingZ
# @Date created: 19 Sep 2017
# @Date last modified: 19 Sep 2017
# Python Version: 2.7

# historical data from Google/yahoo finance
# http://www.google.com/finance/historical?q=JNUG&startdate=20170101&enddate=20170707&output=csv

import pandas_datareader.data as web
import pandas as pd
import datetime
import sys
import tkFileDialog as fd
from Tkinter import *
import os

# start = datetime.datetime(2017,1,1)
# end = datetime.datetime(2017,7,7)
# f = web.DataReader('JNUG','yahoo',start,end)


class Download:
	def __init__(self, symbols, start, end, path):
		def __popup(self,title,text):
			popupwindow = Toplevel()
			popupwindow.attributes("-topmost",1)
			popupwindow.title(title)
			popupwindow.geometry("200x60+400+250")
			label = Label(popupwindow, text=text).pack()
			button = Button(popupwindow, text="ok", command=popupwindow.destroy).pack()

		if not os.path.exists(path):
			__popup(self,"FolderError","file path no exist")

		try:
			start = datetime.datetime(int(start[0:4]),int(start[5:7]),int(start[8:]))
			end = datetime.datetime(int(end[0:4]),int(end[5:7]),int(end[8:]))
			# print start,end
		except:
			__popup(self,"FormatError","date format is wrong")

		f_error = pd.DataFrame()
		row = 0
		for symbol in symbols:
			try:
				f = web.DataReader(symbol,'yahoo',start,end)
				f.to_csv(path +'/'+ symbol + ".csv")
			except:
				f_error.insert(row,row,[symbol])
				row+=1
				f_error.T.to_csv(path+'/'+'error.csv',header=None)
		__popup("Success","Success")


