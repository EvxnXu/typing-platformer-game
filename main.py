import pygame
from views import Graphics
from controllers import GameController

# Prototype Words and Records
from models import Word, Record

prototype_words = []
for word in ["example", "typing", "platform", "character", "difficulty", "leaderboard", "graphics", "controller", "function", "variable"]:
    prototype_words.append(Word(10, word))

prototype_records = [Record("Mario", 99), Record("Mario", 98), Record("Luigi", 95), Record("Bob the Builder", 90)]

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

        # Main Menu State
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
                    elif click == "leaderboard":
                        game_controller.state = "leaderboard"
                    elif click == "difficulty":
                        game_controller.difficulty_multiplier += 1
                        if game_controller.difficulty_multiplier > 3:
                            game_controller.difficulty_multiplier = 1
            pygame.event.clear()
        
        # Game Playing State
        elif game_controller.state == "play":
            game_controller.game.update_time(-dtime)
            graphics.render_game()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    game_controller.state = "pause"
                    break

                game_controller.handle_input(event)
            pygame.event.clear()
            if game_controller.game.is_over():
                game_controller.end_game()

        # Pause State
        elif game_controller.state == "pause":
            graphics.render_pause()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click = graphics.check_button_clicked(event)
                    if click == "resume":
                        game_controller.state = "play"
                    elif click == "end":
                        game_controller.state = "end"
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    game_controller.state = "play"

            pygame.event.clear()

        # Leaderboard State
        elif game_controller.state == "leaderboard":
            graphics.render_leaderboard(prototype_records)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click = graphics.check_button_clicked(event)
                    if click == "close":
                        game_controller.state = "menu"
            pygame.event.clear()

        # End Game State
        elif game_controller.state == "end":
            graphics.render_end_game(game_controller.game.score, username)
            pygame.display.update()
            pygame.key.start_text_input()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    # Save Record
                    prototype_records.append(Record(username, game_controller.game.score))
                    game_controller.state = "leaderboard"
                    username = ""
                    break
                elif event.type == pygame.TEXTINPUT:
                    username += event.text
            pygame.event.clear()
            pygame.key.stop_text_input()        
            
        else:
            game_controller.state = "menu"
        
        pygame.display.flip()
                    
    pygame.quit()