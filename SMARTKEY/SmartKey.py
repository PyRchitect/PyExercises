from sys import path as sys_path
from enum import Enum

import tkinter as tk
from tkinter import 	ttk,		\
						messagebox

# <EXCEPTIONS> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

class DependenciesError(Exception):
	def __str__(self):
		return 	"External dependencies:"								+ \
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

# </EXCEPTIONS> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

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

class frmGumbi(ttk.LabelFrame):

	def __init__(self,master):
		self.root = master
		super().__init__(master)

		self.configure_basic()
		self.attach_widgets()

	def configure_basic(self):
		self.configure(style='frm.TLabelframe',text='Panel s gumbima')

	def use_bell(self):
		messagebox.showinfo("Zvono aktivirano","Netko će uskoro doći i otvoriti vrata")

	def use_key(self):
		self.master.attach_PIN_frame()
		# also used as exit sequence
		# > need to reset current user
		self.root.current_user = None
		# it does not detach > reset frames
		self.root.frm_PIN = None
		self.root.frm_DB = None

	def attach_widgets(self):

		from PIL import Image,ImageTk

		bell_path = sys_path[0]+'\\'+"bell.png"
		self.img_bell = ImageTk.PhotoImage(Image.open(bell_path).resize((25,25)))

		self.btn_pozvoni = ttk.Button(self)
		self.btn_pozvoni.place(x=20, y=30, height=50, width=50, bordermode='ignore')
		self.btn_pozvoni.configure(
			style='btn_gumbi.TButton',
			image=self.img_bell,
			command=self.use_bell)

		key_path = sys_path[0]+'\\'+"key.png"
		self.img_key = ImageTk.PhotoImage(Image.open(key_path).resize((25,25)))

		self.btn_otkljucaj = ttk.Button(self)
		self.btn_otkljucaj.place(x=410, y=30, height=50, width=50, bordermode='ignore')
		self.btn_otkljucaj.configure(
			style='btn_gumbi.TButton',
			image=self.img_key,
			command=self.use_key)

