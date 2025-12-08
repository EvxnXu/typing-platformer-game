"""Graphics Class"""
import pygame
from models import Record, Word, Game
from .button import Button
from .platform import Platform
from .character import Character
from utils import resource_path

class Assets:
    """Asset Class to Load and store Game Assets"""
    def __init__(self, W, H):
        """Load and Scale all Assets to Screen Size"""
        pygame.font.init()
        self.font = pygame.font.Font(resource_path("assets/boldpixels.boldpixels.ttf"), 18)
        self.background = pygame.image.load(resource_path("assets/background.png")).convert_alpha()
        self.main_menu = pygame.image.load(resource_path("assets/main-menu.png")).convert_alpha()
        self.leaderboard_icon = pygame.image.load(resource_path("assets/leaderboard-icon.png")).convert_alpha()
        self.play = pygame.image.load(resource_path("assets/play-banner.png")).convert_alpha()
        self.leaderboard = pygame.image.load(resource_path("assets/leaderboard.png")).convert_alpha()
        self.record_card = pygame.image.load(resource_path("assets/record-card.png")).convert_alpha()
        self.close = pygame.image.load(resource_path("assets/close-button.png")).convert_alpha()
        self.character = pygame.image.load(resource_path("assets/green-char.png")).convert_alpha()
        self.cloud = pygame.image.load(resource_path("assets/cloud.png")).convert_alpha()

        platform_w, platform_h = W // 3, W // 9
        self.platform = pygame.transform.scale(
            self.cloud, (platform_w, platform_h)
        )

