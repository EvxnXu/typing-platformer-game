"""Game Controller Class"""
import pygame
from ..views import Graphics
from ..models import Game
from ..models import Record
from ..models import Leaderboard

class GameController():
    
    def __init__(self):
        pygame.init()
        
        self.state = "Menu"
        self.clock = pygame.time.Clock()
        self.difficulty_multiplier = 1
        self.game = Game(self.difficulty_multiplier)
        self.record = Record()
        self.leaderboard = Leaderboard()
        
        
    def handle_input(self, event: pygame.event):
        # Handle Input
        # To-Do: Gameplay needs this function to check input strings
        # Use pygame to check if letters are typed, store the letters.
        # Check the buffer against the word options.
        if event.type == pygame.KEYDOWN:
            if self.state == "Play":
                if event.key == pygame.K_ESCAPE:
                    self.state == "Pause"
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
        
        
if __name__ == "__main__":
    graphics = Graphics()
    
    game_controller = GameController()
   
    running = True
    # Main Game Loop
    while running:
        
        game_controller.clock.tick(60)
        
        match game_controller.state:
            
            case "Menu":
                # Menu State
                graphics.render_main_menu()
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        break
                    
                    click = graphics.check_button_clicked(event)
                    if click == "Play":
                        game_controller.start_game()
                        
                        # Do we need to implement graphics.clear_graphics() so 
                        # stuff doesn't overlap?
                        graphics.render_game()
                    elif click == "Settings":
                        game_controller.state = "Settings"

            case "Settings":
                # Settings State
                graphics.render_settings()
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        break
                    if event.type == pygame.K_ESCAPE:
                        # graphics.Clear()????
                        graphics.render_main_menu()
                        game_controller.state = "Menu"
                        break
                    click = graphics.check_button_clicked(event)
                    if click == "Difficulty":
                        # Depends on how many difficulties/dictionaries we want
                        game_controller.difficulty_multiplier += 1
                        if game_controller.difficulty_multiplier > 3:
                            game_controller.difficulty_multiplier = 1
                        game_controller.end_game()
                    
        
            case "Play":
                # Play State
                # To-do: render game 
                graphics.render_game(game_controller.game)
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        break
                    if event.type == pygame.K_ESCAPE:
                        game_controller.state = "Pause"
                        break
                    if game_controller.game.is_over() == True:
                        game_controller.state = "End"
                        break
                    game_controller.handle_input(event)
                    
                    # Most gameplay would go here
                    

            case "Pause":
                # Pause State
                # To-do: render pause menu
                graphics.render_pause_menu()
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    
                    game_controller.handle_input(event)
                    
                    click = graphics.check_button_clicked(event)
                    if click == "Play":
                        game_controller.state = "Play"
                        break
                    elif click == "Settings":
                        graphics.render_settings()
                    if click == "Difficulty":
                        # Depends on how many difficulties/dictionaries we want
                        game_controller.difficulty_multiplier += 1
                        if game_controller.difficulty_multiplier > 3:
                            game_controller.difficulty_multiplier = 1
                        game_controller.end_game()
                        

            case "End":
                # End State
                graphics.render_end_screen(game_controller.game, game_controller.record)
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        break
                    click = graphics.check_button_clicked(event)
                    if click == "Play":
                        game_controller.state = "Play"
                        break
                    elif click == "Settings":
                        game_controller.state = "Settings"
                        
                        
            
            case _: # Default
                print("What?")
                game_controller.state = "Menu"
                
    pygame.quit()