class frmPIN(ttk.LabelFrame):

	class Poruke(Enum):
		START =			"UNESI ID U (####) OBLIKU"

		EXIT =			"\n"							+ \
						"\n"							+ \
						"\nZA IZLAZ UNESITE X"

		ID_SUCCESS =	"ID USPJESNO UNESEN."			+ \
						"\n"							+ \
						"\n"							+ \
						"\nUNESI PIN U (####) OBLIKU"

		ID_UNKNOWN =	"NEPOZNAT ID"					+ \
						"\n"							+ \
						"\n"							+ \
						"\nMOLIMO POKUŠAJTE PONOVO"

		ID_ADMIN =		"\n"							+ \
						"\n"							+ \
						"\nADMINISTRATORSKI ID"			+ \
						"\nMOLIMO UNESITE PIN ZA OPERACIJU"

		PIN_SUCCESS =	"PIN USPJESNO UNESEN."			+ \
						"\n"							+ \
						"\n"							+ \
						"\nDOBRODOŠLI, "

		PIN_UNKNOWN =	"POGREŠNO UNESEN PIN."			+ \
						"\n"							+ \
						"\n"							+ \
						"\nMOLIMO POKUŠAJTE PONOVO"

		PIN_ADMIN =		"\n"							+ \
						"\n"							+ \
						"\nADMINISTRATOR"

		ACTIVE_YES =	"\n"							+ \
						"\n"							+ \
						"\nKORISNIK JE AKTIVAN"

		ACTIVE_NO =		"\n"							+ \
						"\n"							+ \
						"\nULAZ NIJE DOPUŠTEN."			+ \
						"\nKORISNIK NIJE AKTIVAN."		+ \
						"\nZA AKTIVACIJU KORISNIKA"		+ \
						"\nKONTAKTIRAJTE ADMINISTRATORA"
		
		CODE_INPUT_UNAVAILABLE = "Unošenje kodova nije dopušteno dok je baza otvorena."

	class Codes(Enum):

		EDIT			= '0000'	# opens database editing frame
		RESET			= '0001'	# resets database to test values
		DELETE			= '0002'	# deletes all accounts except admin
		ACTIVATE		= '0003'	# activates all keys
		DEACTIVATE		= '0004'	# deactivates all keys

	def __init__(self,master):
		self.root = master
		super().__init__(master)
		self.configure_basic()
		self.attach_widgets()

		self.step = 0
		self.ID = None
		self.PIN = None

		self.code_dict = self.generate_code_dict()

	def configure_basic(self):
		self.configure(style='frm.TLabelframe',text='PIN panel')

	def enter_PIN(self,event:'tk.Event'):
		signal = event.widget['text']
		try:
			assert (int(signal) or signal == '0')
			# assert number signal (0==False, doesn't pass assertion)

			# check how many digits entered
			value = frmPIN.join_SVL(self.lbl_PIN_numbers)
			pos = len(value)
			# add signal to row
			self.lbl_PIN_numbers[pos].set(signal)
			if pos == 3:
				# if row full perform check
				# sleep a bit so user can see last num entered
				self.root.tksleep(0.5)

				if self.ID == None:
					# if id not entered perform first step
					self.first_step()
				elif self.PIN == None:
					# if id correct perform second step
					self.second_step()
				else:
					# if user logged in and it is an admin
					# it means a code was entered > trigger
					self.process_code()

		except:
			if signal == 'X':
				self.root.detach_PIN_frame()
				# also used as exit sequence
				# > need to reset current user
				self.root.current_user = None
			elif signal == 'C':
				# check how many digits entered
				value = frmPIN.join_SVL(self.lbl_PIN_numbers)
				pos = len(value)
				# clear last label
				if pos == 0:
					# if empty nothing to do
					return
				else:
					self.lbl_PIN_numbers[pos-1].set("")

	@staticmethod
	def join_SVL(string_var_list):
		return "".join([x.get() for x in string_var_list])

	def verify_step(self,key):
		#check_var = "".join([x.get() for x in self.lbl_PIN_numbers])
		check_var = frmPIN.join_SVL(self.lbl_PIN_numbers)

		# reset label row to empty
		[x.set("") for x in self.lbl_PIN_numbers]

		if key == "ID":
			check_var = int(check_var)
			check_function = self.root.DB_link.check_id
			check_params = (check_var,)
		elif key == "PIN":
			check_function = self.root.DB_link.check_PIN
			check_params = (self.ID,check_var)
		try:
			# catch all db exceptions as DBReadError
			try:
				check_DB = check_function(*check_params)
			except Exception as e:
				raise DBReadError()
		except DBReadError:
			messagebox.showerror("Greška pri otvaranju",DBReadError())
			return

		if check_DB:
			# set ID / PIN to correctly entered value
			self.__dict__[key] = check_var
			return self.verify_successful(check_DB,key)
		else:
			return self.verify_error(key)

	def verify_successful(self,data,key):

		if key == "ID":
			name_insert = ""
		elif key == "PIN":
			name_insert = "\n" + data["firstname"] + " " + data["surname"]

		active = int(data["active"])
		admin = int(data["admin"])

		# messages enum short name
		d = frmPIN.Poruke.__dict__

		active_insert = d["ACTIVE_YES"].value if active else d["ACTIVE_NO"].value
		if admin:
			message = 	d[key+"_SUCCESS"].value	+ \
						name_insert				+ \
						d[key+"_ADMIN"].value	+ \
						active_insert			+ \
						d["EXIT"].value
			self.lbl_PIN_text.set(message)
			return ("admin",data)
		else:
			message =	d[key+"_SUCCESS"].value	+ \
						name_insert				+ \
						active_insert			+ \
						d["EXIT"].value
			self.lbl_PIN_text.set(message)
			return ("user",data)

	def verify_error(self,key):

		# messages enum short name
		d = frmPIN.Poruke.__dict__

		message = 	d[key+"_UNKNOWN"].value		+ \
					d["EXIT"].value
		self.lbl_PIN_text.set(message)
		return ("unknown",None)

	def first_step(self):
		self.verify_step("ID")

	def second_step(self):
		(result,data) = self.verify_step("PIN")

		if result != 'unknown':

			# activate current user DB link:
			self.root.current_user = data

			if messagebox.askyesno(
				"Administracija sustava",
				"Želite li pokrenuti upravljanje podacima?"
				):
				if result == 'admin':
					mode = frmDB.Modes.MODE_ADMIN.value
				elif result == 'user':
					mode = frmDB.Modes.MODE_USER.value

				self.root.attach_DB_frame(mode,data)

	def code_edit(self):
		self.root.attach_DB_frame(
			frmDB.Modes.MODE_ADMIN.value,
			self.root.current_user
		)

	def code_reset(self):
		self.root.DB_link.delete_user_data()
		self.root.DB_link.populate_user_data()

	def code_delete(self):
		self.root.DB_link.delete_non_admin_users()

	def code_activate(self):
		self.root.DB_link.activate_all_users()

	def code_deactivate(self):
		self.root.DB_link.deactivate_all_users()

	def process_code(self):
		check_var = frmPIN.join_SVL(self.lbl_PIN_numbers)
		# reset label row to empty
		[x.set("") for x in self.lbl_PIN_numbers]
		if not (self.root.frm_DB and check_var!=frmPIN.Codes.EDIT.value):
			# cannot process codes with DB data visible, except opening DB edit
			self.code_dict[check_var]()
		else:
			messagebox.showinfo("Greska pri upisu",frmPIN.Poruke.CODE_INPUT_UNAVAILABLE.value)

	def generate_code_dict(self):
		c = frmPIN.Codes

		code_dict = {
			c.EDIT.value		:	self.code_edit,
			c.RESET.value		:	self.code_reset,
			c.DELETE.value		:	self.code_delete,
			c.ACTIVATE.value	:	self.code_activate,
			c.DEACTIVATE.value	:	self.code_deactivate
		}
		return code_dict


	def attach_widgets(self):

		self.lbl_PIN_numbers = []
		for i in range(4):
			self.lbl_PIN_numbers.append(tk.StringVar())
			lbl_PIN = ttk.Label(self)
			lbl_PIN.place(x=20+i*47,y=30,height=39,width=39,bordermode='ignore')
			lbl_PIN.configure(
				style='lbl_PIN.TLabel',
				textvariable=self.lbl_PIN_numbers[i]
			)

		t = [
			["1","2","3"],
			["4","5","6"],
			["7","8","9"],
			["X","0","C"]
			]
		for i in range(4):
			for j in range(3):
				button = ttk.Button(self)
				button.place(x=(20+j*65),y=(95+i*65), height=50, width=50, bordermode='ignore')
				button.configure(
					style='btn_PIN.TButton',
					text=t[i][j]
				)
				button.bind('<Button>',self.enter_PIN)

		self.lbl_PIN_text = tk.StringVar(value=frmPIN.Poruke.START.value)
		lbl_PIN_poruke = ttk.Label(self)
		lbl_PIN_poruke.place(x=220, y=30, height=310, width=240,bordermode='ignore')
		lbl_PIN_poruke.configure(
			style='lbl_PIN_poruke.TLabel',
			textvariable=self.lbl_PIN_text
		)

