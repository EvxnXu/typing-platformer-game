import pygame
from views import Graphics
from controllers import GameController

if __name__ == "__main__":
    pygame.init()
    
    graphics = Graphics()
    
    game_controller = GameController()
    
    running = True
    # Main Game Loop
    while running:
        
        dtime = game_controller.clock.tick(60) / 1000
        pygame.display.update()
        match game_controller.state:
            
            case "Menu":
                # Menu State
                graphics.render_main_menu()
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    
                    click = graphics.check_button_clicked(event)
                    if click == "Play":
                        game_controller.start_game(game_controller.difficulty_multiplier)
                        
                        # Do we need to implement graphics.clear_graphics() so 
                        # stuff doesn't overlap?
                        graphics.render_game()
                    elif click == "Difficulty":
                        # Depends on how many difficulties/dictionaries we want
                        game_controller.difficulty_multiplier += 1
                        if game_controller.difficulty_multiplier > 3:
                            game_controller.difficulty_multiplier = 1
                        game_controller.end_game()
                    
            case "Play":
                # Play State
                # To-do: render game
                graphics.render_game(game_controller.game)
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    
                    if event.type == pygame.K_ESCAPE:
                        game_controller.state = "Pause"
                    
                    game_controller.handle_input(event)
                    
                    if game_controller.game.is_over() == True:
                        game_controller.end_game()
                    
                    # Most gameplay would go here
                    
            case "Pause":
                # Pause State
                # To-do: render pause menu
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    
                    click = graphics.check_button_clicked(event)
                    if click == "Play":
                        game_controller.state = "Play"
                        
                    elif click == "Difficulty":
                        # Depends on how many difficulties/dictionaries we want
                        game_controller.difficulty_multiplier += 1
                        if game_controller.difficulty_multiplier > 3:
                            game_controller.difficulty_multiplier = 1
                        game_controller.end_game()
                        
            case "End":
                # End State
                # To-do: render end screen with leaderboard
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        
                    click = graphics.check_button_clicked(event)
                    if click == "Play":
                        game_controller.state = "Play"
                        
                    elif click == "Difficulty":
                        # Depends on how many difficulties/dictionaries we want
                        game_controller.difficulty_multiplier += 1
                        if game_controller.difficulty_multiplier > 3:
                            game_controller.difficulty_multiplier = 1
                        game_controller.end_game()
                        
            case _: # Default
                print("What?")
                game_controller.state = "Menu"
                
    pygame.quit()