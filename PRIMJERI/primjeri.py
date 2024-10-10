# FUNKCIJE:
import sys
import urllib.request
var = 0
iterable = list()
name = 'name'
expression = 'expression'
obj = 'object'
value = 'value'
default = 'default'
clsinfo = int
iterables = list(list(),list())
args = ['arg','arg']
file = 'file'
start = 0
stop = 100
step = 1

# # POPIS:
# A
abs(var)						# vraća apsolutnu vrijednost integera ili floata, odnosno modul kompleksnog broja
all(iterable) 					# vraća True ako su svi elementi kolekcije true ili ako je kolekcija prazna
any(iterable) 					# vraća True ako je bilo koji element kolekcije true, False ako je kolekcija prazna
# C
callable(obj) 					# vraća True ako je objekt iz vrste callable (funkcija ili klasa s __call__() metodom)
# D
delattr(obj,name)				# briše imenovani atribut klase (delattr(inst,attr) = del inst.attr)
dir(obj)						# lista naziva u lokalnom obuhvatu, ako je klasa s oo __dir__(), daje listu attributa
# E
enumerate(iterable,start=0)		# vraća tuple s indeksom i elementom kolekcije (indeks,element)
eval(expression,globals=None,locals=None) 		# parsing i evaluacija Python naredbe (tj. liste uvjeta)
exec(obj,globals=None,locals=None,closure=None) # omogućuje dinamičko izvršavanje koda
# F
filter(function,iterable)		# konstruira iterator od elemenata za koje (bool) funkcija vrati True
format(value,format_spec='')	# konvertira value u formatiranu reprezentaciju kontroliranu s format_spec
# G
getattr(object,name,default)	# vraća vrijednost atributa objekta (getattr(inst,attr) = inst.attr)
# H
hasattr(object,name)			# vraća True ako objekt ima atribut, False ako nema
help(obj)						# daje osnovne podatke o objektu (modul, funkcija, klasa, metoda, keyword, doc. topic)
help()							# pali se interaktivni help, može se koristiti i za vlastite funkcije (čita docstring)
# I
id(object) 						# vraća "identitet" objekta # jedinstveni broj konstantan za objekt tijekom njegovog trajanja
input(prompt=' ')				# prompt = poruka prije inputa, printa se bez newline charactera
isinstance(object,clsinfo)		# vraća True ako je objekt instanca klase ili jedne od klasa ako se da tuple
issubclass(obj,clsinfo)			# vraća True ako je klasa potklasa nadklase ili jedne od nadklasa iz tuplea
iter(object)					# vraća iterator kolekcije koja podržava iterable (__iter__()) ili sequence (__getitem__()) protokol
# L
len(iterable)					# vraća broj elemenata pohranjenih u kolekciji, odnosno sekvenci
# M
map(function,iterable,*iterables)	# primjenjuje funkciju na svaki element kolekcije(a)
min(iterable,key=None)			# vraća najmanji element iz kolekcije, alternativno min(arg1,arg2,*args,key=None)
max(iterable,key=None)			# vraća najveći element iz kolekcije, alternativno max(arg1,arg2,*args,key=None)
# N
next(iterable,default)			# vraća slijedeći element iteratora, zove __next__() metodu
# O
open(file,mode='r',buffering=-1,encoding=None,errors=None,newline=None,closefd=True,opener=None)
# P
print(*args,sep=' ', end='\n', file=sys.stdout, flush=False)	# prikaz na ekranu
# *args = output, često se koriste f-stringovi zbog fleksibilnosti "... {var} ... {var}...", mogu i klasični
# sep = separator, end = zadnji znak u retku, file = mjesto ispisa, flush = da li prazni stream
property(fget=None,fset=None,fdel=None,doc=None)	# vraća property atribut, koristi se za managed attr
# kada se specificira kao decorator, ima @property > @p.getter + @p.setter + @p.deleter
# R
range(start,stop,step)	# iterator (neopadajućeg/nerastućeg) niza cijelih brojeva, često se koristi u petljama
						# range(n): 0-n, korak:1, range(n,m): n-m, korak:1, range(n,m,k): n-m, korak:k
repr(object)			# vraća string sa printable reprezentacijom, u klasi se oo pomoću __repr__() metode
reversed(iterable)		# vraća obrnuti iterator, seq sadržava __reversed__() metodu ili podržava sequence protocol
# S
setattr(object,name,value)		# ažurira vrijednost atributa (setattr(inst,attr,value) = inst.attr=value)
slice(start,stop,step)			# vraća slice sekvence koji čini set indeksa specificiranih prema range(start,stop,step)
sorted(iterable,key=None,reverse=False)	# vraća sortiranu listu elemenata kolekcije (Tim sort)
sum(iterable,start=0)			# zbraja start i elemente kolekcije (obično brojevi), vraća zbroj
# V
vars(object)					# vraća __dict__ atribut za objekt koji ga ima (modul, klasa, instanca ili slično)
# Z
zip(*iterables,strict=False)	# iterira preko više kolekcija paralelno, vraća tuple po tuple redova
								# strict=True: zahtijeva da kolekcije budu jednake duljine, inače završava s najkraćim

# LISTE
L = list()
indeks = 0
nova_vrijednost = 0
novi_element = 0
element = 0
nova_lista = list()

# # POPIS
L[indeks] = nova_vrijednost # izmjena vrijednosti pohranjene u element na poziciji indeks
L[start:stop:step] # slicing: način kreiranja nove liste na osnovu manipulacije postojećom
L.append(novi_element) # dodavanje novog elementa na kraj liste
L.clear() # naredba za brisanje svih elemenata liste
L.copy() # naredba za kopiranje liste (shallow copy, ne kopira zapravo elemente)
L.count(element) # prebrojava koliko se puta element pojavljuje u listi
L.extend(nova_lista) # proširuje postojeću listu novom listom
L.index(element) # dohvaća prvi indeks pozicije na kojoj se nalazi element
L.insert(indeks,element) # umetanje elementa točno ispred pozicije označene indeksom
L.pop(indeks) # uklanjanje elementa na poziciji označenoj indeksom, default zadnji element
L.reverse() # naredba za obrtanje redoslijeda elemenata liste
L.sort() # naredba za sortiranje elemenata (koristi Tim sort)

# DICTIONARY:
D = dict()
k_iter = (0,1,2)
k = 0
v = 0
DU = dict()

