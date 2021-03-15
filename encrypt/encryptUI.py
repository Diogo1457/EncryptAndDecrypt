try:
	from tkinter import *
	from tkinter import filedialog
	from utils.utils import *
	from encrypt import *
	from base64 import b64encode, b64decode
	from dataBase.database import *
	import os
	import webbrowser
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
USERNAME = None # Main username
PASSWORD = None # Main password
LOGS_FILE = ""  # Log file
db = "dataBase/users.db" # dataBase


def openInTheWeb(url):
	"""
	:param url: website url
	:return: None
	Open website on default browser
	"""
	webbrowser.open(url)


def selectFile(root, task):
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
		filename_show = setFilenameSize(FILE, 70)
		Label(root, text=filename_show, font=("Arial", 14), background="lightblue").place(x=200, y=225)
	else:
		FILE = ""


def saveFileWhere(root, task):
	"""
	:param root: object
	:param task: encrypt or decrypt
	:return: (bool, str or None)
	used to select an output file
	"""
	if task == "e":
		FILE_SAVE = filedialog.asksaveasfilename(initialdir="~", defaultextension=".encrypted", filetypes=(ENCRYPTED_FILES,))
	if task == "d":
		FILE_SAVE = filedialog.asksaveasfilename(initialdir="~", defaultextension=".decrypted", filetypes=(DECRYPTED_FILES,))
	FILE_SAVE = os.path.join(FILE_SAVE)
	if FILE_SAVE:
		if createFile(FILE_SAVE) != True:
			return False,
		else:
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
		content = readFile(filename)
		encrypted_content = encrypt(content, password, IV, mode)
		where_to_save = saveFileWhere(root, "e")
		encryptFileWindow(root, regist)
		if where_to_save[0] == True:
			text = saveFile(encrypted_content, where_to_save[1])
			text_to_show = setFilenameSize(filename, 60)
			Label(root, text=text, background="white", borderwidth=5, font=("Arial", 14)).place(x=100, y=450)
			if regist:
				registLog(LOGS_FILE, OPTIONS[2] + text + f" (Password: {password})", PASSWORD)
		else:
			Label(root, text="Error creating the file", background="lightblue", fg="red", borderwidth=5, font=("Arial", 14, "bold")).place(x=200, y=450)
	elif not response:
		pass
	else:
		encryptFileWindow(root, regist)
		Label(root, text=response, background="lightblue", fg="red", borderwidth=5, font=("Arial", 14, "bold")).place(x=200, y=450)



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
	if response == True:
		content = readFile(filename)
		type = setTypeOfTheFile(content)
		decrypted_content = decrypt(content, password, IV, mode, type)
		if decrypted_content[1] == True:
			where_to_save = saveFileWhere(root, "d")
			if where_to_save[0] == True:
				text = saveFile(decrypted_content[0], where_to_save[1], False, type)
				text_to_show = setFilenameSize(text, n=60)
				Label(root, text=text_to_show, background="white", borderwidth=5, font=("Arial", 12)).place(x=200, y=450)
				if regist:
					registLog(LOGS_FILE, OPTIONS[0] + text + f" (Password: {password})", PASSWORD)
			else:
				Label(root, text="Error creating the file", background="white", borderwidth=5, font=("Arial", 12)).place(x=200, y=450)
		else:
			Label(root, text="Wrong Password", background="white", borderwidth=5, font=("Arial", 12)).place(x=200, y=450)
	elif not response:
		pass
	else:
		Label(root, text=response, background="white", borderwidth=5, font=("Arial", 12)).place(x=200, y=450)



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
			string_encrypted = encrypt(string.encode("utf8"), password, IV, mode)
			string_encrypted = b64encode(string_encrypted).decode("utf8")
			string_to_show = setFilenameSize(string_encrypted)
			Label(root, text=string_to_show, background="lightblue", fg="black", borderwidth=0, font=("Arial", 14, "bold")).place(x=100, y=500)
			if regist:
				registLog(LOGS_FILE, OPTIONS[3] + string_encrypted + f" (Password: {password})", PASSWORD)
			Button(root, text="Copy", command=lambda:copyToClip(root, string_encrypted)).place(x=150, y=550)
		else:
			Label(root, text="Must specefie a password", background="white", borderwidth=5, font=("Arial", 14, "bold")).place(x=100, y=500)


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
		string = isBase64(string)
		if not string:
			Label(root, text="Must be base64 string", background="white", borderwidth=5, font=("Arial", 12, "bold")).place(x=100, y=500)
		else:
			if password != "":
				try_to_decrypt = decrypt(string, password, IV, mode, "t")
				if try_to_decrypt[1]:
					string_decrypted = try_to_decrypt[0]
					string_to_show = setFilenameSize(string_decrypted)
					Label(root, text=string_to_show, fg="black", background="white", borderwidth=5, font=("Arial", 12, "bold")).place(x=100, y=500)
					if regist:
						registLog(LOGS_FILE, OPTIONS[1] + string_decrypted + f" (Password: {password})", PASSWORD)
					Button(root, text="Copy", command=lambda:copyToClip(root, string_decrypted)).place(x=150, y=550)
				else:
					Label(root, text=try_to_decrypt[0], fg="black", background="white", borderwidth=5, font=("Arial", 12, "bold")).place(x=100, y=500)
			else:
				Label(root, text="Must specefie a password", background="white", borderwidth=5, font=("Arial", 12, "bold")).place(x=100, y=500)