class frmDB(ttk.LabelFrame):

	class Poruke(Enum):

		UPDATE_ERROR = 	"Sva polja moraju biti popunjena!"		+ \
						"\n> Ime: tekst, prvo veliko slovo"		+ \
						"\n> Prezime: tekst, prvo veliko slovo"	+ \
						"\n> PIN: 4 znamenke"

		NEW_USER_ON =	"Nakon ispunjavanja polja potvrdom na tipku"				+ \
						"\n'Spremi' generira se novi korisnik u bazi i novi id."	+ \
						"\n"														+ \
						"\nZa povratak na uređivanje postojecih korisnika"			+ \
						"\nodaberite nekog od korisnika s liste."

		DELETE_ADMIN_ERROR = "Nije dopušteno brisati admin account!"



	class Modes(Enum):
		MODE_USER = 'user'
		MODE_ADMIN = 'admin'

	def __init__(self,master):

		self.root = master
		super().__init__(master)

		# attach on config
		self.unos_ime = tk.StringVar()
		self.unos_prezime = tk.StringVar()
		self.unos_PIN = tk.StringVar()
		self.unos_ID = tk.StringVar()
		self.attach_widgets()

	# - - - - - - - - - - - - - - - - - - - - - - - - - - -
	# functions different for each mode
	# to be implemented in child classes
	# primitive abstractmethod style coding

	def configure_basic(self):
		raise NotImplementedError("Must define basic configuration!")

	def save(self):
		raise NotImplementedError("Must define save button function!")

	def abort(self):
		raise NotImplementedError("Must define abort button function!")

	def delete(self):
		raise NotImplementedError("Must define delete button function!")

	# - - - - - - - - - - - - - - - - - - - - - - - - - - -

	def attach_widgets(self):

		# LABELS

		lbl_ime = ttk.Label(self,text='Ime:',style='lbl_unos.TLabel')
		lbl_ime.place(x=220, y=30, height=27, width=60, bordermode='ignore')

		lbl_prezime = ttk.Label(self,text='Prezime:',style='lbl_unos.TLabel')
		lbl_prezime.place(x=220, y=60, height=27, width=60, bordermode='ignore')

		lbl_PIN = ttk.Label(self,text='PIN:',style='lbl_unos.TLabel')
		lbl_PIN.place(x=220, y=90, height=27, width=60, bordermode='ignore')

		lbl_ID = ttk.Label(self,text='ID:',style='lbl_unos.TLabel')
		lbl_ID.place(x=220, y=150, height=27, width=60, bordermode='ignore')

		# ENTRIES

		ent_ime = ttk.Entry(self,style='ent_unos.TEntry',textvariable=self.unos_ime)
		ent_ime.place(x=300, y=30, height=25, width=160, bordermode='ignore')

		ent_prezime = ttk.Entry(self,style='ent_unos.TEntry',textvariable=self.unos_prezime)
		ent_prezime.place(x=300, y=60, height=25, width=160, bordermode='ignore')

		ent_PIN = ttk.Entry(self,style='ent_unos.TEntry',textvariable=self.unos_PIN)
		ent_PIN.place(x=300, y=90, height=25, width=160, bordermode='ignore')

		# ID VALUE LABEL

		lbl_ID_value = ttk.Label(self,textvariable=self.unos_ID,style='lbl_unos.TLabel')
		lbl_ID_value.place(x=300, y=150, height=27, width=65, bordermode='ignore')

		# BUTTONS

		btn_spremi = ttk.Button(self)
		btn_spremi.place(x=220, y=200, height=30, width=70, bordermode='ignore')
		btn_spremi.configure(
			text='Spremi',style='btn_unos.TButton',command=self.save
		)

		btn_odustani = ttk.Button(self)
		btn_odustani.place(x=305, y=200, height=30, width=70, bordermode='ignore')
		btn_odustani.configure(
			text='Odustani',style='btn_unos.TButton',command=self.abort
		)

		btn_izbrisi = ttk.Button(self)
		btn_izbrisi.place(x=390, y=200, height=30, width=70, bordermode='ignore')
		btn_izbrisi.configure(
			text='Izbrisi',style='btn_unos.TButton',command=self.delete
		)

