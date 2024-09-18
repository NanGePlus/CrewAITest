
import pygame
import random

# 游戏参数
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
BOARD_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
BOARD_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE

# 颜色定义
COLORS = {
    'I': (0, 255, 255),
    'T': (128, 0, 128),
    'L': (255, 165, 0),
    'Z': (255, 0, 0),
    'BACKGROUND': (0, 0, 0)
}

# 形状定义
SHAPES = {
    'I': [[1, 1, 1, 1]],
    'T': [[0, 1, 0],
           [1, 1, 1]],
    'L': [[0, 0, 1],
           [1, 1, 1]],
    'Z': [[1, 1, 0],
           [0, 1, 1]]
}

class Tetris:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("经典俄罗斯方块")
        self.clock = pygame.time.Clock()
        self.board = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
        self.score = 0
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.speed = 500
        self.last_fall_time = pygame.time.get_ticks()

    def new_piece(self):
        shape = random.choice(list(SHAPES.keys()))
        return {'shape': SHAPES[shape], 'color': COLORS[shape], 'x': BOARD_WIDTH // 2 - len(SHAPES[shape][0]) // 2, 'y': 0}

    def draw_board(self):
        self.screen.fill(COLORS['BACKGROUND'])
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                if self.board[y][x]:
                    pygame.draw.rect(self.screen, self.board[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def draw_piece(self, piece):
        for y, row in enumerate(piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, piece['color'], ((piece['x'] + x) * BLOCK_SIZE, (piece['y'] + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def rotate_piece(self, piece):
        piece['shape'] = [list(row) for row in zip(*piece['shape'][::-1])]

    def move_piece(self, dx):
        self.current_piece['x'] += dx
        if self.check_collision():
            self.current_piece['x'] -= dx

    def drop_piece(self):
        self.current_piece['y'] += 1
        if self.check_collision():
            self.current_piece['y'] -= 1
            self.lock_piece()
            self.clear_lines()
            self.current_piece = self.next_piece
            self.next_piece = self.new_piece()
            if self.check_collision():
                self.game_over()

    def check_collision(self):
        for y, row in enumerate(self.current_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    board_x = self.current_piece['x'] + x
                    board_y = self.current_piece['y'] + y
                    if board_x < 0 or board_x >= BOARD_WIDTH or board_y >= BOARD_HEIGHT or self.board[board_y][board_x]:
                        return True
        return False

    def lock_piece(self):
        for y, row in enumerate(self.current_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    self.board[self.current_piece['y'] + y][self.current_piece['x'] + x] = self.current_piece['color']

    def clear_lines(self):
        lines_to_clear = [i for i, row in enumerate(self.board) if all(row)]
        for i in lines_to_clear:
            self.board.pop(i)
            self.board.insert(0, [0] * BOARD_WIDTH)
            self.score += 1

    def game_over(self):
        print("游戏结束！得分：", self.score)
        pygame.quit()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move_piece(-1)
                    if event.key == pygame.K_RIGHT:
                        self.move_piece(1)
                    if event.key == pygame.K_DOWN:
                        self.drop_piece()
                    if event.key == pygame.K_UP:
                        self.rotate_piece(self.current_piece)

            current_time = pygame.time.get_ticks()
            if current_time - self.last_fall_time > self.speed:
                self.drop_piece()
                self.last_fall_time = current_time

            self.draw_board()
            self.draw_piece(self.current_piece)
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    game = Tetris()
    game.run()