# # POPIS:
D[k]	# dohvaća value pod tim keyem ako postoji
# provjera: postoji li key
(True if k in dict else False)
(True if D.has_key(k) else False)
(True if dict.get(k) == None else False)
D.clear()				# briše sve key-value parove iz dictionary-ja
D.copy()				# radi shallow copy cijelog dictionary-ja
D.fromkeys(k_iter,v) # kreira dictionary sa specificiranim keyevima sa vrijednošću v
D.get(k)				# vraća vrijednost za specificirani key
D.items()				# dohvaća key-value parove kao listu tupleova
D.keys(), D.values()	# dohvaća keys / values kao listu
D.pop(k,default)		# briše key-value par pod keyem
D.popitem()				# briše item koja je zadnja dodana u dict
D.setdefault(k,v)		# vraća vrijednost za specificirani key, ako nema, dodaje key-value par
D.update(DU)			# dopunjava dictionary specificiranim key-value parovima

# MODULI:

import random as rn							# funkcije za generiranje nasumičnih brojeva
rn.randint(start,stop)						# vraća nasumični broj unutar određenog raspona
rn.choice(iterable)							# vraća nasumični element iz kolekcije (string, range, list, tuple, ...)
rn.choices(iterable,weights=None,k=1)		# vraća kolekciju duljine k uz def. vjer. (w) članova osnovne kolekcije
rn.shuffle(iterable)						# vraća kolekciju nasumično presloženu
rn.sample(iterable,k)						# vraća podniz duljine k iz osnovne kolekcije (bez ponavljanja, k<=len(iterable))
rn.random()									# vraća nasumični float između 0.0 i 1.0
# ...variate() # vraća nasumični float iz određene distribucije (eksponencijalna, normalna, gamma, ...)

import math									# matematičke funkcije i konstante
math.sin(),math.cos(),math.tan()			# trigonometrijske funkcije
math.asin(),math.acos(),math.atan()			# arcus trig. funkcije
math.sinh(),math.cosh(),math.tanh(),		# hiperboličke funkcije
math.asinh(), math.acosh(), math.atanh()	# arcus hip. funkcije
math.pow(),math.exp(),math.log()			# potencija, eksponencijalna i logaritamska funkcija
math.comb()									# binomni koeficijent, perm() # broj permutacija
math.erf(),math.erfc()						# error i komplementarna error funkcija
math.dist(),math.hypot(),math.isclose()		# euklidska udaljenost,euklidska norma, jesu li dvije vrijednosti blizu
math.floor(),math.ceiling(),math.trunc()	# zaokruživanje na niži/viši integer, uklanjanje dijela iza dec. točke
math.factorial(),math.gamma(),math.lgamma()	# faktorijel, gamma funkcija, log gamma funkcija
math.gcd(),math.lcm()						# najveći zajednički dijelitelj, najmanji zajednički višekratnik
math.isfinite(),math.isinf()				# je li broj (bes)konačan
math.inf,math.e,math.nan,math.pi,math.tau	# konstante: beskonačno, e, NaN, pi, tau, …

import os									# funkcije za rad u nekim elementima operativnog sustava
os._exit(),os.abort(),os.kill(),
os.chdir(),os.chmod(),os.chown(),os.chroot(),
os.getcwd(),os.getegid(),os.getenv(),os.geteuid(),os.getgid(),os.getpid(),os.getuid()
os.major(),os.minor()
os.mkdir(),os.mkfifo()
os.open(),os.pipe(),os.popen(),os.read(),
os.remove(),os.rmdir()
os.setgid(),os.setuid(),
os.stat()
os.symlink()
os.umask(),os.wait(),os.write()
os.path.join(path,'dir','dir','…','file')	# spaja put do file-a

import sys									# manipulacija različitim elementima Python runtime environmenta
sys.stdin,sys.stdout,sys.stderr # standard input, standard output, standard error
# na jednostavan način omogućuje redirekciju # samo izmijeniti vrijednost nekog od gornjih objekata
sys.argv # lista cmd line argumenata poslanih Python skripti
sys.getrefcount() 		# broj referenci na objekt
sys.getsizeof(object) 	# veličina objekta u byte-ovima
sys.path[0]				# trenutno aktivni direktorij (iz kojeg je pokrenuta skripta)
sys.platform			# razlikuje "linux" = Linux, "win32" = Windows, "darwin" = macOS

import datetime as dt 						# funkcije za upravljanje tipom varijabli za pohranu vremena

# date klasa: idealizirani datum prema gregorijanskom kalendaru
dt.date.year,dt.date.month,dt.date.day # atributi
dt.date.today()			# danas
dt.date.replace()		# zamjena godine, mjeseca, dana
dt.date.isoformat()		# konvertira dobiveno vrijeme u isoformat
dt.date.ctime()			# date C-style string
dt.date.strftime()		# konvertira dobiveni datum u određeni format

x = datetime.date.today()						# pokupi datum za danas
x = datetime.date(2024,10,20)					# kreira 2024-10-20
x = datetime.date.fromtimestamp(1326244364) 	# pokupi Unix timestamp (broj sec od 01.01.1970.)
print(f"godina: {x.year}, mjesec: {x.month}, dan: {x.day}")

# time klasa: idealizirano vrijeme neovisno o danu
dt.time.hour,dt.time.minute,dt.time.second,dt.time.microsecond # atributi
dt.time.now()			# sada
dt.time.replace()		# zamjena sata, minute, sekunde, mikrosekunde
dt.time.isoformat()		# konvertira dobiveno vrijeme u isoformat
dt.time.strftime()		# konvertira dobiveno vrijeme u određeni format

x = dt.time.now()				# pokupi vrijeme za sada
x = time(12,34,56,123456)		# kreira 12:34:56.123456
print(f"sat: {x.hour}, minuta: {x.minute}, sekunda: {x.second}, ms: {x.microsecond}")

# datetime klasa: kombinacija date i time klase
dt.datetime.year,'...',dt.datetime.microsecond # atributi
dt.datetime.date()				# izvadi datum
dt.datetime.today()				# danas
dt.datetime.time()				# izvadi vrijeme
dt.datetime.now()				# sada
dt.datetime.replace()			# zamjena atribute
dt.datetime.timestamp()			# kreira timestamp
dt.datetime.isoformat()			# konvertira dobiveni datum i vrijeme u isoformat
dt.datetime.ctime()				# datetime C-style string
dt.datetime.strftime()

x = datetime.datetime.now()		# pokupi datum i vrijeme za sada
x = datetime.datetime(2024,10,20,12,34,56,123456) 	# kreira 2024-10-20 12:34:56.123456
print(f"godina: {x.year}, mjesec: {x.month}, dan: {x.day}, sat: {x.hour}, minuta: {x.minute}, ...")
print(f"godina: {x.strftime("%Y")}, mjesec: {x. strftime("%m")}, dan: {x. strftime("%d")}, ...")