class frmDB_user(frmDB):

	def __init__(self,master):
		# vars controlled only by user:
		#

		super().__init__(master)

		self.configure_basic()

	def configure_basic(self):
		self.configure(
			style='frm.TLabelframe',
			text="Upravljanje podacima korisnika")
		# retrieve data from self id
		cu = self.root.current_user
		self.unos_ime.set(cu["firstname"])
		self.unos_prezime.set(cu["surname"])
		self.unos_PIN.set(cu["PIN"])
		self.unos_ID.set(str(cu["id"]).zfill(4))

	def save(self):
		id = self.unos_ID.get()
		data = {
			"firstname" : self.unos_ime.get(),
			"surname" : self.unos_prezime.get(),
			"PIN" : self.unos_PIN.get()
		}
		try:
			assert all([v for v in data.values()])

			assert data["firstname"].istitle()
			assert data["surname"].istitle()

			assert data["PIN"].isnumeric()
			assert len(data["PIN"]) == 4

			try:
				self.root.DB_link.update_user(id,data)
			except Exception as e:
				raise DBWriteError()

		except DBWriteError:
			# error while trying to write to database (ex. DB locked, etc.)
			messagebox.showerror("Greška pri upisu",DBWriteError())
			return

		except:
			# input error (fields have to conform to certain rules)
			messagebox.showerror("Greška pri upisu",frmDB.Poruke.UPDATE_ERROR.value)
			return

	def abort(self):
		self.root.detach_PIN_frame()
		# also used as exit sequence
		# > need to reset current user
		self.root.current_user = None


	def delete(self):
		self.unos_ime.set("")
		self.unos_prezime.set("")
		self.unos_PIN.set("")

