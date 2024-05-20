# PyExercises<br>

<h3>General notes:</h3>

<p>Collection of exercises in Python used to explore some general programming concepts.</p>

<p>The aim of the exercises was not to build a well-behaved application. Rather, a well-known procedure is used as a testing ground for implementation of a certain concept. As a result, in many ways exercises are mostly not only not in line with the procedure itself but in some cases conflict with its usual features in order to expose the concept more cleanly.</p>

<h3>Notes about procedures used:</h3>

+ <h4> Simple games (blackjack, tictactoe, minesweeper)</h4>

	> Well-known games are used to test either a dynamical concept, such as minimax algorithm in turn-based games, or a coding principle, such as engine/graphics separation. Implementation is fairly rudimentary and the game itself is not complete (some or many rules are missing) because it was coded only up to the level neccessary to expose the concept.

+ <h4> RPi Sense Emu (communication with remote device)</h4>

	> Raspberry Pi Sense Emulator is used to test various communication protocols when dealing with remote devices (SSH, HTTPS, ICMP, ...). Since RPi OS can be very quickly deployed and configured on a VM, it is used as a prototype for communicating with a Linux based server-type device. Sense emu available on the RPi is also quickly set up as a data emmiter so a simple data stream is easily obtained. The stream is then analyzed and presented in the app via comm protocol tested.

+ <h4> Admin console interfaces (general services interaction)</h4>

	> Admin consoles with well-known elements, such as various account management systems, are used as templates to explore concepts like DB interaction, customized interface coding, data cleanup, etc. Solutions are in no way complete, error-free or secure - procedures are used only because it is fairly obvious what the app needs to do so emphasis is put on the mechanics of the service.

+ <h4> Geo data statistics (data analysis and visualization)</h4>

	> Data freely available on the internet about countries and cities (GapMinder, OpenWeatherMap, ...) was used to test approaches to data analysis and graph creation. Research is in no way valid in terms of its conclusions because the data was used as-is (mostly incomplete, no cross referencing or reliability checking) and emphasis was put on the structure rather than on the results themselves.

<h3>Notes about concepts explored:</h3>

+ <h4> Coding style development</h4>

	> Attempts in writing cleaner reusable code. Concepts include OOP, role separation, IO control, failover methods, etc. Services and data structures used are often the simplest available (sqlite DB, Tkinter GUI, native Python DS libs, ...) but the code was written in such a way that it can be extended to support more complex structures without major overhaul.

+ <h4> Algorithms and data structures</h4>

	> Exploring tree-like structures, algorithms they support and the resulting complexity (binary search, merge sort, etc.). Analysis tangentially follows CLRS exercises, but puts emphasis either on the implementation on a concrete use case or on comparison between approaches based on data provided. DS classes are not complete with all neccessary methods for regular use and algos are not fully optimized.

+ <h4> Communication between services</h4>

	> Establishing and managing relationships between various services. Emphasis is put on communication with other devices and dealing with waiting time, connection failure and representing data streams to the user. Data persistence is made available with simple DB IO. Due to uncertainty pertaining to comm ops, basic threading is employed so the app doesn't halt if a certain connection fails.

+ <h4> Python structures and implementations</h4>

	> Exploring comps and generators, exceptions design, properties, descriptors, decorators, metaclasses, etc. Concepts are first tested in an abstract environment and examples are fairly basic, then an attempt was made to devise a useful library method which can be employed in a practical environment. Closely follows the book Learning Python by Mark Lutz, Chapters IV-VII. 

<h3>Final notes:</h3>

<p> Everything presented is constantly upgrading and expanding WIP. Files can be used freely and without mention if you find the material useful.