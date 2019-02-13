import random
import settings

from tkinter import Canvas


class Accident(Exception):

    def __init__(self, msg):
        self.msg = msg

    def msg_print(self):
        return self.msg


def set_position(cells: list) -> dict:
    positions = dict()
    for cell in cells:
        positions[cell['cell'].get_id()] = 'cell'

    return positions


class Cell:

    def __init__(self, sell_id: int, x: int, y: int, grid: list, health_id: int) -> None:
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
        self.dna = self._dna_generation()
        self.health_text_id = health_id
        self.had_meal = False
        self.id_ate = 0

    def __str__(self):
        return f'x: {self.x}, y: {self.y}, text: {self.health_text_id}'

    def get_position(self) -> list:
        position = [self.id, self.x, self.y]
        return position

    def can_move(self) -> bool:
        return bool(self.steps)

    def action(self, canvas: Canvas, items: dict) -> None:
        """
        1 - to step
        from 2 to 5 - to turn
        6 - to eat
        :param canvas:
        :param items:
        :return:
        """
        current_action: int = self.dna[self.dna_pointer]
        if 2 <= current_action <= 5:
            self.face = current_action
            self.steps -= 1
            if self.dna_pointer < len(self.dna) - 1:
                self.dna_pointer += 1
            else:
                self.dna_pointer = 0
        elif current_action == 1:
            # cell takes a step in given direction
            if self.face == 3 and not self._check_slot(self.x + 1, self.y, items):  # step to right
                self._step(self.x + 1, self.y, canvas, items)
            elif self.face == 4 and not self._check_slot(self.x, self.y + 1, items):  # step to down
                self._step(self.x, self.y + 1, canvas, items)
            elif self.face == 5 and not self._check_slot(self.x - 1, self.y, items):  # step to left
                self._step(self.x - 1, self.y, canvas, items)
            elif self.face == 2 and not self._check_slot(self.x, self.y - 1, items):  # step to up
                self._step(self.x, self.y - 1, canvas, items)
            self.steps = 0
            self._update_health(canvas, -1)
            self._set_dna_pinter()
        elif current_action == 6:
            # cell take a food
            if self.face == 3 and self._check_slot(self.x + 1, self.y, items, 'food'):
                self._eat(self.y, self.x + 1, canvas, items)
            elif self.face == 4 and self._check_slot(self.x, self.y + 1, items, 'food'):
                self._eat(self.y + 1, self.x, canvas, items)
            elif self.face == 5 and self._check_slot(self.x - 1, self.y, items, 'food'):
                self._eat(self.y, self.x - 1, canvas, items)
            elif self.face == 2 and self._check_slot(self.x, self.y - 1, items, 'food'):
                self._eat(self.y - 1, self.x, canvas, items)

            self.steps = self.steps / 2
            self._set_dna_pinter()
        else:
            raise Accident('Something wrong in action method')

    def reset_steps(self) -> None:
        # sets the steps in the initial value
        self.steps = 10

    def get_coordinates(self) -> tuple:
        return self.x, self.y

    def get_id(self) -> int:
        return self.id

    def _check_slot(self, x: int, y: int, items: dict, slot='busy') -> bool:
        """
        Check the cell with specified coordinate
        :param x: cell x coordinate
        :param y: cell y coordinate
        :param items: list of all non-empty cells
        :param slot: 'busy' - cell is busy with something
        :return: bool
        """

        if slot == 'busy':
            return bool(items.get(self.MAP[y][x]))
        if slot == 'food':
            return items.get(self.MAP[y][x]) == 'food'

    def _eat(self, y: int, x: int, canvas: Canvas, items: dict) -> None:
        # method update cell's health if it ate a food
        self._update_health(canvas, 10)
        self._set_dna_pinter()
        self.had_meal = True
        self.id_ate = self.MAP[y][x]

    def _step(self, next_x: int, next_y: int, canvas: Canvas, items: dict) -> None:
        """
        method moves the cell to a new slot
        :param next_x: x coordinate the new slot
        :param next_y: y coordinate the new slot
        :param canvas: object canvas
        :param items: hash map of all objects on the map
        :return: None
        """

        del items[self.id]  # delete in hash old cell position

        canvas.itemconfig(self.id, fill=settings.EMPTY)
        self.y = next_y
        self.x = next_x
        self.id = self.MAP[self.y][self.x]
        canvas.itemconfig(self.id, fill=settings.CELL_COLOR)

        items[self.id] = 'cell'  # add to hash new cell position

    def _set_dna_pinter(self) -> None:
        if self.dna_pointer < len(self.dna) - 1:
            self.dna_pointer += 1
        else:
            self.dna_pointer = 0

    def _update_health(self, canvas: Canvas, points: int) -> None:
        """
        Updating health counter and text
        :param canvas: object Canvas
        :return: None
        """
        canvas.coords(self.health_text_id,
                      settings.CELL_CENTER + settings.CELL_X * self.x,
                      settings.CELL_CENTER + settings.CELL_Y * self.y)
        self.health += points
        canvas.itemconfig(self.health_text_id, text=str(self.health))

    def has_health(self):
        return self.health > 0

    def kill(self, canvas, items):
        # remove cell from the map and delete health text
        canvas.itemconfig(self.id, fill=settings.EMPTY)
        canvas.delete(self.health_text_id)
        del items[self.id]

    def cell_ate(self) -> bool:
        if self.had_meal:
            self.had_meal = False
            return True
        else:
            return False

    def get_dna(self) -> list:
        return self.dna

    def set_dna(self, dna: list) -> None:
        self.dna = dna

    def get_ate_cell_id(self) -> int:
        return self.id_ate

    def mutation(self) -> None:
        for idx, nucleotide in enumerate(self.dna):
            if idx % 8 == 0:
                self.dna[idx] = random.randint(1, 6)

    @staticmethod
    def _dna_generation():
        return [random.randint(1, 6) for _ in range(64)]

