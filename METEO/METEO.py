from sys import path as sys_path			# working folder
from datetime import datetime as dt			# get date time now
import threading as th						# background IO processing						
from enum import Enum						# const enumeration

import configparser as cp					# RPi config
import paramiko								# SSH to RPIs
from sense_emu import SenseHat				# RPi sense hat
from subprocess import Popen, PIPE, STDOUT	# direct command to RPi
from random import uniform					# test hat randomization

import tkinter as tk						# interface
from tkinter import 	ttk,		\
						messagebox

# <EXCEPTIONS> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

class DependenciesError(Exception):
	def __str__(self):
		return 	"External dependencies:"								+ \
				"\n> PIL (pip install pillow)"							+ \
				"\n> requests (pip install requests)"					+ \
				"\n> paramiko (pip install paramiko)"					+ \
				"\n> sense_emu (pip install sense-emu)"					+ \
				"\n> sqlalchemy (pip install sqlalchemy)"				+ \
				"\n> sqlalchemy_utils (pip install sqlalchemy_utils)"

class DBConnectError(Exception):
	def __str__(self):
		return	"Pogreška pri spajanju na bazu!"

class DBReadError(Exception):
	def __str__(self):
		return	"Pogreška pri čitanju iz baze!"

class DBWriteError(Exception):
	def __str__(self):
		return	"Pogreška pri upisu u bazu!"

class IFOpenError(Exception):
	def __str__(self):
		return	"Pogreška pri otvaranju sučelja!"

class SensorConnectError(Exception):
	def __str__(self):
		return "Pogreška pri spajanju na senzor!"

class ConfigReadError(Exception):
	def __str__(self):
		return "Pogreška pri otvaranju konfiguracijskog filea!"

# </EXCEPTIONS> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# <SENSORS>

class SensorSSH():
	# "real" RPi
	def __init__(self,sensor_data):
		self.type = "SSH"
		self.name = sensor_data['NAME']
		self.sensor_types = ['temp','vlaga','tlak']

		self.ip = sensor_data['IP']
		self.user = sensor_data['USER']
		self.sf = sensor_data['SF']

		from io import StringIO		# convert to stream
		pkf_stream = StringIO(open(sensor_data['PKF']).read())
		self.pk = paramiko.Ed25519Key.from_private_key(pkf_stream)

		self.client = self.ssh_client_create()

		# attempt to start GUI (probe connection)
		self.process_name = 'sense_emu_gui'
		try:
			self.start_process()
		except:
			raise SensorConnectError

		# # # TEST
		# temp = self.get_data('temp')
		# vlaga = self.get_data('vlaga')
		# tlak = self.get_data('tlak')

	def ssh_client_create(self):
		client = paramiko.SSHClient()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		return client

	def start_process(self):
		self.client.connect(self.ip,username=self.user,pkey=self.pk)

		# get count of process:
		command = f"pgrep -c {self.process_name}"
		# execute command on server
		_stdin, stdout, _stderr = self.client.exec_command(command)
		# read output
		count = int(stdout.read().decode())

		# check if exists among running ps:
		if count == 0:
			# if not running, spawn process:

			# set display to view output:
			# > from VM echo $DISPLAY = 0
			# > otherwise login as user, echo

			# launch directly from session
			launch = f"export DISPLAY=:0;{self.process_name}"
			_stdin, stdout, stderr = self.client.exec_command(launch)

			# launch from launcher script placed on the PI
			# launch = f"export DISPLAY=:0;python {self.sf}/sense_emu_gui_launcher.py"
			# _stdin, stdout, stderr = client.exec_command(launch)

		# close conn
		# self.client.close()

	def end_process(self):
		command = f"export DISPLAY=:0;pkill -f {self.process_name}"
		# execute command on server
		_stdin, stdout, _stderr = self.client.exec_command(command)

		# close conn if the client is active
		if self.client.get_transport() is not None:
			if self.client.get_transport().is_active():
				self.client.close()

	def get_data(self,data_type):
		if data_type not in self.sensor_types:
			raise ValueError("SH environment: Unknown data type!")		

		try:
			#with self.client as conn:
				# conn.connect(self.ip,username=self.user,pkey=self.pk)
				# launch from launcher script placed on the PI
				launch = f"export DISPLAY=:0;python {self.sf}/sense_emu_gui_{data_type}.py"
				_stdin, stdout, _stderr = self.client.exec_command(launch)
				# data = stdout.read().decode()
				return round(float(stdout.read().decode().strip("\n")),1)
		except:
			raise SensorConnectError