def copyToClip(root, text):
	"""
	:param root: object
	:param text: text to copy
	:return: None
	copy to clipboard
	"""
	root.clipboard_clear()
	root.clipboard_append(text)


def clearAllElements(root):
	"""
	:param root: object
	:return: None
	clear all elements in the object
	"""
	for child in root.winfo_children():
		child.destroy()


def multiUsedDivs(root, regist, height=350, width=290):
	"""
	:param root: object
	:param regist: bool
	:param height: height of logs button
	:return: (object, object)
	create multi used frames
	"""
	Label(root, text="Password", background="lightblue", borderwidth=0, font=("Arial", 16, "bold")).place(x=195, y=70)
	password = Entry(root, width=25, background="white", fg="black", font=("Arial", 16), show="*")
	password.place(x=100, y=120)
	variable = StringVar(root)
	variable.set("AES MODE_CBC")
	menu = OptionMenu(root, variable, "AES MODE_CBC")
	menu.place(x=500, y=120)
	Button(root, text="Main Menu", background="lightblue", fg="gray", font=("Arial", 14, "bold"), borderwidth=0, command=lambda:encryptWindow(root, regist)).place(x=0, y=0)
	if regist:
		Button(root, text="Logs", background="white", borderwidth=0, command=lambda:logsWindow(), width=15, font=("Arial", 14)).place(x=width, y=height)
	return password, variable


def encryptFileWindow(root, regist):
	"""
	:param root: object
	:param regist: bool (regist logs)
	:return: None
	display the encrypt file window
	"""
	global FILE
	clearAllElements(root)
	FILE = ""
	password, variable = multiUsedDivs(root, regist)
	Button(root, text="Select File", background="white", command=lambda:selectFile(root, task="e"), width=7, font=("Arial", 10)).place(x=100, y=225)
	root.bind("<Return>", lambda e:encryptFile(root, FILE, password.get(), IV, variable.get(), regist))
	Button(root, text="Encrypt File", background="white", command=lambda:encryptFile(root, FILE, password.get(), IV, variable.get(), regist), width=15, font=("Arial", 14)).place(x=290, y=300)



def decryptFileWindow(root, regist):
	"""
	:param root: object
	:param regist: bool (regist logs)
	:return: None
	display the decrypt file window
	"""
	clearAllElements(root)
	password, variable = multiUsedDivs(root, regist)
	Button(root, text="Select File", background="white", borderwidth=0, command=lambda:selectFile(root, task="d"), width=7, font=("Arial", 10)).place(x=100, y=225)
	root.bind("<Return>", lambda e:decodeFile(root, FILE, password.get(), IV, variable.get(), regist))
	Button(root, text="Decrypt File", background="white", borderwidth=0, command=lambda:decodeFile(root, FILE, password.get(), IV, variable.get(), regist), width=15, font=("Arial", 14)).place(x=290, y=300)


