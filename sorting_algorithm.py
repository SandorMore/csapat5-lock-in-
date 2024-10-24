from abc import ABC, abstractmethod

class SortingAlgorithm(ABC):
    def __init__(self, visualizer):
        self.visualizer = visualizer
    
    compareHighlights = [["red", "red"], ["green", "green"]]
    swapHighlights = [["red", "red"], ["green", "green"]]

    @abstractmethod
    def sort(self):
        pass

    def deselectAll(self):
        self.visualizer.canvas.itemconfig("column", tags=("column",))

    def compare(self, idx1, idx2):
        """
        Igazat ad vissza ha az első nagyobb, minden más esetben pedig hamisat
        """
        returnValue = False
        if self.visualizer.data[idx1].value > self.visualizer.data[idx2].value:
            returnValue = True
            if self.compareHighlights[0] != None:
                self.visualizer.steps.append((self.highlightColumns, [self.visualizer.data[idx1].columnId, self.compareHighlights[0][0]], [self.visualizer.data[idx2].columnId, self.compareHighlights[0][1]]))
        else:
            if self.compareHighlights[1] != None:
                self.visualizer.steps.append((self.highlightColumns, [self.visualizer.data[idx1].columnId, self.compareHighlights[1][0]], [self.visualizer.data[idx2].columnId, self.compareHighlights[1][1]]))
        return returnValue

    def swap(self, idx1, idx2):
        if self.swapHighlights[0] != None:
            self.visualizer.steps.append((self.moveAndHighlightColumns, [self.visualizer.data[idx1].columnId, idx1, self.swapHighlights[0][0]], [self.visualizer.data[idx2].columnId, idx2, self.swapHighlights[0][1]]))
        self.visualizer.data[idx1], self.visualizer.data[idx2] = self.visualizer.data[idx2], self.visualizer.data[idx1]
        if self.swapHighlights[1] != None:
            self.visualizer.steps.append((self.moveAndHighlightColumns, [self.visualizer.data[idx1].columnId, idx1, self.swapHighlights[1][0]], [self.visualizer.data[idx2].columnId, idx2, self.swapHighlights[1][1]]))

    def highlightColumns(self, *colIdTagPairs):
        self.deselectAll()
        for pair in colIdTagPairs:
            colId, tag = pair
            if tag != None:
                self.visualizer.canvas.addtag(tag, "withtag", colId)
        self.visualizer.updateCanvasColors()
        self.deselectAll()

    def moveAndHighlightColumns(self, *colIdPosTagTriplets):
        colIds, colPoss, tags = zip(*colIdPosTagTriplets)

        for i in range(len(colIdPosTagTriplets)):
            self.visualizer.canvas.moveto(colIds[i], self.visualizer.columnPositions[colPoss[i]])

        self.highlightColumns(*list(zip(colIds, tags)))

class BubbleSort(SortingAlgorithm):
    compareHighlights = [None, ["green", "green"]]

    def sort(self):
        n = len(self.visualizer.data)
        sortDir = self.visualizer.selectedSortDirection.get()
        for i in range(n-1):
            for j in range(0, n-i-1):
                if (sortDir == "asc" and self.compare(j, j+1)) or (sortDir == "desc" and self.compare(j+1, j)):
                    self.swap(j, j+1)

class ImprovedBubbleSort(SortingAlgorithm):
    compareHighlights = [None, ["green", "green"]]

    def sort(self):
        n = len(self.visualizer.data)
        sortDir = self.visualizer.selectedSortDirection.get()
        i = n
        while i >= 1:
            lastSwapIdx = -1
            for j in range(0, i-1):
                if (sortDir == "asc" and self.compare(j, j+1)) or (sortDir == "desc" and self.compare(j+1, j)):
                    self.swap(j, j+1)
                    lastSwapIdx = j
            i = lastSwapIdx + 1

class SelectionSort(SortingAlgorithm):
    defaultCompareHighlights = [["lightred", "lightgreen"], ["lightgreen", "lightred"]]
    compareHighlights = defaultCompareHighlights

    def sort(self):
        n = len(self.visualizer.data)
        sortDir = self.visualizer.selectedSortDirection.get()
        self.compareHighlights = self.defaultCompareHighlights if sortDir == "asc" else [self.defaultCompareHighlights[1], self.defaultCompareHighlights[0]]
        for i in range(n-1):
            minIdx = i
            for j in range(i+1, n):
                if (sortDir == "asc" and self.compare(minIdx, j)) or (sortDir == "desc" and self.compare(j, minIdx)):
                    minIdx = j
            if minIdx != i:
                self.swap(i, minIdx)