import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        screen.border("|", "|", "-", "-", "#", "#", "#", "#")

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        for pos_x, row in enumerate(self.life.curr_generation):
            for pos_y, value in enumerate(row):
                simbol = "@" if value else " "
                try:
                    screen.addstr(pos_x + 1, pos_y + 1, simbol)
                except curses.error:
                    continue

    def run(self) -> None:
        win = curses.initscr()
        curses.curs_set(0)
        win = curses.newwin(self.life.cols + 1, self.life.rows + 1, 0, 0)
        self.life.curr_generation = self.life.create_grid(True)
        running = True
        while running:
            if not self.life.is_changing or self.life.is_max_generations_exceeded:
                running = False
            win.clear()
            self.draw_grid(win)
            self.life.step()
            self.draw_borders(win)
            win.refresh()
        curses.endwin()