class frmDB_admin(frmDB):

	def __init__(self,master):
		# vars controlled only by admin:
		self.aktivan = tk.IntVar()
		# ref listbox values variable
		self.unos_korisnici = tk.Variable()
		# ref listbox for easier refresh control
		self.box_korisnici = None
		# on abort: new user creation mode
		self.new_user = False

		super().__init__(master)

		self.attach_admin_widgets()

		self.configure_basic()

	def clear_entries(self):
		self.unos_ime.set("")
		self.unos_prezime.set("")
		self.unos_PIN.set("")
		self.aktivan.set(0)
		self.unos_ID.set("")

	def refresh_list(self):
		try:
			# catch all db exceptions as DBReadError
			try:
				users = self.root.DB_link.select_user_names()
			except Exception as e:
				raise DBWriteError()
		except DBReadError:
			messagebox.showerror("Greška pri otvaranju",DBReadError())
			return

		self.unos_korisnici.set(users)

	def configure_basic(self):
		self.configure(
			style='frm.TLabelframe',
			text="Upravljanje podacima")
		# retrieve data from self (admin) id
		cu = self.root.current_user
		self.unos_ime.set(cu["firstname"])
		self.unos_prezime.set(cu["surname"])
		self.unos_PIN.set(cu["PIN"])
		self.aktivan.set(cu["active"])
		self.unos_ID.set(str(cu["id"]).zfill(4))
		# initialize users list in listbox
		self.refresh_list()

	def save(self):
		id = self.unos_ID.get()
		data = {
			"firstname" : self.unos_ime.get(),
			"surname" : self.unos_prezime.get(),
			"PIN" : self.unos_PIN.get()
		}
		try:
			assert all([v for v in data.values()])

			assert data["firstname"].istitle()
			assert data["surname"].istitle()

			assert data["PIN"].isnumeric()
			assert len(data["PIN"]) == 4

		except:
			# input error (fields have to conform to certain rules)
			messagebox.showerror("Greška pri upisu",frmDB.Poruke.UPDATE_ERROR.value)
			return

		# append "active" value after input tests, no need to test
		data["active"] = self.aktivan.get()

		# new users can never be admin > possible future implementation
		# TODO: add admin chk_box in form, get value into data dict, etc.
		data["admin"] = 0

		try:
			if not self.new_user:
				# update user by id
				try:
					self.root.DB_link.update_user(id,data)
				except Exception as e:
					raise DBWriteError()
			else:
				# insert new user
				try:
					self.root.DB_link.insert_user(data)
				except Exception as e:
					raise DBWriteError()

		except DBWriteError:
			# error while trying to write to database (ex. DB locked, etc.)
			messagebox.showerror("Greška pri upisu",DBWriteError())

		else:
			self.new_user = False
			self.refresh_list()

	def abort(self):
		self.unos_ime.set("")
		self.unos_prezime.set("")
		self.unos_PIN.set("")
		self.aktivan.set(0)
		self.unos_ID.set("")

		# deselect everything in list
		self.box_korisnici.select_clear(0,tk.END)

		messagebox.showinfo("Mod: novi korisnik",frmDB.Poruke.NEW_USER_ON.value)

		self.new_user = True

	def delete(self):
		id = self.unos_ID.get()
		try:
			# catch all db exceptions as DBReadError
			try:
				check_DB = self.root.DB_link.check_id(id)
			except Exception as e:
				raise DBReadError()
		except DBReadError:
			messagebox.showerror("Greška pri otvaranju",DBReadError())
			return

		if not check_DB:
			return

		if check_DB['admin']:
			messagebox.showerror("Greška pri upisu",frmDB.Poruke.DELETE_ADMIN_ERROR.value)
			return

		# if not admin procede to delete user by id
		try:
			# catch all db exceptions as DBWriteError
			try:
				self.root.DB_link.delete_user(id)
			except Exception as e:
				raise DBWriteError()

		except Exception as e:
			# error while trying to write to database (ex. DB locked, etc.)
			messagebox.showerror("Greška pri upisu",DBWriteError())
			return

		else:
			self.new_user = False
			self.refresh_list()
			# deselect everything in list
			self.box_korisnici.select_clear(0,tk.END)
			self.clear_entries()

	def box_select(self,event:'tk.Event'):
		if not type(event.widget) == ScrolledListBox:
			return

		(list_id,) = event.widget.curselection()

		user = event.widget.get(list_id)
		user_id = int(user.split(" : ")[0])
		try:
			# catch all db exceptions as DBReadError
			try:
				user_data = self.root.DB_link.check_id(user_id)
			except Exception as e:
				raise DBReadError()
		except DBReadError:
			messagebox.showerror("Greška pri otvaranju",DBReadError())
			return

		self.unos_ime.set(user_data["firstname"])
		self.unos_prezime.set(user_data["surname"])
		self.unos_PIN.set(user_data["PIN"])
		self.aktivan.set(user_data["active"])
		self.unos_ID.set(str(user_data["id"]).zfill(4))

		# reset new user mode to False (update mode)
		self.new_user = False

	def attach_admin_widgets(self):

		# CHECKBOX (ONLY ADMIN MODE)

		lbl_aktivan = ttk.Label(self,text='Aktivan:',style='lbl_unos.TLabel')
		lbl_aktivan.place(x=220, y=120, height=27, width=60, bordermode='ignore')

		chk_aktivan = ttk.Checkbutton(self,style='aktivan.TCheckbutton',variable=self.aktivan)
		chk_aktivan.place(x=300, y=120, width=65, height=29, bordermode='ignore')

		# SCROLLBOX (ONLY ADMIN MODE)

		self.box_korisnici = ScrolledListBox(self)
		self.box_korisnici.place(x=20, y=30, height=200, width=180, bordermode='ignore')
		# custom element containing scroll and list, Listbox NOT ttk
		# easier to configure the widget here (only one element in app)
		# than to define for it a custom ttk class with style specs
		self.box_korisnici.configure(
			listvariable=self.unos_korisnici,
			selectmode=tk.BROWSE,
			background="white",
			disabledforeground="#b4b4b4",
			font=('Segoe UI',9),
			foreground="black",
			highlightcolor="#d9d9d9",
			selectbackground="#d9d9d9",
			selectforeground="black",
			relief="solid",
			cursor="xterm",
		)
		self.box_korisnici.bind("<<ListboxSelect>>",self.box_select)

