import pygame
from controllers import GameController


if __name__ == "__main__":
    pygame.init()
    game_controller = GameController()
    game_controller.main_loop()
    print("Main Loop Ended. Game Exiting...")
    pygame.quit()