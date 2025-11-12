"""Game class"""
class Game():
    def __init__(self, difficulty_multiplier: int):
        self.score = 0
        self.multiplier = difficulty_multiplier
        self.remaining_time = 30
        self.current_words = ['one', 'two', 'three'] # Placeholder