def encryptStringWindow(root, regist):
	"""
	:param root: object
	:param regist: bool (regist logs)
	:return: None
	display the encrypt string window
	"""
	clearAllElements(root)
	password, variable = multiUsedDivs(root, regist, 400, 310)
	Label(root, text="String", background="lightblue", borderwidth=0, font=("Arial", 16, "bold")).place(x=250, y=200)
	string = Entry(root, width=35, background="white", fg="black", font=("Arial", 16))
	string.place(x=100, y=250)
	root.bind("<Return>", lambda e:encodeString(root, string.get(), password.get(), IV, variable.get(), regist))
	Button(root, text="Encrypt String", background="white", command=lambda:encodeString(root, string.get(), password.get(), IV, variable.get(), regist), width=20, font=("Arial", 14)).place(x=290, y=350)


def decryptStringWindow(root, regist):
	"""
	:param root: object
	:param regist: bool (regist logs)
	:return: None
	display the decrypt string window
	"""
	global FILE
	clearAllElements(root)
	FILE = ""
	password, variable = multiUsedDivs(root, regist, 400, 310)
	Label(root, text="Encoded String", background="lightblue", borderwidth=0, font=("Arial", 16, "bold")).place(x=220, y=200)
	string = Entry(root, width=35, background="white", fg="black", font=("Arial", 16))
	string.place(x=100, y=250)
	root.bind("<Return>", lambda e:decodeString(root, string.get(), password.get(), IV, variable.get(), regist))
	Button(root, text="Decrypt String", borderwidth=0, background="white", command=lambda:decodeString(root, string.get(), password.get(), IV, variable.get(), regist), width=20, font=("Arial", 14)).place(x=290, y=350)


def encryptWindow(root, logs=True):
	"""
	:param root: object
	:param logs: bool (regist logs)
	:return: None
	display encrypt menu
	"""
	clearAllElements(root)
	root.unbind("<Return>")
	Label(root, text="Secure your Data", background="lightblue", fg="white", borderwidth=0, font=("Arial", 24, "bold", "italic")).place(x=280, y=50)
	Button(root, text="Encrypt File", command=lambda:encryptFileWindow(root, logs), width=20, background="white", fg="black", borderwidth=0, font=("Arial", 14)).place(x=100, y=150)
	Button(root, text="Decrypt File", command=lambda:decryptFileWindow(root, logs), width=20, background="white", fg="black", borderwidth=0, font=("Arial", 14)).place(x=100, y=220)
	Button(root, text="Encrypt String", command=lambda:encryptStringWindow(root, logs), width=20, background="white", fg="black", borderwidth=0, font=("Arial", 14)).place(x=500, y=150)
	Button(root, text="Decrypt String", command=lambda:decryptStringWindow(root, logs), width=20, background="white", fg="black", borderwidth=0, font=("Arial", 14)).place(x=500, y=220)
	if logs:
		Button(root, text="Profile", command=lambda:profileWindow(root), width=20, background="white", fg="black", borderwidth=0, font=("Arial", 14)).place(x=100, y=290)
		Button(root, text="Logs", command=lambda:logsWindow(), width=20, background="white", fg="black", borderwidth=0, font=("Arial", 14)).place(x=500, y=290)
	else:
		Label(root, text="Logs are disable! All passwords used to encrypt your data won't be save", fg="red", borderwidth=0, background="lightblue", font=("Arial", 14, "bold")).place(x=100, y=300)
	Button(root, text="Change User", command=lambda:loginWindow(root, 0), width=20, background="white", fg="black", borderwidth=0, font=("Arial", 14)).place(x=320, y=400)
	Button(root, text="GitHub", command=lambda:openInTheWeb(URLS[0]), width=20, background="lightblue", fg="black", borderwidth=0, font=("Arial", 14, "bold")).place(x=320, y=500)


