import ctypes, sys
import os
import tkinter
from PIL import Image
import dds
import re

# Importing tkinter modules
import tkinter.colorchooser
import tkinter.filedialog
import tkinter.messagebox
import tkinter.ttk

from lib.findFile import findFile
from lib.findFolder import findFolder
import lib.errors

# |-----------------|
# | PERMISSION FUNC |
# |-----------------|

def checkPerms():
    try:
        # Check if the user currently has elevated permissions/the user is Administrator
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        # Return false if not
        return False

# |----------------------|
# | OCULUS RELATED FUNCS |
# |----------------------|

def getOculusPath():
    oculusPathWin = tkinter.Toplevel(tk)
    tk.resizable(False, False)
    oculusPathWin.transient(tk)
    oculusPathWin.attributes('-topmost', True)
    oculusPathWin.grab_set()

    msg = tkinter.Label(oculusPathWin, text="Enter your Oculus software's path")
    oculuspathprompt = tkinter.Entry(oculusPathWin, width=25); oculuspathprompt.insert(0, "C:\\Program Files\\Oculus")
    explore = tkinter.Button(oculusPathWin, text="Browse", command=lambda: findFolder(oculuspathprompt))
    confirm = tkinter.Button(oculusPathWin, text="Confirm", command=lambda: confirmPath(oculuspathprompt.get(), oculusPathWin))

    oculusPathWin.protocol("WM_DELETE_WINDOW", lambda: sys.exit(0))

    msg.pack()
    oculuspathprompt.pack()
    explore.pack()
    confirm.pack()

def confirmPath(writtenPath: str, root: tkinter.Toplevel or tkinter.Tk):
    global oculusPath
    oculusPath = writtenPath
    root.grab_release()
    root.destroy()

# |--------------|
# | MODDING FUNC |
# |--------------|

def saveMods(elements: list):
    # Creates an index of textures,
    # containing their type, location and format
    textureindex = {}
    for x in elements:
        textureindex.update(x)
    
    try:
        for x in textureindex:
            # Eliminate empty prompts from the modification
            if textureindex[x][0] == "":
                continue
            else:
                # Check the iterable's image format
                match textureindex[x][1]:
                    case "dds":
                        # Copy over the original file 
                        with open(textureindex[x][0], 'rb') as f:
                            with open(f'{oculusPath}\\{locationIndex[x]}', 'wb') as target:
                                target.write(f.read())
                                target.close()
                            f.close()
                        tkinter.messagebox.showinfo("Success", "Done! Put on your Rift/start Oculus Link to see the changes.")
                    
                    case "png":
                        # Convert the image from PNG to DDS
                        img = Image.open(textureindex[x][0], 'r')
                        img.save(f'{oculusPath}\\{locationIndex[x]}', format='DDS')
                        tkinter.messagebox.showinfo("Success", "Done! Put on your Rift/start Oculus Link to see the changes.")

    except Exception as err:
        tkinter.messagebox.showerror("Error!", f"There was an issue!\n{err}")

# |------------------|
# | CONVERTING FUNCS |
# |------------------|

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

# |-------------------------------------------|
# | UNUSED FUNCS - Will be used down the line |
# |-------------------------------------------|

def changeFogColor(color: tuple):
    with open(f'{oculusPath}\\Support\\oculus-dash\\dash\\data\\shaders\\theVoid\\theVoidUniforms.glsl', 'rw') as f:
        contents = f.read()
        replacement = re.sub("vec3\\s+u_voidFogColor\\s*=\\s*\\{[^}]+\\};", "vec3 u_voidFogColor = {" + str(color[0] / 255) + ", " + str(color[1] / 255) + ", " + str(color[2] / 255) + "};", contents)
        f.write(replacement)

def isCorrectSize(img: Image.Image):
    # Checks if the size of an image is 1024p (the size of the Oculus Dash's void textures)
    if img.size == (1024, 1024):
        return True
    else:
        raise lib.errors.InvalidSizeException

# |-----------|
# | MAIN FUNC |
# |-----------|

def main():
    # Verify the user has perms
    if True:
        # Set the icon and title for the main program
        icon = tkinter.PhotoImage(file=os.path.abspath(".\\assets\\ico\\icon.png"));
        tk.iconphoto(False, icon)
        tk.wm_title("Oculus Dash Customizer")

        getOculusPath()

        modifyTab = tkinter.ttk.Frame(tabIndex); tabIndex.add(modifyTab, text='Customize')
        convertTab = tkinter.ttk.Frame(tabIndex); tabIndex.add(convertTab, text='Convert')

        # TODO: Refactor this bullshit
        img6CustomText = tkinter.Label(modifyTab, text="Floor grid (grid_plane_006)")
        img6CustomPath = tkinter.Entry(modifyTab, width=50)
        img6CustomBtn = tkinter.Button(modifyTab, text="Browse", command=lambda: findFile(img6CustomPath, (("DirectDraw Surface (DDS)", "*.dds"), ("Portable Network Graphic (PNG)", "*.png")), "texture"))
        
        savebtn = tkinter.Button(modifyTab, text="Save Changes", command=lambda: saveMods([
                                                                                        { "grid_plane_006": (img6CustomPath.get(), img6CustomPath.get().split(".")[-1]) } # This is the best I can do right now
                                                                                        ]))
        
        quitbtn = tkinter.Button(modifyTab, text="Quit program", command=tk.quit)


        convertPngText = tkinter.Label(convertTab, text="Convert PNG to DDS")
        convertPngPath = tkinter.Entry(convertTab, width=50)
        convertPngBtn = tkinter.Button(convertTab, text="Browse", command=lambda: findFile(convertPngPath, (("Portable Network Graphic (PNG)", "*.png"), ("All files", "*.*")), "texture"))
        confirmPngConvert = tkinter.Button(convertTab, text="Convert to DDS", command=lambda: convertToDDS(convertPngPath.get()))
        quitbtnConvert = tkinter.Button(convertTab, text="Quit program", command=tk.quit)


        tabIndex.pack(expand=True, fill="both")

        img6CustomText.grid(row=1, column=1, padx=10)
        img6CustomPath.grid(row=1, column=2)
        img6CustomBtn.grid(row=1, column=3, padx=10)

        savebtn.grid(row=2, column=2)
        quitbtn.grid(row=3, column=2)

        convertPngText.grid(row=1, column=1, padx=10)
        convertPngPath.grid(row=1, column=2)
        convertPngBtn.grid(row=1, column=3, padx=10)
        confirmPngConvert.grid(row=2, column=2)
        
        quitbtnConvert.grid(row=3, column=2)

        tk.mainloop()
    else:
        # Creates a new process of itself with admin privileges and quits the unprivileged version
        # (kinda like society, huh? /j)
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, os.path.abspath(sys.argv[0]), ' '.join(sys.argv[1:]), 1)
        sys.exit(0)
        return 1
    
    return 0
    
if __name__ == '__main__':
    tk = tkinter.Tk()
    tk.resizable(False, False) # Width, Height
    tabIndex = tkinter.ttk.Notebook(tk)

    locationIndex = {
        "grid_plane_006": "Support\\oculus-dash\\dash\\assets\\raw\\textures\\environment\\the_void\\grid_plane_006.dds"
    }

    if 'wartortle.png' not in os.listdir('assets'): # All praise the wartortle
        sys.exit(1)
    else:
        if 'nt' not in os.name:
            input("[ERROR] This program runs only on Windows!") # Everyday I pray for Meta to release the Oculus software on Linux
        else:
            main()