"""Platform Class"""
import pygame
import random

class Platform:
    def __init__(self, screen: pygame.Surface, image: pygame.Surface, word: str, existing: list = []):
        """Initialize Platform"""
        self.width, self.height = self.get_size(screen)
        self.x, self.y = self.get_random_coords(screen, existing)
        self.word = word
        self.image = pygame.transform.scale(image, (self.width, self.height))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))


    def draw(self, screen: pygame.Surface):
        """Draw the Platform"""
        screen.blit(self.image, self.rect)
        self.render_word(screen)


    def render_word(self, screen: pygame.Surface):
        """Render the word on the platform"""
        self.fit_font()
        word_surf = self.font.render(self.word, True, (0, 0, 0))
        word_rect = word_surf.get_rect(center = self.rect.center)
        screen.blit(word_surf, word_rect)


    def fit_font(self):
        """Fit Font Size to Platform"""
        font_size = self.height // 3
        self.font = pygame.font.Font("assets/Kenney Mini.ttf", font_size)
        

    def get_size(self, screen: pygame.Surface):
        """Get Size of Platform"""
        w = screen.get_size()[0]
        return w // 4, w // 12
    

    def get_random_coords(self, screen: pygame.Surface, existing: list) -> tuple[int, int]:
        """Get Random Coordinates for Platform"""
        W, H = screen.get_size()

        while True: 
            x = random.randint(0, W - self.width)
            y = random.randint(H // 12, H // 2 - self.height)
            
            new_rect = pygame.Rect(x, y, self.width, self.height)

            if not any(new_rect.colliderect(platform.rect) for platform in existing):
                return x, y
    

    def current_position(self) -> tuple[int, int]:
        """Get Current Position of the Platform"""
        return self.x, self.y
    
    
    def update_position(self, dx: int, dy: int, W: int, H: int) -> bool:
        """Update the Position of the Platform"""
        self.x += dx
        self.y += dy

        # Compute boundaries
        left = self.x
        right = self.x + self.width
        top = self.y
        bottom = self.y + self.height

        # Check for fully out of bounds
        if right < 0 or left > W or bottom < 0 or top > H:
            return False

        # Update rect
        self.rect.topleft = (self.x, self.y)
        return True