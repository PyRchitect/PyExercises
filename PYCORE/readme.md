# Pycore

<h3>General notes:</h3>

Collection of exercises exploring some Python core concepts. Concepts were first explored through syntetic exercises set in an abstract context, then an attempt was made to design a useful library method. Follows closely Learning Python by Mark Lutz, chapters IV-VIII.

<h3>Notes about subjects explored:</h3>

+ <h4> functions and generators</h4>

	> list and dict comprehensions, generator functions and expressions, yielding concepts, emulating built-in functions, etc.
	> benchmarking API for timing testing: separated setup stmts, able to change reps amounts, enable or disable tracing, etc.

+ <h4> modules and packages</h4>

	> transitive module reloader, coded in few different styles

+ <h4> classes and OOP</h4>

	> operator overloading, old-style vs. new-style classes, MRO, slots, static and class methods, super(), multiple inheritance, dynamic tree changes, cooperative dispatch, etc.
	> mapattrs tool which maps all atributes on or inherited by an instance to the instance or class from which they are inherited

+ <h4> Exceptions</h4>

	> exceptions design and layering, try-except-finally variations, (re)raising and propagation, asserting, with context mgr, control flow nesting

+ <h4> Advanced Topics</h4>

	> managed attributes (properties / descriptors / get attr comparison), class and function decorators, metaclasses design and comparison with decorator approach
	> argtest decorator used for testing validity of args sent to a function