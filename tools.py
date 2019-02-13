import settings
import random

from cells import Cell


def create_cell(canvas, grid, positions) -> dict:
    text_id = canvas.create_text(settings.CELL_CENTER, settings.CELL_CENTER, text='20')
    x = random.randint(2, 48)
    y = random.randint(2, 26)
    while positions.get(grid[y][x]):
        x = random.randint(2, 48)
        y = random.randint(2, 26)
    temp = {
        'cell': Cell(grid[y][x], x, y, grid, text_id),
        'text': text_id
    }
    canvas.itemconfig(temp['cell'].get_id(), fill=settings.CELL_COLOR)
    positions[temp['cell'].get_id()] = 'cell'
    return temp.copy()


def create_food(positions: dict, map_grid: list) -> int:
    first_id = settings.COL + 2
    last_id = settings.COL * (settings.ROW - 1) - 1
    while True:
        food_id = random.randint(first_id, last_id)
        if food_id not in positions:
            for row in map_grid:
                if food_id in row:
                    return food_id

