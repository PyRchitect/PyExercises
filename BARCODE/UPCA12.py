# https://en.wikipedia.org/wiki/Universal_Product_Code
# https://learn.microsoft.com/en-us/sql/integration-services/import-export-data/get-started-with-this-simple-example-of-the-import-and-export-wizard?view=sql-server-ver16

import random as rn
import itertools as it
import urwid as uw

from enum import Enum

class UPCA12():

	ROWS = 20

	class Seps(Enum):
		QUIET	= [0,0,0,0,0,0,0,0,0]
		START	= [1,0,1]
		MIDDLE	= [0,1,0,1,0]
		END		= [1,0,1]
	
	marks = {	0:[0,0,0,1,1,0,1],
				1:[0,0,1,1,0,0,1],
				2:[0,0,1,0,0,1,1],
				3:[0,1,1,1,1,0,1],
				4:[0,1,0,0,0,1,1],
				5:[0,1,1,0,0,0,1],
				6:[0,1,0,1,1,1,1],
				7:[0,1,1,1,0,1,1],
				8:[0,1,1,0,1,1,1],
				9:[0,0,0,1,0,1,1],
				'EMPTY':[0,0,0,0,0,0,0]}
	
	palette = [	('text','default','default'),
				('light_line','white','black'),
				('dark_line','black','white')]
	
	class LTypes(Enum):
		LIN = 0
		SEP = 1
		CAP = 2

		@staticmethod
		def allowed():
			return [x.value for x in UPCA12.LTypes]
	
	def __init__(self,value_list=None):

		if value_list:
			try:
				# list length check
				assert len(value_list)==12
				# all list elements are digits
				for x in value_list:
					assert x in range(9)
				# check digit algorithm
				assert UPCA12.check_digit(value_list)
			except:
				raise ValueError("value list error")
			else:
				self.__value_list = value_list
		else:
			self.__value_list = UPCA12.__create_value_list()

		self.__lin = self.__create_image(UPCA12.LTypes.LIN.value)
		self.__sep = self.__create_image(UPCA12.LTypes.SEP.value)
		self.__cap = self.__create_image(UPCA12.LTypes.CAP.value)

		self.__info = UPCA12API(self.__value_list).UPCA_JSON

	@staticmethod
	def __invert(bitlist):
		return [0 if x==1 else 1 for x in bitlist]
	
	@staticmethod
	def check_digit(digit_list):
		return True if digit_list[-1]==UPCA12.__calc_digit(digit_list) else False
	
	@staticmethod
	def __create_value_list():
		output = [rn.randint(0,9) for _ in range(11)]
		# fake append because calc_digit needs 12 digits
		# finally to be subsituted with calc_digit result
		output.append(0)
		d = UPCA12.__calc_digit(output)
		output[-1]=d
		return output

	@staticmethod
	def __calc_digit(digit_list):		
		x3 = [d*3 for d in digit_list[:-1:2]] 	# odd
		x1 = [d for d in digit_list[1:-1:2]]	# even
		s = (sum(x3)+sum(x1))%10
		return 0 if s==10 else 10-s

	@staticmethod
	def __create_lin_code(digit_list):
		output = []
		output.append(UPCA12.Seps.QUIET.value)
		output.append(UPCA12.Seps.START.value)
		for x in digit_list[:6]:
			output.append(UPCA12.marks[x])
		output.append(UPCA12.Seps.MIDDLE.value)
		for x in digit_list[6:]:
			output.append(UPCA12.__invert(UPCA12.marks[x]))
		output.append(UPCA12.Seps.END.value)
		output.append(UPCA12.Seps.QUIET.value)
		return output
	
	@staticmethod
	def __create_sep_code():
		output = []
		output.append(UPCA12.Seps.QUIET.value)
		output.append(UPCA12.Seps.START.value)
		for _ in range(6):
			output.append(UPCA12.marks['EMPTY'])
		output.append(UPCA12.Seps.MIDDLE.value)
		for _ in range(6):
			output.append(UPCA12.marks['EMPTY'])
		output.append(UPCA12.Seps.END.value)
		output.append(UPCA12.Seps.QUIET.value)

		return output
	
	def __create_cap_code(digit_list):

		def insert_value(Linput,v):
			d = len(Linput)//2
			output = []
			output.extend(Linput[:d])
			output.append(v)
			output.extend(Linput[d+1:])
			return output
		
		def empty_block(L):
			return [0]*len(L)

		output = []
		output.append(insert_value(UPCA12.Seps.QUIET.value,digit_list[0]))
		output.append(empty_block(UPCA12.Seps.START.value))
		output.append(UPCA12.marks['EMPTY'])	# level formatting (d01 <)
		for x in list(digit_list[1:6]):
			output.append(insert_value(UPCA12.marks['EMPTY'],x))
		output.append(empty_block(UPCA12.Seps.MIDDLE.value))
		for x in list(digit_list[6:11]):
			output.append(insert_value(UPCA12.marks['EMPTY'],x))
		output.append(UPCA12.marks['EMPTY'])	# level formatting (d12 >)
		output.append(empty_block(UPCA12.Seps.END.value))
		output.append(insert_value(UPCA12.Seps.QUIET.value,digit_list[11]))

		return output

	def __create_image(self,type):
		num = False

		if type not in UPCA12.LTypes.allowed():
			raise ValueError("incorrect type!")
		else:
			if type == UPCA12.LTypes.LIN.value:
				barcode = UPCA12.__create_lin_code(self.__value_list)
			elif type == UPCA12.LTypes.SEP.value:
				barcode = UPCA12.__create_sep_code()
			elif type == UPCA12.LTypes.CAP.value:
				barcode = UPCA12.__create_cap_code(self.__value_list)
				positions = UPCA12.__create_cap_code([1]*12)
				num = True

		image = []
		image.append("\n")

		if not num:
			barcode = list(it.chain(*barcode))
			for x in barcode:
				if x:
					image.append(('dark_line',' '))
				else:
					image.append(('light_line',' '))
		else:
			barcode = list(it.chain(*barcode))
			positions = list(it.chain(*positions))
			for i,p in enumerate(positions):
				if p:
					image.append(('light_line',f'{barcode[i]}'))
				else:
					#image.append(('light_line',' '))
					image.append(('light_line',' '))
		
		return image

	def get_value_list(self):
		return self.__value_list
	
	class TextWithExit(uw.Text):
		_selectable = True
		signals = ['exit']

		def exit_to_menu(*args):
			raise uw.ExitMainLoop()
		
		def keypress(self,size,key):
			if key.upper() == "X":
				self._emit('exit')
			else:
				return key
		
	def show_barcode(self):
		
		heading = uw.Text(f"\nGENERIRANI BARCODE: {self.__value_list}")

		lines = []
		for _ in range(UPCA12.ROWS):
			lines.append(self.__lin)
		lines.append(self.__sep)
		lines.append(self.__cap)

		info_formatted = "\n\n"
		info_formatted+= json.dumps(self.__info,indent=2)
		lines.append(info_formatted)

		render = uw.Text(lines)

		exit_caption = UPCA12.TextWithExit("\nPress 'x' to exit . . .")
		uw.connect_signal(exit_caption,'exit',UPCA12.TextWithExit.exit_to_menu)

		pile = uw.Pile([heading,render,exit_caption])
		fill = uw.Filler(pile,'top')

		loop = uw.MainLoop(fill,palette=UPCA12.palette)
		loop.run()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
		
