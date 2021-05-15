try:
    from utils.utils import *
    from encrypt.encrypt import Encrypt
    from base64 import b64encode, b64decode
except Exception as e:
    print("[EXCEPTION] ", e)
    exit()


class Logs():
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
            log = Encrypt.decrypt(log, password, IV, "AES MODE_CBC", "t")
            if log[1] == True:
                logs_decoded.append(log[0])
            else:
                logs_decoded.append(TEXTS[61])
        return logs_decoded


    def reg_log(filename, content, password):
        """
        :param filename: filename
        :param content: string
        :param password: password
        :return: error or None
        regist the logs
        """
        if Logs.createLog(filename):
            content = content
            content = Encrypt.encrypt(content.encode("utf8"), password, IV, "AES MODE_CBC")
            content = b64encode(content).decode("utf8")
            File.write(content, filename)
        else:
            return TEXTS[60]


    def readLog(filename):
        """
        :param filename: filename
        :return: list or None
        read content from the log file
        """
        if File.exits(filename):
            content = File.read(filename, True)
            return content
        else:
            Logs.createLog(filename)


    def createLog(filename):
        """
        :param filename: filename
        :return: bool
        create the log file
        """
        if not File.exits(filename):
            try:
                os.mkdir("logs")
            except:
                pass
            if File.create(filename):
                return True
            else:
                return False
        else:
            return True


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
