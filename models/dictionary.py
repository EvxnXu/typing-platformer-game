"""Dictionary Class"""
from word import Word

class Dictionary():
    def __init__(self, min: int, max: int, words: list[Word]):
        self.min_score = min
        self.max_score = max
        self.words = words