def deleteUserWindow(root):
	"""
	:param root: object
	:return: None
	display the delete user confirmation window
	"""
	global delete_window
	try:
		delete_window.destroy()
	except:
		pass
	delete_window = Tk()
	delete_window.title("Delete")
	delete_window.geometry("400x200")
	delete_window.configure(background="lightblue")
	Label(delete_window, text="Are you sure? All logs will be deleted", background="lightblue").pack(pady=20)
	Button(delete_window, text="Yes", width=10,  command=lambda:deleteConfirmed(root), font=("Arial", 12)).pack()
	Button(delete_window, text="No", width=10, command=lambda:deleteRefused(root), font=("Arial", 12)).pack()
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
	try_delete_user = deleteUser(db, USERNAME)
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
		update_password = updatePassword(db, USERNAME, encryptPassword(password), encryptPassword(PASSWORD))
		if update_password == True:
			logs = readLog(LOGS_FILE)
			if logs:
				if len(logs) != 0:
					decoded_logs = decodeLogs(logs, PASSWORD)
					deleteFileContent(LOGS_FILE)
					for log in decoded_logs:
						registLog(LOGS_FILE, log, password)
			USERNAME = None
			PASSWORD = None
			LOGS_FILE = ""
			loginWindow(root, 0)
		else:
			Label(root, text=update_password, background="lightblue", borderwidth=0, fg="gray", font=("Arial", 14, "bold")).pack()
	else:
		Label(root, text=verify_password, background="lightblue", borderwidth=0, fg="gray", font=("Arial", 14, "bold")).pack()



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
		username_update = updateUsername(db, USERNAME, username, encryptPassword(PASSWORD))
		if username_update == True:
			Label(root, text="Username was Changed", background="lightblue", borderwidth=0, fg="gray", font=("Arial", 14, "bold")).pack()
			USERNAME = username
			LOGS_FILE = f"logs/{username}.log"
		else:
			Label(root, text=username_update, background="lightblue", borderwidth=0, fg="gray", font=("Arial", 14, "bold")).pack()
	else:
		Label(root, text=verify_username, background="lightblue", borderwidth=0, fg="gray", font=("Arial", 14, "bold")).pack()



def profileWindow(root):
	"""
	:param root: object
	:return: None
	display profile settings to update
	"""
	clearAllElements(root)
	Label(root, text=USERNAME, background="lightblue", fg="gray", font=("Arial", 16, "bold")).pack(pady=10)
	Label(root, text="Update your username", background="lightblue", borderwidth=0, fg="gray", font=("Arial", 16, "bold")).pack(pady=10)
	username = Entry(root, width=30, font=("Arial", 14))
	username.pack(pady=10)
	Button(root, text="Update Username", command=lambda:updateUsernameHandle(root, username.get()), width=15, font=("Arial", 14)).pack(pady=20)
	Label(root, text="Update your password", background="lightblue", borderwidth=0, fg="gray", font=("Arial", 16, "bold")).pack(pady=10)
	password = Entry(root, show="*", width=30, font=("Arial", 14))
	password.pack(pady=10)
	Button(root, text="Update Password", command=lambda:updatePasswordHandle(root, password.get()), width=15, font=("Arial", 14)).pack(pady=10)
	Button(root, text="Delete User", command=lambda:deleteUserWindow(root), width=15, font=("Arial", 14)).pack(pady=(50, 0))
	Button(root, text="Back", command=lambda:encryptWindow(root)).pack(pady=(50, 0))




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
		verify_password = verifyPass(db, username, encryptPassword(password))
		if verify_password == True:
			root.unbind("<Return>")
			encryptWindow(root)
			USERNAME = username
			PASSWORD = password
			LOGS_FILE = "logs/" + USERNAME + ".log"
		elif not verify_password:
			Label(root, text=f"Invalid creds", background="lightblue", borderwidth=0, font=("Arial", 14, "bold")).pack()
		else:
			Label(root, text=verify_password, background="lightblue", borderwidth=0, font=("Arial", 14, "bold")).pack()


def authenticateWindow(root, user):
	"""
	:param root: object
	:param user: username
	:return: None
	display the window to type the password
	"""
	clearAllElements(root)
	Label(root, text=f"Password for {user}", fg="gray", background="lightblue", borderwidth=0, font=("Arial", 20, "bold")).pack(pady=50)
	Label(root, text="Password", background="lightblue", borderwidth=0, font=("Arial", 16, "bold")).pack(pady=(0, 20))
	password = Entry(root, width=25, background="white", fg="black", font=("Arial", 16), show="*")
	password.pack(pady=(0, 50))
	root.bind("<Return>", lambda e:authenticate(root, user, password.get()))
	Button(root, text="Login", command=lambda:authenticate(root, user, password.get()), width=12, background="white", fg="black", borderwidth=0, font=("Arial", 14, "bold")).pack()
	Button(root, text="Change User", command=lambda:loginWindow(root, 0), width=12, background="lightblue",borderwidth=0, fg="gray", font=("Arial", 14, "bold")).pack(pady=(50, 50))


