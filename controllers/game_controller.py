"""Game Controller Class"""
import pygame
from models import Game, Record, Leaderboard, Word
from views import Graphics

# Prototype Records and Words
prototype_records = [Record("Mario", 99), Record("Mario", 98), Record("Luigi", 95), Record("Bob the Builder", 90)]
prototype_words = []
for word in ["Example", "Typing", "Words", "Platform", "Python", "Programming", "Development", "Controller", "Graphics", "Functionality"]:
    prototype_words.append(Word(10, word))

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
        pygame.key.start_text_input()

        # Main Game Loop
        while running:
            
            dtime = self.clock.tick(60) / 1000.0
            pygame.display.update()

            # Render According to State

            # Main Menu State
            if self.state == "menu":
                self.graphics.render_main_menu()
            
            # Play State
            if self.state == "play":
                self.game.update_time(-dtime)
                if self.game.is_over():
                    self.state = "end"
                    self.current_input_string = ""
                    self.graphics.render_end_game(self.game.score, self.current_input_string)
                else:
                    self.graphics.render_game(self.game, self.current_input_string)

            # Pause State
            elif self.state == "pause":
                self.graphics.render_pause_menu()

            # Leaderboard State
            elif self.state == "leaderboard":
                self.graphics.render_leaderboard(self.leaderboard.get_top_records())

            # End Game State
            elif self.state == "end":
                self.graphics.render_end_game(self.game.score, self.current_input_string) 


            # Global Event Handling
            for event in pygame.event.get():

                # Quit Game Event
                if event.type == pygame.QUIT:
                    running = False
                    break

                # Text Input
                elif event.type == pygame.TEXTINPUT:
                    self.handle_input(event.text)

                # Keystrokes
                elif event.type == pygame.KEYDOWN:
                    self.handle_key(event.key)

                # Mouse Clicks
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(self.graphics.check_button_clicked(event))
        
        # Stop Text Input when Exiting Game
        pygame.key.stop_text_input()  
    

    def handle_key(self, key):
        """Handle Keystroke Events"""
        if key == pygame.K_ESCAPE:
            if self.state == "play":
                self.state = "pause"
            elif self.state == "pause":
                self.state = "play"
            elif self.state == "leaderboard":
                self.state = "menu"
        elif key == pygame.K_RETURN:
            if self.state == "end":
                self.leaderboard.add_record(Record(self.current_input_string, self.game.score))
                self.current_input_string = ""
                self.state = "leaderboard"
        elif key == pygame.K_BACKSPACE:
            if self.state == "play":
                self.current_input_string = self.current_input_string[:-1]
    

    def handle_click(self, click):
        """Handle Mouse Click Events"""
        if click == "play":
            self.start_game(self.difficulty_multiplier)
            words = []
            for i in range(3):
                words.append(prototype_words[-i])
            self.game.update_words(words) # Placeholder for new words
            self.graphics.init_game_elements(words)
            self.graphics.add_words(words)
            self.state = "play"
        elif click == "leaderboard":
            self.state = "leaderboard"
        elif click == "difficulty":
            self.difficulty_multiplier += 1
            if self.difficulty_multiplier > 3:
                self.difficulty_multiplier = 1
        elif click == "resume":
            self.state = "play"
        elif click == "end":
            self.state = "end"
        elif click == "close":
            self.state = "menu"

        
    def handle_input(self, text: str):
        """Handle Input During Gameplay"""
        # print(f"Handling Input: {text}")
        # To-Do: Gameplay needs this function to check input strings
        # Use pygame to check if letters are typed, store the letters.
        # Check the buffer against the word options.
        self.current_input_string += text

        if self.state == "play":
            print(f"Validating Input... {self.current_input_string}")
            if self.game.validate_word(self.current_input_string):
                # Prototype Logic for Handling Correct Input
                self.game.update_score(10)
                self.game.update_time(5.0)
                words = []
                for i in range(3):
                    words.append(prototype_words[i])
                self.game.update_words(words) # Placeholder for new words
                self.graphics.update_platforms(self.current_input_string)
                self.graphics.add_words(words)
                self.current_input_string = ""
                print("Correct Input")
            else:
                self.graphics.render_game(self.game, self.current_input_string)

        print("End Input Handling")

        
    def start_game(self, difficulty_multiplier: int):
        """Start Game"""
        self.difficulty_multiplier = difficulty_multiplier
        self.game = Game(self.difficulty_multiplier)
        self.state = "play"
    

    def end_game(self):
        """End Game"""
        self.state = "end"