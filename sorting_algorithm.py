from abc import ABC, abstractmethod

class SortingAlgorithm(ABC):
    def __init__(self, visualizer):
        self.visualizer = visualizer
    
    @abstractmethod
    def sort(self, data):
        pass

    @staticmethod
    def check(visualizer, item1, item2):
        higher, lower = item1, item2
        if higher.value < lower.value:
            higher, lower = lower, higher
        visualizer.canvas.itemconfigure(higher.columnId, fill="green")
        visualizer.canvas.itemconfigure(lower.columnId, fill="red")