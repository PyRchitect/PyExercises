#!python3

from os import system as os_system,name as os_name
from time import sleep
from random import randint,sample,choices
from collections import deque
from enum import Enum

from sense_emu import SenseHat

def cls_check():
	return 'cls' if os_name =='nt' else 'clear'

class PulseStream():

	class Constants(Enum):
		BASE_MARK = "M"
		BASE_CLEAR = "X"

		DEF_DENSITY = 1
		DEF_DELAY = 1

		STREAM_RATE = 0.5

	class Objects(Enum):
		PULSE = 1
		PAUSE = 0

	def __init__(self,
			  bandwidth,
			  view_height,
			  stream_rate = None,
			  density = None,
			  delay = None):

		self.stream_rate = stream_rate or PulseStream.Constants.STREAM_RATE.value
		self.width = bandwidth
		self.density = density or PulseStream.Constants.DEF_DENSITY.value
		self.delay = delay or PulseStream.Constants.DEF_DELAY.value

		self.view = deque()
		self.height = view_height
		self.init_view()

	def create_pulse_object(self):		# API ENDPOINT
		return NotImplementedError("Pulse creation not defined!")

	def create_pause_object(self):		# API ENDPOINT
		return NotImplementedError("Pulse creation not defined!")

	def create_object(self,object_type):
		if object_type not in [t.value for t in PulseStream.Objects]:
			raise ValueError("Unknown object type")
		elif object_type == PulseStream.Objects.PULSE.value:
			return self.create_pulse_object()
		elif object_type == PulseStream.Objects.PAUSE.value:
			return self.create_pause_object()

	@staticmethod
	def clear_perimeter(vector:'list',p):
		rel = [[0,1],[-1,0,1],[-1,0]]

		if p > 0 and p < len(vector)-1:				
			d = rel[1]
		elif p == 0:
			d = rel[0]
		elif p == len(vector)-1:
			d = rel[2]

		for x in d:
			vector[p+x] = PulseStream.Constants.BASE_MARK.value
		return vector

	def generate_pulse(self):

		band_base = [PulseStream.Constants.BASE_CLEAR.value]*self.width
		band_active = [self.create_object(PulseStream.Objects.PAUSE.value)]*self.width

		for _ in range(randint(1,self.density)):

			band_available=[]
			for i,x in enumerate(band_base):
				if x == PulseStream.Constants.BASE_CLEAR.value:
					band_available.append(i)
			if not band_available: break
			position = sample(band_available,k=1)[0]

			band_active[position] = self.create_object(PulseStream.Objects.PULSE.value)

			band_base = PulseStream.clear_perimeter(band_base,position)
		
		return band_active

	def generate_pause(self):
		return [self.create_object(PulseStream.Objects.PAUSE.value)]*self.width

	def generate_signal(self):
		signal = []
		signal.append(self.generate_pulse())
		for _ in range(randint(1,self.delay)):
			signal.append(self.generate_pause())
		return signal

	def init_view(self):
		for _ in range(self.height):
			self.view.append(self.generate_pause())
	
	def render_view(self):			# API ENDPOINT
		raise NotImplementedError("Render method not defined!")
	
	def update_view(self):
		for band in self.generate_signal():
			self.view.pop()
			self.view.appendleft(band)
			sleep(self.stream_rate)
			self.render_view()
	
	def simulate(self,packets):
		self.render_view()
		for _ in range(packets):
			self.update_view()

class RPiSenseHatStream(PulseStream):

	def __init__(self,
				 stream_rate = None,
				 density = None,
				 delay = None):
		self.sense = SenseHat()
		bandwidth = 8
		view_height = 8
		super().__init__(bandwidth,
						 view_height,
						 stream_rate,
						 density,
						 delay)

	def create_pulse_object(self):	# API ENDPOINT		
		return choices(range(255),k=3)

	def create_pause_object(self):	# API ENDPOINT
		return (255,255,255)

	def render_view(self):			# API ENDPOINT
		for row in range(self.height):
			for col in range(self.width):
				self.sense.set_pixel(col,row,self.view[row][col])

def main():
	# try:
		signals = int(input("Signal packets:\t"))
		stream_rate = round(float(input("Stream rate:\t")),2)

		density = int(input("Pulse density:\t"))
		delay = int(input("Signal delay:\t"))

		# TEST - - - - - - - - - - - - - - - - - - - - - -
		# signals = 8
		# stream_rate = 0.2

		# density = 2
		# delay = 2
		# TEST - - - - - - - - - - - - - - - - - - - - - -

		# very basic test to exclude nonsense inputs
		assert (stream_rate>0 and stream_rate<2)
		for arg in (density,delay):
			assert arg in range(1,50+1)

		stream = RPiSenseHatStream(
			stream_rate,
			density,
			delay)
		
		stream.simulate(signals)
	# except:
	# 	print("Pogresan unos!")

main()

# python /media/sf_Raspberry_Pi_Shared_Folder/rolling_v6.py