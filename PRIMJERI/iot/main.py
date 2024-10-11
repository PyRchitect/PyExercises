from iot_package.sensors import Sensors
import simulator.simulator
import time

# Za ovaj zadatak koristite Simulator koji
# se nalazi u mapi "simulator" - simulator.py.
# Također, kako bi čitali podatke sa senzora potrebno je
# koristiti klasu `Sensors` koja je već uključena u ovoj datoteci.

# Napišite skriptu koja svake sekunde (1s) sa senzora pročita
# temperaturu.
# Na temelju pročitanih vrijednosti skripta treba na
# zaslon (display) ispisati pripadajuću poruku.
# Idealna temperatura je u rasponu od 18-24.
# Ako je temperatura idealnom rasponu treba na zaslon ispisati:
#   - "IDEALNO".
# Ako je temperatura izvan raspona treba ispisati:
#   - "HLADNO" ako je ispod ili "VRUCE" ako je iznad.

sensors = Sensors()

while True:
	# TODO: Potrebno je implementirati zadano ponasanje
	
	t = sensors.get_temperature()

	if t<18:
		response = 'HLADNO'
	elif (t>=18 and t<=24):
		response = 'IDEALNO'
	else:
		response = 'VRUĆE'
	
	sensors.show_message(response)
	
	time.sleep(1)