class SensorDummy():
	# dummy RPi for testing if no SSH
	def __init__(self,name):
		self.type = "Local"
		self.name = name
		self.sensor_types = ['temp','vlaga','tlak']

		self.hat = SenseHat()

		# attempt to start GUI (probe connection)
		self.process_name = 'sense_emu_gui'
		try:
			self.start_process()
		except:
			raise SensorConnectError

		# temp = self.get_data('temp')
		# vlaga = self.get_data('vlaga')
		# tlak = self.get_data('tlak')

	def start_process(self):
		# get count of process:
		command = f"pgrep -c {self.process_name}"
		# execute command on server
		p = Popen(
			command,
			shell=True,
			stdin=PIPE,
			stdout=PIPE,
			stderr=STDOUT,
			close_fds=True
			)
		# read output
		count = int(p.stdout.read().decode())
		# check if exists among running ps:
		if count == 0:
			# if not running, spawn process:
			Popen(
				self.process_name,
				shell=True,
				stdin=PIPE,
				stdout=PIPE,
				stderr=STDOUT,
				close_fds=True
				)
		
	def end_process(self):
		# kill the GUI process:
		command = f"kill -9 '{self.process_name}'"
		# shutdown the GUI on the connected RPi
		Popen(
			command,
			shell=True,
			stdin=PIPE,
			stdout=PIPE,
			stderr=STDOUT,
			close_fds=True
			)

	def get_data(self,data_type):
		if data_type not in self.sensor_types:
			raise ValueError("SH environment: Unknown data type!")
		elif data_type == 'temp':
			return self.hat.get_temperature()
		elif data_type == 'vlaga':
			return self.hat.get_humidity()
		elif data_type == 'tlak':
			return self.hat.get_pressure()

class SensorTest():
	# demo RPi returns random values for testing

	def __init__(self,name):
		self.type = "Test"
		self.name = name
		self.sensor_types = ['temp','vlaga','tlak']

		# temp = self.get_data('temp')
		# vlaga = self.get_data('vlaga')
		# tlak = self.get_data('tlak')

	def start_process(self): ...
		# nothing to do, only for SM iteration purposes

	def end_process(self): ...
		# nothing to do, only for SM iteration purposes

	def get_data(self,data_type):
		if data_type not in self.sensor_types:
			raise ValueError("SH environment: Unknown data type!")
		elif data_type == 'temp':
			return round(uniform(-15,35))
		elif data_type == 'vlaga':
			return round(uniform(0,100))
		elif data_type == 'tlak':
			return round(uniform(950,1050))

class SensorManager():

	def __init__(self,data_loaded,sensor_data):

		self.RPis = {}

		for sensor in sensor_data:
			# test RPi connection:
			try:
				# no need to try to create ssh clients if no data loaded
				assert data_loaded
				# config data loaded, attempt to create ssh clients:
				# IF SSH DON'T NEED TO RUN HOST PROCESS ON PI
				self.RPis[sensor['NAME']] = SensorSSH(sensor)
			except:
				try:
					# attempt to create dummy clients:
					# IF NO SSH MUST RUN ON RPi TO START DUMMIES
					self.RPis[sensor['NAME']] = SensorDummy(sensor['NAME'])
				except:
					# no SSH RPi, no local RPi, fallback
					# create test clients (return defaults)
					self.RPis[sensor['NAME']] = SensorTest(sensor['NAME'])
	
	def close_connections(self):
		# connections are maintained throughout for faster readings
		# they need to be closed prior to clearing SM for clean exit
		for RPi in self.RPis.values():
			RPi.end_process()

# </SENSORS>
# <INTERFACE> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# <SCROLLBOX> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def _create_container(func):
	# factory function which equips element with a frame container
	# and binds the mouse wheel movement to the frame on hover

	speed_reduction = 100

	def _on_mousewheel(event, widget):
		widget.yview_scroll(-1*int(event.delta/speed_reduction),'units')

	def _bound_to_mousewheel(event, widget):
		child = widget.winfo_children()[0]
		child.bind_all('<MouseWheel>', lambda e: _on_mousewheel(e, child))

	def _unbound_to_mousewheel(event, widget):
		widget.unbind_all('<MouseWheel>')

	def wrapped(cls, master, **kw):
		container = ttk.Frame(master)
		container.bind('<Enter>', lambda e: _bound_to_mousewheel(e, container))
		container.bind('<Leave>', lambda e: _unbound_to_mousewheel(e, container))
		return func(cls, container, **kw)

	return wrapped

class AutoScroll():

	def __init__(self, master):
		vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
		hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)

		self.grid(column=0, row=0, sticky='nsew')
		vsb.grid(column=1, row=0, sticky='ns')
		hsb.grid(column=0, row=1, sticky='ew')

		master.grid_columnconfigure(0, weight=1)
		master.grid_rowconfigure(0, weight=1)

		# take packing methods (except config and internal)
		methods = 	tk.Pack.__dict__.keys() | \
					tk.Grid.__dict__.keys() | \
					tk.Place.__dict__.keys()

		for m in methods:
			if m[0] != '_' and m not in ('config', 'configure'):
				setattr(self, m, getattr(master, m))

class ScrolledListBox(AutoScroll, tk.Listbox):

	@_create_container
	def __init__(self, master, **kw):
		tk.Listbox.__init__(self, master, **kw)
		AutoScroll.__init__(self, master)

# </SCROLLBOX> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# <WIDGETS>  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

