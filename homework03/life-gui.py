import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        # Размер клетки
        self.cell_size = cell_size

        # Ширина и высота окна
        self.width = self.life.cols * self.cell_size
        self.height = self.life.rows * self.cell_size
        self.screen_size = self.width, self.height

        # Инициализация окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Скорость игры
        self.speed = speed

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        for pos_x, row in enumerate(self.life.curr_generation):
            for pos_y, col in enumerate(row):
                color = pygame.Color("white")
                if col:
                    color = pygame.Color("green")
                pygame.draw.rect(
                    self.screen,
                    color,
                    (
                        self.cell_size * pos_x + 1,
                        self.cell_size * pos_y + 1,
                        self.cell_size - 1,
                        self.cell_size - 1,
                    ),
                )

    def run(self) -> None:
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))
        self.grid = self.life.create_grid(True)
        running = True
        while running:
            if not self.life.is_changing or self.life.is_max_generations_exceeded:
                running = False
            for event in pygame.event.get():
                if event.type == QUIT:  # type: ignore
                    running = False
            self.draw_lines()
            self.life.step()
            self.draw_grid()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


# Uncomment to run game
# if __name__ == "__main__":
#     gui = GUI(GameOfLife((50, 50),  True, 10), 20)
#     gui.run()
