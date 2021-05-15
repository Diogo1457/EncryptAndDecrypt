try:
	from tkinter import *
	from tkinter import filedialog
	from config.config import *
	from utils.utils import File
	from utils.settings import Settings
	from utils.display import BetterDisplay
	from utils.json_handle import Json
	from utils.logs import Logs
	from widgets.widgets import *
	from encrypt.encrypt import Encrypt
	from base64 import b64encode, b64decode
	from dataBase.database import Database
	import os
	from verifyForm.verifySigin import VerifySigin
	from verifyForm.verifyInput import VerifyInput
except Exception as e:
	print("[EXCEPTION] ", e)
	exit()



"""
	#---------------------------------------------#
	|	          Made by Diogo Lobo			  |
	|											  |
    |     Github - https://github.com/Diogo1457   |
	|											  |
	|                                             |
	|  Program Description:                       |
	|                                             |
	|  - This program encrypts and decrypt files  |
	|  or strings with passwords.				  |
	|                                             |
	|  - It allows creating local users where it  |
	|  stores encrypted logs (using your main     |
	|  password).								  |
	|											  |
	|	- The logs store the passwords that you   |
	|  used to encrypt data. All logs are         |
	|  encrypted and you can find them on the     |
	|  logs folder created in the same folder     |
	|  that you placed this program. 			  |
	|											  |
	|  - If you forget some file or string        |
    |  encryption password you can check it in    |
    |  your user logs.                            |
	|  ### Note: For keeping logs you need to be  |
	|  logged in with the user you want to save   |
	|  that log.								  |
	|											  |
	|  - You can update your username or          |
	|  password. You cant also delete it.         |
	|											  |
	|  - You can also encrypt or decrypt files    |
	|  without saving the logs (if you forget     |
	|  the password used to encrypt the file or   |
	|  string you can't recover it).              |
	|											  |
	#-------------------Enjoy---------------------#
"""

FILE = ""
DEFAULT_TEXT_PLACE = None # Display File Selected
USERNAME = None # Main username
PASSWORD = None # Main password
LOGS_FILE = ""  # Log file




def selectFile(root, task):
	global DEFAULT_TEXT_PLACE
	"""
	:param root: object
	:param task: encrypt or decrypt
	:return: None
	used to select a file
	"""
	global FILE
	if task == "e":
		FILE = filedialog.askopenfilename(initialdir="~", filetypes=(ALL_FILES,))
	if task == "d":
		FILE = filedialog.askopenfilename(initialdir="~", filetypes=(ENCRYPTED_FILES,))
	if FILE:
		FILE = os.path.join(FILE)
		filename_show = BetterDisplay.filename(FILE, 70)
		if DEFAULT_TEXT_PLACE:
			DEFAULT_TEXT_PLACE.destroy()
		DEFAULT_TEXT_PLACE = displayText(root, filename_show, 200, 225, _font=FONT_W)
	else:
		FILE = ""


def saveFileWhere(root, task):
	"""
	:param root: object
	:param task: encrypt or decrypt
	:return: (bool, str or None)
	used to select an output file
	"""
	global FILE
	if task == "e":
		FILE_SAVE = filedialog.asksaveasfilename(initialdir="~", defaultextension=".encrypted", filetypes=(ENCRYPTED_FILES,))
	if task == "d":
		FILE_SAVE = filedialog.asksaveasfilename(initialdir="~", defaultextension=".decrypted", filetypes=(DECRYPTED_FILES,))
	FILE_SAVE = os.path.join(FILE_SAVE)
	if FILE_SAVE:
		if File.create(FILE_SAVE) != True:
			return False,
		else:
			FILE = FILE_SAVE
			return True, FILE_SAVE
	else:
		return None,