def dontHaveUser(root):
	"""
	:param root: object
	:return: None
	used to display create user and start information
	"""
	Button(root, text="Encrypt or Decrypt without a user", command=lambda:encryptWindow(root, False), background="white", fg="gray", borderwidth=0, font=("Arial", 14, "bold")).place(x=250, y=50)
	Label(root, text=f"Logs won't be saved", background="lightblue", borderwidth=0, fg="red", font=("Arial", 14, "bold")).place(x=320, y=100)
	Label(root, text=f"Logs keep the passwords used to encrypt your data", background="lightblue", borderwidth=0, fg="black", font=("Arial", 14, "bold")).place(x=190, y=150)
	path = os.getcwd()
	path = setFilenameSize(path, 60)
	Label(root, text=f"All users are only local, \nthat means they only exist in your computer, \nif you change computer you will need to export \nyour logs files saved on \n {path}\n /logs/<<username>>.log \n and create a user with the same password", background="lightblue", borderwidth=0, fg="red", font=("Arial", 14, "bold")).place(x=150, y=400)
	Button(root, text="Create a User to start", command=lambda:createUserWindow(root), fg="gray", bg="white", width=20, font=("Arial", 20, "bold")).place(x=250, y=250)


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
		Button(root, text=user, command=lambda user=user:authenticateWindow(root, user), width=10, height=4, background="white", fg="gray", font=("Arial", 20, "bold"), borderwidth=0).grid(row=row, column=cont, padx=(paddingx, 70), pady=(paddingy, 50))
		cont += 1
		if cont >= 2:
			row += 1
			cont = 0
	Button(root, text="+", command=lambda:createUserWindow(root), background="lightblue", fg="gray", borderwidth=0, font=("Arial", 100, "bold")).grid(row=row, column=cont, padx=(paddingx, 70), pady=(paddingy, 40))
	start += 3
	Button(root, text="Encrypt or Decrypt without a user", command=lambda:encryptWindow(root, False), background="gray", fg="white", borderwidth=0, font=("Arial", 14, "bold")).place(x=260, y=20)
	if len(all_users) - start > 0:
		Button(root, text="Next Page", command=lambda:loginWindow(root, start), background="lightblue", fg="gray", borderwidth=0, font=("Arial", 14, "bold")).place(x=620, y=550)
	if start > 3:
		Button(root, text="Previous Page", command=lambda:loginWindow(root, start - 6), background="lightblue", fg="gray", borderwidth=0, font=("Arial", 14, "bold")).place(x=470, y=550)
	return start


def loginWindow(root, start):
	global USERNAME, PASSWORD, LOGS_FILE
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
	clearAllElements(root)
	users = getUsers(db)
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
			createUser(db, username, encryptPassword(password))
			loginWindow(root, 0)
		else:
			Label(root, text=password_verify, background="lightblue", borderwidth=0, font=("Arial", 14, "bold")).place(x=260, y=400)
	else:
		Label(root, text=username_verify, background="lightblue", borderwidth=0, font=("Arial", 14, "bold")).place(x=260, y=400)


def createUserWindow(root):
	"""
	:param root: object
	:return: None
	display the create user window
	"""
	clearAllElements(root)
	Label(root, text="Username", background="lightblue", borderwidth=0, font=("Arial", 16, "bold")).place(x=350, y=70)
	username = Entry(root, width=25, background="white", fg="black", font=("Arial", 16))
	username.place(x=250, y=120)
	Label(root, text="Password", background="lightblue", borderwidth=0, font=("Arial", 16, "bold")).place(x=350, y=180)
	password = Entry(root, width=25, background="white", fg="black", font=("Arial", 16), show="*")
	password.place(x=250, y=230)
	root.bind("<Return>", lambda e: tryCreateUser(root, username.get(), password.get()))
	Button(root, text="Create User", command=lambda:tryCreateUser(root, username.get(), password.get()), background="white", fg="black", font=("Arial", 16, "bold")).place(x=330, y=310)
	Button(root, text="Back", command=lambda:loginWindow(root, 0), background="lightblue", fg="gray", borderwidth=0, font=("Arial", 14, "bold")).place(x=360, y=500)


