import tkinter as tk
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