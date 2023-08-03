import tkinter as tk
from tkinter import ttk
import os
import tkinter.filedialog
from enum import IntEnum

def ApplyPatch():

    folderPath = pathTextbox.get(1.0, tk.END).strip()

    if not (os.path.isfile(folderPath + "/hackGU_vol1.dll") and 
            os.path.isfile(folderPath + "/hackGU_vol2.dll") and 
            os.path.isfile(folderPath + "/hackGU_vol3.dll") and 
            os.path.isfile(folderPath + "/hackGU_vol4.dll")):
        
        tk.messagebox.showerror("Error", "Folder does not contain necessary game files")
        return

    if originalxp:
        xp = bytearray(b'\x96\x00\x00\x00\x91\x00\x00\x00\x8c\x00\x00\x00\x87\x00\x00\x00\x82\x00\x00\x00\x7d\x00\x00\x00\x78\x00\x00\x00\x73\x00\x00\x00\x64\x00\x00\x00\x55\x00\x00\x00\x4b\x00\x00\x00\x41\x00\x00\x00\x2d\x00\x00\x00\x14\x00\x00\x00\x0a\x00\x00\x00\x07\x00\x00\x00\x05\x00\x00\x00\x04\x00\x00\x00\x03')
    else:
        xp = bytearray(b'\xc3\x00\x00\x00\xbd\x00\x00\x00\xb6\x00\x00\x00\xb0\x00\x00\x00\xa9\x00\x00\x00\xa3\x00\x00\x00\x9c\x00\x00\x00\x96\x00\x00\x00\x82\x00\x00\x00\x6f\x00\x00\x00\x62\x00\x00\x00\x55\x00\x00\x00\x3b\x00\x00\x00\x1a\x00\x00\x00\x0d\x00\x00\x00\x0a\x00\x00\x00\x08\x00\x00\x00\x06\x00\x00\x00\x04')

    xpOffset = 0x7d4cc0, 0x8fb2d0, 0x9fa140, 0x9d9260
    lvlScaleAddress = 0x48f695, 0x56b5f5, 0x5744c1, 0x557cb1
    lvlScaleInstructions = bytearray(b'\xF3\x41\x0F\x59\xD8')
    
    for i in range(1, 5):
        filePath = folderPath + "/hackGU_vol" + str(i) + ".dll"

        file = open(filePath, "r+b")
        file.seek(xpOffset[i-1])
        file.write(xp)

        file.seek(lvlScaleAddress[i-1])
        if noLvlScale.get() == True:
            file.write(b"\x90\x90\x90\x90\x90")
        else:
            file.write(lvlScaleInstructions)
        
    file.close()

    tk.messagebox.showinfo("Done", "Patch applied successfully")

def Browse(textbox):
    Path = tk.filedialog.askdirectory()

    textbox.config(state=tk.NORMAL)
    textbox.delete(1.0, tk.END)
    textbox.insert(tk.END, Path)
    textbox.config(state=tk.DISABLED)

def OpenSaveFile(saveFilePath: tk.StringVar ,stats):
    saveFilePath.set(tk.filedialog.askopenfilename())
    saveFile = open(saveFilePath.get(), "r+b")
    ReadSaveFile(saveFile, stats)
    saveFile.close()

def ReadSaveFile(saveFile, stats):
    saveFile.seek(0x5c0)

    stats[0] = int.from_bytes(saveFile.read(2), byteorder="little")
    saveFile.seek(0x5c4)
    stats[1] = int.from_bytes(saveFile.read(2), byteorder="little")
    saveFile.seek(0x5c8)
    
    for i in range(2, 12):
        stats[i] = int.from_bytes(saveFile.read(2), byteorder="little")

    for i in range(0, 12):
        statsEntry[i].delete(0, tk.END)
        statsEntry[i].insert(tk.END, stats[i])

def SaveStats(saveFilePath: tk.StringVar, stats):
    if saveFilePath.get() != None:
        saveFile = open(saveFilePath.get(), "r+b")
        saveFile.seek(0x5c0)

        saveFile.write(int(statsEntry[0].get()).to_bytes(2, byteorder="little"))
        saveFile.seek(0x5c4)
        saveFile.write(int(statsEntry[1].get()).to_bytes(2, byteorder="little"))
        saveFile.seek(0x5c8)

        for i in range(2, 12):
            saveFile.write(int(statsEntry[i].get()).to_bytes(2, byteorder="little"))

        tk.messagebox.showinfo("Done", "Stats saved successfully")
        saveFile.close()

    else:
        tk.messagebox.showerror("Error", "No save file selected")
    
