"""Game class"""
from .word import Word

class Game():
    def __init__(self, difficulty_multiplier: int):
        self.score = 0
        self.multiplier = difficulty_multiplier
        self.remaining_time = 30.0
        self.current_words = ['one', 'two', 'three'] # Placeholder

    def is_over(self) -> bool:
        return self.remaining_time <= 0
    
    def update_time(self, change: float):
        self.remaining_time += change
        return
    
    def update_words(self, words: list[Word]):
        """Temp Function For Prototype"""
        self.current_words = words

    def update_score(self, value: int):
        self.score += value