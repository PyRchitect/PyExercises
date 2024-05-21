# Minesweeper

<h3>General notes:</h3>

Classic minesweeper done in 3 graphical representations: console with text input, console with mouse input (using urwid) and GUI (using tkinter). Able to change board graphical settings, board size and difficulty.

Some features are missing in comparison with the real game because they were not neccessary for concept demonstration (L+R click, board creation rules, etc.).

<h3>Notes about subjects explored:</h3>

+ <h4> separating engine from graphics</h4>

	> game algorithms are designed to operate on an abstract M(m,n) matrix space inside the engine class. Raw transformed matrices (both the visible and the real board) are transferred to the graphics class where images are created and inputs are dealt with.

+ <h4> matrix operations</h4>

	> Boundary fill and perimeter determining algorithms is used to create the board and evaluate moves. Boards are updated after each move using simple symbol replacement.

+ <h4> display settings</h4>

	> Since the appearence is separated from game evaluation, it is possible to dynamically change it. In current implementation it is possible to change settings between games, can be scaled to change it during game.