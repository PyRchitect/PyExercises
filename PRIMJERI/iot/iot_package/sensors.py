from os import path as os_path
from sys import path as sys_path

class Sensors:
	"""
	The `Sensors` class provides methods to interact with sensor data
	and display messages.

	Attributes:
		path_temp (str): The file path for the temperature sensor data.
		path_humidity (str): The file path for the humidity sensor data.
		path_display (str): The file path for displaying messages on a display.

	Methods:
		get_temperature():
			Retrieve the current temperature reading
			from the temperature sensor.

		get_humidity():
			Retrieve the current humidity reading from the humidity sensor.

		show_message(message: str):
			Display a message on a display by writing
			the message to the display.

	Usage:
		# Example usage of the Sensors class:
		sensors = Sensors()
		temperature = sensors.get_temperature()
		humidity = sensors.get_humidity()
		sensors.show_message("Hello, World!")
	"""

	# CONVERT TO RELATIVE PATH:
	# path_temp = "data/temperature.txt"
	path_temp = os_path.join(sys_path[0],'data','temperature.txt')
	# path_humidity = "data/humidity.txt"
	path_humidity = os_path.join(sys_path[0],'data','humidity.txt')
	# path_display = "data/display.txt"
	path_display = os_path.join(sys_path[0],'data','display.txt')

	def get_temperature(self):
		"""
		Retrieve the current temperature reading.

		Returns:
			float: The current temperature reading.

		Example:
			sensors = Sensors()
			temperature = sensors.get_temperature()
		"""
		with open(Sensors.path_temp, 'r') as file:
			return float(file.read())

	def get_humidity(self):
		"""
		Retrieve the current humidity reading.

		Returns:
			float: The current humidity reading.

		Example:
			sensors = Sensors()
			humidity = sensors.get_humidity()
		"""
		with open(Sensors.path_humidity, 'r') as file:
			return float(file.read())

	def show_message(self, message: str):
		"""
		Display a message on a display.

		Args:
			message (str): The message to be displayed.

		Example:
			sensors = Sensors()
			sensors.show_message("Hello, World!")
		"""
		with open(Sensors.path_display, 'w') as file:
			file.write(message)
