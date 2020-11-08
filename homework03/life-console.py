import argparse
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
                symbol = arguments.symbol if value else " "
                try:
                    screen.addstr(pos_x + 1, pos_y + 1, symbol)
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GameOfLife")
    parser.add_argument("--rows", type=int, default=20, help="Enter number of rows in grid")
    parser.add_argument("--cols", type=int, default=40, help="Enter number of columns in grid")
    parser.add_argument("--speed", type=int, default=10, help="Enter game speed")
    parser.add_argument(
        "--maxgenerations", type=int, default=1000, help="Enter max number of generations"
    )
    parser.add_argument("--randomize", type=int, default=1, help="Should grid be randomized?")
    parser.add_argument(
        "--symbol", type=str, default="@", help="Select a symbol to display live cells"
    )
    arguments = parser.parse_args()
    gui = Console(
        GameOfLife((arguments.rows, arguments.cols), arguments.randomize, arguments.maxgenerations)
    )
    gui.run()
