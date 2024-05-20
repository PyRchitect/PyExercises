# UPDATE 01: NEKE STVARI MALO LJEPŠE NAPISANE
# UPDATE 02: UPDATE 01 JE NAPRAVIO PROBLEM PRI UNOSU, ISPRAVLJENO

import os

import random as rn		# generiranje OIB-a ako bude trebalo
import datetime	as dt	# eventualno opcija now() za YYYY-MM
import pandas as pd		# samo za formatiranje tablice za ispis

# from interface import Interface

# # # TEMP: samo da je sve u istom fileu, inače import gore
# interface iz minesweepera bez kaskadnog jer treba stablo

class Interface():
	config = {
		"d_sep": '- ',
		"m_sep": 20}

	separator = config['d_sep'] * config['m_sep']

	def cls_check():
		return 'cls' if os.name =='nt' else 'clear'

	class SimpleMessage():
		def __init__(self,
			   text='',
			   sep=' ',
			   end='\n'):

			self.text = text
			self.sep = sep
			self.end = end			

		def show(self):
			print(self.text,sep=self.sep,end=self.end)

	class MultiMessage():
		def __init__(self,
			   lines='',
			   seps=' ',
			   ends='\n',
			   length=0):
			
			length = length or len(lines)
						
			def init_list(L,length,default):
				return [default]*length if L==default else L
			
			lines = init_list(lines,length,'')
			seps = init_list(seps,length,' ')
			ends = init_list(ends,length,'\n')

			self.messages = []
			for (l,s,e) in zip(lines,seps,ends):
				self.messages.append(Interface.SimpleMessage(l,s,e))
		
		def show(self):
			for m in self.messages:
				m.show()

	class SimpleGetter():
		def __init__(self,
			   choice_label='',
			   choice_sep=' ',
			   choice_type=None,
			   choice_test=None,
			   choice_error=None):
			
			self.choice_label = choice_label
			self.choice_sep = choice_sep
			self.choice_type = choice_type
			self.choice_test = choice_test
			self.choice_error = choice_error
		
		def get_input(self):
			i_test = False
			while i_test == False:
				try:
					Interface.SimpleMessage(self.choice_label,end=' ').show()
					choice = input().split(self.choice_sep)

					if not self.choice_test:
						self.choice_test = [lambda x:x for _ in len(choice)]

					for i,c in enumerate(choice):
						c = self.choice_type[i](c)
						assert self.choice_test[i](c)						
						choice[i] = c
				except:
					Interface.SimpleMessage(self.choice_error).show()
					i_test == False
				else:
					i_test = True
				finally:
					Interface.SimpleMessage(Interface.separator)
			return choice

	class MultiGetter():
		def __init__(self,
			   choice_labels='',
			   choice_seps=' ',
			   choice_types=None,
			   choice_tests=None,
			   choice_errors=None,
			   length=0):
			
			length = length or len(choice_labels)
			
			def init_list(L,length,default):
				return [default]*length if L==default else L

			choice_labels = init_list(choice_labels,length,'')
			choice_seps = init_list(choice_seps,length,'')
			choice_types = init_list(choice_types,length,None)
			choice_tests = init_list(choice_tests,length,None)
			choice_errors = init_list(choice_errors,length,None)

			self.getters = []
			for (cl,cs,ct,ctest,ce) in zip(
				choice_labels,
				choice_seps,
				choice_types,
				choice_tests,
				choice_errors):
				self.getters.append(Interface.SimpleGetter(cl,cs,ct,ctest,ce))
		
		def get_inputs(self):
			choices = []
			for g in self.getters:
				choices.append(g.get_input())
			return choices
			
	class SimpleMenu():
		def __init__(self,
			   title='',
			   options='',
			   choice_label='',
			   choice_sep=' ',
			   choice_type=None,
			   choice_test=None,
			   choice_error=None):

			self.title = title

			self.options = options

			self.getter = Interface.SimpleGetter(
				choice_label,
				choice_sep,
				choice_type,
				choice_test,
				choice_error)
		
		def show_text(self):
			Interface.SimpleMessage('\n'+self.title).show()
			Interface.SimpleMessage(Interface.separator).show()

			for option in self.options:
				Interface.SimpleMessage(option).show()

			Interface.SimpleMessage(Interface.separator).show()
		
		def show_input(self):
			return Interface.SimpleGetter.get_input(self.getter)
		
		def show(self):
			os.system(Interface.cls_check())
			self.show_text()
			return self.show_input()

