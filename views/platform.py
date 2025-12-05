"""Platform Class"""
import pygame
import random

class Platform:
    def __init__(self, screen: pygame.Surface, image: pygame.Surface, word: str, existing: list = []):
        """Initialize Platform"""
        self.width, self.height = self.get_size(screen)
        self.x, self.y = self.get_random_coords(screen, existing)
        self.dest_x, self.dest_y = self.x, self.y
        self.word = word
        self.image = pygame.transform.scale(image, (self.width, self.height))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.speed = max(5, screen.get_width() // 150)


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
        font_size = self.height // 4
        self.font = pygame.font.Font("assets/Kenney Mini.ttf", font_size)
        

    def get_size(self, screen: pygame.Surface):
        """Get Size of Platform"""
        w = screen.get_size()[0]
        return w // 3, w // 9
    

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
    
    def update_destination(self, dx: int, dy: int):
        """Set the Destination of the Platform"""
        self.dest_x += dx
        self.dest_y += dy
    
    def update_position(self, W: int, H: int) -> bool:
        """Update the Position of the Platform, return False if moving offscreen"""
        
        dx = self.dest_x - self.x
        dy = self.dest_y - self.y

        # At Destination
        if dx == 0 and dy == 0:
            return True

        # Computer Remaining Distance to Move
        dist_squared = dx*dx + dy*dy
        speed = self.speed
        
        # If Close enough, snap to destination
        if dist_squared <= speed * speed:
            self.x = self.dest_x
            self.y = self.dest_y
            self.rect.topleft = (self.x, self.y)
            return True
        
        # Calculate Movement
        dist = dist_squared ** 0.5
        step_x = speed * dx / dist
        step_y = speed * dy / dist

        # Apply Movement
        self.x += step_x
        self.y += step_y
        
        # Bounds check for off-screen
        if not (0 <= self.x <= W - self.width and 
                0 <= self.y <= H - self.height):
            return False

        # Update rect
        self.rect.topleft = (int(self.x), int(self.y))
        return True