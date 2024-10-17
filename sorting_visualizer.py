import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import font
import re
import queue
import threading

import freakbob
import sorting_algorithm

class SortingVisualizer:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.data = None
        self.callQueue = queue.Queue()
        self.root.bind("<<queue_call>>", self.queueHandler)
        self.selectedDataType = tk.StringVar(value="num")
        self.selectedDataType.trace_add("write", self.onSelectedDataTypeChange)
        self.quantity = tk.Variable()
        self.min = tk.Variable()
        self.max = tk.Variable()

        self.style = ttk.Style(root)
        self.style.configure("TFrame", background="grey80")
        # self.style.configure("TFrame.red", background="red")

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
        numbersRadiobutton = ttk.Radiobutton(radiobuttonsFrame, text="numbers", variable=self.selectedDataType, value="num")
        numbersRadiobutton.grid(column=0, row=0, sticky="w")

        # root.mainFrame.optionsFrame.radiobuttonsFrame.textRadiobutton
        textRadiobutton = ttk.Radiobutton(radiobuttonsFrame, text="text", variable=self.selectedDataType, value="text")
        textRadiobutton.grid(column=0, row=1, sticky="w")

        # root.mainFrame.optionsFrame.entryFrame
        entryFrame = ttk.Frame(optionsFrame)
        entryFrame.grid(column=0, row=2, sticky="ew")
        entryFrame.columnconfigure(0, weight=1)
        entryFrame.columnconfigure(1, weight=1)
        entryFrame.rowconfigure(0, weight=1)
        entryFrame.rowconfigure(1, weight=1)

        # # root.entryErrorLabel
        # errorFont = font.nametofont("TkDefaultFont").copy()
        # errorFont.configure(size=8)
        # self.entryErrorLabel = ttk.Label(root, text="invalid value", font=errorFont)

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
        quantityEntry = ttk.Entry(quantityFrame, width=3, validate="key", validatecommand=(self.root.register(self.validateNumInput), "%P", "%W", self.quantity))
        quantityEntry.grid(column=1, row=0, sticky="we")
        quantityEntry.validate()

        # root.mainFrame.optionsFrame.entryFrame.minFrame
        self.minFrame = ttk.Frame(entryFrame, padding=3)
        self.minFrame.grid(column=0, row=1, sticky="we")
        self.minFrame.columnconfigure(0, weight=1)
        self.minFrame.columnconfigure(1, weight=1)
        self.minFrame.rowconfigure(0, weight=1)

        # root.mainFrame.optionsFrame.entryFrame.minFrame.minLabel
        minLabel = ttk.Label(self.minFrame, text="Min:")
        minLabel.grid(column=0, row=0, sticky="we")

        # root.mainFrame.optionsFrame.entryFrame.minFrame.minEntry
        minEntry = ttk.Entry(self.minFrame, width=3, validate="key", validatecommand=(self.root.register(self.validateNumInput), "%P", "%W", self.min))
        minEntry.grid(column=1, row=0, sticky="we")
        minEntry.validate()

        # root.mainFrame.optionsFrame.entryFrame.maxFrame
        self.maxFrame = ttk.Frame(entryFrame, padding=3)
        self.maxFrame.grid(column=1, row=1, sticky="we")
        self.maxFrame.columnconfigure(0, weight=1)
        self.maxFrame.columnconfigure(1, weight=1)
        self.maxFrame.rowconfigure(0, weight=1)

        # root.mainFrame.optionsFrame.entryFrame.maxFrame.maxLabel
        maxLabel = ttk.Label(self.maxFrame, text="Max:")
        maxLabel.grid(column=0, row=0, sticky="we")

        # root.mainFrame.optionsFrame.entryFrame.maxFrame.maxEntry
        maxEntry = ttk.Entry(self.maxFrame, width=3, validate="key", validatecommand=(self.root.register(self.validateNumInput), "%P", "%W", self.max))
        maxEntry.grid(column=1, row=0, sticky="we")
        maxEntry.validate()

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

        playButton = ttk.Button(playButtonHolder, command=self.test)
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

    class DataItem:
        def __init__(self, value, toDisplay = None, columnId = None):
            self.value = value
            self.toDisplay = toDisplay if toDisplay else str(value)
            self.columnId = columnId
    
    class CallData:
        def __init__(self, func, args, kwargs):
            self.func = func
            self.args = args
            self.kwargs = kwargs
            self.reply = None
            self.replyEvent = threading.Event()
    
    def callOnMainThread(self, func, *args, **kwargs):
        callData = self.CallData(func, args, kwargs)
        self.callQueue.put(callData)
        self.root.event_generate("<<queue_call>>", when="tail")
        callData.replyEvent.wait()
        return callData.reply

    def queueHandler(self, event):
        try:
            while True:
                callData = self.callQueue.get_nowait()
                callData.reply = callData.func(*callData.args, **callData.kwargs)
                callData.replyEvent.set()
        except queue.Empty:
            pass

    def validateNumInput(self, input, widgetName, varName):
        # self.root.nametowidget(widgetName).configure(style="TFrame.red")
        if re.match("^[0-9]*$", input) != None:
            if input == "":
                self.root.setvar(varName, "")
            else:
                self.root.setvar(varName, int(input))
            print(self.root.getvar(varName))
            return True
        print(self.root.getvar(varName))
        return False
    
    def SetStateForAllChildren(self, state, *objects):
        for object in objects:
            for child in object.winfo_children():
                child.configure(state=state)

    def onSelectedDataTypeChange(self, *args):
        if self.selectedDataType.get() == "num":
            self.SetStateForAllChildren(tk.NORMAL, self.minFrame, self.maxFrame)
        else:
            self.SetStateForAllChildren(tk.DISABLED, self.minFrame, self.maxFrame)

    def generateAndLoadData(self):
        quantity = self.quantity.get()
        minV = self.min.get()
        maxV = self.max.get()
        if quantity == "":
            self.showErrorMessage("Adj meg egy mennyiséget!")
            return
        elif quantity < 2:
            self.showErrorMessage("A mennyiség nem lehet kisebb mint 2.")
            return
        if self.selectedDataType.get() == "num":
            if minV == "" and maxV == "":
                self.showErrorMessage("Adj meg minimum és maximum értékeket!")
                return
            if minV > maxV:
                self.showErrorMessage("A minimum érték nem lehet nagyobb a maximum értéknél.")
                return
            freakbob.Szam_Gen(quantity, minV, maxV)
        else:
            freakbob.Szo_Gen(self.quantity)
        self.getDataFromFile("ki.txt")
        self.drawColumns()

    def getDataFromFile(self, filename):
        self.data = None
        self.canvas.delete("column")

        try:
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read().strip()
        except:
            self.showErrorMessage("Probléma adódott a file megnyitása közben.")
            return

        if re.match("^([0-9]+;)+[0-9]+$", content):
            self.data = [self.DataItem(int(s), s) for s in content.split(";")]
        elif re.match("^([a-zA-Z]+;)+[a-zA-Z]+$", content):
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
            toReturn.append(self.DataItem(value, s))
        return toReturn

    def drawColumns(self):
        self.canvas.delete("column")
        values = [x.value for x in self.data]
        # minV = min(values)
        maxV = max(values)

        cWidth = self.canvas.winfo_width()
        cHeight = self.canvas.winfo_height()
        barAreaWidth = cWidth/len(self.data)
        barWidth = barAreaWidth*0.8

        for i,item in enumerate(self.data):
            # item.columnId = self.canvas.create_rectangle(barAreaWidth*i+(barAreaWidth-barWidth)/2, cHeight, barAreaWidth*i+(barAreaWidth-barWidth)/2+barWidth, cHeight-5-((item.value-minV)/(maxV-minV)*cHeight*0.8), tags=("column"))
            item.columnId = self.canvas.create_rectangle(barAreaWidth*i+(barAreaWidth-barWidth)/2, cHeight, barAreaWidth*i+(barAreaWidth-barWidth)/2+barWidth, cHeight-5-(item.value/maxV*cHeight*0.8), tags=("column"))
        self.updateCanvas()

    def updateCanvas(self):
        self.canvas.itemconfigure("column", fill="grey70")
        self.canvas.itemconfigure("incorrect", fill="red")
        self.canvas.itemconfigure("correct", fill="green")

    def test(self):
        if self.data:
            algorithm = sorting_algorithm.BubbleSort(self)
            threading.Thread(target=algorithm.sort, daemon=True).start()