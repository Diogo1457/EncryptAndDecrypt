try:
    from dataBase.database import *
    import os
    from sys import argv
    import webbrowser
except Exception as e:
    print("[EXCEPTION] ", e)
    exit()


class Settings():
    def changeProgramExec():
        try:
            _path = os.path.dirname(argv[0])
            _path = os.path.join(_path)
            os.chdir(_path)
        except:
            _path = argv[0]
        return _path


    def setThingsToInitializeTheProgram(db):
        """
        :return: bool
        used to see if the database already exists if not creates one
        """
        if not Json.exits(db):
            create_db = Database.create(db)
            if Database.create(db) == True:
                return True,
            else:
                return False, create_db
        else:
            return True,


    def openInTheWeb(url):
        """
        :param url: website url
        :return: None
        Open website on default browser
        """
        webbrowser.open(url)