def encryptFile(root, filename, password, IV, mode, regist=True):
	"""
	:param root: object
	:param filename: file selected
	:param password: password to encrypt the file
	:param IV: Inictial Vector
	:param mode: encryption type
	:param regist: bool (regist logs)
	:return: None
	used to handle encrypt file operation
	"""
	v = VerifyInput(filename, password, "e")
	response = v.verifyInput()
	if response == True:
		content = File.readB(filename)
		encrypted_content = Encrypt.encrypt(content, password, IV, mode)
		where_to_save = saveFileWhere(root, "e")
		encryptFileWindow(root, regist)
		if where_to_save[0] == True:
			text = File.save(encrypted_content, where_to_save[1])
			text_to_show = BetterDisplay.filename(filename, 60)
			displayText(root, text, 100, 450, _bw=5, _font=FONT_W)
			if regist:
				Logs.reg_log(LOGS_FILE, OPTIONS[2] + text + f" (Password: {password})", PASSWORD)
		else:
			displayText(root, TEXTS[0], 200, 450, _fg="red", _bw=5)
	elif not response:
		pass
	else:
		encryptFileWindow(root, regist)
		displayText(root, response, 200, 450, _fg="red", _bw=5)



def decodeFile(root, filename, password, IV, mode, regist=True):
	"""
	:param root: object
	:param filename: file selected
	:param password: password to encrypt the file
	:param IV: Inictial Vector
	:param mode: encryption type
	:param regist: bool (regist logs)
	:return: None
	used to handle decrypt file operation
	"""
	v = VerifyInput(filename, password, "d")
	response = v.verifyInput()
	fg = "white"
	if response == True:
		content = File.readB(filename)
		type = File.setType(content)
		decrypted_content = Encrypt.decrypt(content, password, IV, mode, type)
		if decrypted_content[1] == True:
			where_to_save = saveFileWhere(root, "d")
			if where_to_save[0] == True:
				text = File.save(decrypted_content[0], where_to_save[1], False, type)
				text_to_show = BetterDisplay.filename(text, n=60)
				response = text_to_show
				if regist:
					Logs.reg_log(LOGS_FILE, OPTIONS[0] + text + f" (Password: {password})", PASSWORD)
			else:
				response = TEXTS[0]
		else:
			response = TEXTS[1]
	elif not response:
		return
	else:
		fg = "red"
		decryptFileWindow(root, regist)
	displayText(root, response, 200, 450, _bw=5, _fg="red")



def encodeString(root, string, password, IV, mode, regist):
	"""
	:param root: object
	:param string: str to encrypt
	:param password: password to encrypt the string
	:param IV: Inictial Vector
	:param mode: encryption type
	:param regist: bool (regist logs)
	:return: None
	used to handle encrypt string operation
	"""
	if string != "":
		encryptStringWindow(root, regist)
		if password != "":
			string_encrypted = Encrypt.encrypt(string.encode("utf8"), password, IV, mode)
			string_encrypted = b64encode(string_encrypted).decode("utf8")
			string_to_show = BetterDisplay.filename(string_encrypted)
			displayText(root, string_to_show, 100, 500, _fg="black", _bw=0)
			if regist:
				Logs.reg_log(LOGS_FILE, OPTIONS[3] + string_encrypted + f" (Password: {password})", PASSWORD)
			displayButton(root, TEXTS[2], lambda:copyToClip(root, string_encrypted), 150, 550)
		else:
			displayText(root, TEXTS[3], 100, 500, _bw=5)


def decodeString(root, string, password, IV, mode, regist):
	"""
	:param root: object
	:param string: str to encrypt
	:param password: password to encrypt the string
	:param IV: Inictial Vector
	:param mode: encryption type
	:param regist: bool (regist logs)
	:return: None
	used to handle decrypt string operation
	"""
	if string != "":
		decryptStringWindow(root, regist)
		string = Logs.isBase64(string)
		if not string:
			response = TEXTS[4]
		else:
			if password != "":
				try_to_decrypt = Encrypt.decrypt(string, password, IV, mode, "t")
				if try_to_decrypt[1]:
					string_decrypted = try_to_decrypt[0]
					response = BetterDisplay.filename(string_decrypted)
					if regist:
						Logs.reg_log(LOGS_FILE, OPTIONS[1] + string_decrypted + f" (Password: {password})", PASSWORD)
					displayButton(root, TEXTS[2], lambda:copyToClip(root, string_decrypted), 150, 550)
				else:
					response = try_to_decrypt[0]
			else:
				response = TEXTS[3]
		displayText(root, response, 100, 500, _fg="black", _bw=5, _font=SFONT)


