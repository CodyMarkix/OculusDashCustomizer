import requests
import zipfile as zf
import os, shutil

def fetchTheme():
    destination = os.path.abspath(f"{os.getcwd()}\\assets\\theme")
    
    print("Downloading theme...")
    theme = requests.get('https://github.com/rdbende/Azure-ttk-theme/archive/refs/heads/main.zip')
    print("[OK] Theme downloaded!")

    if theme.status_code == 200:
        with open('C:\\Windows\\Temp\\azure.zip', 'wb') as f:
            f.write(theme.content)
            f.close()

        with zf.ZipFile('C:\\Windows\\Temp\\azure.zip', 'r') as th:
                th.extractall(destination)
                try:
                    shutil.move(src=f"{os.getcwd()}\\assets\\theme\\Azure-ttk-theme-main", dst=f"{os.getcwd()}\\assets\\theme\\azure")
                    # os.rename(f"{os.getcwd()}\\assets\\theme\\Azure-ttk-theme-main", f"{os.getcwd()}\\assets\\theme\\azure")
                except Exception:
                    shutil.rmtree(f"{os.getcwd()}\\assets\\theme\\azure")
                    shutil.move(src=f"{os.getcwd()}\\assets\\theme\\Azure-ttk-theme-main", dst=f"{os.getcwd()}\\assets\\theme\\azure")
    else:
        del theme
        fetchTheme()