x = datetime.date.fromisoformat('2024-10-20')					# kreira iz ISO 8601 formata
print(f"ISO format: {x.isoformat(sep='T',timespec='auto')}")	# kreira string u ISO 8601 formatu
# isoformat: YYYY-MM-DDTHH:MM:SS.ffffff, za separator = T, ako mikrosekunda nije 0

# timedelta: trajanje između dva date-time do rezolucije mikrosekunde
dt.timedelta.days,dt.timedelta.seconds,dt.timedelta.microseconds # atributi
# timedelata konvertira sve u days + seconds + microseconds
timedelta.total_seconds() # konvertira sve u sekunde

t1 = date(), t2 = date()
t1 = time(), t2 = time()
t1 = datetime(...), t2 = datetime(...)
t3 = t2 # t1 # kreira timedelta objekt koji mjeri vremensku udaljenost t1 i t2

td = datetime.timedelta(weeks=2,days=50,hours=5,minutes=5,seconds=27,microseconds=10)

# STRFTIME:
# %a	abbreviated weekday name
# %A	full weekday name
# %b	abbreviated month name
# %B	full month name
# %c	appropriate date and time representation
# %d	day of the month as a decimal number [01,31]
# %f	microseconds as a decimal number
# %H	hour (24-hour clock) as a decimal number [00,23]
# %I	hour (12-hour clock) as a decimal number [01,12]
# %j	day of the year as a decimal number [001,366]
# %m	month as a decimal number [01,12]
# %M	minute as a decimal number [00,59]
# %p	locale’s equivalent of either AM or PM
# %S	second as a decimal number [00,61]
# %U	week number (0=Sunday) as a decimal number [00,53]
# %w	weekday as a decimal number [0=Sunday,6].
# %W	week number (0=Monday) as a decimal number [00,53]
# %x	local appropriate date representation
# %X	local appropriate time representation
# %y	year without century as a decimal number [00,99]
# %Y	year with century as a decimal number.
# %z	TZ offset indicating +/- time difference from UTC/GMT

import csv									# comma separated value format handling

# csv.reader(csvfile,dialect,**)			# čita red po red
with open('f') as f:
	r = csv.reader(f)
	for row in r:
		pass

# csv.writer(csvfile,delimiter,**)			# piše red po red
with open('f','w') as f:
	w = csv.writer(f)
	w.writerow([0,0])
	w.writerows([[0,0],[0,0]])

# csv.DictReader(csvfile,dialect,**)		# mapira na dict
with open('f') as f:
	dr = csv.DictReader(f)
	for row in d:
		pass

# csv.DictWriter(csvfile,dialect,...)		# mapira iz dict
with open('f','w') as f:
	dw = csv.DictWriter(f)
	dw.writerow({0:0})
	dw.writerows({0:0,0:0})

# DATOTEKE:									# funkcije za rad s datotekama
file_path = 'file_path'

# # POPIS:
with open(file_path) as f:
	f.close()					# zatvara file
	f.flush()					# prazni buffer
	f.read(size)				# vraća sadržaj filea, size: broj byteova koji treba vratiti, default -1 = cijeli file
	f.readable()				# vraća da li se file može čitati, True ako može, False ako ne može
	f.readline(size)			# vraća jedan redak iz filea, size: broj byteova koji treba vratiti, default -1 = cijeli redak
	f.readlines(hint)			# vraća listu redaka iz filea, hint: max broj byteova koji vraća, default -1 = svi retci
	f.seek(offset, whence)		# mijenja poziciju, offset od ref. točke whence: 0 # početak, 1 # trenutno, 2 # kraj
	f.seekable()				# vraća da li je dopušten seek, True ako može, False ako ne može
	f.tell()					# vraća poziciju kursora, broj byteova od početka filea
	f.writable()				# vraća da li se u file može zapisivati, True ako može, False ako ne može
	f.write(byte)				# zapisuje string u file, pozicija ovisi je li otvoren kao "w" (briše sve) ili "a" (dodaje na kraj)
	f.writelines()				# zapisuje listu stringova u file, pozicija ovisi kako je otvoren (isto kao write)

import json									# JavaScript Object Notation

try:										# load from file
	with open(file_path,'r') as f:
		var = json.load(f)
except Exception as e:
	print(e)

try:										# dump to file
	with open(file_path,'w') as f:
		var = json.dump(f)
except Exception as e:
	print(e)

var = json.loads('')						# load from string
s = json.dumps(var)							# dump to string

# WEB:

import urllib								# dohvaćanje web sadržaja

URL = ''
connection = urllib.request.Request(URL)
try:
	with urllib.request.urlopen(connection) as response:
		site = response.read().decode()
except Exception as e:
	print(e)

import ssl
context = ssl._create_unverified_context()
try:
	with urllib.request.urlopen(connection,context=context) as response:
		site = response.read().decode()
except Exception as e:
	print(e)

import requests

# otvaranje url-a:
response = requests.get(URL)
print(response.status_code)
print(response.content)
print(response.headers)
print(response.text)

from bs4 import BeautifulSoup
# varijanta 1: urllib
URL = ''
connection = urllib.request.Request(URL)
try:
	with urllib.request.urlopen(connection) as response:
		site = response.read().decode()
except Exception as e:
	print(e)

# varijanta 2: requests
site = requests.get(URL).content

# parsing:
data = BeautifulSoup(site,'html.parser')
paragrafi = data.find_all('p')
linkovi = data.find_all('a')
naslov = data.find('h1').get_text()
css_sel = data.select('.CSS_class_name')

# # PRIMJER # WEB SCRAPING:
# import requests, os, sys

opis_ocjena = {'One':'*','Two':'**','Three':'***','Four':'****','Five':'*****'}
def get_ocjena(tag):
	for (naziv,broj_zvjezdica) in opis_ocjena.items():
		if naziv in tag['class']:
		# vadi value iz tag dictionary kao string (class='star-rating Number')
		# naziv je substring, testira je li key 'Number' unutar velikog stringa
			return broj_zvjezdica

site = requests.get(URL).content
data = BeautifulSoup(site,'html.parser')

naslovi = data.select('.product_pod h3 a')
# odvajanje razmakom zapravo ulazi u podnivoe .product_pod > h3 > a
cijene = data.select('.price_color')
ocjene = data.select('.star-rating')