def multiUsedDivs(root, regist, height=350, width=290):
	"""
	:param root: object
	:param regist: bool
	:param height: height of logs button
	:param width: width of logs button
	:return: (object, object)
	create multi used frames
	"""
	displayText(root, TEXTS[5], 195, 70, _bw=0, _font=BFONT)
	password = displayEntry(root, 100, 120, _width=25, _bg="white", _fg="black", _font=BFONT_W, _show="*")
	variable = StringVar(root)
	variable.set("AES MODE_CBC")
	menu = OptionMenu(root, variable, "AES MODE_CBC")
	menu.place(x=500, y=120)
	displayButton(root, TEXTS[6], lambda:encryptWindow(root, regist), 0, 0, _fg="gray", _bw=0)
	if regist:
		displayButton(root, TEXTS[7], lambda:logsWindow(), width, height, _bg="white", _bw=0, _width=15, _font=FONT_W)
	return password, variable


def encryptFileWindow(root, regist):
	"""
	:param root: object
	:param regist: bool (regist logs)
	:return: None
	display the encrypt file window
	"""
	global FILE, DEFAULT_TEXT_PLACE
	clearAllElements(root)
	if FILE != "":
		filename_show = BetterDisplay.filename(FILE, 70)
		DEFAULT_TEXT_PLACE = displayText(root, filename_show, 200, 225, _font=FONT_W)
	password, variable = multiUsedDivs(root, regist)
	displayButton(root, TEXTS[8], lambda:selectFile(root, task="e"), 100, 225, _bg="white", _width=7, _font=SM_FONT_W)
	root.bind("<Return>", lambda e:encryptFile(root, FILE, password.get(), IV, variable.get(), regist))
	displayButton(root, TEXTS[9], lambda:encryptFile(root, FILE, password.get(), IV, variable.get(), regist), 290, 300, _bg="white", _width=15, _font=FONT_W)



def decryptFileWindow(root, regist):
	"""
	:param root: object
	:param regist: bool (regist logs)
	:return: None
	display the decrypt file window
	"""
	global FILE, DEFAULT_TEXT_PLACE
	clearAllElements(root)
	if FILE != "":
		filename_show = BetterDisplay.filename(FILE, 70)
		DEFAULT_TEXT_PLACE = displayText(root, filename_show, 200, 225, _font=FONT_W)
	password, variable = multiUsedDivs(root, regist)
	displayButton(root, TEXTS[8], lambda:selectFile(root, task="d"), 100, 225, _bg="white", _bw=0, _width=7, _font=SM_FONT_W)
	root.bind("<Return>", lambda e:decodeFile(root, FILE, password.get(), IV, variable.get(), regist))
	displayButton(root, TEXTS[10], lambda:decodeFile(root, FILE, password.get(), IV, variable.get(), regist), 290, 300, _bg="white", _bw=0, _width=15, _font=FONT_W)


def encryptStringWindow(root, regist):
	"""
	:param root: object
	:param regist: bool (regist logs)
	:return: None
	display the encrypt string window
	"""
	clearAllElements(root)
	password, variable = multiUsedDivs(root, regist, 400, 310)
	displayText(root, TEXTS[11], 250, 200, _bw=0, _font=BFONT)
	string = displayEntry(root, 100, 250, _width=35, _bg="white", _fg="black", _font=BFONT_W)
	root.bind("<Return>", lambda e:encodeString(root, string.get(), password.get(), IV, variable.get(), regist))
	displayButton(root, TEXTS[12], lambda:encodeString(root, string.get(), password.get(), IV, variable.get(), regist), 290, 350, _bg="white", _width=20, _font=FONT_W)