class Graphics:
    def __init__(self): 
        self.W, self.H = pygame.display.Info().current_h * 0.8 / 1.5, pygame.display.Info().current_h * 0.8
        self.screen = pygame.display.set_mode((self.W, self.H))
        pygame.display.set_caption("Type Up! Client")

        self.current_platform = None
        self.dx, self.dy = 0, 0

        self.assets = Assets(self.W, self.H)
        self.buttons: list[Button] = []
        self.platforms: list[Platform] = []
        self.character = Character(self.screen, self.assets.character)


    # Functions for Rendering States Onto the Screen
    def render_main_menu(self, difficulty: int):
        """Render the Main Menu onto the Screen"""
        self.buttons = []

        # Fill Background
        bg = pygame.transform.scale(self.assets.main_menu, (self.W, self.H))
        self.screen.blit(bg, (0, 0))

        # Create Buttons

        # Play Button
        button_w, button_h = self.banner_size()
        play_x, play_y = self.W // 2 - button_w // 2, self.H - (self.H // 6) - button_h // 3
        self.buttons.append(Button("play", play_x, play_y, button_w, button_h, self.assets.play))

        # Leaderboard Button
        button_w, button_h = self.small_button_size()
        record_x, record_y = self.anchor_top_right(self.W, button_w)
        self.buttons.append(Button("leaderboard", record_x, record_y, button_w, button_h, self.assets.leaderboard_icon))

        # Difficulty Button
        button_w, button_h = self.banner_size()
        diff_x, diff_y = play_x, self.H - (self.H // 2) - button_h // 3
        diff_text = None
        if difficulty == 1:
            diff_text = "easy"
        elif difficulty == 2:
            diff_text = "medium"
        else:
            diff_text = "hard"
        diff = Button("difficulty", diff_x, diff_y, button_w, button_h, self.assets.record_card)
        self.buttons.append(diff)

        # Draw Buttons
        for button in self.buttons:
            button.draw(self.screen)

        diff.render_text_center(diff_text, self.assets.font, self.screen)
            
    
    def render_pause_menu(self):
        self.buttons = []

        # Fill Background
        bg = pygame.transform.scale(self.assets.background, (self.W, self.H))
        self.screen.blit(bg, (0, 0))

        # Add Pause Card
        pause_width, pause_height = self.W * 0.6, self.W * 0.9
        pause_x, pause_y = self.W * 0.2, self.H * 0.2
        pause = pygame.transform.scale(self.assets.leaderboard, (pause_width, pause_height))

        self.screen.blit(pause, (pause_x, pause_y))

        # Resume Button
        button_w, button_h = self.banner_size()
        resume_x, resume_y = self.W // 2 - button_w // 2, pause_y + button_h
        self.buttons.append(Button("resume", resume_x, resume_y, button_w, button_h, self.assets.record_card))

        # End Game Button
        button_w, button_h = self.banner_size()
        end_x, end_y = resume_x, resume_y + button_h * 1.5
        self.buttons.append(Button("end", end_x, end_y, button_w, button_h, self.assets.record_card))
        
        # Draw Buttons
        for button in self.buttons:
            button.draw(self.screen)
            button.render_text_center(button.name, self.assets.font, self.screen)


    def render_game(self, game: Game, input: str):
        self.buttons = []

        # Fill Background
        bg = pygame.transform.scale(self.assets.background, (self.W, self.H))
        self.screen.blit(bg, (0, 0))

        # Render Text
        score_text = self.assets.font.render(f"Score: {game.score}", True, (0, 0, 0))
        input_text = self.assets.font.render(f"{input}", True, (0, 0, 0))
        time_text = self.assets.font.render(f"Time: {int(game.remaining_time)}", True, (0, 0, 0))

        # Display Text
        self.screen.blit(score_text, self.anchor_top_left())
        self.screen.blit(input_text, self.anchor_top_middle(self.W, input_text.get_width()))
        self.screen.blit(time_text, self.anchor_top_right(self.W, time_text.get_width()))

        # Draw Platforms
        for platform in self.platforms:
            platform.draw(self.screen)

        # Draw the Character
        self.character.draw(self.screen)


    def render_leaderboard(self, records: list[Record]):
        """Render Leaderboard"""
        self.buttons = []

        # Fill Background
        bg = pygame.transform.scale(self.assets.background, (self.W, self.H))
        self.screen.blit(bg, (0, 0))

        # Add Leaderboard Card
        leaderboard_width, leaderboard_height = self.W * 0.8, self.W * 1.2
        leaderboard_x, leaderboard_y = self.W * 0.1, self.H * 0.1
        leaderboard = pygame.transform.scale(self.assets.leaderboard, (leaderboard_width, leaderboard_height))

        self.screen.blit(leaderboard, (leaderboard_x, leaderboard_y))

        # Add Close Button
        close_width, close_height = self.small_button_size()
        close = pygame.transform.scale(self.assets.close, (close_width, close_height))
        self.buttons.append(Button("close", (leaderboard_x + leaderboard_width - close_width * 2), (leaderboard_y - (close_width * 0.2 )), close_width, close_height, close))

        # Add Record Cards
        record_width, record_height = self.W * 0.7, self.H * 0.05
        record_spacing = self.H * 0.01
        record_card = pygame.transform.scale(self.assets.record_card, (record_width, record_height))

        for rank in range(min(10, len(records))):
            # Get the record data
            record = records[rank]

            # Add Record Card
            record_y = leaderboard_y + (leaderboard_height * 0.05) + (record_height + record_spacing) * (rank)
            record_x = self.W * 0.15
            self.screen.blit(record_card, (record_x, record_y))

            # Render Text
            rank_text = self.assets.font.render(str(rank + 1), True, (255, 255, 255))
            name_text = self.assets.font.render(record.username, True, (255, 255, 255))
            score_text = self.assets.font.render(str(record.score), True, (255, 255, 255))

            # Display Text
            text_y = record_y + (record_height // 2) - (name_text.get_height() // 2)

            self.screen.blit(rank_text, (record_x + (record_width // 30), text_y))
            self.screen.blit(name_text, (record_x + (record_width // 10), text_y))
            self.screen.blit(score_text, (self.W * 0.825 - score_text.get_width(), text_y))

        for button in self.buttons:
            button.draw(self.screen)


    def render_end_game(self, score: int, input: str):
        """Render End Game Screen"""
        self.buttons = []

        # Fill Background
        bg = pygame.transform.scale(self.assets.background, (self.W, self.H))
        self.screen.blit(bg, (0, 0))

        # Add Leaderboard Card
        leaderboard_width, leaderboard_height = self.W * 0.8, self.W * 1.2
        leaderboard_x, leaderboard_y = self.W * 0.1, self.H * 0.1
        leaderboard = pygame.transform.scale(self.assets.leaderboard, (leaderboard_width, leaderboard_height))

        self.screen.blit(leaderboard, (leaderboard_x, leaderboard_y))

        # Render Prompt Text
        score_text = self.assets.font.render(f"Score: {score}", True, (0, 0, 0))
        prompt_text = self.assets.font.render(f"Enter your name: {input}", True, (0, 0, 0))


        # Horizontal center of leaderboard
        center_x = leaderboard_x + leaderboard_width // 2

        # Create centered rects
        score_rect = score_text.get_rect(center=(center_x, leaderboard_y + 50))
        prompt_rect = prompt_text.get_rect(center=(center_x, leaderboard_y + 120))

        # Draw text
        self.screen.blit(score_text, score_rect)
        self.screen.blit(prompt_text, prompt_rect)


    # Game Element Management Functions
    def check_button_clicked(self, event: pygame.event):
        """If event was mouse click, return clicked button if applicable"""
        if event.type != pygame.MOUSEBUTTONDOWN:
            return None
        
        for button in self.buttons:
            if button.is_clicked(event):
                print(f"{button.name} was clicked.")
                if button.name in ["easy", "medium", "hard"]:
                    return "difficulty"
                return button.name
        
        return None

    def init_game_elements(self, words: list[Word]):
        """Initialize Start of Game Elements"""
        self.platforms = []
        temp = Platform(self.screen, self.assets.platform, "Type the Words!")
        temp.x, temp.y = self.anchor_bottom_middle(self.W, self.H, temp.width, temp.height)
        temp.dest_x, temp.dest_y = temp.x, temp.y
        temp.rect.topleft = (temp.x, temp.y)
        self.character.update_platform(temp)
        self.character.teleport_to_platform()
        self.current_platform = temp
        self.platforms.append(temp)
        self.add_words(words)


    def add_words(self, words: list[Word]):
        """Add Platforms for New Words"""
        for word in words:
            print(f"Adding Platform {word.word}")
            platform = Platform(self.screen, self.assets.platform, word.word, self.platforms)
            platform.x += self.dx
            platform.y += self.dy
            self.platforms.append(platform)


    def update_platforms(self, matched_word: str):
        """Update Platforms After a Word is Matched"""
        # Find Platform with Matching Word
        for p in self.platforms:
            if p.word == matched_word:
                self.current_platform = p
                self.character.update_platform(p)
            else:
                p.word = ""

        # Compute displacement
        dest_x, dest_y = self.anchor_bottom_middle(
            self.W, self.H,
            self.current_platform.width, self.current_platform.height
        )

        curr_x, curr_y = self.current_platform.current_position()
        dx, dy = curr_x - dest_x, curr_y - dest_y
        self.dx, self.dy = dx, dy
        
        # Update Positions of All Platforms and Character
        for platform in self.platforms:
            platform.update_destination(-dx, -dy)
        
    def move_platforms(self):
        """Move Platforms toward their destination"""
        remaining = []
        for platform in self.platforms:
            if platform.update_position(self.screen.get_width(), self.screen.get_height()):
                remaining.append(platform)
        self.platforms = remaining
        self.character.update_position()


    # Button Size Helpers
    def banner_size(self) -> tuple[int, int]:
        return self.H // 11.25 * 2.875, self.H // 11.25
    
    
    def small_button_size(self) -> tuple[int, int]:
        """Calculate Width, Height of Small Button Relative to Screen Size"""
        return self.W // 20, self.W // 20
    

    # Layout Helpers
    def anchor_top_left(self, margin = 10):
        return margin, margin
    

    def anchor_top_right(self, W: int, w: int, margin = 10):
        return W - w - margin, margin


    def anchor_top_middle(self, W: int, w: int, margin = 10):
        return W // 2 - w // 2, margin
    

    def anchor_bottom_middle(self, W: int, H: int, w: int, h: int):
        return W // 2 - w // 2, H - h - (H // 12)