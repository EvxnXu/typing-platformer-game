"""Game Controller Class"""
import pygame
from models import Game, Record, Leaderboard, Word
from views import Graphics

# Prototype Records and Words
prototype_records = [Record("Mario", 99), Record("Mario", 98), Record("Luigi", 95), Record("Bob the Builder", 90)]
prototype_words = []
for word in ["Example", "Typing", "Words", "Platform", "Python", "Programming", "Development", "Controller", "Graphics", "Functionality"]:
    prototype_words.append([Word(10, word)])

class GameController():
    
    def __init__(self):
        pygame.init()
        self.graphics = Graphics()
        self.clock = pygame.time.Clock()
        self.game: Game = None
        self.leaderboard = Leaderboard()
        self.state = "menu"
        self.difficulty_multiplier = 1
        self.current_input_string = ""

    def main_loop(self):
        running = True

        # Main Game Loop
        while running:
            
            dtime = self.clock.tick(60) / 1000.0
            pygame.display.update()

            # Main Menu State
            if self.state == "menu":
                self.graphics.render_main_menu()
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        break
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        click = self.graphics.check_button_clicked(event)
                        if click == "play":
                            self.start_game(self.difficulty_multiplier)
                        elif click == "leaderboard":
                            self.state = "leaderboard"
                        elif click == "difficulty":
                            self.difficulty_multiplier += 1
                            if self.difficulty_multiplier > 3:
                                self.difficulty_multiplier = 1
                pygame.event.clear()
            
            # Game Playing State
            elif self.state == "play":
                self.game.update_time(-dtime)
                self.graphics.render_game()
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        break
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.state = "pause"
                        break
                    self.handle_input(event)
                pygame.event.clear()
                if self.game.is_over():
                    self.end_game()

            # Pause State
            elif self.state == "pause":
                self.graphics.render_pause()
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        break
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        click = self.graphics.check_button_clicked(event)
                        if click == "resume":
                            self.state = "play"
                        elif click == "end":
                            self.state = "end"
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.state = "play"

                pygame.event.clear()

            # Leaderboard State
            elif self.state == "leaderboard":
                self.graphics.render_leaderboard(prototype_records)
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        break
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        click = self.graphics.check_button_clicked(event)
                        if click == "close":
                            self.state = "menu"
                pygame.event.clear()

            # End Game State
            elif self.state == "end":
                self.graphics.render_end_game(self.game.score, self.current_input_string)
                pygame.display.update()
                pygame.key.start_text_input()
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        break
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        # Save Record
                        prototype_records.append(Record(self.current_input_string, self.game.score))
                        self.state = "leaderboard"
                        self.current_input_string = ""
                        break
                    elif event.type == pygame.TEXTINPUT:
                        self.current_input_string += event.text
                pygame.event.clear()
                pygame.key.stop_text_input()        
                
            else:
                self.state = "menu"
            
            pygame.display.flip()
        
        
    def handle_input(self, event: pygame.event):
        """Handle Input"""
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
                    self.current_input_string += event.text
                    if self.game.validate_word(self.current_input_string):
                        # Prototype Logic for Handling Correct Input
                        self.game.update_score(10)
                        self.game.update_time(5.0)
                        self.game.update_words([Word(10, "Example"), Word(10, "Typing"), Word(10, "Words")]) # Placeholder for new words
                        pygame.key.stop_text_input()
                        print("Correct Input")
                    else:
                        print("Incorrect Input")
                        pass
        pygame.event.clear()

        
    def start_game(self, difficulty_multiplier: int):
        """Start Game"""
        self.difficulty_multiplier = difficulty_multiplier
        self.game = Game(self.difficulty_multiplier)
        self.state = "play"
    

    def end_game(self):
        """End Game"""
        self.state = "end"