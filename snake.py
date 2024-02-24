import pygame
import collections
import sys
import random
import itertools

BACKGROUND = (30, 30, 46)
SNAKE_COLOUR = (166, 227, 161)
APPLE_COLOUR = (243, 139, 168)
FRAMES_PER_SECOND = 60
RESOLUTION = 500
DIRECTIONS = {
    "left": (-1, 0),
    "right": (1, 0),
    "up": (0, -1),
    "down": (0, 1),
}


class Snake:
    def __init__(self, game, pos, size):
        self.game = game
        self.head = pygame.Rect(*pos, *size)
        self.snake = collections.deque([self.head])
        self.movement = DIRECTIONS['right']
        self.to_grow = False
        self.dead = False
        self.moving = False

    def __len__(self):
        return len(self.snake)

    def get_positions(self):
        return [(rect.x, rect.y) for rect in self.snake]

    def change_direction(self, direction):
        self.moving = True
        self.movement = DIRECTIONS[direction]

    def grow(self):
        self.to_grow = True

    def update(self):
        x, y = self.movement
        new_pos = (x * self.game.tilesize[0], y * self.game.tilesize[0])
        self.head = self.head.move(*new_pos)
        self.snake.appendleft(self.head.copy())
        if not self.to_grow:
            self.snake.pop()
        else:
            self.to_grow = False
        self.dead = any(
            self.head.colliderect(body_block)
            for body_block in list(self.snake)[1:]
        )
        self.moving = False

    def render(self):
        for snake_block in self.snake:
            pygame.draw.rect(
                self.game.screen,
                (SNAKE_COLOUR),
                snake_block,
                border_radius=int(self.game.tilesize[0] / 3),
            )


class Apple:
    def __init__(self, game, size):
        self.game = game
        self.apple = pygame.Rect(*self.get_valid_position(), *size)

    def get_valid_position(self):
        snake_pos = set(self.game.snake.get_positions())
        apple_coords = random.choice(list(self.game.tile_coords - snake_pos))
        return apple_coords

    def update(self):
        if self.apple is None:
            apple_coords = self.get_valid_position()
            self.apple = pygame.Rect(*apple_coords, *self.game.tilesize)
        if self.apple.colliderect(self.game.snake.head):
            self.game.snake.grow()
            self.apple = None

    def render(self):
        if self.apple:
            pygame.draw.circle(
                self.game.screen,
                APPLE_COLOUR,
                self.apple.center,
                self.apple.width / 2 - 5,
            )


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((RESOLUTION, RESOLUTION))
        self.clock = pygame.time.Clock()
        self.tilesize = (50, 50)
        self.tile_coords = set(
            itertools.product(range(0, RESOLUTION, self.tilesize[0]), repeat=2)
        )
        self.snake = Snake(
            self, (RESOLUTION / 2, RESOLUTION / 2), self.tilesize
        )
        self.apple = Apple(self, self.tilesize)
        self.speed = 6

    def run(self):
        frame_to_move = int(FRAMES_PER_SECOND / self.speed)
        frame_counter = 0
        while True:
            if len(self.snake) == len(self.tile_coords):
                self.end(win=True)
            if (
                any(
                    p < -5 or p > RESOLUTION + 5 - self.tilesize[0]
                    for p in self.snake.head
                )
                or self.snake.dead
            ):
                self.end(win=False)
            self.render()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if not self.snake.moving:
                        if (
                            self.snake.movement != DIRECTIONS['right']
                            and event.key == pygame.K_LEFT
                        ):
                            self.snake.change_direction('left')
                        if (
                            self.snake.movement != DIRECTIONS['left']
                            and event.key == pygame.K_RIGHT
                        ):
                            self.snake.change_direction('right')
                        if (
                            self.snake.movement != DIRECTIONS['up']
                            and event.key == pygame.K_DOWN
                        ):
                            self.snake.change_direction('down')
                        if (
                            self.snake.movement != DIRECTIONS['down']
                            and event.key == pygame.K_UP
                        ):
                            self.snake.change_direction('up')
            frame_counter += 1
            if frame_to_move == frame_counter:
                frame_counter = 0
                self.snake.update()
            self.apple.update()
            pygame.display.update()
            self.clock.tick(FRAMES_PER_SECOND)

    def render(self):
        self.screen.fill((BACKGROUND))
        self.snake.render()
        self.apple.render()

    def end(self, win):
        print('Game ended')
        if win:
            print("wow fabolous, you win")
        else:
            print("you lose")
        exit()


Game().run()
