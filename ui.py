import tkinter as tk
import numpy as np

class TicTackToeGui:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Tic Tac T-ai')
        
        self._frame = tk.Frame(self.root)
        self._frame.pack(padx=16, pady=16)

        self._board_frame = tk.Frame(self._frame, bg='black')
        self._board_frame.pack()

        self.labels = np.full((3, 3), None)
        self.winner_label = tk.Label(self.root, text='', font=('normal', 20))
        self.winner_label.pack(pady=16)
    # endinit

    def draw_board(self, callback):
        for i in range(3):
            for j in range(3):
                label_frame = tk.Frame(self._board_frame, bg='black')
                label_frame.grid(row=i, column=j, padx=1, pady=1)
                
                label = tk.Label(label_frame, text='', font=('normal', 20), height=2, width=5, bg='lightgrey')
                label.grid(row=0, column=0)
                
                self.labels[i][j] = label

                label.bind('<Button-1>', lambda _, row=i, col=j: callback(row, col))
            # endfor
        # endfor
    # endmethod
# endclass