class frmPostaja(ttk.LabelFrame):

	def __init__(self,master):

		self.root = master
		super().__init__(master)

		self.unos_ugoda_bracket = [0,12,22]
		# ugoda depends on postaja value bracket
		self.unos_ugoda = None
		# data from postaja
		self.unos_postaja = tk.DoubleVar()
		self.unos_postaja.set("")
		self.unos_ugoda = -1
		# station probe
		self.dp = self.load_station_data()
		self.lbl_postaja_v = None
		self.probe_postaja = None
		self.probe_loader = None
		# progress bar
		self.pb = None

		self.configure_basic()

		# initialize label images:
		self.lbl_ugoda_v = []
		self.img_active = []
		self.img_grey = []
		self.img_get = []
		self.init_images()

		self.attach_widgets()

	def configure_basic(self):
		self.configure(
			style='frm.TLabelframe',
			text="Meteo podaci [C]")

	def init_images(self):
		from PIL import Image,ImageTk	# img adjustments

		path_get = sys_path[0]+'\\'+f"IKONE_get.png"
		self.img_get = ImageTk.PhotoImage(
					Image.open(path_get).resize((25,25))
					)

		for x in range(4):
			path_active = sys_path[0]+'\\'+f"IKONE_{x}_active.jpg"
			path_grey = sys_path[0]+'\\'+f"IKONE_{x}_grey.jpg"

			self.img_active.append(
				ImageTk.PhotoImage(
					Image.open(path_active).resize((36,36))
					)
				)
			self.img_grey.append(
				ImageTk.PhotoImage(
					Image.open(path_grey).resize((36,36))
					)
				)

	def set_label_image(self,x):
		if x == self.unos_ugoda:
			self.lbl_ugoda_v[x].configure(image=self.img_active[x])
		else:
			self.lbl_ugoda_v[x].configure(image=self.img_grey[x])

	def load_station_data(self):
		try:
			with open(sys_path[0]+'\\'+"config.ini") as cf:
				config = cp.RawConfigParser()
				config.read_file(cf)

				weather = config["Weather"]

				return {
					"URL"			: weather["URL"],
					"SUBTREE.TAG"	: weather["SUBTREE.TAG"],
					"FILTER.TAG"	: weather["FILTER.TAG"],
					"FILTER.VALUE"	: weather["FILTER.VALUE"],
					"DATA.TAG"		: weather["DATA.TAG"],
					"DATA_TEMP.TAG"	: weather["DATA_TEMP.TAG"],
					"DATA_VLAGA.TAG": weather["DATA_VLAGA.TAG"],
					"DATA_TLAK.TAG"	: weather["DATA_TLAK.TAG"]
				}
		except:
			return {
				"URL"			: 'https://vrijeme.hr/hrvatska_n.xml',
				"SUBTREE.TAG"	: "Grad",
				"FILTER.TAG"	: "GradIme",
				"FILTER.VALUE"	: "Zagreb-Maksimir",
				"DATA.TAG"		: "Podatci",
				"DATA_TEMP.TAG"	: "Temp",
				"DATA_VLAGA.TAG": "Vlaga",
				"DATA_TLAK.TAG"	: "Tlak"
			}	# defaults for testing
			# for production, raise error:
			# raise ConfigReadError()

	def probe_load_worker(self):
		# worker thread stops animation on data load
		while True:
			# check every half-second:
			self.root.tksleep(0.5)
			# whether data gathered:
			if self.unos_postaja is not None:
				# stop animation:
				self.pb.stop()
				# detach progress bar:
				self.detach_progressbar()
				# attach value label:
				self.attach_value_label()
				# probe loaded, set loader to none
				self.probe_loader = None
				# exit loop, end the thread
				break

	def probe_load(self):
		# destroy the label if exists:
		self.detach_sensor_label()
		# reset the variable if value set:
		self.unos_postaja = None
		# attach progress bar:
		self.attach_progressbar()
		# start animation:
		self.pb.start()
		# create the loading probe
		self.probe_loader = th.Thread(target=self.probe_load_worker)
		# start the loading probe
		self.probe_loader.start()
		# start the scraping probe
		self.get_station_data()

	def get_station_worker(self):
		from requests import get as rget			# xml retrieve
		import xml.etree.ElementTree as ET			# xml parsing

		try:
			root = ET.fromstring(rget(self.dp["URL"]).text)
			for grad in root.findall(self.dp["SUBTREE.TAG"]):
				if grad.find(self.dp["FILTER.TAG"]).text == self.dp["FILTER.VALUE"]:
					podaci = grad.find(self.dp["DATA.TAG"])
					t = float(podaci.find(self.dp["DATA_TEMP.TAG"]).text)
					# h = float(podaci.find(self.dp["DATA_VLAGA.TAG"]).text)
					# p = float(podaci.find(self.dp["DATA_TLAK.TAG"]).text)
		except:
			# default to 0 for testing
			t = 0
			# for production, raise error:
			# raise ConfigReadError()

		# img signal (0-3)
		self.unos_ugoda = 0
		for x in self.unos_ugoda_bracket:
			if t > x:
				self.unos_ugoda += 1
		# adjust label images
		for i in range(4):
			self.set_label_image(i)

		# set tk var for lbl value (loader worker signal)
		self.unos_postaja = tk.DoubleVar(value=round(t,1))
		# probe finished, set to none
		self.probe_postaja = None

	def get_station_data(self):
		self.probe_postaja = th.Thread(target=self.get_station_worker)
		self.probe_postaja.start()

	def attach_widgets(self):

		lbl_postaja = ttk.Label(self,text='Ref. postaja:',style='lbl_naslov.TLabel')
		lbl_postaja.place(x=240, y=20, height=22, width=100, bordermode='ignore')

		for i in range(4):
			self.lbl_ugoda_v.append(
				ttk.Label(self,style='lbl_ugoda.TLabel')
			)
			self.lbl_ugoda_v[i].place(x=15+i*(39+8), y=30, height=39, width=39, bordermode='ignore')
			self.set_label_image(i)

		btn_get = ttk.Button(self)
		btn_get.place(x=346, y=30, height=39, width=39, bordermode='ignore')
		btn_get.configure(
			style='btn_get.TButton',
			image=self.img_get,
			command=self.probe_load)

	def attach_value_label(self):
		self.lbl_postaja_v = ttk.Label(self,textvariable=self.unos_postaja,style='lbl_vrijednost.TLabel')
		self.lbl_postaja_v.place(x=240, y=40, height=40, width=100, bordermode='ignore')

	def detach_sensor_label(self):
		if self.lbl_postaja_v and self.lbl_postaja_v.winfo_exists():
			# if the label exists, destroy it:
			self.lbl_postaja_v.destroy()
			self.lbl_postaja_v = None

	def attach_progressbar(self):
		self.pb = ttk.Progressbar(
			self,orient='horizontal',mode='indeterminate',length=60
			)
		self.pb.place(x=270,y=40,anchor='center')

	def detach_progressbar(self):
		self.pb.destroy()
		self.pb = None		