try:
	with open(file_path,'w',encoding='utf-8') as fw:
		for (naslov,cijena,ocjena) in zip(naslovi,cijene,ocjene):
			fw.write(f'naslov: {naslov['title']}; cijena: {cijena.string}; ocjena: {get_ocjena(ocjena)}')
			# naslov["title"]: kad je tag, elementi taga učitavaju se kao dictionary
			# cijena.string: vrijednost između tagova učitava se kao string
			# get_ocjena(ocjena): transformacija iščitane vrijednosti
except Exception as e:
	print(e)

# BAZE PODATAKA:

# # SQL osnovne naredbe:

# kreiranje tablice:
C = 'CREATE TABLE IF NOT EXISTS Djelatnici (id INTEGER PRIMARY KEY, djelatnikId, ime VARCHAR(50) NOT NULL, ime VARCHAR(50) NOT NULL, dob INT, ulica VARCHAR(150))'
# zapisivanje vrijednosti:
I = 'INSERT INTO Djelatnici (djelatnikId, ime, prezime) VALUES (1,"Petar","Peric")'
# dohvaćanje podataka:
S = 'SELECT ime, prezime FROM Djelatnici WHERE ime LIKE "Pet%"'
# ažuriranje vrijednosti:
U = 'UPDATE Djelatnici SET ime = "Petar Krešimir", prezime = "Perić" WHERE djelatnikId = 1'
# brisanje vrijednosti:
D = 'DELETE FROM Djelatnici WHERE djelatnikId = 1'
# brisanje tablice:
D = 'DROP TABLE IF EXISTS Djelatnici'

# # SQLite primjer

import sqlite3

try:
	connection = sqlite3.connect(filepath)
	cursor = connection.cursor()

	query_create = '''CREATE TABLE IF NOT EXISTS Employees
					(id INTEGER PRIMARY KEY,
					name TEXT NOT NULL,
					email TEXT NOT NULL UNIQUE)'''
	cursor.execute(query_create)			# nema values, samo query
	connection.commit()						# mijenja nešto u bazi

	query_insert = '''INSERT INTO Employees
					(name,email) VALUES (?,?)'''
	query_insert_values = [
		('Mate Matić','mate.matic@gmail.com'),
		('Ana Anić','ana.anic@hotmail.com')]
	for value in query_insert_values:		# vrti kroz petlju jer izvršava
		cursor.execute(query_insert,value)	# za svaki element liste posebno
	connection.commit()						# mijenja nešto u bazi

	query_select = 'SELECT * FROM Employees WHERE id = ?'
	query_select_values = (2,)				# čak i kad je 1 value, piše se kao tuple
	cursor.execute(query_select,query_select_values)
	records = cursor.fetchall()				# nešto se vadi iz baze
	print(records)

	query_update = 'UPDATE Employees SET name = ?, email = ? WHERE id = ?'
	query_update_values = ('Ana Anic Matic','ana.anic.matic@hotmail.com',2)
	cursor.execute(query_update,query_update_values)
	connection.commit()						# mijenja nešto u bazi

	query_delete = 'DELETE FROM Employees WHERE id = ?'
	query_delete_values = (2,)				# čak i kad je 1 value, piše se kao tuple
	cursor.execute(query_delete,query_delete_values)
	connection.commit()						# mijenja nešto u bazi

	query_drop = 'DROP TABLE IF EXISTS Employees'
	cursor.execute(query_drop)				# nema values, samo query
	connection.commit()						# mijenja nešto u bazi

except sqlite3.Error as e:
	print(e)

finally:
	if cursor:
		cursor.close()
	if connection:
		connection.close()

# GUI

# # tkinter osnove:
import tkinter as tk
rootWindow = tk.Tk()	# osnovni objekt (root window) je Tk():
rootWindow.mainloop()	# prozor se pokreće kroz main loop
# svaki slijedeći element mora imati naveden element koji mu je roditelj
tk.Button(rootWindow,text="Hello World").pack()		# smještaj komandnog botuna na formi

# # tkinter primjer:
from tkinter import ttk, messagebox

class frm_default(ttk.Labelframe):
	def __init__(self,master):
		self.root = master
		super().__init__(master)

		self.unos_var = tk.StringVar()

		self.configure_basic()
		self.attach_widgets()
	
	def configure_basic(self):
		self.configure(style='frm_okviri.TLabelframe',text="FRAME TITLE")

		self.unos_var.set("template tekst")

	def attach_widgets(self):
		lbl_poruka = ttk.Label(self,text='PORUKA!',style='lbl_poruke.TLabel')
		lbl_poruka.place(x=10,y=20,height=50,width=370,bordermode='ignore')

		lbl_oznaka = ttk.Label(self,text='unos teksta:',style='lbl_oznake.TLabel')
		lbl_oznaka.place(x=10,y=90,height=20,width=80,bordermode='ignore')

		ent_unos = ttk.Entry(self,textvariable=self.unos_var,style='ent_unosi.TEntry')
		ent_unos.place(x=100,y=90,height=20,width=140,bordermode='ignore')

		btn_gumb = ttk.Button(self)
		btn_gumb.configure(text='Potvrdi unos',style='btn_gumbi.TButton',command=self.action)
		btn_gumb.place(x=260,y=72,height=22,width=118)

	def action(self):
		messagebox.showinfo("Status",f"Potvrda unosa: {self.unos_var.get()}")

class TkRoot(tk.Tk):
	def __init__(self):
		super().__init__()
		self.configure_basic()
		self.configure_style()
		self.attach_default_frame()

	def configure_basic(self):
		self.geometry("400x130")
		self.title("TITLE")
		self.resizable(0,0)

	def configure_style(self):
		self.style = ttk.Style(self)
		self.style.configure('frm_okviri.TLabelframe',relief='flat')
		self.style.configure('lbl_poruke.TLabel',background='white',relief='solid',
					   		font=('Segoe UI',12), padding=(2,2,2,2),anchor='nw',
							justify='left',compound='left')
		self.style.configure('lbl_oznake.TLabel',relief='flat',
					   		font=('Segoe UI',9), anchor='w',
							justify='left',compound='left')
		self.style.configure('ent_unosi.TEntry',font=('Segoe UI',9),compound='left')
		self.style.configure('btn_gumbi.TButton',relief='groove',
					   		font=('Segoe UI',9),compound='center')

	def attach_default_frame(self):
		self.frm_default = frm_default(self)
		self.frm_default.place(x=5,y=5,height=120,width=390)

