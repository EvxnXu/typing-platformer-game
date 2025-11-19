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


    def draw(self, screen: pygame.Surface):
        """Draw the Character"""
        screen.blit(self.image, self.rect)
    

    def update_position(self, dx: int, dy: int):
        """Update the Position of the Character"""
        self.x += dx
        self.y += dy
        self.rect.topleft = (self.x, self.y)


    def teleport_to_platform(self, platform: Platform):
        """Teleport Character to Platform"""
        self.x = platform.x + (platform.width - self.width) // 2
        self.y = platform.y - self.height + platform.height // 6
        self.rect.topleft = (self.x, self.y)


    def get_size(self, screen: pygame.Surface):
        """Get Size of Character"""
        w = screen.get_size()[0]
        return w // 10, w // 10