
import random
import curses

# 定义方块形状
SHAPES = [
    [[True, True, True, True]],  # I 形
    [[True, False, False], [True, True, True], [False, False, True]],  # T 形
    [[False, True, False], [True, True, True], [False, False, False]],  # L 形
    [[True, True, False], [True, True, True], [False, False, False]],  # 反L形
    [[True, True], [True, True]]  # Z 形
]

class TetrisGame:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.board_height = 20
        self.board_width = 10
        self.board = [[False] * self.board_width for _ in range(self.board_height)]
        self.current_piece = random.choice(SHAPES)
        self.current_position = [0, self.board_width // 2]
        self.score = 0
        self.speed = 0.5
        self.game_over = False
        self.next_piece = random.choice(SHAPES)

    def draw_board(self):
        self.stdscr.clear()
        for row in self.board:
            for cell in row:
                self.stdscr.addstr("|" if cell else " ", curses.color_pair(1))
            self.stdscr.addstr("\n")
        # 显示下一个方块预览
        self.show_next_piece_preview()
        self.stdscr.refresh()

    def show_next_piece_preview(self):
        self.stdscr.addstr("\nNext Piece:\n")
        for row in self.next_piece:
            for cell in row:
                self.stdscr.addstr("X" if cell else " ", curses.color_pair(2))
            self.stdscr.addstr("\n")

    def move_down(self):
        new_pos = [self.current_position[0] + 1, self.current_position[1]]
        if not self.collides(new_pos, self.current_piece):
            self.current_position = new_pos
        else:
            self.lock_piece()

    def move_left(self):
        new_pos = [self.current_position[0], self.current_position[1] - 1]
        if not self.collides(new_pos, self.current_piece):
            self.current_position = new_pos

    def move_right(self):
        new_pos = [self.current_position[0], self.current_position[1] + 1]
        if not self.collides(new_pos, self.current_piece):
            self.current_position = new_pos

    def rotate(self):
        rotated_piece = list(zip(*reversed(self.current_piece)))
        if not self.collides(self.current_position, rotated_piece):
            self.current_piece = rotated_piece

    def collides(self, position, piece):
        for y, row in enumerate(piece):
            for x, cell in enumerate(row):
                if cell:
                    if position[1] + x < 0 or position[1] + x >= self.board_width or \
                       position[0] + y >= self.board_height or \
                       self.board[position[0] + y][position[1] + x]:
                        return True
        return False

    def lock_piece(self):
        for y, row in enumerate(self.current_piece):
            for x, cell in enumerate(row):
                if cell:
                    self.board[self.current_position[0] + y][self.current_position[1] + x] = True
        self.check_lines()
        self.current_piece = self.next_piece
        self.current_position = [0, self.board_width // 2]
        self.next_piece = random.choice(SHAPES)
        if self.collides(self.current_position, self.current_piece):
            self.game_over = True

    def check_lines(self):
        lines_cleared = 0
        for i, row in enumerate(self.board):
            if all(row):
                del self.board[i]
                self.board.insert(0, [False] * self.board_width)
                lines_cleared += 1
        self.score += lines_cleared ** 2
        # 更新速度基于消行数
        self.speed = min(1.5, self.speed + 0.005 * lines_cleared)

    def start_game(self):
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)  # 为下一个方块预览添加颜色对
        while not self.game_over:
            self.draw_board()
            self.stdscr.timeout(int(1000 / (0.5 + self.speed)))
            key = self.stdscr.getch()
            if key == curses.KEY_DOWN:
                self.move_down()
            elif key == curses.KEY_LEFT:
                self.move_left()
            elif key == curses.KEY_RIGHT:
                self.move_right()
            elif key == curses.KEY_UP:
                self.rotate()
            else:
                self.move_down()
        self.stdscr.addstr("\nGame Over!\nScore: {}\n".format(self.score), curses.A_BOLD)
        self.stdscr.getch()

def main():
    curses.wrapper(TetrisGame().start_game)

if __name__ == "__main__":
    main()