class App():
	def __init__(self):
		try:
			self.interface_root = TkRoot()
		except Exception as e:
			print(e)
	def run(self):
		try:
			self.interface_root.mainloop()
		except Exception as e:
			print(e)

def run_gui():
	try:
		App().run()
	except Exception as e:
		print(e)

run_gui()

# IOT

import sense_emu
sh = sense_emu.SenseHat()

# # SenseHat osnovne funkcije:

# class sense_emu.SenseHat()
sh.clear(*args)							# clears matrix with a single colour, default is black, accepts (r,g,b) as args
sh.flip_h(redraw=True)					# flips matrix horizontal
sh.flip_v(redraw=True)					# flips matrix vertical
sh.get_pixel(x,y)						# returns [r,g,b] representing the pixel specified by (x,y), [TL=(0,0), BR=(7,7)]
sh.get_pixels()							# returns list containing 64 [r,g,b] lists representing pixels
sh.load_image(file_path,redraw=True)	# updates matrix with 8x8 image
sh.set_pixel(x,y,*args)					# updates (x,y) pixel with [r,g,b], [TL=(0,0), BR=(7,7)]
sh.set_pixels(pixel_list)				# updates pixels with a list containing 64 [r,g,b] representing pixels
sh.show_letter('X',text_colour=[255,255,255],back_colour=[0,0,0])	# displays char X on matrix
sh.show_message(text_string,scroll_speed=0.1,text_colour=[255,255,255],back_colour=[255,255,255])

sh.get_accelerometer()				# gets orientation in degrees from accelerometer only
sh.get_accelerometer_raw()			# x y z raw data in Gs
sh.get_compass()					# gets North direction in degrees from magnetometer
sh.get_compass_raw()				# x y z raw data in μT ( micro teslas)
sh.get_gyroscope()					# gets orientation in degrees from gyroscope only
sh.get_gyroscope_raw()				# x y z raw data in radians per second
sh.get_orientation_degrees()		# returns dict with (pitch,roll,yaw) (deg)
sh.get_orientation_radians()		# returns dict with (pitch,roll,yaw) (rad)
sh.get_pressure()					# returns pressure in Millibars
sh.get_temperature()				# returns temperature in Celsius
sh.get_humidity()					# returns percentage of relative humidity
sh.stick							# SenseStick object representing the Sense HAT's joystick

# class sense_emu.SenseStick()
sh.stick.get_events()			# returns list of joystick events since last call to get_events() in order they occured
sh.stick.wait_for_event(emptybuffer=False)	# waits until joystick event becomes available
sh.stick.direction_any			# function calls on joystick use
sh.stick.direction_middle
sh.stick.direction_down
sh.stick.direction_left
sh.stick.direction_up
sh.stick.direction_right

# class sense_emu.InputEvent()
# namedtuple() derivative representing a joystick_event
e = sense_emu.InputEvent()
e.timestamp		# time at which it occured, represented as number of seconds since epoch (like time())
e.direction		# direction of push/release [D=DIRECTION]: D_DOWN,D_LEFT, D_UP,D_RIGHT, D_MIDDLE
				# alternative constants: 'down', 'left', 'up', 'right', 'middle'
e.action		# push/hold/release [A=ACTION]: A_PRESSED, A_RELEASED, A_HELD
				# alternative constants: 'pressed', 'released', 'held'

# # primjer joystick:

sh = sense_emu.SenseHat()
x = 4
y = 4

def joystick_test():

	def update_screen(colour = [255,255,255]):
		sh.clear()
		sh.set_pixels(x,y,colour)

	def clamp(value,min_value=0,max_value=7):
		return min(max_value,max(min_value,value))

	def move_dot(event:'sense_emu.InputEvent'):
		global x
		global y
		
		if event.action in ('pressed','held'):
			x = clamp(x+{'left','right'}.get(event.direction,0))
			y = clamp(y+{'up','down'}.get(event.direction,0))

	update_screen()
	while True:
		for event in sh.stick.get_events():
			move_dot(event)
			update_screen()

joystick_test()

# DS

import numpy as np

# array creation # conversion from other Python structures (lists and tuples)
a1D = np.array([1,2,3,4,5,6,7,8])
a2D = np.array([[1,2,3,4],[5,6,7,8]])
a3D = np.array([[[1,2],[3,4]],[[5,6],[7,8]]])

# intrinsic array creation functions
#1D
np.arange(start,stop,step,dtype=None)		# evenly spaced values with specified steps
np.linspace(start,stop,num,dtype=None)		# evenly spaced over specified interval
#2D
np.eye(N,M,k=0,dtype=None)					# defines a 2D identity matrix NxM, k = diag. shift indeks
np.diag(v,k=0)								# extract diag. (v=2D) or construct diag. (v=1D) array, k = diag. in question
#nD
np.zeros(shape,dtype=float)					# array of given shape and type, filled with zeros
np.ones(shape,dtype=float)					# array of given shape and type, filled with ones
np.full(shape,fill_value,dtype=None)		# array of given shape and type, filled with fill_value

# random input
from numpy.random import default_rng as rng				# random number generator
rng().integers(low,high=None,size=None,dtype=np.int64)	# random integers low # high or 0 # low
rng().random(size=None,dtype=np.float64)				# random [0,1), size = output shape, default is scalar
rng().choice(A,size=None,replace=True,p=0,axis=0)		# random sample from A, p=prob.
rng().shuffle(x,axis=0)									# modify array or sequence in place by shuffling its contents
rng().permutation(x,axis=0)								# copy and randomly permute x, or return a permuted range
rng().permuted(x,axis=None)								# randomly permute x along axis, each slice shuffled independently
rng().some_distribution()								# draws from specified distribution (normal, geometric, poisson, …)
rng().binomial(n,p,size=None)							# sample from binomial distribution, n trials, p prob. of success
rng().geometric(p,size=None)							# sample from geometric distribution, p # prob. of success
rng().standard_normal(size=None,dtype=np.float64)		# sample from φ < np.random.randn(d1,...,dn)
rng().poisson(lam=1.0,size=None)						# sample from poisson distribution, lam # expected events in interval