# # # TEMP: samo da je sve u istom fileu, inače import gore
# interface iz minesweepera bez kaskadnog jer treba stablo

def find_first_hole(L,value=0):
	# find hole algorithm: return first hole in bitvector
	try:
		# return hole index
		return L.index(value)
	except ValueError:
		# return no hole
		return None

class OIB_checker():

	@staticmethod
	def calc_norma(L):
		L = [int(x) for x in L]
		r=[10]
		for i,l in enumerate(L[:-1]):
			r.append((((l+r[i])%10 or 10)*2)%11)
			# print(f"test: {r[-1]}")
		return (11-r[-1] if r[-1]!=1 else 0)

	def OIB_test_norma(self,L):
		if OIB_checker.calc_norma(L) == int(L[-1]):
			return True
		else:
			raise ValueError("nije validan.")
	
	@staticmethod
	def calc_OIB():
		r = rn.choices(range(1,10),k=10)
		k = str(OIB_checker.calc_norma(r+['0']))
		# +['0'] je samo testna jer norma računa do L[-1] pa da je pun broj
		# zato što se u originalnu listu puni samo prvih 10 znamenki broja
		# dolje se testna 0 zamjenjuje izračunatom kontrolnom znamenkom k
		return ''.join([str(x) for x in r+[k]])

class Bank():
	TITLE = 'pyBank'
	FOUNDED = 1996	# year founded, oldest possible account years

	# only business acc implemented
	BUSINESS = 'business'
	PERSONAL = 'personal'
	PUBLIC = 'public'

	# only business acc implemented
	acc_type = {
		BUSINESS:'BA',
		PERSONAL:'PA',
		PUBLIC:'GA'}

	def __init__(self,
			  clients=None,
			  acc_taken=None,
			  ids_taken=None):

		# can assign existent (assume correct, for DB load, etc.)

		# client list -> dict (access,key flexibility)
		self.clients = clients or {}
		# client acc list -> dict(dict(bitvector))
		self.acc_taken = acc_taken or {}
		# client ID list -> bitvector
		self.ids_taken = ids_taken or []

		# initialize menus
		self.menus = Menus()

		# set list display options
		pd.options.display.max_columns = len(Client.info)+1
		pd.options.display.max_rows = 20
		pd.options.display.width = 0
	
	def client_add(self,client:'Client'):
		if client.client_id not in self.clients:
			# if new id add client with id key
			self.clients[client.client_id]=client
		else:
			# if assign to existent id raise error
			raise ValueError("Postojeći ID klijenta!")

	def client_remove(self,client:'Client'):

		# 1. cleanup ids_taken: remove id index from ids_taken list
		if len(self.ids_taken) == 1:
			# if removed only client reset list
			self.ids_taken = []
		else:
			# set id index to False (creates a hole in bitvector)
			self.ids_taken[client.client_id] = 0

		# 2. cleanup acc taken:
		# split acc to components (type)-year-month-number, convert to ints
		(fn,sn,n) = list(map(int,client.acc.acc_string.split('-')[1:]))

		if len(self.acc_taken[fn][sn]) == 1:
			# if only 1 value in month remove month key
			self.acc_taken[fn].pop(sn)
			if len(self.acc_taken[fn]) == 0:
				# if no more months in year after pop remove year key
				self.acc_taken.pop(fn)
				if len(self.acc_taken) == 0:
					# if no more years in dict reset dict
					self.acc_taken = {}
		else:
			# if more than 1 value in month set nth index to False
			self.acc_taken[fn][sn][n] = 0
				

		# 3. remove id:client pair from clients dict
		self.clients.pop(client.client_id)
	
	def client_list(self):
		if self.clients:
			# gather column names
			cols = Client.info
			# gather row names
			rows = [k for k in self.clients.keys()]
			# gather data per client
			input_data = [[x for x in (
				c.name,
				c.company,
				c.OIB,
				c.address,
				c.postal,
				c.city,
				f"{c.acc.acc_string} ({c.acc.acc_currency})",
				c.acc.funds
				)] for c in self.clients.values()]
			# create data table
			df = pd.DataFrame.from_records(data=input_data,columns=cols,index=rows)			
			# return sorted by ID
			return df.sort_index()
		else:
			# if no clients list is empty
			return "Lista je prazna."
	
	def generate_client_id(self):				# TO DO: export assign to f
		# try to find hole in bitvector
		hole = find_first_hole(self.ids_taken)
		if hole is not None:
			# if there is a hole, fill
			self.ids_taken[hole] = 1
		else:
			# if there is no hole, "hole" = last+1
			hole = len(self.ids_taken)
			# add element with True assigned
			self.ids_taken.append(1)

		return hole

	def generate_acc_number(self,fn,sn):

		if self.acc_taken:
			# if there are years in dict
			if fn in self.acc_taken:
				# if there are months in year
				if sn in self.acc_taken[fn]:	# TO DO: export assign to f
					# try to find hole in bitvector
					hole = find_first_hole(self.acc_taken[fn][sn],0)
					if hole is not None:
						# if there is a hole, fill
						self.acc_taken[fn][sn][hole] = 1
					else:
						# if there is no hole, "hole" = last+1
						hole = len(self.acc_taken[fn][sn])
						# add element with True assigned
						self.acc_taken[fn][sn].append(1)
				else:
					# if there are no months set hole to first element
					hole = 0
					# initialize month key with True assigned to first
					self.acc_taken[fn][sn] = [1]
			else:
				# if there are no months in year, initialize month, first
				hole = 0
				self.acc_taken[fn] = {sn: [1]}
		else:
			# if there are no entries, initialize year, month, first
			hole = 0
			self.acc_taken = {fn: {sn: [1]}}
			
		return hole

	def quit_app(self):
		# cleaning, DB operatons, ...
		Interface.SimpleMessage("Hvala i doviđenja").show()
		# exit()

