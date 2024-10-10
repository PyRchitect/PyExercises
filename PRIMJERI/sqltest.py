import sqlite3
from os import path as os_path
from sys import path as sys_path

def main():
	file_path = os_path.join(sys_path[0],'sqltest.db')

	query_create = '''CREATE TABLE IF NOT EXISTS Employees	
					  (id INTEGER PRIMARY KEY,
					   name TEXT NOT NULL,
					   email TEXT NOT NULL UNIQUE)'''
	query_create_values = None

	query_insert = '''INSERT INTO Employees (name,email)
	 				  VALUES (?,?)'''
	query_insert_values = [
		('Mate Matić','mate.matic@gmail.com'),
		('Ana Anić','ana.anic@hotmail.com')
	]

	query_select = 'SELECT * FROM Employees WHERE id = ?'
	query_select_values = (2,)

	query_update = 'UPDATE Employees SET name = ?, email = ? WHERE id = ?'
	query_update_values = ('Ana Anic Matic','ana.anic.matic@hotmail.com',2)

	query_delete = 'DELETE FROM Employees WHERE id = ?'
	query_delete_values = (2,)

	query_drop = 'DROP TABLE IF EXISTS Employees'
	query_drop_values = None

	for (query,values) in zip(
		(query_create,query_insert,query_select,query_update,query_delete,query_drop),
		(query_create_values,query_insert_values,query_select_values,query_update_values,query_delete_values,query_drop_values)
		):
		try:
			connection = sqlite3.connect(file_path)

			cursor = connection.cursor()
			if values is not None:
				if isinstance(values,list):
					for value in values:
						cursor.execute(query,value)		
				else:
					cursor.execute(query,values)
			else:
				cursor.execute(query)
			if 'SELECT' in query:
				records = cursor.fetchall()
				print(records)
				# ako se nešto vadi iz DB (SELECT)
			else:
				connection.commit()
				# connection, ne cursor! ako se nešto mijenja u DB (CREATE,INSERT,UPDATE,DELETE,DROP)
			cursor.close()
		except sqlite3.Error as e:
			print(e)
		finally:
			connection.close()

def main_create(filepath):
	create_table_query = '''CREATE TABLE IF NOT EXISTS Employees 
							(id INTEGER PRIMARY KEY,
							 name TEXT NOT NULL,
							 email TEXT NOT NULL UNIQUE)'''
	try:
		sc = sqlite3.connect(filepath)
		cursor = sc.cursor()
		cursor.execute(create_table_query)
		sc.commit()
		cursor.close()
	except sqlite3.Error as e:
		print(e)
	finally:
		if sc:
			sc.close()

def main_insert(filepath):

	insert_table_query = '''INSERT INTO Employees (name,email)
							VALUES (?,?)'''

	lista_radnika = [
		('Mate Matic','mmatic@mail.com'),
		('Ana Anic','aanic@hotmail.com'),
		('Jure Juric','jjuric@brzi.hr')
	]

	try:
		sc = sqlite3.connect(filepath)
		cursor = sc.cursor()

		for radnik in lista_radnika:
			cursor.execute(insert_table_query,radnik)
		
		sc.commit()

		cursor.close()
		print("Cursor otpusten.")

	except sqlite3.Error as e:
		print(f"Dogodila se greska {e}")

	finally:
		if sc:
			sc.close()
			print("Zatvorena konekcija na bazu")

def main_test(filepath):
	try:
		connection = sqlite3.connect(filepath)
		cursor = connection.cursor()

		query_create = '''CREATE TABLE IF NOT EXISTS Employees
						(id INTEGER PRIMARY KEY,
						name TEXT NOT NULL,
						email TEXT NOT NULL UNIQUE)'''
		cursor.execute(query_create)			# nema values, samo query
		connection.commit()						# mijenja nešto u bazi

		query_insert = '''INSERT INTO Employees
						(name,email) VALUES (?,?)'''
		query_insert_values = [
			('Mate Matić','mate.matic@gmail.com'),
			('Ana Anić','ana.anic@hotmail.com')]
		for value in query_insert_values:		# vrti kroz petlju jer izvršava
			cursor.execute(query_insert,value)	# za svaki element liste posebno
		connection.commit()						# mijenja nešto u bazi

		query_select = 'SELECT * FROM Employees WHERE id = ?'
		query_select_values = (2,)				# čak i kad je 1 value, piše se kao tuple
		cursor.execute(query_select,query_select_values)
		records = cursor.fetchall()				# nešto se vadi iz baze
		print(records)

		query_update = 'UPDATE Employees SET name = ?, email = ? WHERE id = ?'
		query_update_values = ('Ana Anic Matic','ana.anic.matic@hotmail.com',2)
		cursor.execute(query_update,query_update_values)
		connection.commit()						# mijenja nešto u bazi

		query_delete = 'DELETE FROM Employees WHERE id = ?'
		query_delete_values = (2,)				# čak i kad je 1 value, piše se kao tuple
		cursor.execute(query_delete,query_delete_values)
		connection.commit()						# mijenja nešto u bazi

		query_drop = 'DROP TABLE IF EXISTS Employees'
		cursor.execute(query_drop)				# nema values, samo query
		connection.commit()						# mijenja nešto u bazi

	except sqlite3.Error as e:
		print(e)

	finally:
		if cursor:
			cursor.close()
		if connection:
			connection.close()

if __name__ == '__main__':
	# main()
	dbname = 'TvrtkaDB.db'
	filepath = sys_path[0] + '\\' + dbname
	# main_create(filepath)
	# main_insert(filepath)
	main_test(filepath)