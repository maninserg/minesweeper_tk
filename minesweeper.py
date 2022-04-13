from cProfile import label
import tkinter as tk
from random import shuffle
from tkinter.messagebox import showinfo, showerror

colors = {
    1: 'blue',
    2: '#008200',
    3: '#FF0000',
    4: '#000084',
    5: '#840000',
    6: '#008284',
    7: '#840084',
    8: '#000000'
}

class MyButton(tk.Button):

    def __init__(self, master, x, y, number=0, *args, **kwargs):
        super(MyButton, self).__init__(master, width=1, font='Calibri 20 bold', *args, **kwargs)
        self.x = x
        self.y = y
        self.number = number
        self.is_mine = False
        self.count_bombs = 0
        self.is_open = False

    def __repr__(self):
        return f'MyButton[{self.x}]-[{self.y}]#{self.number}%{self.is_mine}'


class MineSweeper:
    
    window = tk.Tk()
    ROWS = 8
    COLUMNS = 8
    MINES = 15 
    IS_GAME_OVER = False
    IS_FIRST_CLICK = True 

    def __init__(self):
        self.buttons = []
        for i in range(MineSweeper.ROWS+2):
            temp = []
            for j in range(MineSweeper.COLUMNS+2):
                btn = MyButton(MineSweeper.window, x=i, y=j)
                btn.config(command=lambda button=btn: self.click(button))
                temp.append(btn)
            self.buttons.append(temp)

    def click(self, clicked_button:MyButton):
        if MineSweeper.IS_GAME_OVER:
            return None
        if MineSweeper.IS_FIRST_CLICK:
            self.insert_mines(clicked_button.number)
            self.count_mines_in_buttons()
            self.print_buttons()
            MineSweeper.IS_FIRST_CLICK = False

        if clicked_button.is_mine:
            clicked_button.config(text="*", background='red', disabledforeground='black')
            clicked_button.is_open = True
            MineSweeper.IS_GAME_OVER = True
            showinfo('Game Over', 'You didnt win')
            for i in range(1, MineSweeper.ROWS + 1):
                for j in range(1, MineSweeper.COLUMNS + 1):
                    btn = self.buttons[i][j]
                    if btn.is_mine:
                        btn['text'] = '*'
        else:
            color = colors.get(clicked_button.count_bombs, 'black')
            if clicked_button.count_bombs:
                clicked_button.config(text=clicked_button.count_bombs, disabledforeground=color)
                clicked_button.is_open = True
            else:
                self.breadth_first_search(clicked_button)
        clicked_button.config(state='disable')
        clicked_button.config(relief=tk.SUNKEN)

    def breadth_first_search(self, btn:MyButton):
        queue = [btn]
        while queue:
            cur_btn = queue.pop()
            color = colors.get(cur_btn.count_bombs, 'black')
            if cur_btn.count_bombs:
                cur_btn.config(text=cur_btn.count_bombs, disabledforeground=color)
            else:
                cur_btn.config(text='', disabledforeground=color)
            cur_btn.is_open = True
            cur_btn.config(state='disable')
            cur_btn.config(relief=tk.SUNKEN)

            if cur_btn.count_bombs == 0:
                x, y = cur_btn.x, cur_btn.y
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        #if not abs(dx-dy) == 1:
                        #    continue
                        next_btn = self.buttons[x + dx][y + dy]
                        if not next_btn.is_open and 1 <= next_btn.x <= MineSweeper.ROWS and \
                            1 <= next_btn.y <= MineSweeper.COLUMNS and next_btn not in queue:
                            queue.append(next_btn)
                        
    def reload(self):
        [child.destroy() for child in self.window.winfo_children()]
        self.__init__()
        self.create_widgets()
        MineSweeper.IS_FIRST_CLICK = True
        MineSweeper.IS_GAME_OVER = False 

    def create_settings_window(self):
        win_settings = tk.Toplevel(self.window)
        win_settings.wm_title('Settings')
        tk.Label(win_settings, text='Count rows').grid(row=0, column=0)
        rows_entry = tk.Entry(win_settings)
        rows_entry.insert(0, MineSweeper.ROWS)
        rows_entry.grid(row=0, column=1, padx=20, pady=20)
        tk.Label(win_settings, text='Count columns').grid(row=1, column=0)
        columns_entry = tk.Entry(win_settings)
        columns_entry.insert(0, MineSweeper.COLUMNS)
        columns_entry.grid(row=1, column=1, padx=20, pady=20)
        tk.Label(win_settings, text='Count mines').grid(row=2, column=0)
        mines_entry = tk.Entry(win_settings)
        mines_entry.insert(0, MineSweeper.MINES)
        mines_entry.grid(row=2, column=1, padx=20, pady=20)

        save_btn = tk.Button(win_settings, text='Save',
                             command=lambda :self.change_settings(rows_entry, columns_entry, mines_entry))
        save_btn.grid(row=3, column=0, columnspan=2, pady=10)
        

    def change_settings(self, row: tk.Entry, column: tk.Entry, mines: tk.Entry):
        try:
            int(row.get()), int(column.get()), int(mines.get())
        except ValueError:
            showerror('Error', 'You had entered the wrong value')
            return 
        MineSweeper.ROWS = int(row.get())
        MineSweeper.COLUMNS = int(column.get())
        MineSweeper.MINES = int(mines.get())
        self.reload()

    def create_widgets(self):
        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)
        setting_menu = tk.Menu(menubar, tearoff=0)
        setting_menu.add_command(label='Play', command=self.reload)
        setting_menu.add_command(label='Settings', command=self.create_settings_window)
        setting_menu.add_command(label='Exit', command=self.window.destroy)
        menubar.add_cascade(label='File', menu=setting_menu)
        count = 1
        for i in range(1, MineSweeper.ROWS+1):
            for j in range(1, MineSweeper.COLUMNS+1):
                btn = self.buttons[i][j]
                btn.number = count
                btn.grid(row=i, column=j, stick='nwse')
                count += 1
        for i in range(1, MineSweeper.ROWS+1):
            tk.Grid.rowconfigure(self.window, i, weight=1)
        for i in range(1, MineSweeper.COLUMNS+1):
            tk.Grid.columnconfigure(self.window, i, weight=1)

    def open_all_buttons(self):
        for i in range(MineSweeper.ROWS+2):
            for j in range(MineSweeper.COLUMNS+2):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    btn.config(text='*', background='red', disabledforeground='black')
                elif btn.count_bombs in colors:
                    color = colors.get(btn.count_bombs, 'black')
                    btn.config(text=btn.count_bombs, fg=color)

    def start(self):
        self.create_widgets()
        # self.open_all_buttons()
        MineSweeper.window.mainloop()

    def print_buttons(self):
        for i in range(1, MineSweeper.ROWS+1):
            for j in range(1, MineSweeper.COLUMNS+1):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    print('B', end='')
                else:
                    print(btn.count_bombs, end='')
            print('')
    
    def insert_mines(self, number:int):
        index_mines = self.get_mines_places(number)
        print(index_mines)
        for i in range(1, MineSweeper.ROWS+1):
            for j in range(1, MineSweeper.COLUMNS+1):
                btn = self.buttons[i][j]
                if btn.number in index_mines:
                    btn.is_mine = True
    
    def count_mines_in_buttons(self):
        for i in range(1, MineSweeper.ROWS+1):
            for j in range(1, MineSweeper.COLUMNS+1):
                btn = self.buttons[i][j]
                count_bombs = 0
                if not btn.is_mine:
                    for row_dx in [-1, 0, 1]:
                        for col_dx in [-1, 0, 1]:
                            neighbour_btn = self.buttons[i+row_dx][j+col_dx]
                            if neighbour_btn.is_mine:
                                count_bombs += 1
                btn.count_bombs = count_bombs

    @staticmethod
    def get_mines_places(exclude_number:int):
        indexes = list(range(1, MineSweeper.COLUMNS * MineSweeper.ROWS + 1))
        indexes.remove(exclude_number)
        shuffle(indexes)
        return indexes[:MineSweeper.MINES]

game = MineSweeper()
game.start()