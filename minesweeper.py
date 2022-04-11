import tkinter as tk


class MyButton(tk.Button):

    def __init__(self, master, x, y, *args, **kwargs):
        super(MyButton, self).__init__(master, width=1, font='Calibri 20 bold', *args, **kwargs)
        self.x = x
        self.y = y
        self.is_mine = False

    def __repr__(self):
        return f'MyButton[{self.x}]-[{self.y}]'


class MineSweeper:
    
    window = tk.Tk()
    ROWS = 5
    COLUMNS = 7

    def __init__(self):
        self.buttons = []
        for i in range(MineSweeper.ROWS):
            temp = []
            for j in range(MineSweeper.COLUMNS):
                btn = MyButton(MineSweeper.window, x=i, y=j)
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

    def print_buttons(self):
        for i in range(MineSweeper.ROWS):
            print(self.buttons[i])

game = MineSweeper()
game.print_buttons()
game.start()