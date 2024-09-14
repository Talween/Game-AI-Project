#   Author: Catherine Leung.
#   This is the game that you will code the bots to play.  You can also play against your bot
#   To run the game you will need pygames installed.  See: https://pypi.org/project/pygame/
#   Once you have pygames, you can run the game by using the command:
#   python game.py
#   
#   the gem images used are from opengameart.org by qubodup
#   https://opengameart.org/content/rotating-crystal-animation-8-step,
#   https://creativecommons.org/licenses/by/3.0/
# New features introduced by: Sagar, Gaganjot Singh, Talween

import pygame
import sys
import math
import random
from a1_partd import overflow
from a1_partc import Queue
from player1 import PlayerOne
from player2 import PlayerTwo

# Dropdown class for creating dropdown menus
class Dropdown:
    def __init__(self, x, y, width, height, options):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.options = options
        self.current_option = 0

    def draw(self, window):
        # Draw the dropdown menu
        pygame.draw.rect(window, BLACK, (self.x, self.y, self.width, self.height), 2)
        font = pygame.font.Font(None, 36)
        text = font.render(self.options[self.current_option], 1, BLACK)
        window.blit(text, (self.x + 5, self.y + 5))

    def handle_event(self, event):
        # Handle mouse button down event to change the current option
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if self.x < x < self.x + self.width and self.y < y < self.y + self.height:
                self.current_option = (self.current_option + 1) % len(self.options)

    def get_choice(self):
        # Return the current selected option
        return self.current_option

# Board class for managing the game board
class Board:
    def __init__(self, width, height, p1_sprites, p2_sprites):
        self.width = width
        self.height = height
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        self.p1_sprites = p1_sprites
        self.p2_sprites = p2_sprites
        self.board[0][0] = 1
        self.board[self.height - 1][self.width - 1] = -1
        self.turn = 0

    def get_board(self):
        # Return a copy of the current game board
        current_board = []
        for i in range(self.height):
            current_board.append(self.board[i].copy())
        return current_board

    def valid_move(self, row, col, player):
        # Check if a move is valid
        if row >= 0 and row < self.height and col >= 0 and col < self.width and (self.board[row][col] == 0 or self.board[row][col] / abs(self.board[row][col]) == player):
            return True
        return False

    def add_piece(self, row, col, player):
        # Add a piece to the game board
        if self.valid_move(row, col, player):
            self.board[row][col] += player
            self.turn += 1
            return True
        return False

    def check_win(self):
        # Check if there is a winner
        if self.turn > 0:
            num_p1 = 0
            num_p2 = 0
            for i in range(self.height):
                for j in range(self.width):
                    if self.board[i][j] > 0:
                        if num_p2 > 0:
                            return 0
                        num_p1 += 1
                    elif self.board[i][j] < 0:
                        if num_p1 > 0:
                            return 0
                        num_p2 += 1
            if num_p1 == 0:
                return -1
            if num_p2 == 0:
                return 1
        return 0

    def do_overflow(self, q):
        # Perform overflow on the game board
        oldboard = []
        for i in range(self.height):
            oldboard.append(self.board[i].copy())
        numsteps = overflow(self.board, q)
        if numsteps != 0:
            self.set(oldboard)
        return numsteps

    def set(self, newboard):
        # Set the game board to a new state
        for row in range(self.height):
            for col in range(self.width):
                self.board[row][col] = newboard[row][col]

    def draw(self, window, frame):
        # Draw the game board
        for row in range(GRID_SIZE[0]):
            for col in range(GRID_SIZE[1]):
                rect = pygame.Rect(col * CELL_SIZE + X_OFFSET, row * CELL_SIZE + Y_OFFSET, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(window, BLACK, rect, 1)
        for row in range(self.height):
            for col in range(self.width):
                if self.board[row][col] != 0:
                    rpos = row * CELL_SIZE + Y_OFFSET
                    cpos = col * CELL_SIZE + X_OFFSET
                    if self.board[row][col] > 0:
                        sprite = self.p1_sprites
                    else:
                        sprite = self.p2_sprites
                    if abs(self.board[row][col]) == 1:
                        cpos += CELL_SIZE // 2 - 16
                        rpos += CELL_SIZE // 2 - 16
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                    elif abs(self.board[row][col]) == 2:
                        cpos += CELL_SIZE // 2 - 32
                        rpos += CELL_SIZE // 2 - 16
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        cpos += 32
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                    elif abs(self.board[row][col]) == 3:
                        cpos += CELL_SIZE // 2 - 16
                        rpos += 8
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        cpos = col * CELL_SIZE + X_OFFSET + CELL_SIZE // 2 - 32
                        rpos += CELL_SIZE // 2
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        cpos += 32
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                    elif abs(self.board[row][col]) == 4:
                        cpos += CELL_SIZE // 2 - 32
                        rpos += 8
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        rpos += CELL_SIZE // 2
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        cpos += 32
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        rpos -= CELL_SIZE // 2
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))