# import urllib.request
# import urllib.parse
import requests
import ssl

import json

import sys

class UPCA12API():

	def __init__(self,key):

		self.__headers = {
			'User-Agent': ' Mozilla/5.0 (Windows NT 6.1; WOW64;rv:12.0) Gecko/20100101 Firefox/12.0'
		}

		self.__url = (
			"https://api.upcdatabase.org/product/"+
			f"{''.join(map(str,key))}"+
			"?apikey=THISISALIVEDEMOAPIKEY19651D54X47"
			)
		
		self.UPCA_JSON = self.get_UPCA_JSON()

	def get_UPCA_JSON(self):

		# try:
		# 	connection = urllib.request.Request(self.__url,headers=self.__headers)
		# 	context = ssl._create_unverified_context()
		# 	with urllib.request.urlopen(connection,context=context) as response:
		# 		data = response.read().decode()
		# except ConnectionError as CE:
		# 	print(f"Connection Error! {CE}")

		data = requests.get(self.__url)
		
		return json.loads(data.content)
	
	def show_UPCA_JSON(self):
		print(self.UPCA_JSON)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

if __name__ == '__main__':

	def test():
		# bc = UPCA12([0,4,2,1,0,0,0,0,5,2,6,4])
		bc = UPCA12([0,4,2,0,0,0,0,6,2,0,0,8])
		#bc = UPCA12()
		bc.show_barcode()

		# bc_api = UPCA12API(bc.get_value_list())
		# bc_api.show_UPCA_JSON()

	test()