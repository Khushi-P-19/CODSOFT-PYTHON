import pygame
import random
import sys
import time

pygame.init()

WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock Paper Scissors")

FONT = pygame.font.SysFont("Arial", 40, bold=True)
SMALL_FONT = pygame.font.SysFont("Arial", 24)
TINY_FONT = pygame.font.SysFont("Arial", 18)

WHITE, BLACK = (255, 255, 255), (0, 0, 0)
DARK_GRAY = (50, 50, 50)
LIGHT_GRAY = (200, 200, 200)
PURPLE = (120, 80, 200)
GREEN, RED = (0, 180, 0), (180, 0, 0)
HOVER_BLUE = (100, 150, 255)

# Load images (ensure rock.png, paper.png, scissors.png are in the same directory)
try:
    ROCK_IMG = pygame.image.load("rock.png")
    PAPER_IMG = pygame.image.load("paper.png")
    SCISSORS_IMG = pygame.image.load("scissors.png")
except pygame.error:
    ROCK_IMG = PAPER_IMG = SCISSORS_IMG = pygame.Surface((100, 100))
    ROCK_IMG.fill((150, 150, 150))
    PAPER_IMG.fill((200, 200, 200))
    SCISSORS_IMG.fill((100, 100, 100))

ROCK_IMG = pygame.transform.scale(ROCK_IMG, (100, 100))
PAPER_IMG = pygame.transform.scale(PAPER_IMG, (100, 100))
SCISSORS_IMG = pygame.transform.scale(SCISSORS_IMG, (100, 100))

