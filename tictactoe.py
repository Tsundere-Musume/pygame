import pygame
from pygame import gfxdraw
import sys

WINDOW_HEIGHT = 720
WINDOW_WIDTH = 1280
BACKGROUND = (0, 0, 0)
FOREGROUND = (255, 255, 255)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Tictactoe')
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        # self.board = [[None, None, None], [None,None,None], [None,None,None]]
        self.board = [None] * 9
        self.gridsize = min(WINDOW_WIDTH, WINDOW_HEIGHT) / 5
        self.gridx = int((WINDOW_WIDTH - 3 * self.gridsize) / 2)
        self.gridy = int((WINDOW_HEIGHT - 3 * self.gridsize) / 2)
        self.rects = []
        for i in range(9):
            x, y = self.get_grid_coord(i)
            self.rects.append(
                pygame.Rect(
                    x + 15, y + 15, self.gridsize - 30, self.gridsize - 30
                )
            )

        self.player_1 = 1
        self.player_2 = 2
        self.current_player = self.player_1

    def draw_circle(self, grid_no, width=5):
        x, y = self.get_grid_coord(grid_no)
        centerx = int(x + self.gridsize / 2)
        centery = y + int(self.gridsize / 2)
        r = int((self.gridsize - 30) / 2)
        pygame.gfxdraw.aacircle(self.screen, centerx, centery, r, FOREGROUND)
        pygame.gfxdraw.filled_circle(
            self.screen, centerx, centery, r, FOREGROUND
        )
        pygame.gfxdraw.aacircle(
            self.screen, centerx, centery, r - width, BACKGROUND
        )
        pygame.gfxdraw.filled_circle(
            self.screen, centerx, centery, r - width, BACKGROUND
        )

    def draw_cross(self, grid_no, width=5):
        x, y = self.get_grid_coord(grid_no)
        pygame.draw.line(
            self.screen,
            FOREGROUND,
            (x + 15, y + 15),
            (x + self.gridsize - 15, y + self.gridsize - 15),
            width=2 * width,
        )
        pygame.draw.line(
            self.screen,
            FOREGROUND,
            (x + self.gridsize - 15, y + 15),
            (x + 15, y + self.gridsize - 15),
            width=2 * width,
        )

    def get_grid_coord(self, grid_no):
        x = self.gridx + (grid_no % 3) * self.gridsize
        y = self.gridy + int(grid_no / 3) * self.gridsize
        return int(x), int(y)

    def draw_grid(self):
        pygame.draw.line(
            self.screen,
            FOREGROUND,
            (self.gridsize + self.gridx, self.gridy),
            (self.gridsize + self.gridx, self.gridy + 3 * self.gridsize),
            width=5,
        )
        pygame.draw.line(
            self.screen,
            FOREGROUND,
            (self.gridsize * 2 + self.gridx, self.gridy),
            (self.gridsize * 2 + self.gridx, self.gridy + 3 * self.gridsize),
            width=5,
        )
        pygame.draw.line(
            self.screen,
            FOREGROUND,
            (self.gridx, self.gridy + self.gridsize),
            (self.gridx + 3 * self.gridsize, self.gridy + self.gridsize),
            width=5,
        )
        pygame.draw.line(
            self.screen,
            FOREGROUND,
            (self.gridx, self.gridy + self.gridsize * 2),
            (self.gridx + 3 * self.gridsize, self.gridy + 2 * self.gridsize),
            width=5,
        )

    def make_move(self, mouse_pos):
        for ind, rect in enumerate(self.rects):
            if rect.collidepoint(mouse_pos):
                move = (
                    self.player_1
                    if self.current_player == self.player_1
                    else self.player_2
                )
                if not self.board[ind]:
                    self.board[ind] = move
                    self.current_player = (
                        self.player_2
                        if self.current_player == self.player_1
                        else self.player_1
                    )

    def check_win(self):
        checks = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6],
        ]
        for c in checks:
            a, b, c = self.board[c[0]], self.board[c[1]], self.board[c[2]]
            if all((a, b, c)) and a == b == c:
                return True
        return False

    def run(self):
        while True:
            pos = pygame.mouse.get_pos()
            self.screen.fill(BACKGROUND)
            self.draw_grid()
            for ind, rect in enumerate(self.rects):
                hit = rect.collidepoint(pos)
                if hit and not self.board[ind]:
                    s = pygame.Surface((rect.width, rect.height))
                    pygame.draw.rect(
                        self.screen, (255, 0, 0), rect, border_radius=15
                    )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.make_move(pygame.mouse.get_pos())

            self.render_moves()
            if self.check_win():
                break
        print(self.current_player)

    def render_moves(self):
        for index, move in enumerate(self.board):
            if move == 1:
                self.draw_circle(index)
            elif move == 2:
                self.draw_cross(index)
        pygame.display.update()


Game().run()