def decryptStringWindow(root, regist):
	"""
	:param root: object
	:param regist: bool (regist logs)
	:return: None
	display the decrypt string window
	"""
	clearAllElements(root)
	password, variable = multiUsedDivs(root, regist, 400, 310)
	displayText(root, TEXTS[13], 220, 200, _bw=0, _font=BFONT)
	string = displayEntry(root, 100, 250, _width=35, _bg="white", _fg="black", _font=BFONT_W)
	root.bind("<Return>", lambda e:decodeString(root, string.get(), password.get(), IV, variable.get(), regist))
	displayButton(root, TEXTS[14], lambda:decodeString(root, string.get(), password.get(), IV, variable.get(), regist), 290, 350, _bw=0, _bg="white", _width=20, _font=FONT_W)


def encryptWindow(root, logs=True):
	"""
	:param root: object
	:param logs: bool (regist logs)
	:return: None
	display encrypt menu
	"""
	clearAllElements(root)
	root.unbind("<Return>")
	displayText(root, TEXTS[15], 280, 50, _bw=0, _font=BFONT_I)
	displayButton(root, TEXTS[9], lambda:encryptFileWindow(root, logs), 100, 150, _width=20, _bg="white", _fg="black", _bw=0, _font=FONT_W)
	displayButton(root, TEXTS[10], lambda:decryptFileWindow(root, logs), 100, 220, _width=20, _bg="white", _fg="black", _bw=0, _font=FONT_W)
	displayButton(root, TEXTS[12], lambda:encryptStringWindow(root, logs), 500, 150, _width=20, _bg="white", _fg="black", _bw=0, _font=FONT_W)
	displayButton(root, TEXTS[14], lambda:decryptStringWindow(root, logs), 500, 220, _width=20, _bg="white", _fg="black", _bw=0, _font=FONT_W)
	if logs:
		displayButton(root, TEXTS[16], lambda:profileWindow(root), 100, 290, _width=20, _bg="white", _fg="black", _bw=0, _font=FONT_W)
		displayButton(root, TEXTS[7], lambda:logsWindow(), 500, 290, _width=20, _bg="white", _fg="black", _bw=0, _font=FONT_W)
	else:
		displayText(root, TEXTS[17], 100, 300, _fg="red", _bw=0)
	displayButton(root, TEXTS[18], lambda:loginWindow(root, 0), 320, 400, _width=20, _bg="white", _fg="black", _bw=0, _font=FONT_W)
	displayButton(root, TEXTS[19], lambda:Settings.openInTheWeb(URLS[0]), 320, 500, _width=20, _fg="black", _bw=0)


def deleteUserWindow(root):
	"""
	:param root: object
	:return: None
	display the delete user confirmation window
	"""
	global delete_window
	try:
		info = delete_window.winfo_children()
	except:
		delete_window = Tk()
		delete_window.title(TEXTS[20])
		delete_window.geometry(DR)
		delete_window.configure(bg=BG)
		displayText(delete_window, TEXTS[21], _place=False).pack(pady=20)
		displayButton(delete_window, TEXTS[22], lambda:deleteConfirmed(root), _width=10, _font=SFONT_W, _place=False).pack()
		displayButton(delete_window, TEXTS[23], lambda:deleteRefused(root), _width=10, _font=SFONT_W, _place=False).pack()
		delete_window.mainloop()


def deleteRefused(root):
	"""
	:param root: object
	:return: None
	delete account wasn't confirm
	"""
	delete_window.destroy()
	profileWindow(root)


def deleteConfirmed(root):
	global USERNAME, PASSWORD, LOGS_FILE
	"""
	:param root: object
	:return: None
	delete account was confirm
	"""
	delete_window.destroy()
	try_delete_user = Database.delUser(DB, USERNAME)
	if try_delete_user:
		USERNAME = None
		PASSWORD = None
		LOGS_FILE = ""
		loginWindow(root, 0)
	else:
		errorWindow(try_delete_user)


