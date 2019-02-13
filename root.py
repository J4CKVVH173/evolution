import settings
import time
import tools
import random

from tkinter import *
from cells import Cell, Accident

root = Tk()
root.title('Evolution')
root.geometry('1265x720')

canvas = Canvas(root, width=1280, height=720, background='yellow')
canvas.pack()

grid = [[0]*settings.COL for g in range(settings.ROW)]
x1 = 0
y1 = 0
x2 = settings.CELL_X
y2 = settings.CELL_Y
cells = []
position_on_map = {}

# create a field for the existence of the cells and saving they id to the array
for idx, row in enumerate(grid):
    if idx == 0 or idx == len(grid) - 1:  # first and last row is grey
        for col in row:
            canvas.create_rectangle(x1, y1, x2, y2, fill=settings.WALL)
            x1 += settings.CELL_X
            x2 += settings.CELL_X
    else:
        for i, col in enumerate(row):
            if i == 0 or i == len(row) - 1:  # right and left col is grey
                canvas.create_rectangle(x1, y1, x2, y2, fill=settings.WALL)
            else:  # other cells is white
                row[i] = canvas.create_rectangle(x1, y1, x2, y2, fill=settings.EMPTY)
            x1 += settings.CELL_X
            x2 += settings.CELL_X
    x1 = 0
    x2 = settings.CELL_X
    y1 += settings.CELL_Y
    y2 += settings.CELL_Y


for _ in range(25):
    cells.append(tools.create_cell(canvas, grid, position_on_map))

position_on_map[0] = 'wall'

for i in range(200):
    food_id = tools.create_food(position_on_map, grid)
    canvas.itemconfig(food_id, fill=settings.FOOD)
    position_on_map[food_id] = 'food'

best_dna = []
dead_cells = []
counter = 0

start = time.clock()
while bool(cells):
    canvas.update()
    for cell in cells:
        if len(cells) > 5:
            while cell['cell'].can_move():
                cell['cell'].action(canvas, position_on_map)
            if cell['cell'].cell_ate():
                remove_id = cell['cell'].get_ate_cell_id()
                canvas.itemconfig(remove_id, fill=settings.EMPTY)
                del position_on_map[remove_id]
                food_id = tools.create_food(position_on_map, grid)
                canvas.itemconfig(food_id, fill=settings.FOOD)
                position_on_map[food_id] = 'food'
            if not cell['cell'].has_health():
                if len(cells) - len(dead_cells) - 1 < 5:
                    """
                     За одну итерацию может быть убито несколько клеток.
                      И это число может стать меньше 5. Чтобы этого не произошло, когда пятая по счету клетка должна 
                      умереть, цикл прекращается, чтобы она не умерла.
                    """
                    break
                else:
                    cell['cell'].kill(canvas, position_on_map)
                    dead_cells.append(cell)
            else:
                cell['cell'].reset_steps()
        else:
            break

    if len(dead_cells) > 0:
        for dead_cell in dead_cells:
            cells.remove(dead_cell)
        dead_cells.clear()

    if len(cells) == 5:
        for cell in cells:
            best_dna.append(cell['cell'].get_dna())
            cell['cell'].kill(canvas, position_on_map)
        cells.clear()
        for j in range(25):
            cells.append(tools.create_cell(canvas, grid, position_on_map))
        for idx, cell in enumerate(cells):
            cell['cell'].set_dna(best_dna[idx % 5].copy())
        best_dna.clear()
        for idx, cell in enumerate(cells):
            if idx == 5:
                break
            elif idx < 5:
                cell['cell'].mutation()
        end = time.clock()
        print(end - start)
        for key in position_on_map:
            if position_on_map[key] == 'food':
                counter += 1
        print('counter-->', counter)
        counter = 0
        start = time.clock()

    elif len(cells) < 5:
        raise Accident('len smaller then 5')

    canvas.update()
    # time.sleep(0.01)

root.mainloop()

"""
hash map of elements on the map 
{
    id: 'type'
    id - id of the map
    type - cell type on this cell  
}
"""
