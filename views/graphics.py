"""Graphics Class"""
import pygame
from models import Record

class Assets:
    def __init__(self):
        self.background = pygame.image.load("assets/main-menu.png").convert_alpha()
        self.leaderboard = pygame.image.load("assets/leaderboard.png").convert_alpha()
        self.record_card = pygame.image.load("assets/record-card.png").convert_alpha()
        self.character = pygame.image.load("assets/green-char.png").convert_alpha()
        self.play = pygame.image.load("assets/play-banner.png").convert_alpha()
        self.settings = pygame.image.load("assets/settings-cog.png").convert_alpha()
        self.close = pygame.image.load("assets/close-button.png").convert_alpha()


class Button:
    def __init__(self, name: str, x: int, y: int, w: int, h: int, image: pygame.Surface):
        """Initialize Button"""
        self.name = name
        self.width, self.height = w, h
        self.image = pygame.transform.scale(image, (w, h))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=(x, y))


    def draw(self, surface: pygame.Surface):
        """Function to Draw button"""
        # Draw Button Rectangle
        # pygame.draw.rect(surface, Color.BACKGROUND.value, self.rect) # Default Color: Blue
        
        # Icon Mode
        img_rect = self.image.get_rect(center=self.rect.center)
        surface.blit(self.image, img_rect)


    def is_clicked(self, event: pygame.event.Event) -> bool:
        """Check if button was clicked"""
        # Mouse Coordinates
        mx, my = event.pos

        # Rectangle Check
        if not self.rect.collidepoint(mx, my):
            return False
        
        # Convert Mouse Coordinates to Image Coordinates
        lx, ly = mx - self.rect.x, my - self.rect.y

        # Pixel Perfect Check
        return self.mask.get_at((lx, ly)) == 1


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
        self.screen.blit(close, (leaderboard_x + leaderboard_width - close_width, leaderboard_y - (close_width * 0.25 )))

        # Add Record Cards
        record_width, record_height = screen_W * 0.7, screen_H * 0.05
        record_spacing = screen_H * 0.01
        record_card = pygame.transform.scale(self.assets.record_card, (record_width, record_height))

        for rank in range(min(10, len(records))):
            # Get the record data
            record = records[rank]

            # Add Record Card
            self.screen.blit(record_card, (screen_W * 0.15, leaderboard_y + (leaderboard_height * 0.05) + (record_height + record_spacing) * (rank)))

            # TODO: Overlay Record Text


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
        return [x, y]


    # Helper Functions for Button Sizes
    def play_button_size(self) -> tuple[int, int]:
        W, H = self.screen.get_size()
        h = H // 11.25
        w = h * 2.875
        return [w, h]
    
    
    def small_button_size(self) -> tuple[int, int]:
        """Calculate Width, Height of Small Button Relative to Screen Size"""
        W, H = self.screen.get_size()
        return W // 20, W // 20