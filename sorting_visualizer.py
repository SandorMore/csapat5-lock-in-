import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import re

class SortingVisualizer:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.data = None
        self.textData = False
        self.radiobuttonIsText = tk.BooleanVar(value=False)
        
        self.style = ttk.Style(root)
        self.style.configure("TFrame", background="grey80")

        # root.mainFrame
        mainFrame = ttk.Frame(root, padding=10)
        mainFrame.pack(fill=tk.BOTH, expand=True)
        mainFrame.columnconfigure(0, weight=5)
        mainFrame.columnconfigure(1, weight=1)
        mainFrame.rowconfigure(0, weight=5)
        mainFrame.rowconfigure(1, weight=1)

        # root.mainFrame.canvasFrame
        canvasFrame = ttk.Frame(mainFrame, width=800, height=500, padding=10)
        canvasFrame.grid(column=0, row=0, sticky="nsew")
        canvasFrame.grid_propagate(False)
        canvasFrame.columnconfigure(0, weight=1)
        canvasFrame.rowconfigure(0, weight=1)

        # root.mainFrame.canvasFrame.canvas
        self.canvas = tk.Canvas(canvasFrame, background="grey90", highlightthickness=1, highlightbackground="grey70")
        self.canvas.grid(column=0, row=0, sticky="nsew")

        # root.mainFrame.canvasFrame.progressbarHolder.progressbar
        progressbarHolder = ttk.Frame(canvasFrame, height=5)
        progressbarHolder.grid(column=0, row=1, sticky="ew")
        progressbarHolder.pack_propagate(False)

        progressbar = ttk.Progressbar(progressbarHolder)
        progressbar.pack(fill=tk.BOTH, expand=True)

        # root.mainFrame.optionsFrame
        optionsFrame = ttk.Frame(mainFrame, width=200, padding=10)
        optionsFrame.grid(column=1, row=0, sticky="nsew")
        optionsFrame.grid_propagate(False)
        optionsFrame.columnconfigure(0, weight=1)
        optionsFrame.rowconfigure(0, weight=1)
        optionsFrame.rowconfigure(1, weight=1)
        optionsFrame.rowconfigure(2, weight=1)
        optionsFrame.rowconfigure(3, weight=1)

        # root.mainFrame.optionsFrame.algorithmCombobox
        algorithmCombobox = ttk.Combobox(optionsFrame)
        algorithmCombobox.grid(column=0, row=0, sticky="ew")

        # root.mainFrame.optionsFrame.radiobuttonsFrame
        radiobuttonsFrame = ttk.Frame(optionsFrame)
        radiobuttonsFrame.grid(column=0, row=1, sticky="ew")

        # root.mainFrame.optionsFrame.radiobuttonsFrame.numbersRadiobutton
        numbersRadiobutton = ttk.Radiobutton(radiobuttonsFrame, text="numbers", variable=self.radiobuttonIsText, value=False)
        numbersRadiobutton.grid(column=0, row=0, sticky="w")

        # root.mainFrame.optionsFrame.radiobuttonsFrame.textRadiobutton
        textRadiobutton = ttk.Radiobutton(radiobuttonsFrame, text="text", variable=self.radiobuttonIsText, value=True)
        textRadiobutton.grid(column=0, row=1, sticky="w")

        # root.mainFrame.optionsFrame.entryFrame
        entryFrame = ttk.Frame(optionsFrame)
        entryFrame.grid(column=0, row=2, sticky="ew")
        entryFrame.columnconfigure(0, weight=1)
        entryFrame.columnconfigure(1, weight=1)
        entryFrame.rowconfigure(0, weight=1)
        entryFrame.rowconfigure(1, weight=1)

        # root.mainFrame.optionsFrame.entryFrame.quantityFrame
        quantityFrame = ttk.Frame(entryFrame, padding=3)
        quantityFrame.grid(column=0, row=0, columnspan=2, sticky="we")
        quantityFrame.columnconfigure(0, weight=1)
        quantityFrame.columnconfigure(1, weight=1)
        quantityFrame.rowconfigure(0, weight=1)

        # root.mainFrame.optionsFrame.entryFrame.quantityFrame.quantityLabel
        quantityLabel = ttk.Label(quantityFrame, text="Mennyiség:")
        quantityLabel.grid(column=0, row=0, sticky="we")

        # root.mainFrame.optionsFrame.entryFrame.quantityFrame.quantityEntry
        quantityEntry = ttk.Entry(quantityFrame, width=3)
        quantityEntry.grid(column=1, row=0, sticky="we")

        # root.mainFrame.optionsFrame.entryFrame.minFrame
        minFrame = ttk.Frame(entryFrame, padding=3)
        minFrame.grid(column=0, row=1, sticky="we")
        minFrame.columnconfigure(0, weight=1)
        minFrame.columnconfigure(1, weight=1)
        minFrame.rowconfigure(0, weight=1)

        # root.mainFrame.optionsFrame.entryFrame.minFrame.minLabel
        minLabel = ttk.Label(minFrame, text="Min:")
        minLabel.grid(column=0, row=0, sticky="we")

        # root.mainFrame.optionsFrame.entryFrame.minFrame.minEntry
        minEntry = ttk.Entry(minFrame, width=3)
        minEntry.grid(column=1, row=0, sticky="we")

        # root.mainFrame.optionsFrame.entryFrame.maxFrame
        maxFrame = ttk.Frame(entryFrame, padding=3)
        maxFrame.grid(column=1, row=1, sticky="we")
        maxFrame.columnconfigure(0, weight=1)
        maxFrame.columnconfigure(1, weight=1)
        maxFrame.rowconfigure(0, weight=1)

        # root.mainFrame.optionsFrame.entryFrame.maxFrame.maxLabel
        maxLabel = ttk.Label(maxFrame, text="Max:")
        maxLabel.grid(column=0, row=0, sticky="we")

        # root.mainFrame.optionsFrame.entryFrame.maxFrame.maxEntry
        maxEntry = ttk.Entry(maxFrame, width=3)
        maxEntry.grid(column=1, row=0, sticky="we")

        # root.mainFrame.optionsFrame.generateDataButton
        generateDataButton = ttk.Button(optionsFrame, text="Új adat generálása", command=self.generateAndLoadData)
        generateDataButton.grid(column=0, row=3, sticky="ew")

        # root.mainFrame.mediaFrame
        mediaFrame = ttk.Frame(mainFrame, height=100)
        mediaFrame.grid(column=0, row=1, sticky="nsew")
        mediaFrame.grid_propagate(False)
        mediaFrame.columnconfigure(0, weight=5)
        mediaFrame.columnconfigure(1, weight=1)
        mediaFrame.columnconfigure(2, weight=5)
        mediaFrame.rowconfigure(1, weight=1)

        # root.mainFrame.mediaFrame.mediaButtonsFrame
        mediaButtonsFrame = ttk.Frame(mediaFrame, width=200)
        mediaButtonsFrame.grid(column=1, row=1, sticky="nsew")
        mediaButtonsFrame.grid_propagate(False)
        mediaButtonsFrame.columnconfigure(0, weight=1)
        mediaButtonsFrame.columnconfigure(1, weight=1)
        mediaButtonsFrame.columnconfigure(2, weight=1)
        mediaButtonsFrame.rowconfigure(0, weight=1)

        # root.mainFrame.mediaFrame.playButtonHolder.playButton
        playButtonHolder = ttk.Frame(mediaButtonsFrame, width=50, height=50)
        playButtonHolder.grid(column=1, row=0)
        playButtonHolder.pack_propagate(False)

        playButton = ttk.Button(playButtonHolder)
        playButton.pack(fill=tk.BOTH, expand=True)

        # root.mainFrame.mediaFrame.backButtonHolder.backButton
        backButtonHolder = ttk.Frame(mediaButtonsFrame, width=50, height=50)
        backButtonHolder.grid(column=0, row=0, sticky="w")
        backButtonHolder.pack_propagate(False)

        backButton = ttk.Button(backButtonHolder)
        backButton.pack(fill=tk.BOTH, expand=True)

        # root.mainFrame.mediaFrame.forwardButtonHolder.forwardButton
        forwardButtonHolder = ttk.Frame(mediaButtonsFrame, width=50, height=50)
        forwardButtonHolder.grid(column=2, row=0, sticky="e")
        forwardButtonHolder.pack_propagate(False)

        forwardButton = ttk.Button(forwardButtonHolder)
        forwardButton.pack(fill=tk.BOTH, expand=True)

        # root.mainFrame.additionalOptionsFrame
        additionalOptionsFrame = ttk.Frame(mainFrame, padding=10)
        additionalOptionsFrame.grid(column=1, row=1, sticky="nsew")
        additionalOptionsFrame.grid_propagate(False)
        additionalOptionsFrame.columnconfigure(0, weight=1)
        additionalOptionsFrame.rowconfigure(0, weight=1)

        # root.mainFrame.additionalOptionsFrame.speedScale
        speedScale = ttk.Scale(additionalOptionsFrame, from_=0.5, to=1.5)
        speedScale.set(1)
        speedScale.grid(column=0, row=0, sticky="ew")

    def generateAndLoadData(self):
        # TODO: freakbob
        self.getDataFromFile("ki_test_1.txt")
        self.drawColumns()

    def getDataFromFile(self, filename):
        self.data = None
        self.textData = False

        try:
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read().strip()
        except:
            self.showErrorMessage("Probléma adódott a file megnyitása közben.")
            return

        if re.match("^([0-9]+;)+[0-9]+$", content):
            self.data = list(map(int, content.split(";")))
        elif re.match("^([a-zA-Z]+;)+[a-zA-Z]+$", content):
            self.textData = True
            self.data = self.assignValuesToStrings(content.split(";"))
        else:
            self.showErrorMessage("A legenerált file-ban helytelen az adatszerkezet.")
    
    def showErrorMessage(self, message):
        messagebox.showerror(message=message)
    
    def assignValuesToStrings(self, textData):
        toReturn = []
        for s in map(str.lower, textData):
            value = 0
            for i,c in enumerate(s):
                value += (ord(c)-ord('a'))/26**(i+1)
            toReturn.append((s, value))
        return toReturn
    
    def drawColumns(self):
        values = self.data if not self.textData else list(map(lambda x: x[1], self.data))

        minV = min(values)
        maxV = max(values)
        cWidth = self.canvas.winfo_width()
        cHeight = self.canvas.winfo_height()
        barAreaWidth = cWidth/len(self.data)

        for i,value in enumerate(values):
            self.canvas.create_rectangle(barAreaWidth*i+barAreaWidth*0.1, cHeight, barAreaWidth*i+barAreaWidth*0.9, cHeight-5-((value-minV)/(maxV-minV)*cHeight*0.8))