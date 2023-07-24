import tkinter
import tkinter.filedialog
import os

def findFolder(textField: tkinter.Entry):
    """
    Literally just prompts the user to pick a folder and replaces
    the text of a chosen tkinter entry lmao.
    
    Parameters:
        textField (tkinter.Entry) - the Entry to have its text modified
    """

    path = tkinter.filedialog.askdirectory(initialdir="C:\\", title="Pick your Oculus folder").replace("/", "\\")
    
    textField.delete(0, tkinter.END)
    textField.insert(0, path)