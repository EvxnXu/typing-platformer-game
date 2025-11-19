"""Game Controller Class"""
import pygame
from models import Game
from models import Record
from models import Leaderboard

class GameController():
    
    def __init__(self):
        pygame.init()
        
        self.state = "menu"
        self.clock = pygame.time.Clock()
        self.difficulty_multiplier = 1
        self.game = Game(self.difficulty_multiplier)
        self.leaderboard = Leaderboard()
        
        
    def handle_input(self, event: pygame.event):
        # Handle Input
        # To-Do: Gameplay needs this function to check input strings
        # Use pygame to check if letters are typed, store the letters.
        # Check the buffer against the word options.
        if event.type == pygame.KEYDOWN:
            if self.state == "play":
                if event.type == pygame.K_ESCAPE:
                    self.state = "pause"
            elif self.state == "pause":
                if event.type == pygame.K_ESCAPE:
                    self.state = "play"
        if self.state == "play":
            pygame.key.start_text_input()
            for event in pygame.event.get():
                if event.type == pygame.TEXTINPUT:
                    input_text += event.text
                    if input_text in self.game.current_words:
                        self.game.update_score(10)
                        self.game.update_time(5.0)
                        self.game.update_words(['four', 'five', 'six']) # Placeholder for new words
                        pygame.key.stop_text_input()
                        print("Correct Input")
                    else:
                        print("Incorrect Input")
                        pass
        pygame.event.clear()

        
        
    def start_game(self, difficulty_multiplier: int):
        # Start Game
        self.difficulty_multiplier = difficulty_multiplier
        self.game = Game(self.difficulty_multiplier)
        self.state = "play"
    
    def end_game(self):
        # End Game
        self.state = "end"