class frmBasic(ttk.LabelFrame):

	def __init__(self,master):

		self.root = master
		super().__init__(master)

		# attach on config
		self.unos_unutar = tk.StringVar()
		self.unos_izvan = tk.StringVar()
		self.unos_ocitanja = tk.Variable()

		# ref listbox for easier refresh control
		self.box_ocitanja = None
		self.data_column = self.get_data_column()

		self.configure_basic()

		self.attach_widgets()

		self.init_sensors()
		# needs to set unutar, izvan values
		self.get_sensor_data()

		self.refresh_list(self.data_column)

	def init_sensors(self):
		...

	# - - - - - - - - - - - - - - - - - - - - - - - - - - -
	# functions different for each mode
	# to be implemented in child classes
	# primitive abstractmethod style coding

	def configure_basic(self):
		raise NotImplementedError("Configure labelframe style, text, ...")

	def get_data_column(self):
		raise NotImplementedError("Define data column (return 't','h','p')")

	def get_sensor_data(self):
		raise NotImplementedError("Set: self.unos_unutar, self.unos_izvan")

	# - - - - - - - - - - - - - - - - - - - - - - - - - - -

	def refresh_list(self,data_type):
		try:
			# catch all db exceptions as DBReadError
			try:
				res = self.root.DB_link.select_data(data_type)
			except Exception as e:
				raise DBWriteError()
		except DBReadError:
			messagebox.showerror("Greška pri otvaranju",DBReadError())
			return

		self.unos_ocitanja.set(res)

	def attach_widgets(self):

		# LABELS

		lbl_unutar = ttk.Label(self,text='Unutar kuće:',style='lbl_naslov.TLabel')
		lbl_unutar.place(x=240, y=20, height=22, width=100, bordermode='ignore')

		lbl_unutar_v = ttk.Label(self,textvariable=self.unos_unutar,style='lbl_vrijednost.TLabel')
		lbl_unutar_v.place(x=240, y=40, height=40, width=100, bordermode='ignore')

		lbl_izvan = ttk.Label(self,text='Izvan kuće:',style='lbl_naslov.TLabel')
		lbl_izvan.place(x=240, y=100, height=22, width=100, bordermode='ignore')

		lbl_izvan_v = ttk.Label(self,textvariable=self.unos_izvan,style='lbl_vrijednost.TLabel')
		lbl_izvan_v.place(x=240, y=120, height=40, width=100, bordermode='ignore')

		# SCROLLBOX

		self.box_ocitanja = ScrolledListBox(self)
		self.box_ocitanja.place(x=15, y=25, height=130, width=180, bordermode='ignore')
		# custom element containing scroll and list, Listbox NOT ttk
		# easier to configure the widget here (only one element in frm)
		# than to define for it a custom ttk class with style specs
		self.box_ocitanja.configure(
			listvariable=self.unos_ocitanja,
			selectmode=tk.BROWSE,
			background="white",
			disabledforeground="#b4b4b4",
			font=('Segoe UI',7),
			foreground="black",
			highlightcolor="#d9d9d9",
			selectbackground="#d9d9d9",
			selectforeground="black",
			relief="solid",
			cursor="xterm",
		)
		self.box_ocitanja.bind("<<ListboxSelect>>",self.box_select)

	def box_select(self,event:'tk.Event'):
		# nothing to do, template method
		pass

class frmTemp(frmBasic):

	def __init__(self,master):
		# nothing to do, template method
		# initialize master
		super().__init__(master)

	def get_data_column(self):
		return 'temp'

	def get_sensor_data(self):
		self.unos_unutar.set("")
		self.unos_izvan.set("")

	def configure_basic(self):
		self.configure(
			style='frm.TLabelframe',
			text="Temperatura [C]")

