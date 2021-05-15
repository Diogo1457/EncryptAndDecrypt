try:
    import json
except Exception as e:
    print("[EXCEPTION] ", e)
    exit()



class Json():
    def write(_filename, _content, _alarms):
        try:
            _alarms.append(_content)
            _content = json.dumps(_alarms, indent=2)
        except Exception as e:
            _content = json.dumps([_content], indent=2)
        File.write(_filename, _content)
        _content = File.read(_filename)
        _alarms = json.loads(_content)
        return _alarms


    def remove(_filename, c, _alarms):
        _alarms.pop(c)
        _content = json.dumps(_alarms, indent=2)
        File.write(_filename, _content)
        _content = File.read(_filename)
        _alarms = json.loads(_content)
        return _alarms


    def edit(_filename, c, value, key, _alarms):
        _alarms[c][key] = value
        _content = json.dumps(_alarms, indent=2)
        File.write(_filename, _content)
        _content = File.read(_filename)
        _alarms = json.loads(_content)
        return _alarms


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


    def readF(filename):
        """
        :param filename: filename
        :return: list or error
        read text from a file
        """
        try:
            a = open(filename, "rt")
        except Exception as e:
            return "[EXCEPTION] " + e
        else:
            return a.read()


    def createF(filename):
        try:
            a = open(filename, "wt+")
        except Exception as e:
            return "[EXCEPTION] " + e
        else:
            return True


    def read(_filename, _create=False):
        if not Json.exits(_filename):
            if _create:
                Json.createF(_filename)
            return []
        else:
            _content = Json.readF(_filename)
            try:
                _json = json.loads(_content)
            except Exception as e:
                print("[EXCEPTION] ", e)
                return []
            else:
                return _json