# stacking and block composing
np.repeat(a,repeats,axis=None)			# repeat each element of an array after themselves
np.concatenate((a1,a2),axis=0)			# join a sequence of arrays along an existing axis
np.hstack(L1,L2)						# stacks arrays in sequence horizontally (column wise)
np.vstack(L1,L2)						# stacks arrays in sequence vertically (row wise)
np.dstack(L1,L2)						# stacks arrays in sequence along third axis (depth wise)
np.column_stack(L1,L2)					# take 1D arrays, stack as columns to make single 2D array
np.block(arrays)						# assemble ndarray from nested lists of blocks, dim from last to first
# unstacking and splitting
np.unstack(x,axis=0)					# split ndarray into sequence of arrays along given axis
np.split(A,indices_or_sections,axis=0)	# split into sub-arrays along specified axis
np.hsplit(A,indices_or_sections)		# split into sub-arrays horizontally (column wise)
np.vsplit(A,indices_or_sections)		# split into sub-arrays vertically (row wise)
np.dsplit(A,indices_or_sections)		# split into sub-arrays along third axis (depth wise)

# Array attributes
A = np.array()
A.ndim			# number of dimensions
A.shape			# tuple of non-negative integers, number of elements along each dimension
A.size			# total number of elements, product of shape items
A.dtype			# data type for homogenous arrays
A.itemsize		# size of each element of array in bytes
A.nbytes 		# = A.itemsize * A.size , total bytes consumed

# indexing
A[x]			# single element: returns x-th element of A, like Python list
				# number of x dim. in relation to A dim. gives sub-array of appropriate dimensionality
# slicing and striding
A[i:j:k]		# selects [i,i+k,+2k,...(m-i)*k where m=q+(r!=0), j-i = qk+r, i+(m-1)k<j
x = np.array([1,2,3,4,5,6,7,8,9]), x[1:7:2] = array([1,3,5])
# dimensional indexing
A = array([[[1],[2],[3]],[[4],[5],[6]]])	# A [...,0] = A[:, :, 0] = array([[1,2,3],[4,5,6]])
											# ... expands to number of ":" needed for selection to index all dimensions
# integer array indexing: A[np.array([x1,x2,...])] selects items based on their N-dimensional index
A = [10,9,8,7,6,5,4,3,2,1], A[np.array([3,3,1,8])] # = [8,8,9,2]
A = [[list(range(0,7))],[list(range(7,14))],[list(range(14,21))],[list(range(21,28))],[list(range(28,35))]]
A[np.array([0,2,4]),np.array([0,1,2])]		# = [0,15,30]
A[np.array([0,2,4]),1] 						# = [1,15,29]
A[np.array([0,2,4])]						# = [[0,....6],[14,...,20],[28,...,34]]
# boolean array indexing: A[obj] where obj is an array of boolean type (returned from comparisons,etc.)
A = [1,-2,-3,4], A[A<0] 					# = [-2,-3]
A = [0,1,0,2], A[A.nonzero()] 				# = [1,2]
np.argwhere(A) 								# indices of array elements that are non-zero, grouped by element
# stacking conditions using logical operators (& = and, | = or):
A = np.array(list(range(12))), A[(A>2)&(A<11)]	# = [3,4,5,6,7,8,9,10]
# conditional indexing
np.where(condition,[x,y])					# where true yield x, otherwise yield y, x and y # manipulate array values
np.select(condlist, choicelist, default=0)	# condlist # list of conditions
											# choicelist # list of arrays from which the output elements are taken, same length as condlist
											# default scalar when all conditions return False

# saving and loading
np.savetxt(filename,A,format,delimiter=' ',newline='\n',header='',footer='')	# save array to txt file
np.loadtxt(filename,converters=None,delimiter=None,skiprows=0,usecols=None)		# load array from txt file

# basic array operations
# basic operators (+,-,*,/,%) can be used directly and are applied item by item
A = [1,2,3,4], B = [5,6,7,8], A+B = [6,8,10,12], A-B = [-4,-4,-4,-4], ...
np.sum(A,axis=None)				# sums the elements in an array, all or by specified axis
np.prod(A,axis=None)			# multiplies the elements in an array, all or by specified axis
np.max(A,axis=None)				# returns max item in an array, all or by specified axis
np.argmax(A,axis=None)			# returns indices of max values along an axis
np.min(A,axis=None)				# returns min item in an array, all or by specified axis
np.argmin(A,axis=None)			# returns indices of min values along an axis
np.unique(A,axis=None)			# returns sorted unique items, can return index,inverse,counts
np.sort(A,axis=-1,kind=None)	# sorts array, kind:{'quicksort','mergesort','heapsort','stable'}

# transposing and reshaping
A.T, np.transpose(A,axes=None) 			# returns transposed matrix
np.reshape(A,shape=None,copy=None)		# returns array reshaped to specified shape

# reversing
np.flip(A,axis=None)		# flips array along the specified axis
A = np.arange(1,13).reshape(3,4)
np.flip(A)					# = [[12,...,9],[8,...,5],[4,...,1]]
np.flip(A,axis=0)			# = [[9,...,12],[5,...,8],[1,...,4]]
np.flip(A,axis=1)			# = [[4,...,1],[8,...,5],[12,...,9]]
np.fliplr(A)				# flips left-right
np.flipud(A)				# flips up-down
np.rot90(A,k=1,axes=(0,1))	# rotates array 90 degrees, k = number of rotations, axes = rotation plane

# flattening
np.flatten(A)	# less memory efficient, creates a copy
np.ravel(A)		# more memory efficient, creates a view

# Working with functions (element wise)
np.sin(),np.cos(),np.tan(),np.arcsin(),np.arccos(),np.arctan()			# trigonometric functions
np.sinh(),np.cosh(),np.tanh(),np.arcsinh(),np.arccosh(),np.arctanh()	# hyperbolic functions
np.hypot(x1,x2)												# given legs of right triangle calculates hypotenuse
np.round(A,d)												# evenly round A to given d number of decimals
np.rint(),np.floor(), np.ceil(), np.trunc()					# other rounding functions
np.exp(), np.exp2(), np.log(), np.log2(), np.log10()		# exponents and logarithms
np.lcm(x1,x2), np.gcd(x1,x2)								#lowest common denominator, greatest common divisor
np.add(),np.subtract(),np.multiply(),np.divide(),np.mod()	# arithmetic operations
np.reciprocal(),np.power(),np.sqrt(),np.square()			# power operations
np.absolute(),np.negative(),np.positive,(),np.sign()		# numerical values

# logic functions
np.all()					# test if all along axis are True, any - test if any along axis are True
np.isfinite()				# (not infinity, not NaN), isinf (infinity), isnan (not a number)
np.iscomplex()				# complex number
np.isreal()					# real number
np.isnan()					# not a number
np.logical_and(),np.logical_or(),np.logical_not(),np.logical_xor()	# logical operations
np.is_close()				# equal within a tolerance

