"""Graphics Class"""
import pygame
from models import Record
from .button import Button

class Assets:
    def __init__(self):
        pygame.font.init()
        self.font = pygame.font.Font("assets/Kenney Future Narrow.ttf")
        self.background = pygame.image.load("assets/main-menu.png").convert_alpha()
        self.settings = pygame.image.load("assets/settings-cog.png").convert_alpha()
        self.play = pygame.image.load("assets/play-banner.png").convert_alpha()
        self.leaderboard = pygame.image.load("assets/leaderboard.png").convert_alpha()
        self.record_card = pygame.image.load("assets/record-card.png").convert_alpha()
        self.close = pygame.image.load("assets/close-button.png").convert_alpha()
        self.character = pygame.image.load("assets/green-char.png").convert_alpha()


class Graphics:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.assets = Assets()
        self.buttons: list[Button] = []


    # Functions for Rendering Screens
    def render_main_menu(self):
        """Render the Main Menu onto the Screen"""
        # Get Size of Screen
        screen_W, screen_H = self.screen.get_size()

        # Fill Background
        bg = pygame.transform.scale(self.assets.background, (screen_W, screen_H))
        self.screen.blit(bg, (0, 0))

        # Create Buttons

        # Play Button
        button_w, button_h = self.play_button_size()
        play_x, play_y = self.anchor_bottom_middle(screen_W, screen_H, button_w, button_h)
        self.buttons.append(Button("play", play_x, play_y, button_w, button_h, self.assets.play))

        # Settings Button
        button_w, button_h = self.small_button_size()
        settings_x, settings_y = self.anchor_top_right(screen_W, button_w)
        self.buttons.append(Button("settings", settings_x, settings_y, button_w, button_h, self.assets.settings))

        # TODO: Add Difficulty Buttons

        # Draw Buttons
        for button in self.buttons:
            button.draw(self.screen)
            
    
    def render_settings(self):
        pass


    def render_game(self):
        pass


    def render_leaderboard(self, records: list[Record]):
        """Render Leaderboard"""
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
    

    def anchor_bottom_middle(self, W: int, H: int, w: int, h: int):
        x = W // 2 - w // 2
        y = H - (H // 6) - h // 3
        return x, y


    # Helper Functions for Button Sizes
    def play_button_size(self) -> tuple[int, int]:
        W, H = self.screen.get_size()
        h = H // 11.25
        w = h * 2.875
        return w, h
    
    
    def small_button_size(self) -> tuple[int, int]:
        """Calculate Width, Height of Small Button Relative to Screen Size"""
        W, H = self.screen.get_size()
        return W // 20, W // 20