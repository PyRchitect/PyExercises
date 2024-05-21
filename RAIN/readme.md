# Rain

<h3>General notes:</h3>

Use pulse streams to emit traffic to a device. Colored rain animation on RPi Sense Hat is used as a template to explore the concept of relaying data streams to remote services where one device sends a stream and the other is responsible for processing.

<h3>Notes about subjects explored:</h3>

+ <h4> pulse and signal generation</h4>

	> Signal packets are created using a customizable set of rules (density, velocity, delay) and sent to a display device.

+ <h4> separating signals from display</h4>

	> Signals are basically vectors in [bitvectors x colors] product space so the display is complety dependant on the display device itself