class Client():

	# information gathered about client (for listing)
	info = ["VL","TVRTKA","OIB","ADRESA","PB","GRAD","RACUN","SALDO"]

	def __init__(self,bank:'Bank',
			  client_type=None,
			  client_id=None,
			  name=None,
			  company=None,
			  OIB=None,
			  address=None,
			  postal=None,
			  city=None,
			  currency=None,
			  acc=None):

		# basic error handling for available account types
		if client_type not in Bank.acc_type:
			# if tried non-existent type raise error, send types
			raise ValueError(f"tipovi klijenta: {[v for v in Bank.acc_type.values]}")

		# can assign existent (assume correct, for DB load, etc.)
		self.client_type = client_type
		self.client_id = client_id or bank.generate_client_id()

		self.name = name
		self.company = company
		self.OIB = OIB
		self.address = address
		self.postal = postal
		self.city = city

		# account can be provided as string (existent acc) or (fn,sn) tuple
		if acc:
			if len(acc) == 1:
				# if string provided assume account number valid, assign
				self.acc = acc
			elif len(acc) == 2:
				# if tuple provided generate account number using fn,sn
				(fn,sn) = acc
				n = bank.generate_acc_number(fn,sn)
				self.acc = Account((fn,sn,n),currency)
		else:
			# no account or (fn,sn), generate fn and sn using datetime now
			fn = dt.datetime.now().year
			sn = dt.datetime.now().month
			n = bank.generate_acc_number(fn,sn)
			self.acc = Account((fn,sn,n))
		
	def client_info(self):
		info = ""
		info += "\nPodaci o klijentu:"
		info += "\n"+Interface.separator
		info += f"\nID klijenta: {self.client_id}"

		# gather client data
		data = [self.name,self.company,self.OIB,self.address,self.postal,self.city,
		self.acc.acc_string,f"{self.acc.funds} ({self.acc.acc_currency})"]

		for (t,d) in zip(Client.info,data):
			info += f"\n{t}:\t{d}"

		return info