#--------------------------------------------

# Main
mw = tk.Tk()
mw.title("Dot Hack Mod Menu")
mw.geometry("700x200")

tabControl = ttk.Notebook(master=mw)

# --------------- Tweaks tab ----------------

tweaksTab = ttk.Frame(tabControl)
tabControl.add(tweaksTab, text="Tweaks")
tabControl.pack(expand=1, fill="both")

# ------ Folder Frame ------
folderFrame = tk.Frame(tweaksTab)
folderFrame.grid(row=0, column=0)

tk.Label(folderFrame, text="Path to game folder").grid(row=0, column=0)

folderPath = tk.StringVar()
folderPath.set("C:/Program Files (x86)/Steam/steamapps/common/hackGU")

pathTextbox = tk.Text(folderFrame, width=60, height=1, xscrollcommand=True)
pathTextbox.grid(row=0, column=1)
pathTextbox.insert(tk.END, folderPath.get())
pathTextbox.config(state=tk.DISABLED)

tk.Button(folderFrame, text="Browse", command=lambda: Browse(pathTextbox)).grid(row=0, column=2)
# ---------------------------

# ------ Tweaks Frame ------
tweaksFrame = tk.Frame(tweaksTab)
tweaksFrame.grid(row=1, column=0)

noLvlScale = tk.BooleanVar()
tk.Checkbutton(tweaksFrame, text="No Level Scaling", variable=noLvlScale).grid(row=1, column=1)

originalxp = tk.BooleanVar()
originalxp.set(False)
tk.Radiobutton(tweaksFrame, text="Last Recode XP", variable=originalxp, value=False).grid(row=1, column=0)
tk.Radiobutton(tweaksFrame, text="Original XP", variable=originalxp, value=True).grid(row=2, column=0)

tk.Button(tweaksFrame, text="Apply", command=ApplyPatch).grid(row=3, column=1)
# ---------------------------

# ------------ Save Editor tab --------------
saveEditorTab = ttk.Frame(tabControl)
tabControl.add(saveEditorTab, text="Save Editor")
tabControl.pack(expand=1, fill="both")

stats = [0] * 12
saveFilePath = tk.StringVar()

tk.Label(saveEditorTab, text="Save File (inside Steam/userdata/{userid}/525480/remote/savedata)").grid(row=0, column=0)

tk.Button(saveEditorTab, text="Browse", command=lambda: OpenSaveFile(saveFilePath, stats)).grid(row=0, column=1)

# ------ Stats Frame ------
statsFrame = tk.Frame(saveEditorTab)
statsFrame.grid(row=1, column=0, columnspan=2)

statsEntry = [0] * 12
statsNames = ["HP", "SP", "P-Atk", "P-Def", "M-Atk", "M-Def", "Fire", "Water", "Wind", "Earth", "Light", "Dark"]
statsPlacement = [[0,0], [0,2], [1,0], [2,0], [1,2], [2,2], [3,0], [3,2], [4,0], [4,2], [5,0], [5,2]]

def StatsLabel(text: str, enum: int, placement):
    tk.Label(statsFrame, text=text).grid(row=placement[0], column=placement[1])
    entry = tk.Entry(statsFrame, width=5)
    entry.config(validate="key", validatecommand=(entry.register(ValidateEntry), "%P", "%d"))
    entry.grid(row=placement[0], column = placement[1] + 1)
    return entry

def ValidateEntry(text: str, action: str):
    if action == "1":
        if text.isdigit() and int(text) < 0xFFFF:
            return True
        else:
            return False
    else:
        return True

for i in range(0, 12):
    statsEntry[i] = StatsLabel(statsNames[i], i, statsPlacement[i])

tk.Button(saveEditorTab, text="Save", command=lambda: SaveStats(saveFilePath, stats)).grid(row=13, column=1)
# ---------------------------

mw.mainloop()