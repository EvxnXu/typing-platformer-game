"""Game class"""
from .word import Word

class Game():
    def __init__(self, difficulty_multiplier: int):
        self.score = 0
        self.multiplier = difficulty_multiplier
        self.remaining_time = 30.0
        self.current_words = []


    def is_over(self) -> bool:
        """Check if Game has Ended"""
        return self.remaining_time <= 0
    

    def update_time(self, change: float):
        """Update Remaining Time"""
        self.remaining_time += change
        return
    

    def validate_word(self, input: str) -> bool:
        """Validate Input against Current Words"""
        if input in self.current_words:
            return True
        return False
    

    def update_words(self, words: list[Word]):
        """Temp Function For Prototype to get new words"""
        self.current_words = words


    def update_score(self, value: int):
        """Update Score"""
        self.score += value