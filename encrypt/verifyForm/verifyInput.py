from utils.utils import *



def decryptOrEncrypt(extension, type):
    """
    :param extension: str
    :param type: str (d or e)
    :return: str or True
    check if the file is to encrypt or to decrypt
    """
    if type == "d":
        if extension == ".encrypted":
            return True
        else:
            return "Invalid Extension"
    else:
        if extension != ".encrypted":
            return True
        else:
            return "Already Encrypted"


class VerifyInput:
    def __init__(self, filename, password, type):
        """
        :param self: object
        :param filename: filename
        :param password: password
        :param type: str (d or e)
        :return: None
        initialize the class
        """
        self.filename = filename
        self.password = password
        self.type = type


    def verifyInput(self):
        """
        :param self: object
        :return: str or bool
        check if the file, password and extension are correct
        """
        if self.filename != "" and self.filename != None:
            if self.password != "":
                extension = getFileExtension(self.filename)
                if fileExist(self.filename):
                    return decryptOrEncrypt(extension, self.type)
                else:
                    return "File does not exist"
            else:
                return "Must specefie a password"
        else:
            return False
