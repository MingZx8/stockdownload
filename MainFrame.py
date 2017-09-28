#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: MingZ
# @Date created: 21 Sep 2017
# @Date last modified: 21 Sep 2017
# Python Version: 2.7

from Tkinter import *
import tkFileDialog as fd
import datetime
import pandas
import sys
from StockDownload import *

class MainFrame:
	def __init__(self):
		today = datetime.date.today()
		preday = today-datetime.timedelta(days=2)

		root = Tk()
		root.title("STOCK DOWNLOAD")
		root.geometry('%dx%d+%d+%d' % (800,800,(root.winfo_screenwidth()/2-400),(root.winfo_screenheight()/2-400)))
		# root.geometry("800x500")
		# root.columnconfigure(0, weight=1)
		frame = Frame(root)
		frame.grid_rowconfigure(0, weight=1)
		frame.grid_columnconfigure(0, weight=1)

		#输入起始日期
		l_start = Label(frame,text="start:").grid(row=0)
		e_start = Entry(frame)
		e_start.grid(row=0,column=1)
		e_start.insert(0,preday)

		#输入结束日期
		l_end = Label(frame,text="end:").grid(row=1)
		e_end = Entry(frame)
		e_end.grid(row=1,column=1)
		e_end.insert(0,today)

		# 选项
		scrollbar = Scrollbar(frame)
		scrollbar.grid(row=7,column=2, sticky=N+S+W)
		lb_symbol = Listbox(frame,yscrollcommand=scrollbar.set,height=30,selectmode=SINGLE)

		def src_path(relative_path):
			if hasattr(sys, "_MEIPASS"):
				base_path = sys._MEIPASS
			else:
				base_path = os.path.abspath(".")
			return os.path.join(base_path,relative_path)

		file_path =src_path("src/Symbol.csv")
		file = pandas.read_csv(file_path,index_col='Symbol')
		for index in file.index:
			lb_symbol.insert(END, index)
		lb_symbol.grid(row=7,column=1,sticky=N+S+E+W)
		scrollbar.config(command=lb_symbol.yview)

		#下载位置
		def __browse():
			filename = fd.askdirectory()
			folder_path.set(filename)

		folder_path = StringVar()
		l_dl = Label(frame,text="download to..").grid(row=2)
		e_dl = Entry(frame,textvariable=folder_path)
		e_dl.grid(row=2,column=1)

		b_dl = Button(frame,text="browse",command=__browse).grid(row=2,column=2)
		b_action = Button(frame,text="Download",
			command=lambda:StockDownload(lb_select.get(0,END),e_start.get(),e_end.get(),e_dl.get())).grid(row=3,column=1)

		Label(frame, text="").grid(row=4,column=2)

		#全选按钮
		def __bSelect():
			lb_select.delete(0,END)
			temp = lb_symbol.get(0,END)
			for item in temp:
				lb_select.insert(END,item)
		def __bClear():
			lb_select.delete(0,END)

		b_select = Button(frame,text="select all",command=__bSelect)
		b_clear = Button(frame,text="clear",command=__bClear)
		b_clear.grid(row=5,column=3)
		b_select.grid(row=5,column=1)

		#查找按钮
		def __popup(titletext,valuetext):
			popupwindow = Toplevel()
			popupwindow.attributes("-topmost",1)
			popupwindow.title(titletext)
			popupwindow.geometry("250x60+400+250")
			label = Label(popupwindow, text=valuetext).pack()
			button = Button(popupwindow, text="ok", command=popupwindow.destroy).pack()


		def __eFind(Event):
			try:
				symbolTemp = e_find.get().upper()
				index = lb_symbol.get(0,END).index(symbolTemp)
				lb_symbol.see(index)
				if symbolTemp not in lb_select.get(0,END):
					lb_select.insert(0,symbolTemp)
			except ValueError:
				__popup("ValueError","Symbol no exist")

		l_find = Label(frame,text="find&select:").grid(row=6)
		e_find = Entry(frame)
		l_select = Label(frame,text="selected:").grid(row=6,column=3)

		def __delSelect(Event):
			w = Event.widget
			index = int(w.curselection()[0])
			lb_select.delete(index)
		def __addSelect(Event):
			w = Event.widget
			lb_order = list(lb_select.get(0,END))
			index = int(w.curselection()[0])
			value = w.get(index)
			if value not in lb_order:
				lb_order.append(value)
				lb_order.sort()
				lb_select.delete(0,END)
				for item in lb_order:
					lb_select.insert(END,item)

		s_select = Scrollbar(frame)
		s_select.grid(row=7,column=4, sticky=N+S+W)
		lb_select = Listbox(frame,yscrollcommand=s_select.set)
		lb_select.grid(row=7,column=3,sticky=N+S+E+W)
		s_select.config(command=lb_select.yview)

		lb_select.bind('<<ListboxSelect>>',__delSelect)
		lb_symbol.bind('<<ListboxSelect>>',__addSelect)

		e_find.grid(row=6,column=1)
		e_find.insert(1,"A")
		e_find.bind('<Return>',__eFind)

		def __browse_list():
			symbol_file_name = fd.askopenfilename(filetypes = (("csv files","*.csv"),("all files","*.*")))
			symbol_file = pd.read_csv(symbol_file_name)
			try:
				for item in symbol_file['Symbol']:
					if item in lb_symbol.get(0,END) and item not in lb_select.get(0,END):
						lb_select.insert(END,item)
				__popup("Success","Success")
			except:
				__popup("Error","Header should contain 'Symbol'")


		folder_path_symbol = StringVar()
		l_load = Label(frame, text='load symbol list:').grid(row=8,column=3)
		b_load = Button(frame, text='browse',command=__browse_list)
		b_load.grid(row=9,column=3)

		frame.pack()
		root.mainloop()

# s = MainFrame()
