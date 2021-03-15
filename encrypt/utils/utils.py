try:
    from encrypt import *
    from base64 import b64encode, b64decode
    import os
except Exception as e:
    print("[EXCEPTION] ", e)



ALL_FILES = ("All Files", "*.*") # All files tuple
ENCRYPTED_FILES = ("Encrypted Files", "*.encrypted") # encrypted files tuple
DECRYPTED_FILES = ("Decrypted Files", "*.decrypted") # decrypted files tuple
OPTIONS = ["Decrypted File - ", "Decrypted String - ", "Encrypted File - ", "Encrypted String - "] # types of files
URLS = ["https://github.com/Diogo1457"] # Urls

IV = b'al\x82-\xe3\x95]N\xda\xda\x83\xd8\xd8}\xcde' # Initial Vector

def fileExist(filename):
    """
    :param filename: filename
    :return: bool
    verify if the file exist
    """
    try:
        a = open(filename, "rb")
    except:
        return False
    else:
        return True


def readFile(filename):
    """
    :param filename: filename
    :return: bytes or string
    read bytes from a file
    """
    try:
        a = open(filename, "rb").read()
    except:
        return "Error reading the file"
    else:
        return a


def createFile(filename):
    """
    :param filename: filename
    :return: bool or string
    create a file
    """
    try:
        a = open(filename, "wt+")
    except Exception as e:
        print("[EXCEPTION] ", e)
        return "Error creating the file"
    else:
        return True


def writeBytes(content, filename):
    """
    :param content: bytes
    :param filename: filename
    :return: str
    write bytes in a file
    """
    try:
        a = open(filename, "wb")
    except:
        return "Error saving the file"
    else:
        a.write(content)
        return f"File {filename} created"


def writeText(content, filename):
    """
    :param content: string
    :param filename: filename
    :return: str
    write bytes in a file
    """
    try:
        a = open(filename, "at")
    except:
        return "Error saving the file"
    else:
        a.write(f"{content}\n")
        return f"File {filename} created"


def setFilenameSize(string, n=50):
	"""
	:param string: str to short
	:param n: number to short
	:return: string
	short a string, used to display long strings
	"""
	cut_string = ""
	if len(string) > 50:
		if n > len(string):
			n = len(string)
		cut_string = string[:n:1]
		if cut_string != string:
			cut_string += "..."
	else:
		cut_string = string
	return cut_string


def saveFile(content, filename, to_encrypt=True, type=None):
    """
    :param content: str or bytes
    :param filename: filename
    :param to_encrypt: bool
    :param type: str (t or b)
    :return: string
    save the content in a file
    """
    if to_encrypt == True or type == "b":
        return writeBytes(content, filename)
    else:
        return writeText(content, filename)


def createFileLog(filename):
    """
    :param filename: filename
    :return: bool
    create the log file
    """
    if not fileExist(filename):
        try:
            os.mkdir("logs")
        except:
            pass
        if createFile(filename):
            return True
        else:
            return False
    else:
        return True


def registLog(filename, content, password):
    """
    :param filename: filename
    :param content: string
    :param password: password
    :return: error or None
    regist the logs
    """
    if createFileLog(filename):
        content = content
        content = encrypt(content.encode("utf8"), password, IV, "AES MODE_CBC")
        content = b64encode(content).decode("utf8")
        writeText(content, filename)
    else:
        return "Error creating the log"


def readText(filename):
    """
    :param filename: filename
    :return: list or error
    read text from a file
    """
    try:
        a = open(filename, "rt").readlines()
    except:
        return "Error reading the file"
    else:
        return a


def readLog(filename):
    """
    :param filename: filename
    :return: list or None
    read content from the log file
    """
    if fileExist(filename):
        content = readText(filename)
        return content
    else:
        createFileLog(filename)


def deleteFileContent(filename):
    """
    :param filename: filename
    :return: None or error
    delete content from a file
    """
    try:
        a = open(filename, "wt")
    except Exception as e:
        return f"[EXCEPTION] {e}"


def decodeLogs(logs, password):
    """
    :param logs: list
    :param password: password
    :return: list
    decode the logs
    """
    logs_decoded = []
    for log in logs:
        log = b64decode(log)
        log = decrypt(log, password, IV, "AES MODE_CBC", "t")
        if log[1] == True:
            logs_decoded.append(log[0])
        else:
            logs_decoded.append("Error decoding the log")
    return logs_decoded


def isBase64(string):
    """
    :param string: base64 input
    :return: str or False
    check if a string is base64
    """
    try:
    	string = b64decode(string.encode("utf8"))
    except:
    	return False
    else:
    	return string


def setTypeOfTheFile(content):
	"""
	:param content: str
	:return: str
	used to see if the file is in plain text or in bytes
	"""
	try:
		content.decode("utf8")
	except AttributeError:
		type = "t"
	except:
		type = "b"
	else:
		type = "b"
	return type


def getFileExtension(filename):
    """
    :param filename: filename
    :return: str
    gets the filename extension
    """
    extension = filename[filename.rfind(".")::1]
    return extension
