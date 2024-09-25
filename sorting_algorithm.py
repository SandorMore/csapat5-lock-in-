from abc import ABC, abstractmethod

class SortingAlgorithm(ABC):
    def __init__(self, visualizer):
        self.visualizer = visualizer
    
    @abstractmethod
    def sort(self, data):
        pass