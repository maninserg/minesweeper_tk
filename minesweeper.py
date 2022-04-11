import tkinter as tk

window = tk.Tk()

ROWS = 5
COLUMNS = 7

buttons = []

for i in range(ROWS):
    temp = []
    for j in range(COLUMNS):
        btn = tk.Button(window, width=1, font='Calibri 20 bold')
        temp.append(btn)
    buttons.append(temp)

for i in range(ROWS):
    for j in range(COLUMNS):
        btn = buttons[i][j]
        btn.grid(row=i, column=j)

window.mainloop()