class Account():

	EUR = 'EUR'
	HRK = 'HRK'
	currencies = [EUR,HRK]

	MAX_D = 10000
	MAX_W = 10000

	DEPOSIT = 'Deponiranje'
	WITHDRAW = 'Podizanje'
	actions = [DEPOSIT,WITHDRAW]

	def __init__(self,
			  acc_string,
			  acc_currency=None,
			  funds=None,
			  transactions=None):

		# can assign existent (assume correct, for DB load, etc.)

		# only business accounts implemented
		acc_type = Bank.acc_type[Bank.BUSINESS]

		# account can be provided as string (existent acc) or (fn,sn,n) tuple
		if len(acc_string)==1:
			# if string provided assume account number valid, assign
			self.acc_string = acc_string
		elif len(acc_string)==3:
			# if tuple provided create account string using fn,sn,n
			(fn,sn,n) = acc_string
			self.acc_string = self.create_acc_string(acc_type,fn,sn,n)
		
		self.acc_currency = acc_currency or 'EUR'
		if self.acc_currency not in Account.currencies:
			raise ValueError(f"Valute: {Account.currencies}")		

		self.funds = funds or 0
		self.transactions = transactions or []

	def create_acc_string(self,acc_type,fn,sn,n):
		# justify string padding to specified length
		fn = str(fn).rjust(4,"0")
		sn = str(sn).rjust(2,"0")
		n = str(n).rjust(5,"0")
		# return type - fn - sn - n
		return '-'.join((acc_type,fn,sn,n))

	def funds_add(self,funds):
		# append transactions
		self.transactions.append((Account.DEPOSIT,funds))
		# change saldo
		self.funds += funds
	
	def funds_remove(self,funds):		
		if self.funds - funds < 0:
			# if insufficient funds raise error
			raise ValueError("Nedostatan saldo!")
		else:
			# append transactions
			self.transactions.append((Account.WITHDRAW,funds))
			# change saldo
			self.funds -= funds

	def transactions_list(self):
		if self.transactions:
			tl = []
			# create readable list of transactions
			for (t,f) in self.transactions:
				tl.append(f"{t}:\t{f}")
			return tl
		else:
			# if no transactions yet return empty
			return "Lista je prazna."

