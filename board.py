"""
Tetris Game Implementation
This module implements the core functionality of a Tetris game using Pygame. It includes the game board, tetrominoes, 
and game logic such as block generation, row clearing, and game over conditions.
Modules:
    - pygame: Used for game development.
    - sys: Provides access to some variables used or maintained by the interpreter.
    - draw: Custom module for drawing game elements.
    - tetrominoe: Custom module for tetrominoe shapes and operations.
    - copy: Provides shallow and deep copy operations.
    - random: Implements pseudo-random number generators for various distributions.
Global Variables:
    - board: A 2D list representing the game board.
    - O, L, J, S, Z, T, I: Lists representing different tetromino shapes.
    - blocks: A list of Tetrominoe objects representing all possible tetrominoes.
    - block_queue: A list to hold the next blocks to be played.
    - screen: The Pygame display surface.
    - score: The player's score.
    - down: Counter for the number of times the down key is pressed.
    - TIMEEVENT: Custom Pygame event for handling timed events.
Functions:
    - get_random_block(): Returns a random tetromino, ensuring it is not the same as the last one.
    - fill_block_queue(): Fills the block queue with random tetrominoes until it has at least 3 blocks.
    - new_block(): Adds a new block to the queue and returns the next block to be played.
    - check_filled_rows(): Checks for filled rows in the board and updates the score based on the number of rows cleared.
    - remove_rows(rows): Removes the specified rows from the board and shifts the rows above down.
    - is_lost(): Checks if the game is lost by looking for blocks in the top row.
    - game_over(): Displays the game over screen and waits for a short period.
    - row_cleared(): Animates the row clearing process and removes the filled rows from the board.
Main Loop:
    - Initializes Pygame and sets up the game window.
    - Runs the main game loop, handling events, updating game state, and drawing the game elements.
    - Quits Pygame and exits the program when the game loop ends.
"""
import pygame
import sys
import draw
import tetrominoe
import copy
import random
    
board = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

O = [[1, 1], 
     [1, 1]]
    
L = [[0, 0, 2], 
     [2, 2, 2], 
     [0, 0, 0]]
    
J = [[3, 0, 0], 
     [3, 3, 3], 
     [0, 0, 0]]
    
S = [[0, 4, 4], 
     [4, 4, 0], 
     [0, 0, 0]]
    
Z = [[5, 5, 0], 
     [0, 5, 5], 
     [0, 0, 0]]
    
T = [[0, 6, 0], 
     [6, 6, 6], 
     [0, 0, 0]]
    
I = [[0, 0, 0, 0], 
     [7, 7, 7, 7], 
     [0, 0, 0, 0],
     [0, 0, 0, 0]]

blocks = [tetrominoe.Tetrominoe(1, [4, 0], 1, O), 
          tetrominoe.Tetrominoe(2, [4, 0], 1, L), 
          tetrominoe.Tetrominoe(3, [4, 0], 1, J), 
          tetrominoe.Tetrominoe(4, [4, 0], 1, S), 
          tetrominoe.Tetrominoe(5, [4, 0], 1, Z), 
          tetrominoe.Tetrominoe(6, [4, 0], 1, T), 
          tetrominoe.Tetrominoe(7, [4, 0], 1, I)]

block_queue = []

def get_random_block():
    block = random.choice(blocks)
    if len(block_queue) != 0:
        while block.shape == block_queue[len(block_queue)-1].shape:
            block = random.choice(blocks)
    return copy.deepcopy(block)

def fill_block_queue():
    global block_queue
    while len(block_queue) < 3:
        block_queue.append(get_random_block())

def new_block():
    global block_queue
    block_queue.append(get_random_block())
    return block_queue.pop(0)
    
def check_filled_rows():
    filled_rows = []
    for i, row in enumerate(board):
        if all(cell > 0 for cell in row):
            filled_rows.insert(0, i)
    global score
    match len(filled_rows):
        case 1:
            score += 40
        case 2:
            score += 100
        case 3:
            score += 300
        case 4:
            score += 1200
    return filled_rows

def remove_rows(rows):
    global board
    for row_index in reversed(rows):
        if row_index == 0:
            board[0] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        else:
            for i in reversed(range(len(board))):
                if i <= row_index:
                    board[i] = board[i-1]
            board[0] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

def is_lost():
    if any(cell > 0 for cell in board[0]):
        return True
    return False

def game_over():
    draw.draw_game_over(screen)
    pygame.display.flip()
    pygame.time.wait(350)
    draw.draw_board(board, block_queue, screen, score)
    pygame.display.flip()
    pygame.time.wait(350)

def row_cleared():
    draw.draw_filled_rows(screen, filled_rows)
    pygame.display.flip()
    pygame.time.wait(350)
    draw.draw_board(board, block_queue, screen, score)
    pygame.display.flip()
    pygame.time.wait(350)
    draw.draw_filled_rows(screen, filled_rows)
    pygame.display.flip()
    pygame.time.wait(350)
    draw.draw_board(board, block_queue, screen, score)
    pygame.display.flip()
    pygame.time.wait(350)
    remove_rows(filled_rows)
    block.position = [4,1]

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((400, 360))
pygame.display.set_caption('Tetris')

# Main loop
running = True
score = 0
down = 0
fill_block_queue()
block = new_block()
TIMEEVENT = pygame.USEREVENT + 1
pygame.time.set_timer(TIMEEVENT, 1000)
pygame.key.set_repeat(350, 15)


while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == TIMEEVENT: 
            if not block.is_obstructed_down(board):
                block.position[1] += 1
            else:
                block.land(board)
                score += down
                down = 0
                if not is_lost():
                    del block
                    block = new_block()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                prior = copy.deepcopy(block)
                block.rotate90() 
                if not block.check_rotation(board):
                    block = prior
            else:
                block.move(event.key, board)
            if event.key == pygame.K_DOWN:
                down += 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN and block.position[1] < 17:
                down = 0
    if is_lost():
        game_over()
    if filled_rows := check_filled_rows():
        row_cleared()
    draw.draw_board(board, block_queue, screen, score)
    draw.draw_tetrominoe(block, screen)
    pygame.display.flip()

# Quit pygame
pygame.quit()
sys.exit()



