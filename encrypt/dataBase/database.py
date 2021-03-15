try:
	import sqlite3 as sql
	from utils.utils import *
	import os
except:
	pass
	exit()


def createDB(db):
	"""
	:param db: database location
	:return: True or an error
	create a database
	"""
	if createFile(db):
		try:
			conn = sql.connect(db)
			c = conn.cursor()
			c.execute("""
				CREATE TABLE users(
					username text,
					password text
				)
			""")
			conn.commit()
		except Exception as e:
			return f"[EXCEPTION] {e}"
		else:
			return True
	else:
		return "Error creating the DB"



def getUsers(db):
	"""
	:param db: database location
	:return: (list or string, bool)
	get all users in the database
	"""
	try:
		conn = sql.connect(db)
		c = conn.cursor()
		c.execute("SELECT * FROM users")
		items = c.fetchall()
	except Exception as e:
		return f"[EXCEPTION] {e}", False
	else:
		users = []
		for item in items:
			users.append(item[0])
		return users, True


def createUser(db, username, password):
	"""
	:param db: database location
	:param username: username
	:param password: password
	:return: True or error
	create a new user
	"""
	try:
		conn = sql.connect(db)
		c = conn.cursor()
		c.execute("INSERT INTO users values (?, ?)", (username, password))
		conn.commit()
	except Exception as e:
		return f"[EXCEPTION] {e}"
	else:
		return True


def deleteUser(db, username):
	"""
	:param db: database location
	:param username: username
	:return: True or error
	"""
	try:
		conn = sql.connect(db)
		c = conn.cursor()
		c.execute("DELETE FROM users WHERE username = ?", (username,))
		conn.commit()
	except Exception as e:
		return f"[EXCEPTION] {e}"
	else:
		try:
			os.remove(f"logs/{username}.log")
		except:
			pass
		return True


def updateUsername(db, username, new_user, password):
	"""
	:param db: database location
	:param username: old username
	:param new_user: new username
	:param password: password
	:return: True or error
	update the username
	"""
	try:
		conn = sql.connect(db)
		c = conn.cursor()
		c.execute("UPDATE users SET username = ? WHERE username = ? AND password = ?", (new_user, username, password))
		conn.commit()
	except Exception as e:
		return f"[EXCEPTION] {e}"
	else:
		try:
			os.rename(f"logs/{username}.log", f"logs/{new_user}.log")
		except:
			pass
		return True


def updatePassword(db, username, password, old_password):
	"""
	:param db: database location
	:param username: username
	:param password: new password
	:param old_password: old password
	:return: None
	update the password
	"""
	try:
		conn = sql.connect(db)
		c = conn.cursor()
		c.execute("UPDATE users SET password = ? WHERE username = ? AND password = ?", (password, username, old_password))
		conn.commit()
	except Exception as e:
		return f"[EXCEPTION] {e}"
	else:
		return True


def verifyPass(db, username, password):
	"""
	:param db: database location
	:param username: username
	:param password: password
	:return: bool or error
	verify creds
	"""
	try:
		conn = sql.connect(db)
		c = conn.cursor()
		c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
		items = c.fetchall()
	except Exception as e:
		return f"[EXCEPTION] {e}"
	else:
		if len(items) > 0:
			return True
		else:
			return False
