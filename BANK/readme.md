# Bank

<h3>General notes:</h3>

<p>Using a simple (completely fake) bank account mgmt system in order to explore data cleaning and compacting procedures. Able to add and remove clients, accounts, funds, generate client, account, transaction lists etc. Able to generate random input test data. Persistence not implemented. Uses a custom simple interface for processing inputs and outputs.</p>

<h3>Notes about subjects explored:</h3>

+ <h4> finding holes in bitvector</h4>

	> Uses a simple hole finding algorithm in order to keep data points lists compact: new list, append m data points, remove n<m data points. Add k<n data points. Max data point index should be lower than m.

+ <h4> dictionary cleaning</h4>

	> Performs dynamic appending and removal of keys in order to keep data dicts compact: data hierarchy is chronological: years > months > indices. Removing last existing index in some branch triggers pruning of all unused keys. Appending new data creates new neccessary keys.

+ <h4> custom interface</h4>

	> A simple interface is designed to process inputs (data getters) and outputs (printouts). Employs customizable input testing procedures via lists of lambda functions which is used to create menus.