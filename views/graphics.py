"""Graphics Class"""
import pygame

class Assets:
    def __init__(self):
        self.character = pygame.image.load("assets/green-char.png", "character").convert_alpha()
        self.play = pygame.image.load("assets/play-banner.png", "play").convert_alpha()
        self.settings = pygame.image.load("assets/settings-cog.png", "settings").convert_alpha()


class Button:
    def __init__(self, x: int, y: int, w: int, h: int, image: pygame.Surface):
        """Initialize Button"""
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


    def render_main_menu(self):
        """Render the Main Menu onto the Screen"""
        # Get Size of Screen
        screen_W, screen_H = self.screen.get_size()

        # Fill Background
        bg = pygame.image.load("assets/main-menu.png").convert()
        bg = pygame.transform.scale(bg, (screen_W, screen_H))
        self.screen.blit(bg, (0, 0))

        # Create Buttons

        # Play Button
        button_w, button_h = self.get_play_button_size()
        play_x, play_y = self.anchor_bottom_middle(screen_W, screen_H, button_w, button_h)
        self.buttons.append(Button(play_x, play_y, button_w, button_h, self.assets.play))

        # Settings Button
        button_w, button_h = self.get_settings_button_size()
        settings_x, settings_y = self.anchor_top_right(screen_W, button_w)
        self.buttons.append(Button(settings_x, settings_y, button_w, button_h, self.assets.settings))

        # Draw Buttons
        for button in self.buttons:
            button.draw(self.screen)
            

    def check_button_clicked(self, event: pygame.event):
        """If event.type is pygame.MOUSEBUTTONDOWN, check all buttons to see if they've been clicked"""
        if event.type != pygame.MOUSEBUTTONDOWN:
            return
        
        for button in self.buttons:
            if button.is_clicked(event):
                # TODO: Communicate Button Behavior to Controller
                print(f"button was clicked.")
        return
    
            
    # Layout Helpers
    def anchor_top_left(self, w, h, margin = 10):
        return margin, margin
    

    def anchor_top_right(self, W: int, w: int, margin = 10):
        return W - w - margin, margin
    

    def anchor_bottom_middle(self, W: int, H: int, w: int, h: int):
        x = W // 2 - w // 2
        y = H - (H // 6) - h // 3
        return [x, y]


    # Helper Functions for Button Sizes
    def get_play_button_size(self) -> tuple[int, int]:
        W, H = self.screen.get_size()
        h = H //11.25
        w = h * 2.875
        return [w, h]
    
    def get_settings_button_size(self) -> tuple[int, int]:
        W, H = self.screen.get_size()
        return W // 20, H // 30