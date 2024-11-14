import pygame

class Tetrominoe: 
    def __init__(self, shape="O", position=[4, 0], rotation=1, matrix=[[1, 1], [1, 1]]):
        # Initialize the Tetrominoe with shape, position, rotation, and matrix
        self.shape = shape
        self.position = position
        self.rotation = rotation
        self.matrix = matrix
    
    def is_in_bounds(self):
        # Check if the Tetrominoe is within the game board boundaries
        for y, row in enumerate(self.matrix):
            for x, cell in enumerate(row):
                if cell > 0:
                    if self.position[0] + x < 0 or self.position[0] + x >= 10: 
                        return False
                    if self.position[1] + y >= 20 or self.position[1] + y < 0:
                        return False
        return True

    def is_obstructed_down(self, board):
        # Check if the Tetrominoe is obstructed from moving down
        for y, row in enumerate(self.matrix):
            for x, cell in enumerate(row):
                if cell > 0:
                    if self.position[1] + y + 1 >= 20:
                        return True
                    elif board[self.position[1] + y + 1][self.position[0] + x] > 0:
                        return True
        return False
    
    def is_obstructed_right(self, board):
        # Check if the Tetrominoe is obstructed from moving right
        for y, row in enumerate(self.matrix):
            for x, cell in enumerate(row):
                if cell > 0:
                    if self.position[0] + x + 1 >= 10:
                        return True
                    elif board[self.position[1] + y][self.position[0] + x + 1] > 0:
                        return True
        return False
    
    def is_obstructed_left(self, board):
        # Check if the Tetrominoe is obstructed from moving left
        for y, row in enumerate(self.matrix):
            for x, cell in enumerate(row):
                if cell > 0:
                    if self.position[0] + x - 1 < 0:
                        return True
                    if board[self.position[1] + y][self.position[0] + x - 1] > 0:
                        return True
        return False
    
    def move(self, key, board):
        # Move the Tetrominoe based on the key input if not obstructed
        old = self.position.copy()
        
        if key == pygame.K_LEFT:  
            if not self.is_obstructed_left(board):
                self.position[0] -= 1
        if key == pygame.K_RIGHT: 
            if not self.is_obstructed_right(board):
                self.position[0] += 1      
        if key == pygame.K_DOWN: 
            if not self.is_obstructed_down(board):
                self.position[1] += 1

    def land(self, board):
        # Place the Tetrominoe on the board when it lands
        for y, row in enumerate(self.matrix):
            for x, cell in enumerate(row):
                if cell > 0:
                    board[self.position[1] + y][self.position[0] + x] = cell
        
    def rotate_adjust_position(self):
        # Adjust the position of the Tetrominoe after rotation to keep it within bounds
        # I shape
        if self.shape == 7:
            if self.rotation == 2:
                if self.position[0] >= 7:
                    self.position[0] -= 1
                if self.position[0] <= -1:
                    self.position[0] += 2
            if self.rotation == 4:
                if self.position[0] >= 7:
                    self.position[0] -= 2
                if self.position[0] <= -1:
                    self.position[0] += 1
            if self.rotation == 1:
                if self.position[1] == 17:
                    self.position[1] -= 1
                if self.position[1] >= 18:
                    self.position[1] -= 2
            if self.rotation == 3:
                if self.position[1] >= 17:
                    self.position[1] -= 1
        # L shape
        if self.shape == 2:
            if self.rotation == 4:
                if self.position[0] >= 8:
                    self.position[0] -= 1
            if self.rotation == 2:
                if self.position[0] <= -1:
                    self.position[0] += 1
            if self.rotation == 1:
                if self.position[1] >= 18:
                    self.position[1] -= 1
        # J shape
        if self.shape == 3:
            if self.rotation == 4:
                if self.position[0] >= 8:
                    self.position[0] -= 1
            if self.rotation == 2:
                if self.position[0] <= -1:
                    self.position[0] += 1
            if self.rotation == 1:
                if self.position[1] >= 18:
                    self.position[1] -= 1
        # S shape
        if self.shape == 4:
            if self.rotation == 4:
                if self.position[0] >= 8:
                    self.position[0] -= 1
            if self.rotation == 2:
                if self.position[0] <= -1:
                    self.position[0] += 1
            if self.rotation == 1:
                if self.position[1] >= 18:
                    self.position[1] -= 1
        # Z shape
        if self.shape == 5:
            if self.rotation == 4:
                if self.position[0] >= 8:
                    self.position[0] -= 1
            if self.rotation == 2:
                if self.position[0] <= -1:
                    self.position[0] += 1
            if self.rotation == 1:
                if self.position[1] >= 18:
                    self.position[1] -= 1
        # T shape
        if self.shape == 6:
            if self.rotation == 4:
                if self.position[0] >= 8:
                    self.position[0] -= 1
            if self.rotation == 2:
                if self.position[0] <= -1:
                    self.position[0] += 1
            if self.rotation == 1:
                if self.position[1] >= 18:
                    self.position[1] -= 1  
        self.rotation += 1
        if self.rotation > 4:
            self.rotation = 1
    
    def rotate90(self):
        # Rotate the Tetrominoe 90 degrees clockwise
        mat = self.matrix
        n = len(mat)
        for i in range(n // 2):
            for j in range(i, n - i - 1):
                temp = mat[i][j]
                mat[i][j] = mat[n - 1 - j][i]                # Move P4 to P1
                mat[n - 1 - j][i] = mat[n - 1 - i][n - 1 - j]  # Move P3 to P4
                mat[n - 1 - i][n - 1 - j] = mat[j][n - 1 - i]  # Move P2 to P3
                mat[j][n - 1 - i] = temp                      # Move P1 to P2
        self.rotate_adjust_position()

    def check_rotation(self, board):
        # Check if the Tetrominoe can rotate without obstruction
        for y, row in enumerate(self.matrix):
                for x, cell in enumerate(row):
                    if cell > 0 and (self.position[1] + y >= 20 or board[self.position[1] + y][self.position[0] + x] > 1):   
                        return False
        return True
    
    def to_string(self):
        # Print the Tetrominoe's shape, position, and rotation
        print(str(self.shape) + " " + str(self.position) + " " + str(self.rotation))
