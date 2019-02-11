import settings
import cells
import time
import tools

from tkinter import *

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

# create a field for the existence of the cells and saving they id to the array
for idx, row in enumerate(grid):
    if idx == 0 or idx == len(grid) - 1:  # first and last row is grey
        for col in row:
            canvas.create_rectangle(x1, y1, x2, y2, fill='grey')
            x1 += settings.CELL_X
            x2 += settings.CELL_X
    else:
        for i, col in enumerate(row):
            if i == 0 or i == len(row) - 1:  # right and left col is grey
                canvas.create_rectangle(x1, y1, x2, y2, fill='grey')
            else:  # other cells is white
                row[i] = canvas.create_rectangle(x1, y1, x2, y2, fill='white')
            x1 += settings.CELL_X
            x2 += settings.CELL_X
    x1 = 0
    x2 = settings.CELL_X
    y1 += settings.CELL_Y
    y2 += settings.CELL_Y

id2 = canvas.create_text(settings.CELL_CENTER, settings.CELL_CENTER, text='20')
cell_one = cells.Cell(grid[2][2], 2, 2, grid, id2)
canvas.move(id2, settings.CELL_X * 2, settings.CELL_Y * 2)

cells = [cell_one]


position_on_map = tools.set_position(cells)
position_on_map[0] = 'wall'

while True:

    canvas.move(id, settings.CELL_X* 2, 0)
    for cell in cells:
        while cell.can_move():
            cell.action(canvas, position_on_map)
        cell.reset_steps()
    canvas.update()
    time.sleep(0.9)

root.mainloop()
