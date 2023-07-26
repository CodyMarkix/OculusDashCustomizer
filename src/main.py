import ctypes, sys
import os
import tkinter
from PIL import Image
import re

# Importing tkinter modules
from tkinter import ttk # Such pretty widgets! *anime wow sound effect*
import tkinter.colorchooser
import tkinter.filedialog
import tkinter.messagebox

from lib.findFile import findFile
from lib.findFolder import findFolder
from lib.convert import convertToDDS, convertToPNG
from lib.themeCheck import isDarkModeEnabled
from lib.fetch import fetchTheme
from lib.dataManiuplation import strToTuple
from lib.backupTools import backupFile
import lib.errors

# |-----------------|
# | PERMISSION FUNC |
# |-----------------|

def checkPerms(debug=False):
    if not debug:
        try:
            # Check if the user currently has elevated permissions/the user is Administrator
            return ctypes.windll.shell32.IsUserAnAdmin()
        except Exception:
            # Return false if not
            return False
    else:
        return True

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

def modTexture(texture):
    try:
        # Check the iterable's image format
        match texture[3]:
            case "dds":
                # Copy over the original file 
                with open(texture[2], 'rb') as f:
                    with open(f'{oculusPath}\\{locationIndex[texture[1]]}', 'wb') as target:
                        target.write(f.read())
                        target.close()
                    f.close()
            
            case "png":
                # Convert the image from PNG to DDS
                img = Image.open(texture[2], 'r')
                img.save(f'{oculusPath}\\{locationIndex[texture[1]]}', format='DDS')
                
    except Exception as err:
        tkinter.messagebox.showerror("Error!", f"There was an issue!\n{err}")

def changeVec3(vector3: tuple):
    with open(f'{oculusPath}\\Support\\oculus-dash\\dash\\data\\shaders\\theVoid\\theVoidUniforms.glsl', 'r+') as f:
        contents = f.read()
        colorValues = strToTuple(vector3[2])

        # We can divide all the values by 255 since all the values in theVoidUniforms.glsl are stored that way
        regex = vector3[1] + r" = \{[^}]+\};"
        repl = vector3[1] + r" = {" + f"{colorValues[0] / 255}, {colorValues[1] / 255}, {colorValues[2] / 255}" + "};"
        newFile = re.sub(regex, repl, contents)

        f.seek(0, 0)
        f.write(newFile)

def saveMods(elements: list):
    if tkinter.messagebox.askyesno("Confirm", "WARNING: The changes you make are irreversible. ODC has safety precautions but it's still recomended you back up any wanted configs. Continue?"):
        for x in elements:
            match x[0]:
                case "vec3":
                    # backupFile(f"{oculusPath}\\{locationIndex['theVoidUniforms']}", backupsFolder) # Backs up the original texture
                    changeVec3(x)
                case "texture":
                    # backupFile(f"{oculusPath}\\{locationIndex[x[1]]}", backupsFolder) # Backs up theVoidUniforms.glsl
                    modTexture(x)
        
        tkinter.messagebox.showinfo("Success", "Done! Put on your Rift/start Oculus Link to see the changes.")
    else:
        return

def askForColor(entry: ttk.Entry):
    colorCode = tkinter.colorchooser.askcolor(title="Choose a color")
    entry.config(state=tkinter.ACTIVE)

    entry.delete(0, tkinter.END)
    entry.insert(0, str(colorCode[0]))
    entry.config(state=tkinter.DISABLED)

