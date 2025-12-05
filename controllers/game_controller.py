"""Game Controller Class"""
import pygame
from models import Game, Record, Leaderboard, Word, WordManager
from views import Graphics

# Prototype Records and Words
prototype_records = [Record("Mario", 99), Record("Mario", 98), Record("Luigi", 95), Record("Bob the Builder", 90)]

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
        self.word_manager = WordManager()

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
                self.graphics.move_platforms()
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
                self.graphics.render_leaderboard(prototype_records)

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
                prototype_records.append(Record(self.current_input_string, self.game.score))
                self.current_input_string = ""
                self.state = "leaderboard"
        elif key == pygame.K_BACKSPACE:
            if self.state == "play":
                self.current_input_string = self.current_input_string[:-1]
    

    def handle_click(self, click):
        """Handle Mouse Click Events"""
        if click == "play":
            self.start_game(self.difficulty_multiplier)
            self.game.update_words(self.word_manager.get_three_cloud_words())
            self.graphics.init_game_elements(self.game.current_words)
            self.graphics.add_words(self.game.current_words)
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
                # Use the matched word's configured score (apply game multiplier)
                matched_word_obj = None
                for w in self.game.current_words:
                    if w.word == self.current_input_string:
                        matched_word_obj = w
                        break
                if matched_word_obj is not None:
                    score_value = int(matched_word_obj.score * self.game.multiplier)
                else:
                    # fallback to 10 if something unexpected happened
                    score_value = 10
                self.game.update_score(score_value)
                self.game.update_time(5.0)
                # Fetch a fresh set of words from the (possibly updated) difficulty window
                # Passing `increment_correct=True` marks this fetch as occurring after a correct guess
                # and allows the WordManager to advance difficulty when the session threshold is met.
                self.game.update_words(self.word_manager.get_three_cloud_words(increment_correct=True))
                self.graphics.update_platforms(self.current_input_string)
                self.graphics.add_words(self.game.current_words)
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
        #TODO: Save Record