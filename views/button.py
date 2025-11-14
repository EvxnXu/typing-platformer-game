"""Button Class"""
import pygame

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