# Function to animate a piece drop
def animate_piece_drop(window, sprite, start_pos, end_pos):
    for i in range(30):
        current_pos = (
            start_pos[0] + (end_pos[0] - start_pos[0]) * i / 30,
            start_pos[1] + (end_pos[1] - start_pos[1]) * i / 30
        )
        window.fill((200, 200, 255))
        board.draw(window, frame)
        window.blit(sprite, current_pos)
        pygame.display.update()
        pygame.time.delay(15)

# Function to create particles for particle effects
def create_particles(x, y):
    particles = []
    for _ in range(30):
        particles.append([x, y, random.randint(1, 3), random.choice([-1, 1]) * random.random() * 2, random.choice([-1, 1]) * random.random() * 2, random.choice([(255, 100, 100), (100, 255, 100), (100, 100, 255)])])
    return particles

# Function to update particles for particle effects
def update_particles(particles, window):
    for particle in particles:
        particle[0] += particle[3]
        particle[1] += particle[4]
        particle[2] -= 0.05
        if particle[2] <= 0:
            particles.remove(particle)
        else:
            pygame.draw.circle(window, particle[5], (int(particle[0]), int(particle[1])), int(particle[2]))

# Function to fade in the screen
def fade_in(window):
    fade = pygame.Surface((1200, 800))
    fade.fill((200, 200, 255))
    for alpha in range(0, 300):
        fade.set_alpha(alpha)
        window.fill(BLACK)
        window.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(5)

# Function to fade out the screen
def fade_out(window):
    fade = pygame.Surface((1200, 800))
    fade.fill((200, 200, 255))
    for alpha in range(300, 0, -1):
        fade.set_alpha(alpha)
        window.fill(BLACK)
        window.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(5)

# Constants
GRID_SIZE = (5, 6)
CELL_SIZE = 100
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
X_OFFSET = 0
Y_OFFSET = 100
FULL_DELAY = 5
TURN_TIME_LIMIT = 5  # 5 seconds per turn

# Initialize Pygame
pygame.init()

# Initialize the mixer
pygame.mixer.init()

# Load sound effects
move_sound = pygame.mixer.Sound('move_sound.wav')  # Replace with actual sound file
win_sound = pygame.mixer.Sound('win_sound.wav')    # Replace with actual sound file

# Load sprites
p1spritesheet = pygame.image.load('blue.png')
p2spritesheet = pygame.image.load('pink.png')
p1_sprites = []
p2_sprites = []
player_id = [1, -1]

# Split spritesheet into individual sprites
for i in range(8):
    curr_sprite = pygame.Rect(32 * i, 0, 32, 32)
    p1_sprites.append(p1spritesheet.subsurface(curr_sprite))
    p2_sprites.append(p2spritesheet.subsurface(curr_sprite))

frame = 0

window = pygame.display.set_mode((1200, 800))
pygame.font.init()
font = pygame.font.Font(None, 36)
bigfont = pygame.font.Font(None, 108)

# Create the game board
player1_dropdown = Dropdown(900, 50, 200, 50, ['Human', 'AI'])
player2_dropdown = Dropdown(900, 110, 200, 50, ['Human', 'AI'])
status = ["", ""]
current_player = 0
board = Board(GRID_SIZE[1], GRID_SIZE[0], p1_sprites, p2_sprites)