def updatePasswordHandle(root, password):
	"""
	:param root: object
	:password: new password
	:return: None
	used to handle the update password operation
	"""
	global USERNAME, PASSWORD, LOGS_FILE
	profileWindow(root)
	v = VerifySigin(USERNAME, password)
	verify_password = v.verifyPassword()
	if verify_password == True:
		update_password = Database.pass_up(DB, USERNAME, Encrypt.encryptPassword(password), Encrypt.encryptPassword(PASSWORD))
		if update_password == True:
			logs = Logs.readLog(LOGS_FILE)
			if logs:
				if len(logs) != 0:
					decoded_logs = Logs.decodeLogs(logs, PASSWORD)
					File.delCont(LOGS_FILE)
					for log in decoded_logs:
						Logs.reg_log(LOGS_FILE, log, password)
			USERNAME = None
			PASSWORD = None
			LOGS_FILE = ""
			loginWindow(root, 0)
		else:
			displayText(root, update_password, _bw=0, _fg="gray", _place=False).pack()
	else:
		displayText(root, verify_password, _bw=0, _fg="gray", _place=False).pack()



def updateUsernameHandle(root, username):
	"""
	:param root: object
	:username: new user
	:return: None
	used to handle the update username operation
	"""
	global USERNAME, PASSWORD, LOGS_FILE
	profileWindow(root)
	v = VerifySigin(username, PASSWORD)
	verify_username = v.verifyUsername()
	if verify_username == True:
		username_update = Database.user_up(DB, USERNAME, username, Encrypt.encryptPassword(PASSWORD))
		if username_update == True:
			text = TEXTS[24]
			USERNAME = username
			LOGS_FILE = f"logs/{username}.log"
		else:
			text = username_update
	else:
		text = verify_username
	displayText(root, text, _bw=0, _place=False).pack()



def profileWindow(root):
	"""
	:param root: object
	:return: None
	display profile settings to update
	"""
	clearAllElements(root)
	displayText(root, USERNAME, _font=BFONT, _place=False).pack(pady=10)
	displayText(root, TEXTS[25], _bw=0, _font=BFONT, _place=False).pack(pady=10)
	username = displayEntry(root, _width=30, _font=BFONT_W, _fg="black")
	username.pack(pady=10)
	displayButton(root, TEXTS[26], lambda:updateUsernameHandle(root, username.get()), _width=15, _bg=FG, _font=FONT_W, _place=False).pack(pady=20)
	displayText(root, TEXTS[27], _bw=0, _font=BFONT, _place=False).pack(pady=10)
	password = displayEntry(root, _show="*", _width=30, _font=BFONT_W, _place=False, _fg="black")
	password.pack(pady=10)
	displayButton(root, TEXTS[28], lambda:updatePasswordHandle(root, password.get()), _width=15, _bg=FG, _font=FONT_W, _place=False).pack(pady=10)
	displayButton(root, TEXTS[29], lambda:deleteUserWindow(root), _width=15, _bg=FG, _font=FONT_W, _place=False).pack(pady=(50, 0))
	displayButton(root, TEXTS[30], lambda:encryptWindow(root), _place=False).pack(pady=(50, 0))




def authenticate(root, username, password):
	"""
	:param root: object
	:param username: username
	:param password: password
	:return: None
	used to verify if username and password are correct
	"""
	global USERNAME, PASSWORD, LOGS_FILE
	if password != "":
		authenticateWindow(root, username)
		verify = VerifySigin(username, password)
		if verify.verifyPassword() == True:
			verify_password = Database.checkCreds(DB, username, Encrypt.encryptPassword(password))
			if verify_password == True:
				root.unbind("<Return>")
				encryptWindow(root)
				USERNAME = username
				PASSWORD = password
				LOGS_FILE = "logs/" + USERNAME + ".log"
			elif not verify_password:
				displayText(root, TEXTS[31], _bw=0, _place=False).pack()
			else:
				displayText(root, verify_password, _bw=0, _place=False).pack()
		else:
			displayText(root, TEXTS[31], _bw=0, _place=False).pack()


