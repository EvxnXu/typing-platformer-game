"""Graphics Class"""
import pygame
from models import Record, Word
from .button import Button
from .platform import Platform
from .character import Character

class Assets:
    """Asset Class to Load and store Game Assets"""
    def __init__(self):
        pygame.font.init()
        self.font = pygame.font.Font("assets/Kenney Future Narrow.ttf", 18)
        self.background = pygame.image.load("assets/background.png").convert_alpha()
        self.main_menu = pygame.image.load("assets/main-menu.png").convert_alpha()
        self.settings = pygame.image.load("assets/settings-cog.png").convert_alpha()
        self.play = pygame.image.load("assets/play-banner.png").convert_alpha()
        self.leaderboard = pygame.image.load("assets/leaderboard.png").convert_alpha()
        self.record_card = pygame.image.load("assets/record-card.png").convert_alpha()
        self.close = pygame.image.load("assets/close-button.png").convert_alpha()
        self.character = pygame.image.load("assets/green-char.png").convert_alpha()
        self.cloud = pygame.image.load("assets/cloud.png").convert_alpha()


class Graphics:
    def __init__(self): 
        w = pygame.display.Info().current_w
        self.screen =  pygame.display.set_mode((w/4, w/4*1.5))
        pygame.display.set_caption("Test")

        self.assets = Assets()
        self.buttons: list[Button] = []
        self.platforms: list[Platform] = []
        self.character = Character(self.screen, self.assets.character)


    # Functions for Rendering States Onto the Screen
    def render_main_menu(self):
        """Render the Main Menu onto the Screen"""
        self.buttons = []
        # Get Size of Screen
        screen_W, screen_H = self.screen.get_size()

        # Fill Background
        bg = pygame.transform.scale(self.assets.main_menu, (screen_W, screen_H))
        self.screen.blit(bg, (0, 0))

        # Create Buttons

        # Play Button
        button_w, button_h = self.banner_size()
        play_x, play_y = screen_W // 2 - button_w // 2, screen_H - (screen_H // 6) - button_h // 3
        self.buttons.append(Button("play", play_x, play_y, button_w, button_h, self.assets.play))

        # Settings Button
        button_w, button_h = self.small_button_size()
        settings_x, settings_y = self.anchor_top_right(screen_W, button_w)
        self.buttons.append(Button("leaderboard", settings_x, settings_y, button_w, button_h, self.assets.settings))

        # TODO: Add Difficulty Button

        # Draw Buttons
        for button in self.buttons:
            button.draw(self.screen)
            
    
    def render_pause(self):
        self.buttons = []
        # Get Size of Screen
        screen_W, screen_H = self.screen.get_size()

        # Fill Background
        bg = pygame.transform.scale(self.assets.background, (screen_W, screen_H))
        self.screen.blit(bg, (0, 0))

        # Add Pause Card
        pause_width, pause_height = screen_W * 0.6, screen_W * 0.9
        pause_x, pause_y = screen_W * 0.2, screen_H * 0.2
        pause = pygame.transform.scale(self.assets.leaderboard, (pause_width, pause_height))

        self.screen.blit(pause, (pause_x, pause_y))

        # Resume Button
        button_w, button_h = self.banner_size()
        resume_x, resume_y = screen_W // 2 - button_w // 2, pause_y + button_h
        self.buttons.append(Button("resume", resume_x, resume_y, button_w, button_h, self.assets.record_card))

        # End Game Button
        button_w, button_h = self.banner_size()
        end_x, end_y = resume_x, resume_y + button_h * 1.5
        self.buttons.append(Button("end", end_x, end_y, button_w, button_h, self.assets.record_card))
        
        # Draw Buttons
        for button in self.buttons:
            button.draw(self.screen)
            button.render_text_center(button.name, self.assets.font, self.screen)


    def render_game(self, new_words: list[Word] = [], matched_word: str = None):
        self.buttons = []
        # Get Size of Screen
        screen_W, screen_H = self.screen.get_size()

        # Fill Background
        bg = pygame.transform.scale(self.assets.background, (screen_W, screen_H))
        self.screen.blit(bg, (0, 0))

        # If No Platforms Exist, Create Initial Platform and Place Character on It
        if not self.platforms:
            initial_platform = Platform(self.screen, self.assets.cloud, "start")
            initial_platform.x, initial_platform.y = self.anchor_middle(screen_W, screen_H, initial_platform.width, initial_platform.height)
            initial_platform.rect.topleft = (initial_platform.x, initial_platform.y)
            self.platforms.append(initial_platform)
            self.character.teleport_to_platform(initial_platform)

        # Update the Location of Current Platforms if Applicable
        if matched_word:
            dx, dy = 0, 0
            # Calculate Displacement to Center Matched Platform
            for platform in self.platforms:
                if platform.word == matched_word:
                    dest_x, dest_y = self.anchor_middle(screen_W, screen_H, platform.width, platform.height)
                    curr_x, curr_y = platform.current_position()
                    dx, dy = curr_x - dest_x, curr_y - dest_y
            # Update Positions of All Platforms and Character
            for platform in self.platforms:
                platform.update_position(-dx, -dy)
                if platform.word == matched_word:
                    self.character.teleport_to_platform(platform)

        # Add Platforms for New Words if Applicable
        for word in new_words:
            print(word.word)
            platform = Platform(self.screen, self.assets.cloud, word.word, self.platforms)
            platform.draw(self.screen)
            self.platforms.append(platform)

        # Draw Platforms
        for platform in self.platforms:
            platform.draw(self.screen)

        # Draw the Character
        self.character.draw(self.screen)


    def render_leaderboard(self, records: list[Record]):
        """Render Leaderboard"""
        self.buttons = []
        # Get Size of Screen
        screen_W, screen_H = self.screen.get_size()

        # Fill Background
        bg = pygame.transform.scale(self.assets.background, (screen_W, screen_H))
        self.screen.blit(bg, (0, 0))

        # Add Leaderboard Card
        leaderboard_width, leaderboard_height = screen_W * 0.8, screen_W * 1.2
        leaderboard_x, leaderboard_y = screen_W * 0.1, screen_H * 0.1
        leaderboard = pygame.transform.scale(self.assets.leaderboard, (leaderboard_width, leaderboard_height))

        self.screen.blit(leaderboard, (leaderboard_x, leaderboard_y))

        # Add Close Button
        close_width, close_height = self.small_button_size()
        close = pygame.transform.scale(self.assets.close, (close_width, close_height))
        self.buttons.append(Button("close", (leaderboard_x + leaderboard_width - close_width * 2), (leaderboard_y - (close_width * 0.2 )), close_width, close_height, close))

        # TODO: Add Column Labels for Records

        # Add Record Cards
        record_width, record_height = screen_W * 0.7, screen_H * 0.05
        record_spacing = screen_H * 0.01
        record_card = pygame.transform.scale(self.assets.record_card, (record_width, record_height))

        for rank in range(min(10, len(records))):
            # Get the record data
            record = records[rank]

            # Add Record Card
            record_y = leaderboard_y + (leaderboard_height * 0.05) + (record_height + record_spacing) * (rank)
            record_x = screen_W * 0.15
            self.screen.blit(record_card, (record_x, record_y))

            # Render Text
            rank_text = self.assets.font.render(str(rank + 1), True, (255, 255, 255))
            name_text = self.assets.font.render(record.username, True, (255, 255, 255))
            score_text = self.assets.font.render(str(record.score), True, (255, 255, 255))

            # Display Text
            text_y = record_y + (record_height // 2) - (name_text.get_height() // 2)

            self.screen.blit(rank_text, (record_x + (record_width // 30), text_y))
            self.screen.blit(name_text, (record_x + (record_width // 10), text_y))
            self.screen.blit(score_text, (screen_W * 0.825 - score_text.get_width(), text_y))

        for button in self.buttons:
            button.draw(self.screen)


    def check_button_clicked(self, event: pygame.event):
        """If event was mouse click, return clicked button if applicable"""
        if event.type != pygame.MOUSEBUTTONDOWN:
            return None
        
        for button in self.buttons:
            if button.is_clicked(event):
                print(f"{button.name} was clicked.")
                return button.name
        
        return None
    

    # Layout Helpers
    def anchor_top_left(self, margin = 10):
        return margin, margin
    

    def anchor_top_right(self, W: int, w: int, margin = 10):
        return W - w - margin, margin
    

    def anchor_middle(self, W: int, H: int, w: int, h: int):
        return W // 2 - w // 2, H // 2 - h // 2


    # Button Helpers
    def banner_size(self) -> tuple[int, int]:
        W, H = self.screen.get_size()
        h = H // 11.25
        w = h * 2.875
        return w, h
    
    
    def small_button_size(self) -> tuple[int, int]:
        """Calculate Width, Height of Small Button Relative to Screen Size"""
        W, H = self.screen.get_size()
        return W // 20, W // 20