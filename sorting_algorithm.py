from abc import ABC, abstractmethod

class SortingAlgorithm(ABC):
    def __init__(self, visualizer):
        self.visualizer = visualizer
    
    @abstractmethod
    def sort(self):
        pass

    def select(self, *idxs):
        for idx in idxs:
            self.visualizer.canvas.addtag("selected", "withtag", self.visualizer.data[idx].columnId)

    def deselectAll(self):
        self.visualizer.canvas.dtag("column", "selected")
        self.visualizer.canvas.dtag("column", "correct")
        self.visualizer.canvas.dtag("column", "incorrect")

    def compare(self, idx1, idx2):
        """
        1-et ad vissza ha az első nagyobb, minden más esetben pedig 0-t
        """
        self.deselectAll()
        self.select(idx1, idx2)
        returnValue = 0

        if self.visualizer.data[idx1].value > self.visualizer.data[idx2].value:
            returnValue = 1
            self.visualizer.canvas.addtag("incorrect", "withtag", "selected")
        else:
            self.visualizer.canvas.addtag("correct", "withtag", "selected")

        self.visualizer.updateCanvas()
        return returnValue

    def swap(self, idx1, idx2):
        self.deselectAll()
        self.select(idx1, idx2)

        # TODO: valahogy nem pontosan cseréli ki az oszlopokat. Valahol valami egy kicsit elcsúszik.
        tempPos = self.visualizer.canvas.coords(self.visualizer.data[idx1].columnId)
        self.visualizer.canvas.moveto(self.visualizer.data[idx1].columnId, self.visualizer.canvas.coords(self.visualizer.data[idx2].columnId)[0])
        self.visualizer.canvas.moveto(self.visualizer.data[idx2].columnId, tempPos[0])

        self.visualizer.data[idx1], self.visualizer.data[idx2] = self.visualizer.data[idx2], self.visualizer.data[idx1]

        self.visualizer.canvas.addtag("correct", "withtag", "selected")
        self.visualizer.updateCanvas()

import time

class BubbleSort(SortingAlgorithm):
    def sort(self):
        n = len(self.visualizer.data)
        for i in range(n):
            swapped = False
            for j in range(0, n-i-1):
                time.sleep(0.5)
                if self.visualizer.callOnMainThread(self.compare, j, j+1):
                    time.sleep(0.5)
                    self.visualizer.callOnMainThread(self.swap, j, j+1)
                    swapped = True
            if swapped == False:
                break
        self.visualizer.callOnMainThread(self.deselectAll)
        self.visualizer.callOnMainThread(self.visualizer.updateCanvas)