class frmVlaga(frmBasic):

	def __init__(self,master):
		# nothing to do, template method
		# initialize master
		super().__init__(master)

	def get_data_column(self):
		return 'vlaga'

	def get_sensor_data(self):
		self.unos_unutar.set("")
		self.unos_izvan.set("")

	def configure_basic(self):
		self.configure(
			style='frm.TLabelframe',
			text="Vlažnost [%]")

class frmTlak(frmBasic):

	def __init__(self,master):
		# nothing to do, template method
		# initialize master
		super().__init__(master)

	def get_data_column(self):
		return 'tlak'

	def get_sensor_data(self):
		self.unos_unutar.set("")
		self.unos_izvan.set("")

	def configure_basic(self):
		self.configure(
			style='frm.TLabelframe',
			text="Tlak [hPa][mbar]")

class tkRoot(tk.Tk):

	def __init__(self,DB_link):
		# database link
		self.DB_link:'DB' = DB_link
		# sensor manager link
		self.SM_link:'SensorManager' = None
		# live sensor reading
		self.sensor_names = [
			{'NAME':'unutar'},
			{'NAME':'izvan'}
			]
		self.lbl_sensor = None
		self.probe = None
		self.probe_loader = None
		self._probe_kill = th.Event()
		# progress bar
		self.pb = None

		super().__init__()

		self.configure_basic()
		self.style = self.style_config()

		self.attach_frames()
		self.attach_widgets()

	def load_sensor_data(self):
		sensor_data = []
		names_test:'list' = self.sensor_names.copy()

		try:
			with open(sys_path[0]+'\\'+"config.ini") as cf:
				config = cp.RawConfigParser()
				config.read_file(cf)
				assert config.has_option("DEFAULT","RPis")
				
				for sensor in [x.strip() for x in config["DEFAULT"]["RPis"].split(',')]:
					data = {
						'NAME'	: config[sensor]['NAME'],
						'IP'	: config[sensor]['IP'],
						'USER'	: config[sensor]['USER'],
						'PKF'	: config[sensor]['PKF'],	# private key file
						'SF'	: config[sensor]['SF']		# shared folder
					}
					# basic check:
					assert all(v is not None for v in data.values())
					# strong names check (sections need to be in order):
					assert data['NAME'] == names_test.pop(0)['NAME']
					# IPs check:
					from ipaddress import ip_address
					assert ip_address(data['IP'])
					# paths check (pathvalidate)
	 				# ... PKF
	  				# ... SF

					sensor_data.append(data)

			return (True,sensor_data)

		except:
			# same shape dict, only name keys
			return (False,self.sensor_names)

	def configure_basic(self):
		self.title("PROGNOZA")
		self.resizable(0,0)

		self.configure(
			highlightcolor="SystemWindowText"
		)

	def refresh_all_lists(self):

		self.frm_temp.refresh_list(
			self.frm_temp.data_column
		)
		self.frm_vlaga.refresh_list(
			self.frm_vlaga.data_column
		)
		self.frm_tlak.refresh_list(
			self.frm_tlak.data_column
		)

	def save(self):

		# COLLECT
		data = {
			'temp_unutar'	: self.frm_temp.unos_unutar.get(),
			'temp_izvan'	: self.frm_temp.unos_izvan.get(),
			'vlaga_unutar'	: self.frm_vlaga.unos_unutar.get(),
			'vlaga_izvan'	: self.frm_vlaga.unos_izvan.get(),
			'tlak_unutar'	: self.frm_tlak.unos_unutar.get(),
			'tlak_izvan'	: self.frm_tlak.unos_izvan.get(),
			'date'			: dt.now().strftime("%Y-%m-%d"),
			'time'			: dt.now().strftime("%H:%M:%S")
		}

		# APPEND
		try:
			assert all([v for v in data.values()])
		except:
			messagebox.showerror(
				"Greška pri upisu","Neispravne vrijednosti. Upis nije moguć."
				)
			return
		else:
			try:
				self.DB_link.insert_data(data)
			except Exception as e:
				raise DBWriteError()

		# refresh all lists
		self.refresh_all_lists()

		# disable save button > no (continuous reading!)
		# self.btn_spremi.configure(state = 'disabled')
		# enable delete button
		self.btn_izbrisi.configure(state = 'normal')
		# start button unchanged
		#
		# stop button unchanged
		#

	def delete(self):
		# only 1 table in DB so it doesn't matter
		# no choosing, might as well pick from inst
		self.DB_link.delete_data_all(
			self.DB_link.table_name
		)

		# refresh all lists
		self.refresh_all_lists()

		# save button unchanged
		#
		# disable delete button
		self.btn_izbrisi.configure(state = 'disabled')
		# start button unchanged
		#
		# stop button unchanged
		#

	# <SENSOR PROBE>
			
	def probe_load_worker(self):
		# worker thread stops animation on sensor load
		while True:
			# check every half-second:
			self.tksleep(0.5)
			# whether sensors established:
			if self.SM_link is not None:
				# stop animation:
				self.pb.stop()
				# detach progress bar:
				self.detach_progressbar()
				# attach status label:
				self.attach_sensor_label()
				# update start button text
				self.btn_pokreni.configure(					
					text='Pokreni', state='normal')
				# probe loaded, set loader to none
				self.probe_loader = None
				# exit loop, end the thread
				break

	def probe_load(self):
		# on first start, try to load the sensors

		# attach progress bar:
		self.attach_progressbar()
		# start animation:
		self.pb.start()
		# create the loading probe
		self.probe_loader = th.Thread(target=self.probe_load_worker)
		# start the loading probe
		self.probe_loader.start()
		# start the linking probe
		self.probe_create_link()

	def probe_link_worker(self):
		data_loaded, sensor_data = self.load_sensor_data()
		self.SM_link = SensorManager(data_loaded, sensor_data)

	def probe_create_link(self):
		try:
			# generate/connect to sensors, break on error
			self.probe = th.Thread(target=self.probe_link_worker).start()			
		except Exception as e:
			# kill all new threads
			self._probe_kill.set()
			# raise error
			raise SensorConnectError()
	
	def probe_disable_link(self):
		#self.SM_link.close_connections()
		self.SM_link = None

	def probe_start(self):
		# if sensors not yet established, start load procedure:
		if self.SM_link == None:
			self.probe_load()
			self.btn_pokreni.configure(state='disabled')
		else:
			# start reading sensor data
			self.probe_loader = None
			self.probe_read()

			# enable save button
			self.btn_spremi.configure(state = 'normal')
			# delete button unchanged
			#
			# disable start button
			self.btn_pokreni.configure(state = 'disabled')
			# enable stop button
			self.btn_zaustavi.configure(state = 'normal')

	def probe_stop_worker(self):
		from re import findall as re_findall
		while True:
			# check every half-second:
			self.tksleep(0.5)
			for t in th.enumerate()[1:]:
				# exclude main thread (0 in enumerate)
				# wait for all read workers to finish
				t_test = re_findall(r'\(.*?\)',t.name)
				if t_test == ['(probe_read_worker)']:
					t.join()

			# safe to close RPi conns:
			self.SM_link.close_connections()
			# unlink Sensor Manager:
			self.probe_disable_link()
			# prepare for new probe creation:
			self._probe_kill.clear()

			# stop animation:
			self.pb.stop()
			# detach progress bar:
			self.detach_progressbar()	
			# clear all readings:
			self.clear_reading()

			# exit loop, end thread:
			break

	def probe_stop(self):
	
		# detach status label:
		self.detach_sensor_label()
		# attach progress bar:
		self.attach_progressbar()
		# start animation:
		self.pb.start()

		# stop new probe threads:
		self._probe_kill.set()
		# stop the monitoring process:
		self.after_cancel(self.probe)
		# start thread shutdown monitor
		self.probe = th.Thread(target=self.probe_stop_worker).start()	
		
		# set start button to "create conn" mode
		self.btn_pokreni.configure(text='Otvori')

		# disable save button
		self.btn_spremi.configure(state = 'disabled')
		# delete button unchanged
		#
		# enable start button
		self.btn_pokreni.configure(state = 'normal')
		# disable stop button
		self.btn_zaustavi.configure(state = 'disabled')

	def probe_killed(self):
		return self._probe_kill.is_set()

	def probe_read_worker(self):
		# load sensor data into labels
		self.show_reading()
		# reset the monitoring probe
		self.probe_loader = None

	def probe_read(self):
		# if stop signal don't create new threads:
		if self.probe_killed():
			return
		# don't crowd probes, if active no need for new ones
		if self.probe_loader is None:
			# prepare the new monitoring probe
			self.probe_loader = th.Thread(target=self.probe_read_worker)
			# start the monitoring probe:
			self.probe_loader.start()

		# take new readings every second
		self.probe = self.after(1000,self.probe_read)

	# </SENSOR PROBE>

	def show_reading(self):

		self.frm_temp.unos_unutar.set(self.SM_link.RPis["unutar"].get_data('temp'))
		self.frm_temp.unos_izvan.set(self.SM_link.RPis["izvan"].get_data('temp'))

		self.frm_vlaga.unos_unutar.set(self.SM_link.RPis["unutar"].get_data('vlaga'))
		self.frm_vlaga.unos_izvan.set(self.SM_link.RPis["izvan"].get_data('vlaga'))

		self.frm_tlak.unos_unutar.set(self.SM_link.RPis["unutar"].get_data('tlak'))
		self.frm_tlak.unos_izvan.set(self.SM_link.RPis["izvan"].get_data('tlak'))

	def clear_reading(self):

		self.frm_temp.unos_unutar.set("")
		self.frm_temp.unos_izvan.set("")

		self.frm_vlaga.unos_unutar.set("")
		self.frm_vlaga.unos_izvan.set("")

		self.frm_tlak.unos_unutar.set("")
		self.frm_tlak.unos_izvan.set("")

	def attach_frames(self):
		self.geometry("430x680")

		self.frm_postaja = frmPostaja(self)
		self.frm_postaja.place(x=15, y=10, height=85, width=400)
		self.frm_temp = frmTemp(self)
		self.frm_temp.place(x=15, y=100, height=170, width=400)
		self.frm_vlaga = frmVlaga(self)
		self.frm_vlaga.place(x=15, y=275, height=170, width=400)
		self.frm_tlak = frmTlak(self)
		self.frm_tlak.place(x=15, y=450, height=170, width=400)

	def attach_widgets(self):

		self.btn_spremi = ttk.Button(self)
		self.btn_spremi.place(x=15, y=635, height=30, width=75, bordermode='ignore')
		self.btn_spremi.configure(
			text='Spremi',
			state='disabled',
			style='btn_general.TButton',
			command=self.save)

		self.btn_izbrisi = ttk.Button(self)
		self.btn_izbrisi.place(x=100, y=635, height=30, width=75, bordermode='ignore')
		self.btn_izbrisi.configure(
			text='Izbrisi',
			state=('normal' if self.DB_link.select_data('temp') else 'disabled'),
			style='btn_general.TButton',
			command=self.delete)

		self.btn_pokreni = ttk.Button(self)
		self.btn_pokreni.place(x=255, y=635, height=30, width=75, bordermode='ignore')
		self.btn_pokreni.configure(
			text='Otvori',
			state='normal',
			style='btn_general.TButton',
			command=self.probe_start)

		self.btn_zaustavi = ttk.Button(self)
		self.btn_zaustavi.place(x=340, y=635, height=30, width=75, bordermode='ignore')
		self.btn_zaustavi.configure(
			text='Zaustavi',
			state='disabled',
			style='btn_general.TButton',
			command=self.probe_stop)

	def attach_sensor_label(self):
		if self.SM_link:
			# collect loaded sensor type initials into a string
			sensor_types = f"< {' | '.join([x.type[0] for x in self.SM_link.RPis.values()])} >"

			self.lbl_sensor = ttk.Label(self,text=sensor_types,style='lbl_sensor.TLabel')
			self.lbl_sensor.place(x=185, y=635, height=30, width=60, bordermode='ignore')
		else:
			raise SensorConnectError

	def detach_sensor_label(self):
		if self.lbl_sensor and self.lbl_sensor.winfo_exists():
			# if the label exists, destroy it:
			self.lbl_sensor.destroy()
			self.lbl_sensor = None

	def attach_progressbar(self):
		self.pb = ttk.Progressbar(
			self,orient='horizontal',mode='indeterminate',length=60
			)
		self.pb.place(x=215,y=650,anchor='center')

	def detach_progressbar(self):
		self.pb.destroy()
		self.pb = None

	def style_config(self):
		self.style = ttk.Style(self)
		# self.style.theme_use('xpnative')
		self.style.configure(
			'.', font = 'TkDefaultFont'
		)
		self.style.configure(
			"frm.TLabelframe",
			relief='flat'
		)
		self.style.configure(
			'lbl_ugoda.TLabel',
			background='white',
			borderwidth=1,
			relief="solid",
			font=('Segoe UI',12),
			anchor='center',
			justify='center',
			compound='image'
		)
		self.style.configure(
			'btn_general.TButton',
			relief='groove',
			compound='center',
			font=('Segoe UI',9),
		)
		self.style.configure(
			'btn_get.TButton',
			relief='groove',
			compound='center',
			font=('Segoe UI',9),
		)
		self.style.configure(
			'lbl_naslov.TLabel',
			font=('Segoe UI',9),
			relief="flat",
			anchor='w',
			justify='left',
			compound='left'
		)
		self.style.configure(
			'lbl_sensor.TLabel',
			foreground="#808080",
			font=('Segoe UI',9),
			relief="flat",
			anchor='center',
			justify='center',
			compound='center'
		)
		self.style.configure(
			'lbl_vrijednost.TLabel',
			font=('Segoe UI',18),
			relief="flat",
			anchor='w',
			justify='left',
			compound='left'
		)

	def __enter(self):
		return self

	def __exit__(self,exc_type=None,exc_value=None,exc_traceback=None):
		if self.probe:
			self.probe_stop()

	def tksleep(self,t):
		# emulate time.sleep(seconds)
		var = tk.IntVar(self)
		self.after(int(t*1000), var.set, 1)
		self.wait_variable(var)