def authenticateWindow(root, user):
	"""
	:param root: object
	:param user: username
	:return: None
	display the window to type the password
	"""
	clearAllElements(root)
	displayText(root, TEXTS[32] + user, _bw=0, _font=BG_FONT, _place=False).pack(pady=50)
	displayText(root, TEXTS[5], _bw=0, _font=BFONT, _place=False).pack(pady=(0, 20))
	password = displayEntry(root, _width=25, _bg="white", _fg="black", _font=BFONT_W, _show="*", _place=False)
	password.pack(pady=(0, 50))
	root.bind("<Return>", lambda e:authenticate(root, user, password.get()))
	displayButton(root, TEXTS[33], lambda:authenticate(root, user, password.get()), _width=12, _bg=LB_BG, _fg="white", _bw=0, _place=False).pack()
	displayButton(root, TEXTS[34], lambda:loginWindow(root, 0), _width=12,_bw=0, _place=False).pack(pady=(50, 50))


def dontHaveUser(root):
	"""
	:param root: object
	:return: None
	used to display create user and start information
	"""
	displayButton(root, TEXTS[35], lambda:encryptWindow(root, False), 250, 50, _bg="white", _fg="gray", _bw=0)
	displayText(root, TEXTS[36], 320, 100, _bw=0, _fg="red")
	displayText(root, TEXTS[37], 190, 150, _bw=0, _fg="black")
	path = os.getcwd()
	path = BetterDisplay.filename(path, 60)
	big_text = BetterDisplay.bigText(TEXTS[38], path)
	displayText(root, big_text, 150, 400, _bw=0, _fg="red")
	displayButton(root, TEXTS[39], lambda:createUserWindow(root), 250, 250, _fg="gray", _bg="white", _width=20, _font=BG_FONT)


def displayUsers(root, all_users, start):
	"""
	:param root: object
	:param all_users: list of users
	:return: int
	used to display the users
	"""
	cont = 0
	row = 0
	users = all_users[start:start+3:1]
	paddingx = 150
	paddingy = 100
	for user in users:
		paddingx = 150
		paddingy = 100
		if cont != 0:
			paddingx = 100
		if row != 0:
			paddingy = 50
		displayButton(root, user, lambda user=user:authenticateWindow(root, user), _fg=FG, _width=10, _bg="#0b8c63", _height=4, _font=BG_FONT, _bw=0, _place=False).grid(row=row, column=cont, padx=(paddingx, 70), pady=(paddingy, 50))
		cont += 1
		if cont >= 2:
			row += 1
			cont = 0
	displayButton(root, "+", lambda:createUserWindow(root), _bw=0, _font=HFONT, _fg=FG, _place=False).grid(row=row, column=cont, padx=(paddingx, 70), pady=(paddingy, 40))
	start += 3
	displayButton(root, TEXTS[35], lambda:encryptWindow(root, False), 260, 20, _fg=FG, _bg="#026571", _bw=0)
	if len(all_users) - start > 0:
		displayButton(root, TEXTS[40], lambda:loginWindow(root, start), 620, 550, _fg=FG, _bg=PN_BG, _bw=0)
	if start > 3:
		displayButton(root, TEXTS[41], lambda:loginWindow(root, start - 6), 470, 550, _fg=FG, _bg=PN_BG, _bw=0)
	return start


def loginWindow(root, start):
	global USERNAME, PASSWORD, LOGS_FILE, FILE, DEFAULT_TEXT_PLACE
	"""
	:param root: object
	:param start: int
	:return: None
	display all the users
	"""
	root.unbind("<Return>")
	USERNAME = None
	PASSWORD = None
	LOGS_FILE = ""
	FILE = ""
	DEFAULT_TEXT_PLACE = None
	clearAllElements(root)
	users = Database.users(DB)
	if users[1]:
		all_users = users[0]
		if len(all_users) == 0:
			dontHaveUser(root)
		else:
			start = displayUsers(root, all_users, start)
	else:
		error_window(users[0])



