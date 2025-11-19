import pygame
from views import Graphics
from controllers import GameController

if __name__ == "__main__":
    pygame.init()
    
    graphics = Graphics()
    
    game_controller = GameController()
    
    username = ""
    running = True
    # Main Game Loop
    while running:
        
        dtime = game_controller.clock.tick(60) / 1000.0
        pygame.display.update()
        if game_controller.state == "menu":
            graphics.render_main_menu()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click = graphics.check_button_clicked(event)
                    if click == "play":
                        game_controller.start_game(game_controller.difficulty_multiplier)
                    elif click == "difficulty":
                        game_controller.difficulty_multiplier += 1
                        if game_controller.difficulty_multiplier > 3:
                            game_controller.difficulty_multiplier = 1
            pygame.event.clear()
        elif game_controller.state == "play":
            game_controller.game.update_time(-dtime)
            graphics.render_game()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

                game_controller.handle_input(event)
            pygame.event.clear()
            if game_controller.game.is_over():
                game_controller.end_game()

        elif game_controller.state == "pause":
            graphics.render_pause_menu()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click = graphics.check_button_clicked(event)
                    if click == "play":
                        game_controller.state = "play"
                    elif click == "difficulty":
                        game_controller.difficulty_multiplier += 1
                        if game_controller.difficulty_multiplier > 3:
                            game_controller.difficulty_multiplier = 1
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    game_controller.state = "play"

            pygame.event.clear()

        elif game_controller.state == "end":
            graphics.render_leaderboard([])
            pygame.display.update()
            pygame.key.start_text_input()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                if event.type == pygame.TEXTINPUT:
                    username += event.text
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click = graphics.check_button_clicked(event)
                    if click == "play":
                        game_controller.start_game(game_controller.difficulty_multiplier)
                        username = ""
                    elif click == "difficulty":
                        game_controller.difficulty_multiplier += 1
                        if game_controller.difficulty_multiplier > 3:
                            game_controller.difficulty_multiplier = 1

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    game_controller.state = "play"
            pygame.event.clear()
            pygame.key.stop_text_input()        
            
        else:
            game_controller.state = "menu"
        
        pygame.display.flip()
                    
    pygame.quit()