class tkRoot(tk.Tk):

	def __init__(self,DB_link):
		self.DB_link = DB_link

		# receives DB row on registration
		self.current_user = None

		super().__init__()
		self.configure_basic()
		self.style = self.style_config()

		self.attach_default_frame()
		self.frm_PIN = None
		self.frm_DB = None

	def configure_basic(self):
		self.title("SmartKey")
		self.resizable(0,0)

		self.configure(
			highlightcolor="SystemWindowText"
		)

	def attach_default_frame(self):
		self.geometry("510x120")
		self.frm_gumbi = frmGumbi(self)
		self.frm_gumbi.place(x=15, y=10, height=100, width=480)

	def attach_PIN_frame(self):
		self.geometry("510x500")
		self.frm_PIN = frmPIN(self)
		self.frm_PIN.place(x=15, y=125, height=360, width=480)

	def detach_PIN_frame(self):
		if self.frm_DB and self.frm_DB.winfo_exists():
			self.detach_DB_frame()
		if self.frm_PIN and self.frm_PIN.winfo_exists():
			self.frm_PIN.destroy()
			self.frm_PIN = None
		self.geometry("510x120")

	def attach_DB_frame(self,mode,data):
		if mode not in [x.value for x in frmDB.Modes]:
			raise ValueError("Nepoznat mod korištenja!")

		# expand form, insert frame:
		self.geometry("510x760")
		if mode == frmDB.Modes.MODE_USER.value:
			self.frm_DB = frmDB_user(self)
		elif mode == frmDB.Modes.MODE_ADMIN.value:
			self.frm_DB = frmDB_admin(self)

		self.frm_DB.place(x=15, y=500, height=245, width=480)

	def detach_DB_frame(self):
		if self.frm_DB and self.frm_DB.winfo_exists():
			self.frm_DB.destroy()
			self.frm_DB = None
		self.geometry("510x500")

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
			"btn_gumbi.TButton",
			relief='groove',
			compound='center',
			font=('Segoe UI',12),
		)
		self.style.configure(
			'lbl_PIN.TLabel',
			background='white',
			relief="solid",
			font=('Segoe UI',12),
			anchor='center',
			justify='center',
			compound='center'
		)
		self.style.configure(
			'btn_PIN.TButton',
			relief='groove',
			compound='center',
			font=('Segoe UI',12),
		)
		self.style.configure(
			'lbl_PIN_poruke.TLabel',
			background='white',
			relief="solid",
			font=('Segoe UI',9),
			padding=(2,2,2,2),
			anchor='nw',
			justify='left',
			compound='left'
		)
		self.style.configure(
			'lbl_unos.TLabel',
			font=('Segoe UI',9),
			relief="flat",
			anchor='w',
			justify='left',
			compound='left'
		)
		self.style.configure(
			'ent_unos.TEntry',
			font=('Segoe UI',9),
			compound='left'
		)
		self.style.configure(
			'aktivan.TCheckbutton',
			compound='left'
		)
		self.style.configure(
			'btn_unos.TButton',
			relief='groove',
			font=('Segoe UI',9),
			compound='center'
		)

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
							Boolean

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
		DATABASE = "SmartKeyUsers.db"

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

		users = self.tables.get("user_account")
		if users is None:
			self.create_user_table()
			self.populate_user_data()

	def create_user_table(self):
		Table(
			"user_account",
			self.meta,
			Column('id',Integer,primary_key=True),
			Column('firstname',String),
			Column('surname',String),
			Column('PIN',String),
			Column('active',Boolean),
			Column('admin',Boolean)
		)
		self.meta.create_all(bind=self.engine)

	def delete_user_data(self):
		users = self.tables["user_account"]
		stmt = delete(users)
		with self.engine.begin() as conn:
			conn.execute(stmt)
	
	def delete_non_admin_users(self):
		users = self.tables["user_account"]
		condition = (users.c.admin==0)
		stmt = delete(users).where(condition)
		with self.engine.begin() as conn:
			conn.execute(stmt)
	
	def activate_all_users(self):
		users = self.tables["user_account"]
		condition = (users.c.admin==0)
		stmt = update(users).where(condition).values(active=1)
		with self.engine.begin() as conn:
			conn.execute(stmt)
	
	def deactivate_all_users(self):
		users = self.tables["user_account"]
		condition = (users.c.admin==0)
		stmt = update(users).where(condition).values(active=0)
		with self.engine.begin() as conn:
			conn.execute(stmt)

	def populate_user_data(self):

		with self.engine.begin() as conn:
			conn.execute(insert(self.tables["user_account"]),
				[
					{"firstname":"Mate","surname":"Matic","PIN":"0001","active":1,"admin":1},
					{"firstname":"Ivan","surname":"Ivic","PIN":"0002","active":0,"admin":1},
					{"firstname":"Ana","surname":"Anic","PIN":"0003","active":1,"admin":0},
					{"firstname":"Josip","surname":"Josipovic","PIN":"0004","active":1,"admin":0},
					{"firstname":"Marko","surname":"Markovic","PIN":"0005","active":0,"admin":0},
				]
			)

	def display_data(self):
		for table_name,table_object in self.tables.items():
			print(f"\n> table: {table_name}")
			with self.engine.connect() as conn:
				for row in conn.execute(select(table_object)):
					print(row)

	def check_id(self,id):
		users = self.tables["user_account"]

		condition_id = (users.c.id == id)
		stmt = select(users).where(condition_id)

		with self.engine.connect() as conn:
			result = conn.execute(stmt)

		result = [row._asdict() for row in result]
		return result[0] if result else None

	def check_PIN(self,id,PIN):
		users = self.tables["user_account"]

		condition_id = (users.c.id==id)
		condition_PIN = (users.c.PIN==PIN)
		stmt = select(users).where(condition_id,condition_PIN)

		with self.engine.connect() as conn:
			result = conn.execute(stmt)

		result = [row._asdict() for row in result]
		return result[0] if result else None

	def select_user_names(self):
		users = self.tables["user_account"]

		stmt = select(
			(users.c.id).label("id"),
			(users.c.firstname).label("fn"),
			(users.c.surname).label("sn")
			)
		with self.engine.connect() as conn:
			result = conn.execute(stmt)
		rl = [f"{str(x.id).zfill(4)} : {x.fn} {x.sn}" for x in result]
		return rl

	def update_user(self,id,data:"dict"):
		users = self.tables["user_account"]
		stmt = update(users).where(users.c.id == id).values(data)
		with self.engine.begin() as conn:
			conn.execute(stmt)

	def insert_user(self,data):
		users = self.tables["user_account"]
		stmt = insert(users)
		with self.engine.begin() as conn:
			conn.execute(stmt,data)

	def delete_user(self,id):
		users = self.tables["user_account"]
		stmt = delete(users).where(users.c.id == id)
		with self.engine.begin() as conn:
			conn.execute(stmt)

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
	except Exception as e:
		print(f"Error! {e}")

if __name__ == '__main__':
		main()

# </APPLICATION> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -