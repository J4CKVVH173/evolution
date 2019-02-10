import random

from tkinter import Canvas
from tools import Accident


class Cell:

    def __init__(self, sell_id: int, x: int, y: int, grid: list) -> None:
        """
        init object
        :param sell_id: id sell on the map
        :param x: the x position of the sell
        :param y: the y position of the sell
        :param grid: current map
        """
        self.id = sell_id
        self.x = x
        self.y = y
        self.health = 25
        self.face = random.randint(2, 5)  # front side of the cell
        self.steps = 10  # number of available cell moves
        self.dna_pointer = 0
        self.MAP = grid.copy()
        self.dna = self.dna_generation()

    def get_position(self) -> list:
        position = [self.id, self.x, self.y]
        return position

    def can_move(self) -> bool:
        return bool(self.steps)

    def action(self, canvas: Canvas) -> None:
        current_action: int = self.dna[self.dna_pointer]
        if 2 <= current_action <= 5:
            self.face = current_action
            self.steps -= 1
            if self.dna_pointer < len(self.dna) - 1:
                self.dna_pointer += 1
            else:
                self.dna_pointer = 0
        elif current_action == 1:
            if self.face == 3 and bool(self.MAP[self.y][self.x + 1]):  # step to right
                canvas.itemconfig(self.id, fill='white')
                self.x += 1
                self.id = self.MAP[self.y][self.x]
                canvas.itemconfig(self.id, fill='green')
            elif self.face == 4 and bool(self.MAP[self.y + 1][self.x]):  # step to down
                canvas.itemconfig(self.id, fill='white')
                self.y += 1
                self.id = self.MAP[self.y][self.x]
                canvas.itemconfig(self.id, fill='green')
            elif self.face == 5 and bool(self.MAP[self.y][self.x - 1]):  # step to left
                canvas.itemconfig(self.id, fill='white')
                self.x -= 1
                self.id = self.MAP[self.y][self.x]
                canvas.itemconfig(self.id, fill='green')
            elif self.face == 2 and bool(self.MAP[self.y - 1][self.x]):  # step to up
                canvas.itemconfig(self.id, fill='white')
                self.y -= 1
                self.id = self.MAP[self.y][self.x]
                canvas.itemconfig(self.id, fill='green')
            self.steps = 0
            if self.dna_pointer < len(self.dna) - 1:
                self.dna_pointer += 1
            else:
                self.dna_pointer = 0
        else:
            raise Accident('Something wrong in action method')

    def reset_steps(self) -> None:
        # sets the steps in the initial value
        self.steps = 10

    @staticmethod
    def dna_generation():
        return [random.randint(1, 5) for _ in range(64)]