def setThingsToInitializeTheProgram():
	"""
	:return: bool
	used to see if the database already exists if not creates one
	"""
	if not fileExist(db):
		create_db = createDB(db)
		if createDB(db) == True:
			return True,
		else:
			return False, create_db
	else:
		return True,


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
	error_window = Tk()
	root.title("Error")
	root.resizable(width=False, height=False)
	root.configure(background="lightblue")
	Label(error_window, text=error)
	root.mainloop()


def createScrollbar(root):
	"""
	:param root: object
	:return: None
	create a scrollbar
	"""
	canvas = Canvas(root, background="lightblue")
	canvas.pack(side=LEFT, fill=BOTH, expand=1)
	scroll_bar = Scrollbar(root, orient=VERTICAL, command=canvas.yview)
	canvas.configure(yscrollcommand=scroll_bar.set)
	scroll_bar.pack(side=RIGHT, fill=Y)
	canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
	frame = Frame(canvas, background="lightblue")
	canvas.create_window((0, 0), window=frame, anchor="nw")
	return frame



def displayTheLogs(root, logs, string):
	"""
	:param root: object
	:param logs: logs encoded
	:param string: str (used to show only a type of logs)
	:return: None
	used to display the logs
	"""
	clearAllElements(root)
	Button(root, text="Back", command=lambda:logsWindow(False)).pack()
	Label(root, text="Logs", background="lightblue", borderwidth=0, font=("Arial", 14, "bold")).pack(pady=10)
	frame = createScrollbar(root)
	if logs:
		logs_to_show = []
		logs = decodeLogs(logs, PASSWORD)
		logs = logs[::-1]
		for log in logs:
			if string == "*":
				logs_to_show.append(log)
			else:
				if log[0:len(string):1] == string:
					logs_to_show.append(log)
		cont = 0
		for log in logs_to_show:
			Label(frame, text=log, background="lightblue", borderwidth=0, font=("Arial", 14)).pack(pady=5)
			cont += 1



def placeLogsButtons(logs_window, logs):
	"""
	:param logs_window: object
	:param logs: encoded logs
	:return: None
	used to place the buttons in logs window
	"""
	Button(logs_window, command=lambda:displayTheLogs(logs_window, logs, "*"), text="All Logs", width=15).pack(pady=20)
	Button(logs_window, command=lambda:displayTheLogs(logs_window, logs, OPTIONS[2]), text="Encrypt File Logs", width=15).pack(pady=20)
	Button(logs_window, command=lambda:displayTheLogs(logs_window, logs, OPTIONS[3]), text="Encrypt String Logs", width=15).pack(pady=20)
	Button(logs_window, command=lambda:displayTheLogs(logs_window, logs, OPTIONS[0]), text="Decrypt File Logs", width=15).pack(pady=20)
	Button(logs_window, command=lambda:displayTheLogs(logs_window, logs, OPTIONS[1]), text="Decrypt Strings Logs", width=15).pack(pady=20)


def logsWindow(reload=True):
	"""
	:param reload: bool
	:return: None
	used to display the logs options
	"""
	logs = readLog(LOGS_FILE)
	if reload:
		# When click
		global logs_window
		try:
			logs_window.destroy()
		except:
			pass
		logs_window = Tk()
		logs_window.title("Logs")
		logs_window.geometry("600x400")
		logs_window.configure(background="lightblue")
		placeLogsButtons(logs_window, logs)
		logs_window.mainloop()
	else:
		# When click on back button
		clearAllElements(logs_window)
		placeLogsButtons(logs_window, logs)


if __name__ == "__main__":
	root = Tk() # Call the object
	root.title("Encrypt or Decrypt") # Set the title
	root.geometry("800x600") # Set the geometry
	root.resizable(width=False, height=False) # Don't allow to resize
	root.configure(background="lightblue") # Set background to lightblue
	things_to_set = setThingsToInitializeTheProgram() # Call the initialize settings
	if things_to_set[0] == True:
		loginWindow(root, 0) # Call the login window
	else:
		error = things_to_set[1]
		errorWindow(error) # Call the error window
	root.mainloop() # Keep window open
