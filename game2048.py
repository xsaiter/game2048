import tkinter as tk
import random
from enum import Enum

N = 4
N2 = N * N

PANE_SIZE = 400
PANE_COLOR = "white"

CELL_SIZE = PANE_SIZE / N
CELL_COLOR = "grey"
CELL_PAD = 4
CELL_FONT = ("Verdana", 35, "bold")


class Directions(Enum):
    LEFT = 1,
    RIGHT = 2,
    DOWN = 3,
    UP = 4


def get_pos(row, col):
    return N * row + col


class MainWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid(row=4, column=1)

        self.master.title("game 2048")

        self.menu = tk.Menu(master)
        self.menu.add_command(label="New", command=self.new_game)
        self.menu.add_command(label="Quit", command=master.quit)
        master.config(menu=self.menu)

        self.info_bar = tk.Label(self)
        self.info_bar.grid(row=1, column=0)
        self.score = 0
        self.update_score(self.score)

        pane = tk.Frame(self, bg=PANE_COLOR, width=PANE_SIZE, height=PANE_SIZE)
        pane.grid(row=2, column=0)

        pane.bind("<Left>", self.do_left)
        pane.bind("<Right>", self.do_right)
        pane.bind("<Up>", self.do_up)
        pane.bind("<Down>", self.do_down)

        pane.focus_set()

        self.status_bar = tk.Label(self, text="")
        self.status_bar.grid(row=3, column=0, sticky=tk.W)

        self.cells = []
        self.m = []
        self.moved = False

        for i in range(N):
            for j in range(N):
                cell = tk.Frame(master=pane, bg=CELL_COLOR, width=CELL_SIZE, height=CELL_SIZE)
                cell.grid(row=i, column=j, padx=CELL_PAD, pady=CELL_PAD)

                label = tk.Label(cell, font=CELL_FONT, text="", width=4, height=2)
                label.grid()

                self.m.append(0)
                self.cells.append(cell)

        self.gen()
        self.gen()

    def new_game(self):
        for i in range(N2):
            self.update_cell(i, 0)
        self.gen()
        self.gen()
        self.status_bar["text"] = ""

    def do_up(self, event):
        self.do_move(Directions.UP)

    def do_down(self, event):
        self.do_move(Directions.DOWN)

    def do_left(self, event):
        self.do_move(Directions.LEFT)

    def do_right(self, event):
        self.do_move(Directions.RIGHT)

    def do_move(self, direction):
        if not self.game_over():
            self.moved = False
            self.move_xy(direction)
            self.gen_if()

    def move_xy(self, direction):
        rows = range(N)

        cols = range(N)
        if direction == Directions.RIGHT or direction == Directions.DOWN:
            cols = range(N - 1, -1, -1)

        for row in rows:
            for col in cols:
                i = get_pos(row, col)
                if direction == Directions.DOWN or direction == Directions.UP:
                    i = get_pos(col, row)

                if self.m[i] != 0:
                    p = col
                    c = col - 1
                    if direction == Directions.RIGHT or direction == direction.DOWN:
                        c = col + 1

                    while 0 <= c <= N - 1:
                        ci = get_pos(row, c)
                        pi = get_pos(row, p)
                        if direction == Directions.DOWN or direction == Directions.UP:
                            ci = get_pos(c, row)
                            pi = get_pos(p, row)
                        if self.m[ci] != 0:
                            if self.m[ci] == self.m[pi]:
                                value = self.m[ci] + self.m[pi]
                                self.move(pi, ci, value)
                                self.update_score(value)
                            break
                        else:
                            self.move(pi, ci, self.m[pi])
                        p = c
                        if direction == Directions.RIGHT or direction == Directions.DOWN:
                            c += 1
                        else:
                            c -= 1

    def move(self, source, destination, value):
        if source != destination:
            self.update_cell(source, 0)
            self.update_cell(destination, value)
            self.moved = True

    def gen_if(self):
        if self.moved is True:
            self.gen()

    def gen(self):
        if not self.no_empty_cells():
            while True:
                n = random.randint(0, N2 - 1)
                if self.m[n] == 0:
                    self.update_cell(n, 2)
                    break

        if self.game_over():
            self.update_status_bar("game over!")

    def game_over(self):
        return self.no_empty_cells() and self.no_moves()

    def no_empty_cells(self):
        return all(x != 0 for x in self.m)

    def no_moves(self):
        for row in range(N):
            for col in range(N):
                i = get_pos(row, col)

                if col < N - 1:
                    x = get_pos(row, col + 1)
                    if self.m[i] == self.m[x]:
                        return False

                if row < N - 1:
                    y = get_pos(row + 1, col)
                    if self.m[i] == self.m[y]:
                        return False

        return True

    def update_cell(self, i, value):
        c = self.cells[i]
        for v in c.children.values():
            if value == 0:
                v["text"] = ""
            else:
                v["text"] = str(value)
            self.m[i] = value

    def update_score(self, value):
        self.score += value
        self.info_bar["text"] = "score: {0}".format(self.score)

    def update_status_bar(self, text):        
        self.status_bar["text"] = text


root = tk.Tk()
window = MainWindow(master=root)
window.mainloop()
