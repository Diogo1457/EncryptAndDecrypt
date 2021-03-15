try:
    from Crypto.Cipher import AES
    from hashlib import sha256, sha512
    from utils.utils import *
except Exception as e:
	print("[EXCEPTION] ", e)
	exit()


IV = b'al\x82-\xe3\x95]N\xda\xda\x83\xd8\xd8}\xcde' # Initial Vector

modes = {
    "AES MODE_CBC": AES.MODE_CBC
} #Encryption Modes


def contentLen(content):
    """
    :param content: bytes
    :return: bytes
    set the len of content to a multiple of 16
    """
    while len(content) % 16 != 0:
        content += " ".encode("utf8")
    return content


def encrypt(content, password, IV, mode):
    """
    :param content: bytes
    :param password: password
    :param IV: initial vector
    :param mode: type of encryption
    :return: bytes
    encrypt the content
    """
    mode = modes[mode]
    password = sha256(password.encode("utf8")).digest()
    content = contentLen(content)
    cipher = AES.new(password, mode, IV)
    encrypted = cipher.encrypt(content)
    return encrypted.rstrip()


def decrypt(content, password, IV, mode, type):
    """
    :param content: bytes
    :param password: password
    :param IV: initial vector
    :param mode: type of encryption
    :param type: str (t or b)
    :return: (string or bytes, bool)
    decrypt the content
    """
    mode = modes[mode]
    password = sha256(password.encode("utf8")).digest()
    content = contentLen(content)
    cipher = AES.new(password, mode, IV)
    try:
        decrypted = cipher.decrypt(content)
        if type == "b":
            decrypted = (decrypted.rstrip(), True)
        if type == "t":
            decrypted = (decrypted.rstrip().decode("utf8"), True)
    except Exception as e:
        decrypted = ("Wrong Password", False)
    return decrypted


def encryptPassword(password):
    """
    :param password: password
    :return: str
    encrypt the main password
    """
    for c in range(500):
        password = sha512(password.encode("utf8")).hexdigest()
    return password