# |-------------------------------------------|
# | UNUSED FUNCS - Will be used down the line |
# |-------------------------------------------|

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
    if checkPerms(debug=False):
        # Fetch the theme
        themepath = f"{sys.argv[0][:-8]}\\assets\\theme\\azure\\azure.tcl"
        if not os.path.exists(themepath):
            fetchTheme()

        # Set the icon and title for the main program
        icon = tkinter.PhotoImage(file=os.path.abspath(".\\assets\\ico\\icon.png"))
        tk.iconphoto(False, icon)
        tk.wm_title("Oculus Dash Customizer")

        # Initializing the theme
        tk.tk.call("source", os.path.join("assets", "theme", "azure", "azure.tcl"))
        if isDarkModeEnabled():
            tk.tk.call("set_theme", "dark")
        else:
            tk.tk.call("set_theme", "light")

        getOculusPath()

        modifyTab = ttk.Frame(tabIndex); tabIndex.add(modifyTab, text='Customize')
        convertTab = ttk.Frame(tabIndex); tabIndex.add(convertTab, text='Convert')

        # TODO: Refactor this bullshit
        img6CustomText = ttk.Label(modifyTab, text="Floor grid (grid_plane_006)")
        img6CustomPath = ttk.Entry(modifyTab, width=50)
        img6CustomBtn = ttk.Button(modifyTab, text="Browse", command=lambda: findFile(img6CustomPath, (("DirectDraw Surface (DDS)", "*.dds"), ("Portable Network Graphic (PNG)", "*.png")), "texture"))
        
        colorPickText = ttk.Label(modifyTab, text="Fog Color")
        colorPickValue = ttk.Entry(modifyTab, width=25); colorPickValue.insert(0, f"({0.78 * 255}, {0.78 * 255}, {0.78 * 255})"); colorPickValue.config(state=tkinter.DISABLED)
        colorPickBtn = ttk.Button(modifyTab, text="Pick Color", command=lambda: askForColor(colorPickValue))

        savebtn = ttk.Button(modifyTab, text="Save Changes", command=lambda: saveMods([
                                                                                        [ "texture", "grid_plane_006", img6CustomPath.get(), img6CustomPath.get().split(".")[-1] ],
                                                                                        [ "vec3", "u_voidFogColor", colorPickValue.get()]
                                                                                        ]))
        
        quitbtn = ttk.Button(modifyTab, text="Quit program", command=tk.quit)

        convertPngText = ttk.Label(convertTab, text="Convert PNG to DDS")
        convertPngPath = ttk.Entry(convertTab, width=50)
        convertPngBtn = ttk.Button(convertTab, text="Browse", command=lambda: findFile(convertPngPath, (("Portable Network Graphic (PNG)", "*.png"), ("All files", "*.*")), "image"))
        confirmPngConvert = ttk.Button(convertTab, text="Convert to DDS", command=lambda: convertToDDS(convertPngPath.get()))
        
        convertDdsText = ttk.Label(convertTab, text="Convert DDS to PNG")
        convertDdsPath = ttk.Entry(convertTab, width=50)
        convertDdsBtn = ttk.Button(convertTab, text="Browse", command=lambda: findFile(convertDdsPath, (("DirectDraw Surface (DDS)", "*.dds"), ("All files", "*.*")), "image"))
        confirmDdsConvert = ttk.Button(convertTab, text="Convert to PNG", command=lambda: convertToPNG(convertDdsPath.get()))
        
        quitbtnConvert = ttk.Button(convertTab, text="Quit program", command=tk.quit)


        tabIndex.pack(expand=True, fill="both")

        img6CustomText.grid(row=2, column=1, padx=10)
        img6CustomPath.grid(row=2, column=2)# ; img6CustomPath.insert(0, f"{oculusPath}\\{locationIndex['grid_plane_006']}")
        img6CustomBtn.grid(row=2, column=3, padx=10)

        colorPickText.grid(row=3, column=1, pady=10)
        colorPickBtn.grid(row=3, column=3, pady=10)
        colorPickValue.grid(row=3, column=2, pady=10)

        savebtn.grid(row=4, column=2, pady=5)
        quitbtn.grid(row=5, column=2, pady=2)

        convertPngText.grid(row=1, column=1, padx=10)
        convertPngPath.grid(row=1, column=2)
        convertPngBtn.grid(row=1, column=3, padx=10, pady=5)
        confirmPngConvert.grid(row=2, column=2)
        
        convertDdsText.grid(row=3, column=1, padx=10)
        convertDdsPath.grid(row=3, column=2)
        convertDdsBtn.grid(row=3, column=3, padx=10, pady=5)
        confirmDdsConvert.grid(row=4, column=2)

        quitbtnConvert.grid(row=5, column=2, pady=5)

        tk.mainloop()
    else:
        # Creates a new process of itself with admin privileges and quits the unprivileged version
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, os.path.abspath(sys.argv[0]), ' '.join(sys.argv[1:]), 1)
        sys.exit(0)
        return 1
    
    return 0
    
if __name__ == '__main__':
    tk = tkinter.Tk()
    tk.resizable(False, False) # Width, Height
    tabIndex = ttk.Notebook(tk)

    locationIndex = {
        "theVoidUniforms": "Support\\oculus-dash\\dash\\data\\shaders\\theVoid\\theVoidUniforms.glsl",
        "grid_plane_006": "Support\\oculus-dash\\dash\\assets\\raw\\textures\\environment\\the_void\\grid_plane_006.dds"
    }

    backupsFolder = os.environ["USERPROFILE"] + "\\ODC\\backups"
    if not os.path.exists(backupsFolder):
        os.mkdir(backupsFolder[:-8])
        os.mkdir(backupsFolder)

    if 'nt' not in os.name:
        input("[ERROR] This program runs only on Windows!") # Everyday I pray for Meta to release the Oculus software on Linux
    else:
        main()