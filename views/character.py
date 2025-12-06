"""Character Class"""
import pygame
from .platform import Platform

class Character:
    def __init__(self, screen: pygame.Surface, image: pygame.Surface):
        """Initialize Character"""
        self.width, self.height = self.get_size(screen)
        self.x, self.y = 0, 0
        self.image = pygame.transform.scale(image, (self.width, self.height))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.attatched = False
        self.target_platform = None


    def draw(self, screen: pygame.Surface):
        """Draw the Character"""
        screen.blit(self.image, self.rect)

    
    def update_platform(self, platform: Platform):
        """Change Target Platform"""
        self.attatched = False
        self.target_platform = platform
    

    def update_position(self):
        """Update the Position of the Character"""
        if self.attatched:
            self.teleport_to_platform()
            return
        
        dx = self.target_platform.x + (self.target_platform.width - self.width) // 2 - self.x
        dy = self.target_platform.y - (self.height + self.target_platform.height) // 6 - self.y
        dist = (dx * dx + dy * dy) ** 0.5
        if dist <= 5:
            self.teleport_to_platform()
        else:
            self.x += dx / dist * 5
            self.y += dy / dist * 5
            self.rect.topleft = (self.x, self.y)


    def teleport_to_platform(self):
        """Teleport Character to Platform"""
        self.attatched = True
        self.x = self.target_platform.x + (self.target_platform.width - self.width) // 2
        self.y = self.target_platform.y - self.height + self.target_platform.height // 6
        self.rect.topleft = (self.x, self.y)


    def get_size(self, screen: pygame.Surface):
        """Get Size of Character"""
        w = screen.get_size()[0]
        return w // 10, w // 10