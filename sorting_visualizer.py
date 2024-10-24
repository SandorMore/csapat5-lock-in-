import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import font
import re
import queue
import threading
import time

import freakbob
import sorting_algorithm

class SortingVisualizer:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Rendezési algoritmusok")
        self.data = None
        self.steps = []
        self.currentStep = 0
        self.selectedDataType = tk.StringVar(value="num")
        self.selectedDataType.trace_add("write", self.onSelectedDataTypeChange)
        self.selectedSortDirection = tk.StringVar(value="asc")
        self.quantity = tk.Variable()
        self.min = tk.Variable()
        self.max = tk.Variable()
        self.lastStepTime = time.perf_counter()
        self.stepDelay = tk.DoubleVar()
        self.stepCycleLoopRunning = False
        self.algoritms = {
            "Bubble sort": sorting_algorithm.BubbleSort,
            "Improved Bubble Sort": sorting_algorithm.ImprovedBubbleSort,
            "Selection sort": sorting_algorithm.SelectionSort,
        }
        self.colors = {
            "red": "red",
            "green": "green",
            "lightgreen": "lightgreen",
            "lightred": "#FF7F7F",
            "yellow": "yellow",
            "blue": "blue",
        }

        self.style = ttk.Style(root)
        self.style.configure("TFrame", background="grey80")
        self.style.configure("TRadiobutton", background="grey80")
        self.style.configure("TLabel", background="grey80")
        self.style.configure("TScale", background="grey80")

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
        progressbarHolder = ttk.Frame(canvasFrame, height=6)
        progressbarHolder.grid(column=0, row=1, sticky="nsew")
        progressbarHolder.pack_propagate(False)

        self.progressbar = ttk.Progressbar(progressbarHolder)
        self.progressbar.pack(fill=tk.BOTH, expand=True)

        # root.mainFrame.optionsFrame
        optionsFrame = ttk.Frame(mainFrame, width=200, padding=10)
        optionsFrame.grid(column=1, row=0, sticky="nsew")
        optionsFrame.grid_propagate(False)
        optionsFrame.columnconfigure(0, weight=1)
        optionsFrame.rowconfigure(0, weight=1)
        optionsFrame.rowconfigure(1, weight=1)
        optionsFrame.rowconfigure(2, weight=1)
        optionsFrame.rowconfigure(3, weight=1)
        optionsFrame.rowconfigure(4, weight=3)

        # root.mainFrame.optionsFrame.algorithmCombobox
        self.algorithmCombobox = ttk.Combobox(optionsFrame, state="readonly", values=list(self.algoritms.keys()))
        self.algorithmCombobox.grid(column=0, row=0, sticky="ew")
        self.algorithmCombobox.current(0)

        # root.mainFrame.optionsFrame.dataTypeRadiobuttonsFrame
        dataTypeRadiobuttonsFrame = ttk.Frame(optionsFrame)
        dataTypeRadiobuttonsFrame.grid(column=0, row=1, sticky="ew")
        # dataTypeRadiobuttonsFrame.rowconfigure(2, minsize=10)

        # root.mainFrame.optionsFrame.dataTypeRadiobuttonsFrame.numbersRadiobutton
        numbersRadiobutton = ttk.Radiobutton(dataTypeRadiobuttonsFrame, text="Számok", variable=self.selectedDataType, value="num")
        numbersRadiobutton.grid(column=0, row=0, sticky="w")

        # root.mainFrame.optionsFrame.dataTypeRadiobuttonsFrame.textRadiobutton
        textRadiobutton = ttk.Radiobutton(dataTypeRadiobuttonsFrame, text="Szövegek", variable=self.selectedDataType, value="text")
        textRadiobutton.grid(column=0, row=1, sticky="w")

        # root.mainFrame.optionsFrame.sortDirectionRadiobuttonsFrame
        sortDirectionRadiobuttonsFrame = ttk.Frame(optionsFrame)
        sortDirectionRadiobuttonsFrame.grid(column=0, row=2, sticky="ew")

        # root.mainFrame.optionsFrame.sortDirectionRadiobuttonsFrame.ascendingRadiobutton
        ascendingRadiobutton = ttk.Radiobutton(sortDirectionRadiobuttonsFrame, text="Növekvő", variable=self.selectedSortDirection, value="asc")
        ascendingRadiobutton.grid(column=0, row=3, sticky="w")

        # root.mainFrame.optionsFrame.sortDirectionRadiobuttonsFrame.descendingRadiobutton
        descendingRadiobutton = ttk.Radiobutton(sortDirectionRadiobuttonsFrame, text="Csökkenő", variable=self.selectedSortDirection, value="desc")
        descendingRadiobutton.grid(column=0, row=4, sticky="w")

        # root.mainFrame.optionsFrame.entryFrame
        entryFrame = ttk.Frame(optionsFrame)
        entryFrame.grid(column=0, row=3, sticky="ew")
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
        generateDataButton.grid(column=0, row=4, sticky="ew")

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

        playButton = ttk.Button(playButtonHolder, command=self.toggleStepCycleLoopRunning)
        playButton.pack(fill=tk.BOTH, expand=True)

        # root.mainFrame.mediaFrame.backButtonHolder.backButton
        backButtonHolder = ttk.Frame(mediaButtonsFrame, width=50, height=50)
        backButtonHolder.grid(column=0, row=0, sticky="w")
        backButtonHolder.pack_propagate(False)

        backButton = ttk.Button(backButtonHolder, command=lambda: self.step(forward=False))
        backButton.pack(fill=tk.BOTH, expand=True)

        # root.mainFrame.mediaFrame.forwardButtonHolder.forwardButton
        forwardButtonHolder = ttk.Frame(mediaButtonsFrame, width=50, height=50)
        forwardButtonHolder.grid(column=2, row=0, sticky="e")
        forwardButtonHolder.pack_propagate(False)

        forwardButton = ttk.Button(forwardButtonHolder, command=lambda: self.step(forward=True))
        forwardButton.pack(fill=tk.BOTH, expand=True)

        # root.mainFrame.additionalOptionsFrame
        additionalOptionsFrame = ttk.Frame(mainFrame, padding=10)
        additionalOptionsFrame.grid(column=1, row=1, sticky="nsew")
        additionalOptionsFrame.grid_propagate(False)
        additionalOptionsFrame.columnconfigure(0, weight=1)
        additionalOptionsFrame.rowconfigure(0, weight=1)

        # root.mainFrame.additionalOptionsFrame.speedScale
        speedScale = ttk.Scale(additionalOptionsFrame, from_=1, to=0, variable=self.stepDelay)
        speedScale.set(0.5)
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

    def addToCallQueue(self, func, *args, **kwargs):
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
        # widget = self.root.nametowidget(widgetName)
        if re.match("^[0-9]*$", input) != None:
            if input == "":
                self.root.setvar(varName, "")
            else:
                self.root.setvar(varName, int(input))
            return True
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
        if self.stepCycleLoopRunning:
            self.toggleStepCycleLoopRunning()

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
            if minV == "" or maxV == "":
                self.showErrorMessage("Adj meg minimum és maximum értékeket!")
                return
            if minV > maxV:
                self.showErrorMessage("A minimum érték nem lehet nagyobb a maximum értéknél.")
                return
            freakbob.Szam_Gen(quantity, minV, maxV)
        else:
            freakbob.Szo_Gen(quantity)
        if not self.getDataFromFile("ki.txt"):
            return
        self.drawColumns()

        threading.Thread(target=self.algoritms[self.algorithmCombobox.get()](self).sort(), daemon=True).start()

    def getDataFromFile(self, filename):
        self.data = None
        self.steps = []
        self.currentStep = -1
        self.progressbar.configure(value=0)
        self.canvas.delete("column")

        try:
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read().strip()
        except:
            self.showErrorMessage("Probléma adódott a file megnyitása közben.")
            return False

        if re.match("^([0-9]+;)+[0-9]+$", content):
            self.data = [self.DataItem(int(s)) for s in content.split(";")]
        elif re.match("^([a-zA-Z]+;)+[a-zA-Z]+$", content):
            self.data = self.assignValuesToStrings(content.split(";"))
        else:
            self.showErrorMessage("A legenerált file-ban helytelen az adatszerkezet.")
            return False
        return True

    def showErrorMessage(self, message):
        messagebox.showerror(message=message)

    def assignValuesToStrings(self, textData):
        toReturn = []
        for s in textData:
            value = 0
            for i,c in enumerate(s):
                value += (ord(c.lower())-ord('a'))/26**(i+1)
            toReturn.append(self.DataItem(value, s))
        return toReturn

    def drawColumns(self):
        self.canvas.delete("column")
        values = [x.value for x in self.data]
        maxV = max(values)

        cWidth = self.canvas.winfo_width()
        cHeight = self.canvas.winfo_height()
        barAreaWidth = (cWidth-5)/len(self.data)
        barWidth = barAreaWidth*0.8

        self.columnPositions = [int(barAreaWidth*i+(barAreaWidth-barWidth)/2+2) for i in range(len(self.data))]

        for i,item in enumerate(self.data):
            item.columnId = self.canvas.create_rectangle(self.columnPositions[i], cHeight, self.columnPositions[i]+barWidth, cHeight-5-(item.value/maxV*cHeight*0.8), tags=("column"))
        self.updateCanvasColors()

    def updateCanvasColors(self):
        self.canvas.itemconfigure("column", fill="grey70")
        for cName, cValue in self.colors.items():
            self.canvas.itemconfigure(cName, fill=cValue)

    def startStepCycleLoop(self):
        self.stepCycleLoopRunning = True
        while self.stepCycleLoopRunning and self.currentStep < len(self.steps):
            if (time.perf_counter() - self.lastStepTime) >= self.stepDelay.get():
                self.step(True)
        self.stepCycleLoopRunning = False

    def toggleStepCycleLoopRunning(self):
        if self.steps:
            if not self.stepCycleLoopRunning and self.currentStep < len(self.steps):
                threading.Thread(target=self.startStepCycleLoop, daemon=True).start()
            else:
                self.stepCycleLoopRunning = False

    def step(self, forward):
        if self.steps:
            if not forward and self.currentStep > -1:
                self.currentStep -= 1
            elif forward and self.currentStep < len(self.steps):
                self.currentStep += 1

            self.progressbar.configure(maximum=len(self.steps)+1, value=self.currentStep+1)

            if self.currentStep >= 0 and self.currentStep < len(self.steps):
                func, *args = self.steps[self.currentStep]  
                func(*args)
            else:
                self.updateCanvasColors()

            self.lastStepTime = time.perf_counter()