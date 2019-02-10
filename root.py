import settings
import cells
import time

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


cell_one = cells.Cell(grid[2][2], 2, 2, grid)
cell_two = cells.Cell(grid[3][3], 3, 3, grid)
cell_three = cells.Cell(grid[4][2], 4, 2, grid)

cells = [cell_one, cell_two, cell_three]

while True:

    for cell in cells:
        while cell.can_move():
            cell.action(canvas)
        cell.reset_steps()
    canvas.update()
    time.sleep(0.3)

root.mainloop()