# </WIDGETS> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# </INTERFACE> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# <DATABASE> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# <DB IMPORTS> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

try:
	import sqlalchemy as sa
	from sqlalchemy import	create_engine,	\
							MetaData,		\
							select,			\
							insert,			\
							update,			\
							delete,			\
							Table,			\
							Column,			\
							String,			\
							Integer,		\
							Float

	from sqlalchemy_utils import	database_exists,	\
									create_database

except Exception as e:
	raise DependenciesError()

# </DB IMPORTS> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# <DB MGMT> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# allow only one instance of core classes (engine,meta,session,...)
class singleton_class:
	def __init__(self,aClass):
		self.aClass = aClass
		self.instance = None
	def __call__(self,*args,**kwargs):
		if self.instance == None:
			self.instance = self.aClass(*args,**kwargs)
		return self.instance
	def __getattr__(self,attrname):
		return getattr(self.aClass,attrname)

class DB():

	class ConnParams(Enum):
		ECHO = False
		DIALECT = "sqlite"
		DBAPI = "pysqlite"
		DATABASE = "meteo.db"

	@staticmethod
	def create_conn_string():
		return	f"{DB.ConnParams.DIALECT.value}"	+ \
				f"+{DB.ConnParams.DBAPI.value}:"	+ \
				f"///{sys_path[0]}"+"\\"			+ \
				f"{DB.ConnParams.DATABASE.value}"

	def __init__(self):
		self.engine = create_engine(
			DB.create_conn_string(),
			echo=DB.ConnParams.ECHO.value)
		self.meta = MetaData()

		if not database_exists(self.engine.url):
			create_database(self.engine.url)
		self.meta.reflect(bind=self.engine)
		self.tables = self.meta.tables

		self.table_name = 'thp_data'

		tbl = self.tables.get(self.table_name)
		if tbl is None:
			self.create_table()
			self.populate_data()

	def create_table(self):
		Table(
			self.table_name,
			self.meta,
			Column('id',Integer,primary_key=True),
			Column('temp_unutar',Float),
			Column('temp_izvan',Float),
			Column('vlaga_unutar',Float),
			Column('vlaga_izvan',Float),
			Column('tlak_unutar',Float),
			Column('tlak_izvan',Float),
			Column('date',String),
			Column('time',String)
		)
		self.meta.create_all(bind=self.engine)

	def delete_data_all(self,table_name):
		tbl = self.tables[table_name]
		stmt = delete(tbl)
		with self.engine.begin() as conn:
			conn.execute(stmt)

	def populate_data(self):

		with self.engine.begin() as conn:
			conn.execute(insert(self.tables[self.table_name]),
				[
					{	"temp_unutar":20.0,"vlaga_unutar":50.0,"tlak_unutar":1020.0,
						"temp_izvan":16.0,"vlaga_izvan":40.0,"tlak_izvan":1010.0,
	  					"date":"2024-03-20","time":"10:00:00"},

					{	"temp_unutar":21.0,"vlaga_unutar":51.0,"tlak_unutar":1021.0,
						"temp_izvan":17.0,"vlaga_izvan":41.0,"tlak_izvan":1011.0,
	  					"date":"2024-03-21","time":"11:00:00"},

					{	"temp_unutar":22.0,"vlaga_unutar":52.0,"tlak_unutar":1022.0,
						"temp_izvan":18.0,"vlaga_izvan":42.0,"tlak_izvan":1012.0,
	  					"date":"2024-03-22","time":"12:00:00"},

					{	"temp_unutar":23.0,"vlaga_unutar":53.0,"tlak_unutar":1023.0,
						"temp_izvan":19.0,"vlaga_izvan":43.0,"tlak_izvan":1013.0,
	  					"date":"2024-03-23","time":"13:00:00"},

					{	"temp_unutar":24.0,"vlaga_unutar":54.0,"tlak_unutar":1024.0,
						"temp_izvan":20.0,"vlaga_izvan":44.0,"tlak_izvan":1014.0,
	  					"date":"2024-03-24","time":"14:00:00"},
				]
			)

	def _display_data(self):		# internal, for testing
		for table_name,table_object in self.tables.items():
			print(f"\n> table: {table_name}")
			with self.engine.connect() as conn:
				for row in conn.execute(select(table_object)):
					print(row)

	def _check_id(self,id):			# internal, for testing
		tbl = self.tables[self.table_name]

		condition_id = (tbl.c.id == id)
		stmt = select(tbl).where(condition_id)

		with self.engine.connect() as conn:
			result = conn.execute(stmt)

		result = [row._asdict() for row in result]
		return result[0] if result else None

	def select_data(self,data_type):
		tbl = self.tables[self.table_name]

		if data_type not in ['temp','vlaga','tlak']:
			raise ValueError("Unknown data type!")

		# both sensors baked into data selection
		# if needed separately, pass sensor as arg
		stmt = select(
			(tbl.columns[f"{data_type}_unutar"]),
			(tbl.columns[f"{data_type}_izvan"]),
			(tbl.c.date),
			(tbl.c.time),
			)
		with self.engine.connect() as conn:
			result = conn.execute(stmt)

		# # # !
		rl = [f"{x[0]:^4} | {x[1]:^4} : {x[2]} {x[3]}" for x in result]
		return rl

	def insert_data(self,data):
		tbl = self.tables[self.table_name]
		stmt = insert(tbl)
		with self.engine.begin() as conn:
			conn.execute(stmt,data)

# </DB MGMT>  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# </DATABASE> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# <APPLICATION> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

class App():

	def __init__(self):

		try:
			# generate/connect to DB, break on error
			self.database = DB()
		except Exception as e:
			raise DBConnectError()
		try:
			# generate tk interface, break on error
			self.interface_root = tkRoot(self.database)
		except Exception as e:
			raise IFOpenError()

	def run(self):
		self.interface_root.mainloop()

def main():
	try:
		App().run()
	except DBConnectError as dbe:
		print(dbe)
	except IFOpenError as ioe:
		print(ioe)
	except SensorConnectError as sce:
		print(sce)
	except Exception as e:
		print(f"Error! {e}")

if __name__ == '__main__':
		main()

# </APPLICATION> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -