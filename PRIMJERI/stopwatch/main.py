import tkinter as tk

# TODO: Potrebno je implementirati Start, Stop i Restart.

from stopwatch.stopwatch import StopwatchApp
class PyWatch(StopwatchApp):
	def __init__(self):
		super().__init__()
		self.start_button.configure(command=self.start_button_action)
		self.stop_button.configure(command=self.stop_button_action)
		self.restart_button.configure(command=self.restart_button_action)

	def restart_button_action(self):
		self.restart_stopwatch()
	
	def start_button_action(self):
		self.start_stopwatch()        

	def stop_button_action(self):
		self.stop_stopwatch()

def main():
	app = PyWatch()
	app.mainloop()

if __name__ == "__main__":
	main()