class Menus():
	class MainMenu():
		def __init__(self):
			self.menu = Interface.SimpleMenu()
			self.menu.title = "GLAVNI MENU"

			opt = []
			opt.append('[0] - izlaz')
			opt.append('[ ]   KLIJENTI:')
			opt.append('[1] - lista')
			opt.append('[2] - otvori')
			opt.append('[3] - dodaj')
			opt.append('[4] - ukloni')
			opt.append('[ ]   HELPERS:')
			opt.append('[5] - calc OIB')
			opt.append('[6] - random DB')
			self.menu.options = opt

			g = Interface.SimpleGetter()
			g.choice_label = 'Odabir [0|...|6]'
			g.choice_sep = ' '
			g.choice_type = (int,)
			g.choice_test = (lambda x: x in list(range(6+1)),)
			g.choice_error = 'Pogresan unos!'
			self.menu.getter = g
		
		def show(self):
			return self.menu.show()

	class AddClient():
		def __init__(self):

			labels = (
				f"> Vlasnik:\t",
				f"> Naziv:\t",
				f"> OIB:\t\t",
				f"> Adresa:\t",
				f"> PBroj:\t",
				f"> Grad:\t\t",
				f"> Valuta:\t",
				f"> Generacija računa [0=auto,1=manual]: ",)

			# seps set to rare chr when ' ' is expected (prevents splitting)
			seps = ('~','~',' ','~',' ','~',' ',' ')

			types = (
				(str,),
				(str,),
				(int,),
				(str,),
				(int,),
				(str,),
				(str,),
				(int,))

			tests = (
				# director - first letters capital (+not empty+contain only letters), >1 word
				(lambda x: len(x.split())>1, lambda x: all(w.istitle() for w in x.split()),),
				# name - no real check is possible except it has to have a name (len>0)
				(lambda x: True if x else False,),
				# OIB - 11 digits, test according to ISO
				(lambda x: len(str(x))==11,OIB_checker.OIB_test_norma,),
				# address - first letter first word capital (+not empty+contain only letters)
				(lambda x: x[0].istitle(),),
				# postal - five digits
				(lambda x: len(str(x))==5,),
				# city - first letter capital (+not empty+contain only letters)
				(lambda x: x[0].istitle(),),
				# currency - 3 letters, capital, in available currencies)
				(lambda x: len(x) == 3, lambda x: x.upper() in Account.currencies,),
				# gen - 0 = auto, 1 = manual
				(lambda x: x in [0,1],),)
			
			errors = (
				'Neispravno uneseno ime vlasnika!',
				'Neispravno unesen naziv!',
				'Neispravno unesen OIB!',
				'Neispravno unesena adresa!',
				'Neispravno unesen postanski broj!',
				'Neispravno unesen grad!',
				'Neispravno unesena valuta!',
				'Neispravan odabir generacije računa!')

			self.gwh = Interface.MultiGetter(labels,seps,types,tests,errors)
		
		def show(self):
			return self.gwh.get_inputs()
		
	class GenAccount():
		def __init__(self):

			labels = (f"> Godina:\t",f"> Mjesec:\t")
			seps = (' ',' ')
			types = ((int,),(int,),)
			tests = (
				# year - up to 4 digits, since founding, less than today
				(lambda x: (x>=Bank.FOUNDED and x<=dt.datetime.now().year),),
				# month - between 1 and 12
				(lambda x: (x>=1 and x<=12),),)			
			errors = (
				f'Neispravno unesena godina! ({Bank.FOUNDED}-{dt.datetime.now().year})',
				'Neispravno unesen mjesec!')

			self.gwh = Interface.MultiGetter(labels,seps,types,tests,errors)
		
		def show(self):
			return self.gwh.get_inputs()

	class RemoveClient():
		def __init__(self):
			self.g = Interface.SimpleGetter()
			self.g.choice_label = f"> ID klijenta koji zatvara račun: "
			self.g.choice_sep = ' '
			self.g.choice_type = (int,)
			self.g.choice_test = (lambda x: x>=0,)
			self.g.choice_error = 'Pogresan unos!'

		def show(self):
			return self.g.get_input()
		
	class ClientOpen():
		def __init__(self):
			self.g = Interface.SimpleGetter()
			self.g.choice_label = f"> ID klijenta: "
			self.g.choice_sep = ' '
			self.g.choice_type = (int,)
			self.g.choice_test = (lambda x: x>=0,)
			self.g.choice_error = 'Pogresan unos!'

		def show(self):
			return self.g.get_input()
	
	class ClientOps():
		def __init__(self,c:'Client'):
			self.menu = Interface.SimpleMenu()
			self.menu.title = c.client_info() 
			self.menu.title += "\n"+Interface.separator
			self.menu.title += "\nOPERACIJE PO RAČUNU"

			opt = []
			opt.append('[0] - izlaz')
			opt.append('[ ]   OPERACIJE:')
			opt.append('[1] - lista transakcija')
			opt.append('[2] - položi')
			opt.append('[3] - podigni')
			self.menu.options = opt

			g = Interface.SimpleGetter()
			g.choice_label = 'Odabir [0|...|3]'
			g.choice_sep = ' '
			g.choice_type = (int,)
			g.choice_test = (lambda x: x in list(range(3+1)),)
			g.choice_error = 'Pogresan unos!'
			self.menu.getter = g
		
		def show(self):
			return self.menu.show()

	class ClientDeposit():
		def __init__(self):
			self.g = Interface.SimpleGetter()
			self.g.choice_label = f"> Položi iznos: "
			self.g.choice_sep = ' '
			self.g.choice_type = (int,)
			self.g.choice_test = (lambda x: x>0 and x<Account.MAX_D,)
			self.g.choice_error = f'Deponiranje 0 - {Account.MAX_D}!'

		def show(self):
			return self.g.get_input()

	class ClientWithdraw():
		def __init__(self):
			self.g = Interface.SimpleGetter()
			self.g.choice_label = f"> Podigni iznos: "
			self.g.choice_sep = ' '
			self.g.choice_type = (int,)
			self.g.choice_test = (lambda x: x>0 and x<Account.MAX_W,)
			self.g.choice_error = f'Podizanje 0 - {Account.MAX_W}!'

		def show(self):
			return self.g.get_input()

def client_list(b:'Bank'):
	os.system(Interface.cls_check())
	# title
	Interface.SimpleMessage("\nPopis klijenata:").show()
	Interface.SimpleMessage(Interface.separator*2).show()
	# generated dataframe
	Interface.SimpleMessage(b.client_list()).show()
	# press any key
	Interface.SimpleMessage("\nUnesi bilo koji znak za izlaz").show()
	input()

def client_ops_transactions(c:'Client'):
	os.system(Interface.cls_check())
	# title
	Interface.SimpleMessage("\n"+c.client_info()).show()
	Interface.SimpleMessage(Interface.separator).show()
	Interface.SimpleMessage("Transakcije po računu:").show()
	Interface.SimpleMessage(Interface.separator).show()

	tl = c.acc.transactions_list()
	if c.acc.transactions:
		Interface.MultiMessage(tl).show()
	else:
		Interface.SimpleMessage(tl).show()

	Interface.SimpleMessage(Interface.separator).show()
	Interface.SimpleMessage(f"Saldo: {c.acc.funds} ({c.acc.acc_currency})").show()
	# press any key
	Interface.SimpleMessage("\nUnesi bilo koji znak za izlaz").show()
	input()

