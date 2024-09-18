
import pygame
import random

# --- Game Configuration ---
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
GRID_SIZE = 30

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [
    (0, 255, 255),  # I
    (255, 0, 255),  # T
    (255, 165, 0),  # L
    (255, 0, 0)     # Z
]

# Shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 1, 0], [0, 1, 1]]   # Z
]

# --- Game Classes ---
class Tetris:
    def __init__(self):
        self.grid = [[0 for _ in range(SCREEN_WIDTH // GRID_SIZE)] for _ in range(SCREEN_HEIGHT // GRID_SIZE)]
        self.shapes = SHAPES
        self.colors = COLORS
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.score = 0
        self.game_over = False

    def new_piece(self):
        shape = random.choice(self.shapes)
        color = self.colors[self.shapes.index(shape)]
        return Piece(shape, color)

    def rotate_piece(self):
        self.current_piece.shape = [list(row) for row in zip(*self.current_piece.shape[::-1])]
        if self.collision():
            self.current_piece.shape = [list(row) for row in zip(*self.current_piece.shape)][::-1]

    def move_piece(self, dx, dy):
        self.current_piece.x += dx
        self.current_piece.y += dy
        if self.collision():
            self.current_piece.x -= dx
            self.current_piece.y -= dy
            return False
        return True

    def collision(self):
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    if (
                        x + self.current_piece.x < 0 or
                        x + self.current_piece.x >= SCREEN_WIDTH // GRID_SIZE or
                        y + self.current_piece.y >= SCREEN_HEIGHT // GRID_SIZE or
                        self.grid[y + self.current_piece.y][x + self.current_piece.x]
                    ):
                        return True
        return False

    def lock_piece(self):
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[y + self.current_piece.y][x + self.current_piece.x] = self.current_piece.color
        self.clear_lines()
        self.current_piece = self.next_piece
        self.next_piece = self.new_piece()
        if self.collision():
            self.game_over = True

    def clear_lines(self):
        lines_to_clear = [i for i, row in enumerate(self.grid) if all(row)]
        for i in lines_to_clear:
            del self.grid[i]
            self.grid.insert(0, [0 for _ in range(SCREEN_WIDTH // GRID_SIZE)])
        self.score += len(lines_to_clear)

    def update(self):
        if not self.move_piece(0, 1):
            self.lock_piece()

    def draw(self, screen):
        screen.fill(BLACK)
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, cell, pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, self.current_piece.color, pygame.Rect((x + self.current_piece.x) * GRID_SIZE, (y + self.current_piece.y) * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        pygame.display.flip()

class Piece:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = SCREEN_WIDTH // GRID_SIZE // 2 - len(shape[0]) // 2
        self.y = 0

# --- Main Program ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("经典俄罗斯方块")
    clock = pygame.time.Clock()

    tetris = Tetris()
    fall_time = 0
    fall_speed = 0.5

    running = True
    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    tetris.move_piece(-1, 0)
                if event.key == pygame.K_RIGHT:
                    tetris.move_piece(1, 0)
                if event.key == pygame.K_DOWN:
                    tetris.move_piece(0, 1)
                if event.key == pygame.K_UP:
                    tetris.rotate_piece()

        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            tetris.update()
            if tetris.game_over:
                running = False

        tetris.draw(screen)

    pygame.quit()

if __name__ == "__main__":
    main()
