from dataBase.database import getUsers


db = "dataBase/users.db" # database location


class VerifySigin():
	def __init__(self, username, password):
		"""
		:param self: method
		:param username: username
		:param password: password
		:return: None
		init the class
		"""
		self.username = username
		self.password = password


	def verifyUsername(self):
		"""
		:param self: method
		:return: True or string
		verify if the username format is correct
		"""
		if self.username != "":
			if self.username.islower():
				if self.username.isalnum():
					if len(self.username) <= 15:
						valid = True
						users = getUsers(db)[0]
						if self.username in users:
							valid = "Username already exists"
						return valid
					else:
						return "Username length must be less than 15 chars"
				else:
					return "Username must be alpha numeric"
			else:
				return "Username must be all lower case"
		else:
			return "You must set a username"


	def verifyPassword(self):
		"""
		:param self: method
		:return: True or string
		verify if the password format is correct
		"""
		if self.password != "":
			if len(self.password) >= 4:
				if len(self.password) <= 30:
					return True
				else:
					return"Password must be 30 chars max"
			else:
				return "Password must be 4 chars longer"
		else:
			return "You must set a password"