# comparison
np.array_equal()			# same?
np.array_equiv()			# look same?
np.greater(),np.greater_equal(),np.less(),np.less_equal(),np.equal(),np.not_equal()

# custom functions
np.fromfunction(function,shape,dtype)	# construct array by executing a function over each coordinate

# statistics
# order statistics
np.ptp()				# range of values (maximum - minimum)
np.percentile()			# compute the q-th percentile
np.quantile()			# compute the q-th quantile
# averages and variances
np.average()			# (weighted) average
np.mean()				# (arithmetic)
np.median()
np.std()				# (standard deviation)
np.var()				# (variance)
# correlating
np.corrcoef()			# Pearson product-moment correlation coefficients
np.correlate()			# cross-corelation of two 1-dimensional sequences
np.cov()				# estimate a covariance matrix, given data and weights
np.histogram()			# compute the histogram of a dataset

import pandas as pd
df = pd.DataFrame()

# Head and Tail
df.head(n=5)	# return the first n rows, for negative values returns all rows except last |n| rows
df.tail(n=3) 	# return the last n rows, for negative values returns all rows except first |n| rows

# Summary
df.describe() 	# generate descriptive statistics (central tendency, dispersion, dist. shape, ...)

# DataFrame attributes
df.index 		# displays the index attribute - index labels of the DataFrame
df.columns 		# displays the columns attribute - columns labels of the DataFrame

# Sorting data
df.sort_index(axis=0,ascending=True, inplace=False, kind="quicksort", na_position="last")
# axes: 0 = rows, 1 = columns
# kind: {"quicksort", "mergesort", "heapsort", "stable"}
df.sort_values(by,axis=0,ascending=True,inplace=False, kind="quicksort",na_position="last")
# by: str or list of str, name or list of names to sort by - if given a list, it represents crit. order
df.sort_values(by=['crit_1','crit_2',...],ascending=False) # sort by crit_1 then by crit_2,... descending

# Getting data
# passing a single label selects columns and yields a Series
df["A"], df.A				# return column "A" as Series
# passing a slice : selects matching rows
df[0:3]						# return first 3 rows as DataFrame
df["20230101":"20240101"]	# returns rows within 2023 as DataFrame
# selection by label using loc
df.loc[dates[0]]			# returns all columns, row which corresponds to first date in date range
df.loc[dates[0],"A"]		# returns column "A", row which corresponds to first date in date range
df.loc[:,["A","B"]]			# returns columns "A" and "B", rows for the whole date range
df.loc["20230101":"20240101",["A","B"]] # returns columns "A" and "B", rows in the slice
# selection by position using iloc
df.iloc[3]					# returns row at index number 3 (starting index is 0), all columns
df.iloc[3:5,0:2]			# returns rows at indices number 3 and 4, columns 0 and 1
df.iloc[[1,2,4],[0,2]]		# returns rows at indices number 1,2,4, columns 0 and 2
df.iloc[1:3,:]				# returns rows at indices 1 and 2, all columns
df.iloc[:,1:3]				# returns all rows, columns 1 and 2
df.iloc[1,1]				# returns value at row index 1, column 1
# boolean indexing:
df[df["A"] > 0]				# returns all rows where values in column "A" are greater than 0
df[df > 0]					# returns the whole df, cells with values less than 0 converted to NaN
df[df["E"].isin(["two","four"])]		# returns all rows where value in column "E" is "two" or "four"

# Setting data
# adding a new column auto aligns the data by the indices
s1 = pd.Series([1,2,3,4,5,6], index = pd.date_range("20240101", periods=6)) # append col, align dates
df.at[dates[0],"A"] 		# by label: sets the value in first row, column "A" to 0
df.iat[0,1] = 0				# by position: sets the value in first row, first column to 0
df.loc[:,"D"] = np.array([5]*len(df)) # by assigning with a NumPy array: sets all values in column "D" to 5.0
df[df > 0] = -df			# by boolean indexing: makes all positive values in df negative with same abs value
df.replace(find, value,inplace=False) # replaces found (num, str, list, dict) by specified value
df.drop(labels,axis=0,index=None,columns=None) # return Series with spec. index labels removed

# Dealing with NaN
df.dropna(axis,how,tresh,subset=None,inplace=False,ignore_index=False) # remove missing values
# how = {"any","all"}, remove row if any NaN or all NaN, or tresh = remove row if at least tresh NaN
df.dropna(how="any")	# removes all rows which contain at least 1 NaN
df.fillna(value=None,method=None,axis=None,inplace=False,limit=None) # fill missing values
# value = how to fill holes, accepts var, dict, Series, DataFrame to separate filling by index and column
df.fillna(value=5)		# replaces all NaN in df with the value 5.0
pd.isna(obj)			# creates boolean mask where NaN values are True, obj is the object to check for NaN values
pd.isna(df)				# returns boolean mask with all NaN values in df are labeled True

# Basic functions
df.abs()					# return series or df with absolute numeric values of each element
# many math functions available: min, cummin, max, cummax, sum, cumsum, prod, cumprod, pow, ...
df.idxmin(),df.idxmax()		# return index (row label) of located value
df.apply(func,axis=0)		# appy a function along an axis of the data frame
df.apply(lambda x: x*2+3)	# user defined lambda functions

# Statistics
# axes: 0 - per column, default, 1 - per row
df.mean(axis=0,skipna=True,numeric_only=False) # calculates mean of rows or columns
# many stats functions available: corr, cov, kurt, median, mode, quantile, skew, std, var, ...
df.agg(func,axis=0)				# aggregate using one or more ops over the specified axis
df.agg(lambda x: np.mean(x)*5)	# user defined lambda functions over rows or columns
df.agg(['sum','min'])			# common functions applied to all rows or columns stacked into lists
df.agg({"A":['sum','min'],'B':['min','max']})		# common functions per column (rep. by dicts)
df.agg(x=('A','max'),y=('B','min'),z=('C','mean'))	# different functions and index renaming
df.value_counts()				# Counting: returns number of repeats of a value in a series

# Pivot Tables
pd.pivot_table(data, values, index, columns, aggfunc='mean',fill_value=None, dropna=True,margins=False)
# data = df, values = columns to aggregate, index, columns = keys to group by on p.t. index, columns
# aggfunc = aggregation function, list of functions, dict of functions
# margins = add special "All" rows and columns with partial group aggregates across categories
pd.pivot_table(df, values="D", index=["A","B"],columns=["C"], aggfunc="sum")
# aggregate values in column "D", use sum as the aggregate function
# separate columns by values in column "D", separate rows by values in columns "A" and "B",

