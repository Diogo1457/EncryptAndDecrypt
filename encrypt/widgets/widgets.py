from tkinter import *
from config.config import *



def copyToClip(_root, _text):
    """
    :param _root: object
    :param _text: text to copy
    :return: None
    copy to clipboard
    """
    _root.clipboard_clear()
    _root.clipboard_append(_text)


def clearAllElements(_root):
    """
    :param _root: object
    :return: None
    clear all elements in the object
    """
    for _child in _root.winfo_children():
        _child.destroy()


def displayText(_root, _text, _x=None, _y=None, _fg=FG, _bg=BG, _hb=BG, _bw=BW, _font=FONT, _place=True):
    _label = Label(_root, 
    text=_text, 
    fg=_fg, 
    font=_font, 
    background=_bg, 
    borderwidth=_bw,
    highlightbackground=_hb
    )
    if _place:
        _label.place(x=_x, y=_y)
    return _label


def displayEntry(_root, _x=None, _y=None, _width=EW, _font=FONT, _bg=BG_B, _fg=FG, _bw=BW, _hb=BG, _place=True, _show=None):
    _entry = Entry(_root, 
    width=_width, 
    font=_font, 
    bg=_bg,
    fg=_fg,
    borderwidth=_bw, 
    highlightbackground=_hb,
    show=_show
    )
    if _place:
        _entry.place(x=_x, y=_y)
    return _entry


def displayButton(_root, _text, _command, _x=None, _y=None, _fg=B_FG, _font=FONT, _bw=BW, _hb=BG, _bg=BG, _height=None, _width=None, _place=True):
    _button = Button(_root,
    text=_text, 
    command=_command, 
    font=_font,
    bg=_bg,
    fg=_fg, 
    borderwidth=_bw,
    height=_height,
    width=_width, 
    highlightbackground=_hb)
    if _place:
        _button.place(x=_x, y=_y)
    return _button


def createScrollbar(_root):
    """
    :param _root: object
    :return: None
    create a scrollbar
    """
    _canvas = Canvas(_root, background=BG, highlightbackground=BG) 
    _canvas.pack(side=LEFT, fill=BOTH, expand=1, pady=(0, 100))
    _scroll_bar = Scrollbar(_root, orient=VERTICAL, command=_canvas.yview)
    _canvas.configure(yscrollcommand=_scroll_bar.set)
    _scroll_bar.pack(side=RIGHT, fill=Y)
    _canvas.bind("<Configure>", lambda e: _canvas.configure(scrollregion=_canvas.bbox("all")))
    _frame = Frame(_canvas, background=BG, highlightbackground=BG)
    _canvas.create_window((0, 0), window=_frame, anchor="nw")
    return _frame


def createRootWindow(_title, _size=None, _bg=BG, _resizable=(False, False)):
	root_window = Tk()
	root_window.title(_title)
	root_window.resizable(width=_resizable[0], height=_resizable[1])
	if _size:
		root_window.geometry(_size)
	root_window.configure(bg=_bg)
	return root_window
