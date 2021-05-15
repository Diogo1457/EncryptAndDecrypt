try:
    from utils.settings import Settings
    from utils.json_handle import Json
    import os
except Exception as e:
    print("[EXCEPTION] ", e)
    exit()


Settings.changeProgramExec()

JSON_FILE = "config/variables.json"
LANGUAGES_FILE = "config/languages.json"
JSON_CONTENT = Json.read(JSON_FILE)
TEXTS = Json.read(LANGUAGES_FILE)["english"]


VARIABLES = JSON_CONTENT["configs"]
TT = VARIABLES["title"]
FG = VARIABLES["font-color"]
FONT = VARIABLES["normal-font"]
SFONT = VARIABLES["small-font"]
BFONT = VARIABLES["big-font"]
BG = VARIABLES["background"]
BG_B = VARIABLES["background-button"]
RS = VARIABLES["resolution"]
SB = VARIABLES["selected-button"]
BW = VARIABLES["border-width"]
BTW = VARIABLES["button-width"]
LT = VARIABLES["logs-title"]
LR = VARIABLES["logs-resolution"]
DR = VARIABLES["del-resolution"]
EFONT = VARIABLES["error-font"]
FONT_W = VARIABLES["normal-font-no-bold"]
SM_FONT_W = VARIABLES["smaller-font-no-bold"]
SFONT_W = VARIABLES["small-font-no-bold"]
BFONT_W = VARIABLES["big-font-no-bold"]
BG_FONT = VARIABLES["bigger-font"]
HFONT = VARIABLES["huge-font"]
BFONT_I = VARIABLES["big-font-italic"]
LB_BG = VARIABLES["login-button-background"]
PN_BG = VARIABLES["prev-next-background"]
B_FG = VARIABLES["button-font-color"]


ALL_FILES = ("All Files", "*.*") # All files tuple
ENCRYPTED_FILES = ("Encrypted Files", "*.encrypted") # encrypted files tuple
DECRYPTED_FILES = ("Decrypted Files", "*.decrypted") # decrypted files tuple

OPTIONS = ["Decrypted File - ", "Decrypted String - ", "Encrypted File - ", "Encrypted String - "] # types of files

URLS = ["https://github.com/Diogo1457"] # Urls

DB = "dataBase/users.db" # dataBase

IV = b'al\x82-\xe3\x95]N\xda\xda\x83\xd8\xd8}\xcde' # Initial Vector