# Game loop
running = True
overflow_boards = Queue()
overflowing = False
numsteps = 0
has_winner = False
bots = [PlayerOne(), PlayerTwo()]
grid_col = -1
grid_row = -1
choice = [None, None]
particles = []
scores = [0, 0]  # Initialize scores for both players
turn_timer = TURN_TIME_LIMIT

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            player1_dropdown.handle_event(event)
            player2_dropdown.handle_event(event)
            choice[0] = player1_dropdown.get_choice()
            choice[1] = player2_dropdown.get_choice()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row = y - Y_OFFSET
                col = x - X_OFFSET
                grid_row, grid_col = row // CELL_SIZE, col // CELL_SIZE
                win = board.check_win()
                if win != 0:
                    winner = 1
                    if win == -1:
                        winner = 2
                    has_winner = True
                    win_sound.play()  # Play win sound

                if not has_winner:
                    if overflowing:
                        status[0] = "Overflowing"
                        if not overflow_boards.is_empty():
                            if repeat_step == FULL_DELAY:
                                next = overflow_boards.dequeue()
                                board.set(next)
                                repeat_step = 0
                            else:
                                repeat_step += 1
                        else:
                            overflowing = False
                            current_player = (current_player + 1) % 2
                            turn_timer = TURN_TIME_LIMIT
                    else:
                        status[0] = "Player " + str(current_player + 1) + "'s turn"
                        make_move = False
                        if choice[current_player] == 1:
                            (grid_row, grid_col) = bots[current_player].get_play(board.get_board())
                            status[1] = "Bot chose row {}, col {}".format(grid_row, grid_col)
                            if not board.valid_move(grid_row, grid_col, player_id[current_player]):
                                has_winner = True
                                winner = ((current_player + 1) % 2) + 1
                            else:
                                make_move = True
                        else:
                            if board.valid_move(grid_row, grid_col, player_id[current_player]):
                                make_move = True

                        if make_move:
                            board.add_piece(grid_row, grid_col, player_id[current_player])
                            scores[current_player] += 10  # Example scoring logic
                            move_sound.play()  # Play move sound
                            numsteps = board.do_overflow(overflow_boards)
                            if numsteps != 0:
                                overflowing = True
                                repeat_step = 0
                            else:
                                animate_piece_drop(window, p1_sprites[0] if player_id[current_player] == 1 else p2_sprites[0], (grid_col * CELL_SIZE + X_OFFSET, 0), (grid_col * CELL_SIZE + X_OFFSET, grid_row * CELL_SIZE + Y_OFFSET))
                                particles.extend(create_particles(grid_col * CELL_SIZE + X_OFFSET + CELL_SIZE // 2, grid_row * CELL_SIZE + Y_OFFSET + CELL_SIZE // 2))
                                current_player = (current_player + 1) % 2
                                turn_timer = TURN_TIME_LIMIT
                            grid_row = -1
                            grid_col = -1

    # Update timer
    turn_timer -= 1 / 60  # Assuming 60 FPS
    if turn_timer <= 0:
        current_player = (current_player + 1) % 2
        turn_timer = TURN_TIME_LIMIT

    # Draw the game board
    window.fill((200, 200, 255))
    board.draw(window, frame)
    window.blit(p1_sprites[math.floor(frame)], (850, 60))
    window.blit(p2_sprites[math.floor(frame)], (850, 120))
    frame = (frame + 0.5) % 8
    player1_dropdown.draw(window)
    player2_dropdown.draw(window)

    # Display status, scores, and timer
    if not has_winner:
        text = font.render(status[0], True, (0, 0, 0))  # Black color
        window.blit(text, (X_OFFSET, 750))
        text = font.render(status[1], True, (0, 0, 0))  # Black color
        window.blit(text, (X_OFFSET, 700))
        timer_text = font.render(f"Time left: {int(turn_timer)}s", True, (0, 0, 0))
        window.blit(timer_text, (900, 200))
        score_text = font.render(f"Scores - Player 1: {scores[0]} Player 2: {scores[1]}", True, (0, 0, 0))
        window.blit(score_text, (900, 250))  # Display scores
    else:
        text = bigfont.render("Player " + str(winner) + " wins!", True, (0, 0, 0))  # Black color
        window.blit(text, (300, 250))

    update_particles(particles, window)
    pygame.display.update()
    pygame.time.delay(100)

pygame.quit()
sys.exit()
