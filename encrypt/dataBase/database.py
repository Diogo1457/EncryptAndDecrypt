try:
	import sqlite3 as sql
	from utils.json_handle import Json
	import os
except:
	pass
	exit()


CREATE_DB_COMMAND = """
CREATE TABLE users(
	username text,
	password text
)
"""

SELECT_USERS_COMMAND = "SELECT * FROM users"
CREATE_USER_COMMAND = "INSERT INTO users values (?, ?)"
DELETE_USER_COMMAND = "DELETE FROM users WHERE username = ?"
UPDATE_USERNAME_COMMAND = "UPDATE users SET username = ? WHERE username = ? AND password = ?"
UPDATE_PASSWORD_COMMAND = "UPDATE users SET password = ? WHERE username = ? AND password = ?"
CHECK_CREDS_COMMAND = "SELECT * FROM users WHERE username = ? AND password = ?"


class Database():
	def create(db):
		"""
		:param db: database location
		:return: True or an error
		create a database
		"""
		if Json.createF(db):
			try:
				conn = sql.connect(db)
				c = conn.cursor()
				c.execute(CREATE_DB_COMMAND)
				conn.commit()
			except Exception as e:
				return f"[EXCEPTION] {e}"
			else:
				return True
		else:
			return TEXTS[66]



	def users(db):
		"""
		:param db: database location
		:return: (list or string, bool)
		get all users in the database
		"""
		try:
			conn = sql.connect(db)
			c = conn.cursor()
			c.execute(SELECT_USERS_COMMAND)
			items = c.fetchall()
		except Exception as e:
			return f"[EXCEPTION] {e}", False
		else:
			users = []
			for item in items:
				users.append(item[0])
			return users, True


	def new_user(db, username, password):
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
			c.execute(CREATE_USER_COMMAND, (username, password))
			conn.commit()
		except Exception as e:
			return f"[EXCEPTION] {e}"
		else:
			return True


	def delUser(db, username):
		"""
		:param db: database location
		:param username: username
		:return: True or error
		"""
		try:
			conn = sql.connect(db)
			c = conn.cursor()
			c.execute(DELETE_USER_COMMAND, (username,))
			conn.commit()
		except Exception as e:
			return f"[EXCEPTION] {e}"
		else:
			try:
				os.remove(f"logs/{username}.log")
			except:
				pass
			return True


	def user_up(db, username, new_user, password):
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
			c.execute(UPDATE_USERNAME_COMMAND, (new_user, username, password))
			conn.commit()
		except Exception as e:
			return f"[EXCEPTION] {e}"
		else:
			try:
				os.rename(f"logs/{username}.log", f"logs/{new_user}.log")
			except:
				pass
			return True


	def pass_up(db, username, password, old_password):
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
			c.execute(UPDATE_PASSWORD_COMMAND, (password, username, old_password))
			conn.commit()
		except Exception as e:
			return f"[EXCEPTION] {e}"
		else:
			return True


	def checkCreds(db, username, password):
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
			c.execute(CHECK_CREDS_COMMAND, (username, password))
			items = c.fetchall()
		except Exception as e:
			return f"[EXCEPTION] {e}"
		else:
			if len(items) > 0:
				return True
			else:
				return False
