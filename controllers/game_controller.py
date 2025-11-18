"""Game Controller Class"""
import pygame
from views import Graphics
from models import Game
from models import Record
from models import Leaderboard

class GameController():
    
    def __init__(self):
        pygame.init()
        
        self.state = "Menu"
        self.clock = pygame.time.Clock()
        self.difficulty_multiplier = 1
        self.game = Game(self.difficulty_multiplier)
        self.records = list[Record()]
        self.leaderboard = Leaderboard()
        
        
    def handle_input(self, event: pygame.event):
        # Handle Input
        # To-Do: Gameplay needs this function to check input strings
        # Use pygame to check if letters are typed, store the letters.
        # Check the buffer against the word options.
        if event.type == pygame.KEYDOWN:
            if self.state == "Play":
                if event.key == pygame.K_ESCAPE:
                    self.state = "Pause"
            elif self.state == "Pause":
                if event.key == pygame.K_ESCAPE:
                    self.state = "Play"
        
        
    def start_game(self, difficulty_multiplier: int):
        # Start Game
        self.game.multiplier = difficulty_multiplier
        self.game = Game(self.game.multiplier)
        self.state = "Play"
    
    def end_game(self):
        # End Game
        self.state = "End"