def client_ops_deposit(b:'Bank',c:'Client'):
	os.system(Interface.cls_check())
	# title
	Interface.SimpleMessage("\n"+c.client_info()).show()
	Interface.SimpleMessage(Interface.separator).show()
	Interface.SimpleMessage(f"Deponiranje sredstava (0 - {Account.MAX_D}):").show()
	Interface.SimpleMessage(Interface.separator).show()

	(deposit_amount,) = b.menus.ClientDeposit().show()
	c.acc.funds_add(deposit_amount)
	Interface.SimpleMessage("Sredstva uspješno položena.").show()

	# press any key
	Interface.SimpleMessage("\nUnesi bilo koji znak za izlaz").show()
	input()

def client_ops_withdraw(b:'Bank',c:'Client'):
	os.system(Interface.cls_check())
	# title
	Interface.SimpleMessage("\n"+c.client_info()).show()
	Interface.SimpleMessage(Interface.separator).show()
	Interface.SimpleMessage(f"Podizanje sredstava (0 - {Account.MAX_W}):").show()
	Interface.SimpleMessage(Interface.separator).show()

	(withdraw_amount,) = b.menus.ClientWithdraw().show()
	try:
		c.acc.funds_remove(withdraw_amount)
	except ValueError as err:
		Interface.SimpleMessage(err).show()
	else:
		Interface.SimpleMessage("Sredstva uspješno podignuta.").show()

	# press any key
	Interface.SimpleMessage("\nUnesi bilo koji znak za izlaz").show()
	input()

def client_ops(b:'Bank'):
	os.system(Interface.cls_check())
	# title
	Interface.SimpleMessage("\nOdabir klijenta:").show()
	Interface.SimpleMessage(Interface.separator).show()

	(received_id,) = b.menus.ClientOpen().show()

	try:
		c = b.clients[received_id]
	except:
		Interface.SimpleMessage("Nepostojeći ID klijenta!").show()
		# press any key
		Interface.SimpleMessage("\nUnesi bilo koji znak za izlaz").show()
		input()
	else:
		action = True
		while action:
			(action,) = b.menus.ClientOps(c).show()

			if action == 0:			
				action = False
				# clean exit
				continue			
			elif action == 1:
				# lista transakcija
				client_ops_transactions(c)
			elif action == 2:
				# položi novac
				client_ops_deposit(b,c)
			elif action == 3:
				# podigni novac
				client_ops_withdraw(b,c)

def client_add(b:'Bank'):
	os.system(Interface.cls_check())
	# title
	Interface.SimpleMessage("Unos novog klijenta:").show()
	Interface.SimpleMessage(Interface.separator).show()

	((name,),(company,),(OIB,),(address,),(postal,),(city,),(cur,),(gen,)) = b.menus.AddClient().show()

	if gen:
		Interface.SimpleMessage(Interface.separator).show()
		Interface.SimpleMessage("Generiranje broja računa:").show()
		Interface.SimpleMessage(Interface.separator).show()
		((fn,),(sn,))=b.menus.GenAccount().show()
		acc = (fn,sn)
	else:
		acc = None

	try:
		b.client_add(Client(b,Bank.BUSINESS,None,name,company,OIB,address,postal,city,cur.upper(),acc))
	except:
		Interface.SimpleMessage("Pogreška pri unosu u bazu.").show()
	else:
		Interface.SimpleMessage("Klijent uspješno dodan.").show()
	# press any key
	Interface.SimpleMessage("\nUnesi bilo koji znak za izlaz").show()
	input()

def client_remove(b:'Bank'):
	os.system(Interface.cls_check())
	# title
	Interface.SimpleMessage("Zatvaranje računa klijenta klijenta:").show()
	Interface.SimpleMessage(Interface.separator).show()

	(received_id,) = b.menus.RemoveClient().show()
	try:
		b.client_remove(b.clients[received_id])
	except:
		Interface.SimpleMessage("Nepostojeći ID klijenta!").show()
	else:
		Interface.SimpleMessage("Račun uspješno zatvoren.").show()
	# press any key
	Interface.SimpleMessage("\nUnesi bilo koji znak za izlaz").show()
	input()

