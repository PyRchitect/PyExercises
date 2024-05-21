# Meteo

<h3>General notes:</h3>

Light app for weather sensor tracking. Connects to publicly available service in order to obtain weather data and to an interior and exterior RPi with Sense Hats in order to obtain local measurements. Tkinter used as GUI. Config parser used for Linux style input, can be scaled to accept data from a main home assistant type app. Data persistence made available via sqlite DB.

<h3>Notes about subjects explored:</h3>

+ <h4> connection management</h4>

	> SSH login to RPis with Sense Hats (virtualized in VM for demonstration purposes, key pairs expected to be established, shared folder expected to be set up), runs scripts on RPis in order to receive data streams. Two failover methods: if run on a RPi, connects to a local Sense Hat, if no connections available, streams random data.

+ <h4> load balancing with threading</h4>

	> Basic threading is employed and progress bars are used in order to signal the processing to the user and so the app doesn't halt due to a connection failure. Workers are used to control establishing connection, receiving data stream and closing connections.

+ <h4> database interaction</h4>

	> measurements can be saved to a simple DB and later retrieved for analysis or similar. Uses sqlite DB, can be scaled to use MySQL or similar if neccessary. DB data presented in the GUI as a chronological table, split by measurement type.

+ <h4> running scripts on a server</h4>

	> The exercise is aimed in general at exploring running procedures on remote devices and analyzing received data streams. The app establishes connection with a server-type device, checks whether a certain process is running and (re)starts it if needed. Then, it prepares for stream receiving and displays results. When closing connection, the app cleans up on the server by stopping running scripts and shutting down the service.