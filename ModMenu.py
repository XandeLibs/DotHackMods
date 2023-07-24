import tkinter as tk

def ApplyPatch(folderPath, Originalxp, noLevelScaling):
    if Originalxp:
        xp = 0x96, 0x91, 0x8c, 0x87, 0x82, 0x7d, 0x78, 0x73, 0x64, 0x55, 0x4b, 0x41, 0x2d, 0x14, 0x0a, 0x07, 0x05, 0x04, 0x03
    else:
        xp = 0xc3, 0xbd, 0xb6, 0xb0, 0xa9, 0xa3, 0x9c, 0x96, 0x82, 0x6f, 0x62, 0x55, 0x3b, 0x1a, 0x0d, 0x0a, 0x08, 0x06, 0x04

    xpOffset = 0x7d4cc0, 0x8fb2d0, 0x9fa140, 0x9d9260
    lvlScaleAddress = 0x48f695, 0x56b5f5, 0x5744c1, 0x557cb1
    lvlScaleInstructions = 0xF3, 0x41, 0x0F, 0x59, 0xD8
    
    for i in range(1, 4):
        filePath = folderPath + "hackGU_vol" + i + ".dll"

        file = open(filePath, "r+b")
        file.seek(xpOffset[i])
        file.write(xp)

        file.seek(lvlScaleAddress[i])
        if noLevelScaling == True:
            file.write(b"\x90\x90\x90\x90\x90")
        else:
            file.write(lvlScaleInstructions)
        
    file.close()

# Main
mw = tk.Tk()
mw.title("Dot Hack Mod Menu")
mw.size = (300, 300)

# Only contains folder, not file name
tk.Label(mw, text="Path to file").grid(row=0)
pathEntry = tk.Entry(mw)
pathEntry.grid(row=0, column=1)

noLvlScale = tk.BooleanVar()
noLvlScale.set(False)
tk.Checkbutton(mw, text="No Level Scaling", variable=noLvlScale).grid(row=1, column=1)

originalxp = tk.BooleanVar()
originalxp.set(False)
tk.Radiobutton(mw, text="Last Recode XP", variable=originalxp, value=False).grid(row=1, column=0)
tk.Radiobutton(mw, text="Original XP", variable=originalxp, value=True).grid(row=2, column=0)

tk.Button(mw, text="Apply", command=lambda: ApplyPatch(pathEntry.get(), originalxp.get(), noLvlScale.get())).grid(row=3, column=1)

mw.mainloop()