# Splitting and Merging (operating with multiple objects)
# Concatenating
pd.concat(list_of_objs, axis=0, join='outer', ignore_index=False, keys=None, sort=False)
# axis - 0 (rows) or 1 (columns), join - 'outer' or 'inner', ignore_index - resets index for concat. df
pd.concat(list_of_df,axis=0 or 1) # concatenates dfs by rows or columns
# Joining
pd.merge(left, right, how='inner', on=None, sort=False, copy=None) # database-style join
# how = {'left', 'right', 'inner', 'outer', 'cross'}, on = names to join on
pd.merge(left, right, on="key") # merges dfs left and right on column "key"
# Grouping
# group by = split into groups based on criteriy + apply function to each group + combine results
df.groupby(by, axis, as_index=True, sort=True, group_keys=True, dropna=True)
# by = determining the groups, axis = 0 (rows) or 1 (columns), as_index = group labels as index
df.groupby("A")[["C","D"]].sum() # group by column "A" label, apply sum to cols in groups, combine to df
df.groupby("A").size() # number of rows in each group as Series / DataFrame (as_index True / False)
# Binary operations
df.OPERATION(other, axis='columns') # df OPERATION df, element-wise
pd.add(df,df),pd.sub(df,df),pd.mul(df,df),pd.div(df,df),pd.mod(df,df),pd.pow(df,df)	# operations, return df
pd.lt(df,df),pd.le(df,df),pd.eq(df,df),pd.ne(df,df),pd.ge(df,df),pd.gt(df,df)		# comparisons, return bool
# broadcasting is auto applied (scalars to whole df, series to rows, df to cells, dicts to rows or columns)

# Creating date ranges
pd.date_range(start=None, end=None, periods=None, freq=None, tz=None, name=None, unit=None)
# start = left bound, end = right bound, periods = number of periods, name = datetimeindex name
# freq = offset aliases: s = second, min = minute, h = hour, W = week, MS&ME = month, YS&YE = year
# reshaping to fit a different interval:
rng = pd.date_range("1/1/2024",periods=100,freq="s")			# 100 seconds from 2024 new year
ts = pd.Series(np.random.randint(0,500,len(rng),index=rng))		# series with 100 random ints 0-500
ts.resample("5min").sum()	# sums values to reshape data into 5 minute intervals (300 s)

# Importing and exporting data
# importing: read_FORMAT functions, exporting: to_FORMAT functions
# CSV
pd.read_csv(file_path,sep=',',delimiter=None,header='infer',names=[],index_col=None,
	usecols=None, skiprows=None, skipfooter=0, nrows=None, skip_blank_lines=True)
# sep = char or regex to treat as delimiter, header = row number containing column labels,
# names = sequence of column labels to apply, index_col = columns to use as row labels,
# usecols = subset of columns to select, skiprows = line numbers to skip or number of lines to skip,
# skipfooter = number of lines from bottom to skip, nrows = number of rows to read, ...
pd.to_csv(file_path,sep=',',columns=None,header=True,index=True,index_label=None)
# sep = field delimiter for the output file, columns = columns to write, header = write out the column names
# (if list, assumed to be column aliases), index = write row names, index_label = col label for index col)

# Example:

# mport numpy as np
# import pandas as pd

# data loading and df creation
red_wine = pd.read_csv(file_name, delimiter=';')
white_wine = pd.read_csv(file_name, delimiter=';')
wine_data = pd.concat([red_wine, white_wine], ignore_index=True)

# data cleaning and preparation
wine_data.replace([float('inf'),float('-inf')], float('nan'), inplace=True)

# creating correlation matrix and getting max correlation
corr_matrix = wine_data.corr()
ph_corr = corr_matrix['pH'].drop('pH') # otherwise pH would be most correlated with pH
ph_corr_max = ph_corr.idxmax() # row index value of the highest correlation with pH

# plotting results
print(f"Most correlated attribute with pH is: {ph_corr_max}")
print(f"Correlation between pH and {ph_corr_max}: {ph_corr[ph_corr_max]}")

import matplotlib.pyplot as plt

# basic mechanism:
fig, ax = plt.subplots()		# create figure containing single Axes
ax.plot([1,2,3,4],[1,2,3,4])	# plot some data on the Axes
plt.show()						# show figure (if required by backend)

# Figure: the whole figure. It keeps track of all the child Axes, a group of special Artists
fig = plt.figure()				# an empty figure with no Axes
fig, ax = plt.subplots()		# a figure with a single Axes
fig, axs = plt.subplots(2,2)	# a figure with 2x2 grid of Axes
fig, axs = plt.subplot_mosaic([['left','right_top'],['left','right_bottom']]) # 1 Axes on the left, 2 on the right

# Axes: Artist attached to a Figure that contains a region for plotting data, usually includes 2/3 Axis objects
Axes.plot()						# plot y vs x as lines and/or markers, returns a list of Line2D

# plotting using pandas:
df.plot() # makes plots of Series or DataFrame
# by default matplotlib backend is used (plotting.backend)

# parameters:
# data: object for which the method is called
# x=None: label or position (only for df)
# y=None: label or list of labels, allows plotting one col vs another (only for df)
# kind = {'line' | 'bar' | 'barh' | 'hist' | 'box' | 'kde' | 'density' | 'area' | pie' | 'scatter' | 'hexbin'}
# ax=None, an axes of the current figure (matplotlib axes object)
# subplots=False: if True, make separate subplots for each column
# layout: tuple (rows, cols) for the layout of the subplots
# use_index=True: use index as ticks for x axis
# title: title to use for the plot (str for single or list of str for subplots)
# grid=False: if True, plot axis grid lines
# legend=False: if True, place legend on axis subplots
# xticks,yticks=sequence: values to use for the ticks
# xlabel,ylabel=None: label to use for the x and y axis
# rot=None: rotation (float) for ticks
# fontsize=None: float, font size for ticks

# Example (wine continued):
fig,ax = plt.subplots(figsize=(10,5),layout='constrained')
ax.hist(wine_data['pH'].dropna(),bins=30,alpha=0.75)
ax.set_title("Histogram for pH value")
ax.set_xlabel('pH')
ax.set_ylabel('Frequency')

# Example (wine continued):
fig,ax = plt.subplots(figsize=(10,5),layout='constrained')
ax.hist(wine_data[ph_corr_max].dropna(),bins=30,alpha=0.75)
ax.set_title(f"Histogram for most correlated attribute ({ph_corr_max})")
ax.set_xlabel({ph_corr_max})
ax.set_ylabel('Frequency')