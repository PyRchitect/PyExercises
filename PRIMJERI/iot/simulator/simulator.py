import tkinter as tk

from os import path as os_path
from sys import path as sys_path

# CONVERT TO RELATIVE PATH:
# path_temp = "data/temperature.txt"
path_temp = os_path.join(sys_path[0],'data','temperature.txt')
# path_humidity = "data/humidity.txt"
path_humidity = os_path.join(sys_path[0],'data','humidity.txt')
# path_display = "data/display.txt"
path_display = os_path.join(sys_path[0],'data','display.txt')


def init():
    with open(path_temp, 'w') as file:
        file.write(str(temperature_scale.get()))

    with open(path_humidity, 'w') as file:
        file.write(str(humidity_scale.get()))

    with open(path_display, 'w') as file:
        file.write("DISPLAY")

    start_timer()


def update_temperature(event):
    with open(path_temp, 'w') as file:
        file.write(str(temperature_scale.get()))


def update_humidity(event):
    with open(path_humidity, 'w') as file:
        file.write(str(humidity_scale.get()))


def start_timer():
    update_lcd()
    root.after(500, start_timer)


# Function to update the LCD display with the current sensor data
def update_lcd():
    with open(path_display, 'r') as file:
        message = file.read()
        lcd_display.config(text=message)


# Create the main window
root = tk.Tk()
root.title("Sensor Simulator")
root.geometry("300x150")

# Create scales (scroll bars) for temperature and humidity
temperature_scale = tk.Scale(root, from_=-20, to=50, orient="horizontal",
                             resolution=0.1, label="Temperature (°C)")
temperature_scale.bind("<ButtonRelease-1>", update_temperature)

humidity_scale = tk.Scale(root, from_=0, to=100, orient="horizontal",
                          resolution=0.1, label="Humidity (%)")
humidity_scale.bind("<ButtonRelease-1>", update_humidity)

# Create an LCD-like label for displaying sensor data
lcd_display = tk.Label(root, text="DISPLAY",
                       font=("Arial", 16), bg="white", fg="black")

# Pack the widgets
temperature_scale.pack()
humidity_scale.pack()
lcd_display.pack()

# Initially update the sensor data
init()

# Start the GUI event loop
root.mainloop()
