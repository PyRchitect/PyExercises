# Meteo

<h3>General notes:</h3>

Light app for a (completely fake) smart key account management system.

Connects to a simple database, retreives information, provides feedback based on input, differentiates user privileges. Able to manage users through admin console - add or remove users, change PIN numbers, etc.

<h3>Notes about subjects explored:</h3>

+ <h4> database operations</h4>

	> the app interacts with the database through the console, commands are made available depending on user privileges. Privileges can be dealt and revoked, and the connection adapts (adding and removing admin status).

+ <h4> dynamic GUI adjustments</h4>

	> the app changes appearence based on user interaction - along with message relaying, app frames are added or removed depending on the session status

+ <h4> user verification</h4>

	> two step verification is employed - firstly, a user number is obtained, then a PIN is processed. Active users are dealt a certain set of rights, inactive another set, and admins can fully interact with the app.

+ <h4> console commands</h4>

	> in addition to interacting with the backend directly, it is possible to instruct the console with a predefined set of codes which are then translated to commands. Used for automating db work without the need of GUI. Can be scaled to full scale CLI by adding commands and flags which could be sent remotely to the app.