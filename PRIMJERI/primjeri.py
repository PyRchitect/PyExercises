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

# DATOTEKE:
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

