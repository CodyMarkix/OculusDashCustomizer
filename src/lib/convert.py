import tkinter
import tkinter.messagebox
from PIL import Image
import dds

def convertToPNG(fp: str):
    newpath = '\\'.join(fp.split("\\")[:-1]) + "\\" + fp.split("\\")[-1].split(".")[0] + ".png" # Path contining OG file + OG file name with no extension + .dds extension
    img = dds.decode_dds(fp)
    img.save(newpath, format='PNG')
    tkinter.messagebox.showinfo("Success", "Converted " + fp.split("\\")[-1] + " to " + fp.split("\\")[-1].split(".")[0] + ".png!")

def convertToDDS(fp: str):
    newpath = '\\'.join(fp.split("\\")[:-1]) + "\\" + fp.split("\\")[-1].split(".")[0] + ".dds" # Path contining OG file + OG file name with no extension + .dds extension
    img = Image.open(fp, 'r')
    img.save(newpath, format='PNG')
    tkinter.messagebox.showinfo("Success", "Converted " + fp.split("\\")[-1] + " to " + fp.split("\\")[-1].split(".")[0] + ".dds!")