def client_generate(b:'Bank',DB_data=None):

	if DB_data:	# supports existent data
		(fname,sname,(ctitle,ctype),OIB,(street,hn),pcity,currencies) = DB_data
	else:		# template entries
		DB_entries = 12

		fname =	["Marko", "Ivo", "Jure", 
				"Pero", "Frane", "Duje", 
				"Ana", "Marina", "Ivana", 
				"Karla", "Lucija", "Marija"]

		sname =	["Marković", "Ivić", "Jurić",
				"Perić", "Franić", "Dujić",
				"Anić", "Marinović", "Ivanović",
				"Karlović", "Lucić", "Marić"]

		ctitle = ["Zemun", "Fontana", "Merkator",
			 	"Pekar", "Lekar", "Apotekar",
				"Gile", "Šampion", "Favorit",
				"Glista","Kik boks", "Rokenrol"]
		# unique > only serial read, requires shuffling
		rn.shuffle(ctitle)
	
		ctype = ["d.d.","d.o.o.","j.d.o.o.",
		   		"obrt za usluge","udruga","zadruga"]
		
		# unique > only serial read, no shuffling required (rand.gen.)
		OIB =  [int(OIB_checker.calc_OIB()) for _ in range(DB_entries)]

		street = ["Dubrovačka", "Splitska", "Šibenska",
				"Zadarska", "Gospićka", "Riječka",
				"Pulska", "Karlovačka", "Zagrebačka",
				"Varaždinska", "Osiječka", "Vukovarska"]
		
		hn = range(1,100)

		pcity = ["20000 Dubrovnik", "21000 Split", "22000 Šibenik",
				"23000 Zadar", "52000 Gospić", "53000 Rijeka",
				"52000 Pazin", "47000 Karlovac", "10000 Zagreb",
				"42000 Varaždin", "31000 Osijek", "32000 Vukovar"]
		
		currencies = Account.currencies

	# (fn,sn) for acc
	
	try:
		for i in range(DB_entries):
			ccur = f"{rn.sample(currencies,1)[0]}"
			cname = f"{rn.sample(fname,1)[0]} {rn.sample(sname,1)[0]}"
			ccomp = f"{ctitle[i]} {rn.sample(ctype,1)[0]}"
			cOIB = OIB[i]
			caddr = f"{rn.sample(street,1)[0]} {rn.sample(hn,1)[0]}"
			(cpost,ccity) = rn.sample(pcity,1)[0].split(' ')
			cpost = int(cpost)	

			fn = rn.randint(Bank.FOUNDED,dt.datetime.now().year)
			sn = rn.randint(1,12+1)
			cacc = (fn,sn)

			# add client, generate ID, generate acc number using (fn,sn)
			b.client_add(Client(b,Bank.BUSINESS,None,cname,ccomp,cOIB,caddr,cpost,ccity,ccur,cacc))
	except:
		Interface.SimpleMessage("Pogreška pri generiranju baze.").show()
	else:
		Interface.SimpleMessage("Klijenti uspješno generirani.").show()
	# press any key
	Interface.SimpleMessage("\nUnesi bilo koji znak za izlaz").show()
	input()

def main():
	b = Bank()

	Interface.SimpleMessage("\n"+b.TITLE).show()
	Interface.SimpleMessage(Interface.separator).show()

	action = True
	while action:
		(action,) = b.menus.MainMenu().show()

		if action == 0:
			# izlaz iz aplikacije
			action = False
			# clean exit
			b.quit_app()
		elif action == 1:
			# lista klijenata
			client_list(b)
		elif action == 2:
			# otvori klijenta
			client_ops(b)
		elif action == 3:
			# dodaj klijenta
			client_add(b)
		elif action == 4:
			# ukloni klijenta
			client_remove(b)
		elif action == 5:
			# generiraj OIB
			Interface.SimpleMessage("\nGenerirani OIB").show()
			Interface.SimpleMessage(Interface.separator).show()
			Interface.SimpleMessage(OIB_checker.calc_OIB()).show()
			# press any key
			Interface.SimpleMessage("\nUnesi bilo koji znak za izlaz").show()
			input()
		elif action == 6:
			# generiraj random bazu
			client_generate(b)

if __name__ == '__main__':
	main()