from datetime import datetime

# NOT WORKING
def backupFile(fp: str, backupFolder: str):
    newFileName = fp.split("\\")[-1] + "_w" + "_".join(datetime.now().__str__().split(" "))
    breakpoint()

    with open(fp, 'r') as f:
        contentsToBackup = f.read()
        breakpoint()

        with open(f"{backupFolder}\\{newFileName}.bak", "w") as backup:
            backup.write(contentsToBackup)