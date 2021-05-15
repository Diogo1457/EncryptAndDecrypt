from dataBase.database import Database
from config.config import *


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
						users = Database.users(db)[0]
						if self.username in users:
							valid = TEXTS[49]
						return valid
					else:
						return TEXTS[50]
				else:
					return TEXTS[51]
			else:
				return TEXTS[52]
		else:
			return TEXTS[53]


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
					return TEXTS[54]
			else:
				return TEXTS[54]
		else:
			return TEXTS[55]