class Button:
    def __init__(self, text, x, y, w, h, action=None, color=LIGHT_GRAY, text_color=BLACK, img=None):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.text_color = text_color
        self.action = action
        self.img = img
        self.hovered = False

    def draw(self):
        self.hovered = self.rect.collidepoint(pygame.mouse.get_pos())
        current_color = HOVER_BLUE if self.hovered else self.color
        pygame.draw.rect(screen, current_color, self.rect, border_radius=15)
        pygame.draw.rect(screen, DARK_GRAY, self.rect, width=2, border_radius=15)
        if self.img:
            img_rect = self.img.get_rect(center=(self.rect.centerx, self.rect.centery - 30))
            screen.blit(self.img, img_rect)
        txt = SMALL_FONT.render(self.text, True, self.text_color)
        screen.blit(txt, (self.rect.centerx - txt.get_width()//2, self.rect.centery + 30 if self.img else self.rect.centery - txt.get_height()//2))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def winner(p1, p2):
    if p1 == p2: return "Tie"
    if (p1, p2) in [("rock", "scissors"), ("paper", "rock"), ("scissors", "paper")]: return "Player"
    return "Opponent"

def draw_gradient_background():
    for y in range(HEIGHT):
        r = 220 - y * 0.1
        g = 220 - y * 0.05
        b = 240 + y * 0.05
        pygame.draw.line(screen, (max(0, r), max(0, g), min(255, b)), (0, y), (WIDTH, y))

game_state = "home"
mode = "computer"
win_limit = None
time_limit = None
start_time = None
player_score = 0
opponent_score = 0
round_result = ""
player_choice = ""
opponent_choice = ""
waiting_for_p2 = False
player1_selected = False

home_buttons = [
    Button("Play vs Computer", 300, 150, 300, 60, action="mode_select", color=LIGHT_GRAY),
    Button("Time Attack", 300, 230, 300, 60, action="time_select", color=LIGHT_GRAY),
    Button("2 Player Mode", 300, 310, 300, 60, action="2player", color=LIGHT_GRAY),
    Button("Instructions", 300, 390, 300, 60, action="instructions", color=LIGHT_GRAY),
    Button("Quit", 300, 470, 300, 60, action="quit", color=(200, 100, 100))
]

mode_buttons = [
    Button("Best of 1", 300, 120, 300, 60, action=1),
    Button("Best of 3", 300, 200, 300, 60, action=3),
    Button("Best of 5", 300, 280, 300, 60, action=5),
    Button("Endless Mode", 300, 360, 300, 60, action=None)
]

time_buttons = [
    Button("30 Seconds", 300, 120, 300, 60, action=30),
    Button("1 Minute", 300, 200, 300, 60, action=60),
    Button("2 Minutes", 300, 280, 300, 60, action=120)
]

back_button = Button("Back to Menu", 20, 20, 180, 50, action="home", color=LIGHT_GRAY)

choices = [
    Button("Rock", 100, 400, 160, 160, "rock", img=ROCK_IMG, text_color=WHITE),
    Button("Paper", 370, 400, 160, 160, "paper", img=PAPER_IMG, text_color=WHITE),
    Button("Scissors", 640, 400, 160, 160, "scissors", img=SCISSORS_IMG, text_color=WHITE)
]

result_buttons = [
    Button("Play Again", 250, 350, 200, 60, "game", LIGHT_GRAY),
    Button("Main Menu", 450, 350, 200, 60, "home", LIGHT_GRAY)
]

endless_exit_button = Button("End Game", 350, 500, 200, 50, "result", color=(200, 100, 100))

def main():
    global game_state, mode, win_limit, time_limit, start_time, player_score, opponent_score
    global round_result, player_choice, opponent_choice, waiting_for_p2, player1_selected
    clock = pygame.time.Clock()
    while True:
        draw_gradient_background()
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_state == "home":
                    for btn in home_buttons:
                        if btn.is_clicked(pos):
                            if btn.action == "quit":
                                pygame.quit(); sys.exit()
                            elif btn.action == "2player":
                                mode = "2player"
                                game_state = "mode_select"
                            elif btn.action == "time_select":
                                mode = "time_attack"
                                game_state = "time_select"
                            else:
                                mode = "computer"
                                game_state = btn.action
                elif game_state == "mode_select":
                    for btn in mode_buttons:
                        if btn.is_clicked(pos):
                            win_limit = btn.action
                            time_limit = None
                            round_result = ""
                            game_state = "game"
                            if mode != "2player":
                                player_score = opponent_score = 0
                            waiting_for_p2 = mode == "2player"
                            player1_selected = False
                elif game_state == "time_select":
                    for btn in time_buttons:
                        if btn.is_clicked(pos):
                            time_limit = btn.action
                            win_limit = None
                            round_result = ""
                            game_state = "game"
                            player_score = opponent_score = 0
                            start_time = time.time()
                            player1_selected = False
                elif game_state == "instructions":
                    if back_button.is_clicked(pos):
                        game_state = "home"
                elif game_state == "game":
                    if (win_limit is None and time_limit is None and endless_exit_button.is_clicked(pos)):
                        game_state = "result"
                    else:
                        for btn in choices:
                            if btn.is_clicked(pos):
                                if mode == "computer" or mode == "time_attack":
                                    player_choice = btn.action
                                    opponent_choice = random.choice(["rock", "paper", "scissors"])
                                    outcome = winner(player_choice, opponent_choice)
                                else:
                                    if not player1_selected:
                                        player_choice = btn.action
                                        round_result = "Player 1 has chosen. Player 2's turn."
                                        player1_selected = True
                                        continue
                                    else:
                                        opponent_choice = btn.action
                                        outcome = winner(player_choice, opponent_choice)
                                        player1_selected = False
                                if outcome:
                                    if outcome == "Player":
                                        player_score += 1
                                        round_result = f"You Win! ({player_choice.capitalize()} beats {opponent_choice.capitalize()})"
                                    elif outcome == "Opponent":
                                        opponent_score += 1
                                        round_result = f"Opponent Wins! ({opponent_choice.capitalize()} beats {player_choice.capitalize()})"
                                    else:
                                        round_result = f"Tie! (Both chose {player_choice.capitalize()})"
                                    if mode != "time_attack" and win_limit and (player_score >= win_limit or opponent_score >= win_limit):
                                        game_state = "result"
        # Check time limit for time attack mode
        if game_state == "game" and mode == "time_attack" and time_limit:
            elapsed = time.time() - start_time
            if elapsed >= time_limit:
                game_state = "result"
        
        # Draw UI based on game state
        if game_state == "home":
            title = FONT.render("Rock Paper Scissors", True, PURPLE)
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
            for b in home_buttons: b.draw()
        elif game_state == "mode_select":
            title = FONT.render("Choose Game Mode", True, PURPLE)
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
            for b in mode_buttons: b.draw()
        elif game_state == "time_select":
            title = FONT.render("Choose Time Limit", True, PURPLE)
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
            for b in time_buttons: b.draw()
        elif game_state == "instructions":
            title = FONT.render("Instructions", True, PURPLE)
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
            instructions = [
                "Select Rock, Paper, or Scissors to play.",
                "Rules:",
                "- Rock crushes Scissors",
                "- Paper covers Rock",
                "- Scissors cuts Paper",
                "Best of X: Reach the win limit to end.",
                "Endless: Play until you stop.",
                "Time Attack: Score max wins in time limit.",
                "2 Player: Players alternate turns."
            ]
            for i, line in enumerate(instructions):
                screen.blit(TINY_FONT.render(line, True, BLACK), (80, 150 + i * 35))
            back_button.draw()
        elif game_state == "game":
            score = SMALL_FONT.render(f"Player: {player_score}  |  Opponent: {opponent_score}", True, BLACK)
            screen.blit(score, (WIDTH // 2 - score.get_width() // 2, 50))
            if mode == "time_attack" and time_limit:
                elapsed = time.time() - start_time
                time_left = max(0, time_limit - elapsed)
                timer = SMALL_FONT.render(f"Time Left: {int(time_left)}s", True, RED if time_left < 10 else BLACK)
                screen.blit(timer, (WIDTH // 2 - timer.get_width() // 2, 80))
            result = TINY_FONT.render(round_result, True, PURPLE)
            screen.blit(result, (WIDTH // 2 - result.get_width() // 2, 120))
            for b in choices: b.draw()
            if win_limit is None and time_limit is None:
                endless_exit_button.draw()
        elif game_state == "result":
            if mode == "time_attack":
                final_text = f"Time's Up! Your Score: {player_score}"
                final = FONT.render(final_text, True, PURPLE)
            else:
                final_text = "You Win!" if player_score > opponent_score else "Opponent Wins!" if opponent_score > player_score else "It's a Tie!"
                final = FONT.render(final_text, True, GREEN if player_score > opponent_score else RED if opponent_score > player_score else PURPLE)
            screen.blit(final, (WIDTH // 2 - final.get_width() // 2, 100))
            score = SMALL_FONT.render(f"Final Score: Player {player_score} - Opponent {opponent_score}", True, BLACK)
            screen.blit(score, (WIDTH // 2 - score.get_width() // 2, 200))
            for b in result_buttons: b.draw()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
