import tkinter
import tkinter.filedialog
import os

def findFile(textField: tkinter.Entry, fileFormats: tuple, fileTypeReq: str = "generic"):
    """
    Prompts the user to pick a file, replaces a chosen tkinter Entry's content with the path

    Args:
        textField (tkinter.Entry) - Chosen entry
        fileFormats (tuple) - List of file formats, should be written in accordance to tkinter's neeeds
        fileTypeReq (str) - What type of file are you looking for? findFile() will take the argument and set the window title accordingly
    """
    prompt = None
    
    match fileTypeReq: # Can add more prompts later down the line
        case "texture":
            prompt = "Pick a texture"

    path = tkinter.filedialog.askopenfilename(initialdir=os.getcwd(), title=prompt, filetypes=fileFormats).replace('/', '\\')
    
    textField.delete(0, tkinter.END)
    textField.insert(0, path)