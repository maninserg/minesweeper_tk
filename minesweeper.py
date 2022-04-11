import tkinter as tk

class MineSweeper:
    
    window = tk.Tk()
    ROWS = 5
    COLUMNS = 7

    def __init__(self):
        self.buttons = []
        for i in range(MineSweeper.ROWS):
            temp = []
            for j in range(MineSweeper.COLUMNS):
                btn = tk.Button(MineSweeper.window, width=1, font='Calibri 20 bold')
                temp.append(btn)
            self.buttons.append(temp)

    def create_widgets(self):
        for i in range(MineSweeper.ROWS):
            for j in range(MineSweeper.COLUMNS):
                btn = self.buttons[i][j]
                btn.grid(row=i, column=j)
    
    def start(self):
        self.create_widgets()
        MineSweeper.window.mainloop()


game = MineSweeper()
game.start()