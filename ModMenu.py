import tkinter as tk
import os
import tkinter.filedialog

def ApplyPatch():

    folderPath = textbox.get(1.0, tk.END).strip()

    print("Applying patch to " + folderPath)

    if not (os.path.isfile(folderPath + "/hackGU_vol1.dll") and os.path.isfile(folderPath + "/hackGU_vol2.dll") and os.path.isfile(folderPath + "/hackGU_vol3.dll") and os.path.isfile(folderPath + "/hackGU_vol4.dll")):
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
            print("With level scaling")
            file.write(lvlScaleInstructions)
        
    file.close()

    tk.messagebox.showinfo("Done", "Patch applied successfully")

def Browse():
    Path = tk.filedialog.askdirectory()

    textbox.config(state=tk.NORMAL)
    textbox.delete(1.0, tk.END)
    textbox.insert(tk.END, Path)
    textbox.config(state=tk.DISABLED)
    
#--------------------------------------------

# Main
mw = tk.Tk()
mw.title("Dot Hack Mod Menu")
mw.size = (300, 300)

tk.Label(mw, text="Path to game folder").grid(row=0, column=0)

folderPath = tk.StringVar()
folderPath.set("C:/Program Files (x86)/Steam/steamapps/common/hackGU")

textbox = tk.Text(mw, width=60, height=1, xscrollcommand=True)
textbox.grid(row=0, column=1)
textbox.insert(tk.END, folderPath.get())
textbox.config(state=tk.DISABLED)

tk.Button(mw, text="Browse", command=Browse).grid(row=0, column=2)

noLvlScale = tk.BooleanVar()
tk.Checkbutton(mw, text="No Level Scaling", variable=noLvlScale).grid(row=1, column=1)

originalxp = tk.BooleanVar()
originalxp.set(False)
tk.Radiobutton(mw, text="Last Recode XP", variable=originalxp, value=False).grid(row=1, column=0)
tk.Radiobutton(mw, text="Original XP", variable=originalxp, value=True).grid(row=2, column=0)

tk.Button(mw, text="Apply", command=ApplyPatch).grid(row=3, column=1)

mw.mainloop()