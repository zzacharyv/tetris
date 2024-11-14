import pygame

white = (255, 255, 255)
black = (0,0,0)
orange = (254,138,0,255)
red = (255,57,104,255)
grey =  (211, 211, 211)
light_blue = (0,214,244,255)
green = (0,211,0,255)
blue = (35,100,255,255)
yellow = (255,225,0,255)
purple = (197,69,222,255)

def draw_background(screen):
    """
    Draws the background grid for the Tetris game.
    
    Args:
        screen (pygame.Surface): The surface to draw on.
    """
    count = 1
    y = 0
    while y < 360:
        x = 0
        while x < 400:
            # Alternate colors for the grid
            if count % 2 == 0:
                color = (15,16,64,255)
            else:
                color = (13,13,52,255)
            count += 1
            pygame.draw.rect(screen, color, (x, y, 18, 18), 0)
            x += 18
        y += 18

def draw_board(board, block_queue, screen, score):
    """
    Draws the entire game board including the background, tiles, block queue, and score.
    
    Args:
        board (list of list of int): The current state of the game board.
        block_queue (list): The queue of upcoming blocks.
        screen (pygame.Surface): The surface to draw on.
        score (int): The current score of the game.
    """
    # Draw the background grid
    draw_background(screen)
    
    count = 0
    # Iterate through each cell in the board
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell == 0:
                # Alternate colors for empty cells
                if count % 2 == 0:
                    color = (13,23,83,255)
                else:
                    color = (13,26,91,255)
                pygame.draw.rect(screen, color, (x * 18+36, y * 18, 18, 18), 0)
            else:
                # Draw the tile with the corresponding color for filled cells
                color = get_tetrominoe_color(cell)
                draw_tile([x, y], screen, color)
            count += 1
        count += 1
    
    # Draw the borders of the game board
    pygame.draw.rect(screen, (39,61,199,255), (28, 0, 4, 360), 0)
    pygame.draw.rect(screen, (10,12,55,255), (32, 0, 4, 360), 0)
    pygame.draw.rect(screen, (39,61,199,255), (18*12+4, 0, 4, 360), 0)
    pygame.draw.rect(screen, (10,12,55,255), (18*12, 0, 4, 360), 0)

    # Draw the block queue and the score
    draw_block_queue(block_queue, screen)
    draw_score(screen, score)
    
def draw_tile(pos, screen, color=red):
    """
    Draws a single tile on the game board.
    
    Args:
        pos (list of int): The position [x, y] to draw the tile.
        screen (pygame.Surface): The surface to draw on.
        color (tuple): The color of the tile.
    """
    pygame.draw.rect(screen, (13,13,52,255), (pos[0]*18+36, pos[1]*18, 18, 18), 0)
    pygame.draw.rect(screen, color, (pos[0]*18+36+1, pos[1]*18+1, 16, 16), 0)
    
def draw_block_queue(queue, screen):
    """
    Draws the queue of upcoming blocks.
    
    Args:
        queue (list): The queue of upcoming blocks.
        screen (pygame.Surface): The surface to draw on.
    """
    pygame.draw.rect(screen, (13,26,91,255), (260, 160, 120, 185), 0)
    pygame.draw.rect(screen, (39,61,199,255), (260, 160, 120, 185), 4)
    pygame.draw.rect(screen, (10,12,55,255), (264, 164, 112, 177), 4)
    count = 0
    for block in queue:
        for y, row in enumerate(block.matrix):
            for x, cell in enumerate(row):
                if cell > 0:
                    draw_tile([block.position[0] + x + 10, block.position[1] + y + 10 + 3*count], screen, get_tetrominoe_color(cell))
        count += 1

def draw_score(screen, score=0):
    """
    Draws the current score on the screen.
    
    Args:
        screen (pygame.Surface): The surface to draw on.
        score (int): The current score of the game.
    """
    pygame.draw.rect(screen, (39,61,199,255), (224, 46, 200, 69), 4)
    pygame.draw.rect(screen, (13,26,91,255), (224, 50, 200, 61), 0)
    pygame.draw.line(screen, (10,12,55,255), (224, 51), (400, 51), 4)
    pygame.draw.line(screen, (10,12,55,255), (224, 108), (400, 108), 4)

    font_path = './fonts/tetris-atari.ttf'
    font = pygame.font.Font(font_path, 21)
    title = font.render('SCORE', True, white)
    score = font.render(str(score), True, white)
    rect = score.get_rect(topright = (373, 75))

    pygame.draw.rect(screen, (13,26,91,255), (258, 23, 120, 42), 0)
    pygame.draw.rect(screen, (39,61,199,255), (258, 23, 120, 42), 4)
    pygame.draw.rect(screen, (10,12,55,255), (262, 27, 112, 34), 4)
    screen.blit(title, (269, 32))
    screen.blit(score, rect)

def draw_filled_rows(screen, rows):
    """
    Draws the filled rows on the game board.
    
    Args:
        screen (pygame.Surface): The surface to draw on.
        rows (list of int): The list of row indices that are filled.
    """
    for row in rows:
        pygame.draw.rect(screen, grey, (36, row*18, 180, 18), 0)
        pygame.draw.rect(screen, grey, (36, row*18, 180, 18), 4)
        pygame.draw.rect(screen, grey, (40, row*18+4, 172, 10), 4)

def draw_game_over(screen):
    """
    Draws the 'GAME OVER' message on the screen.
    
    Args:
        screen (pygame.Surface): The surface to draw on.
    """
    font_path = './fonts/tetris-atari.ttf'
    font = pygame.font.Font(font_path, 21)
    title = font.render('GAME OVER', True, white)
    screen.blit(title, (32, 75))
    
def get_tetrominoe_color(shape: int):
    """
    Returns the color corresponding to the given tetrominoe shape.
    
    Args:
        shape (int): The shape identifier of the tetrominoe.
        
    Returns:
        tuple: The color corresponding to the shape.
    """
    match shape:
        case 1:
            return yellow
        case 2: 
            return orange
        case 3:
            return blue
        case 4:
            return green
        case 5:
            return red
        case 6:
            return purple
        case 7:
            return light_blue
        
def draw_tetrominoe(tetro, screen):
    """
    Draws a tetrominoe on the game board.
    
    Args:
        tetro: The tetrominoe object containing its matrix and position.
        screen (pygame.Surface): The surface to draw on.
    """
    for y, row in enumerate(tetro.matrix):
        for x, cell in enumerate(row):
            if cell > 0:
                draw_tile([tetro.position[0] + x, tetro.position[1] + y], screen, get_tetrominoe_color(cell))

def print_board(board):
    """
    Prints the game board to the console.
    
    Args:
        board (list of list of int): The current state of the game board.
    """
    for row in board:
        print(" ".join(str(cell) for cell in row))