def tryCreateUser(root, username, password):
	"""
	:param root: object
	:param username: username
	:param password: password
	:return: None
	used to handle the create user operation
	"""
	v = VerifySigin(username, password)
	username_verify = v.verifyUsername()
	password_verify = v.verifyPassword()
	createUserWindow(root)
	if username_verify == True:
		if password_verify == True:
			root.unbind("<Return>")
			Database.new_user(DB, username, Encrypt.encryptPassword(password))
			loginWindow(root, 0)
		else:
			displayText(root, password_verify, 260, 400, _bw=0)
	else:
		displayText(root, username_verify, 260, 400, _bw=0)


def createUserWindow(root):
	"""
	:param root: object
	:return: None
	display the create user window
	"""
	clearAllElements(root)
	displayText(root, TEXTS[42], 350, 70, _bw=0, _font=BFONT)
	username = displayEntry(root, 250, 120, _width=25, _bg="white", _fg="black", _font=BFONT)
	displayText(root, TEXTS[5], 350, 180, _bw=0, _font=BFONT)
	password = displayEntry(root, 250, 230, _width=25, _bg="white", _fg="black", _font=BFONT, _show="*")
	root.bind("<Return>", lambda e: tryCreateUser(root, username.get(), password.get()))
	displayButton(root, TEXTS[43], lambda:tryCreateUser(root, username.get(), password.get()), 330, 310, _bg="white", _fg="black", _font=BFONT)
	displayButton(root, TEXTS[30], lambda:loginWindow(root, 0), 360, 500, _fg="gray", _bw=0)


def errorWindow(error):
	"""
	:param error: error
	:return: None
	used to display the errors
	"""
	global error_window
	try:
		error_window.destroy()
	except:
		pass
	error_window = createRootWindow(TEXTS[67])
	displayText(error_window, error, _font=EFONT).pack()
	error_window.mainloop()


def displayTheLogs(root, logs, string):
	"""
	:param root: object
	:param logs: logs encoded
	:param string: str (used to show only a type of logs)
	:return: None
	used to display the logs
	"""
	clearAllElements(root)
	displayButton(root, TEXTS[30], lambda:logsWindow(False), _place=False).pack()
	displayText(root, TEXTS[7], _bw=0, _place=False).pack(pady=10)
	frame = createScrollbar(root)
	if logs:
		logs_to_show = []
		logs = Logs.decodeLogs(logs, PASSWORD)
		logs = logs[::-1]
		for log in logs:
			if string == "*":
				logs_to_show.append(log)
			else:
				if log[0:len(string):1] == string:
					logs_to_show.append(log)
		cont = 0
		for log in logs_to_show:
			displayText(frame, log, _bw=0, _font=FONT_W, _place=False).pack(pady=5)
			cont += 1


def placeLogsButtons(logs_window, logs):
	"""
	:param logs_window: object
	:param logs: encoded logs
	:return: None
	used to place the buttons in logs window
	"""
	cont = 44
	options = ["*", OPTIONS[2], OPTIONS[3], OPTIONS[0], OPTIONS[1]]
	for option in options:
		displayButton(logs_window, TEXTS[cont], lambda option=option:displayTheLogs(logs_window, logs, option), _width=20, _place=False).pack(pady=20)
		cont += 1


def logsWindow(reload=True):
	"""
	:param reload: bool
	:return: None
	used to display the logs options
	"""
	logs = Logs.readLog(LOGS_FILE)
	if reload:
		# When click
		global logs_window
		try:
			info = logs_window.winfo_children()
		except:
			logs_window = createRootWindow(LT, LR, _resizable=(True, True))
			placeLogsButtons(logs_window, logs)
			logs_window.mainloop()
	else:
		# When click on back button
		clearAllElements(logs_window)
		placeLogsButtons(logs_window, logs)


if __name__ == "__main__":
	root = createRootWindow(TT, RS) # Call the object
	things_to_set = Settings.setThingsToInitializeTheProgram(DB) # Call the initialize settings
	if things_to_set[0] == True:
		loginWindow(root, 0) # Call the login window
	else:
		error = things_to_set[1]
		errorWindow(error) # Call the error window
	root.mainloop()
