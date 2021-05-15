try:
    from config.config import *
    import os
except Exception as e:
    print("[EXCEPTION] ", e)
    exit()


class File():
    def exits(filename):
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


    def readB(filename):
        """
        :param filename: filename
        :return: bytes or string
        read bytes from a file
        """
        try:
            a = open(filename, "rb").read()
        except:
            return TEXTS[56]
        else:
            return a


    def read(filename, readlines=False, is_first=False):
        """
        :param filename: filename
        :return: list or error
        read text from a file
        """
        try:
            a = open(filename, "rt")
        except Exception as e:
            if is_first:
                return "[EXCEPTION] " + e
            return TEXTS[56]
        else:
            if readlines:
                return a.readlines()
            else:
                return a.read()


    def create(filename, is_first=False):
        """
        :param filename: filename
        :return: bool or string
        create a file
        """
        try:
            a = open(filename, "wt+")
        except Exception as e:
            if is_first:
                return "[EXCEPTION] " + e
            return TEXTS[57]
        else:
            return True


    def writeB(content, filename):
        """
        :param content: bytes
        :param filename: filename
        :return: str
        write bytes in a file
        """
        try:
            a = open(filename, "wb")
        except:
            return TEXTS[58]
        else:
            a.write(content)
            return TEXTS[59] + filename


    def write(content, filename):
        """
        :param content: string
        :param filename: filename
        :return: str
        write bytes in a file
        """
        try:
            a = open(filename, "at")
        except:
            return TEXTS[58]
        else:
            a.write(f"{content}\n")
            return TEXTS[59] + filename


    def save(content, filename, to_encrypt=True, type=None):
        """
        :param content: str or bytes
        :param filename: filename
        :param to_encrypt: bool
        :param type: str (t or b)
        :return: string
        save the content in a file
        """
        if to_encrypt == True or type == "b":
            return File.writeB(content, filename)
        else:
            return File.write(content, filename)


    def delCont(filename):
        """
        :param filename: filename
        :return: None or error
        delete content from a file
        """
        try:
            a = open(filename, "wt")
        except Exception as e:
            return f"[EXCEPTION] {e}"


    def getExt(filename):
        """
        :param filename: filename
        :return: str
        gets the filename extension
        """
        extension = filename[filename.rfind(".")::1]
        return extension

    
    def setType(content):
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
