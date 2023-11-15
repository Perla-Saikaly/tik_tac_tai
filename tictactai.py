import sys
import os
import tkinter as tk

import problem

def resource_path(relative_path: str) -> str:
    try:
        base_path = sys._MEIPASS2
    # endtry
    except:
        base_path = os.path.abspath('.')
    # endcatch

    return os.path.join(base_path, relative_path)
# endfunc

resource_path('tictactai.png')

def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius, color, border_color, border_width):
    canvas.create_polygon(
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1,
        x1 + radius, y1,
        outline=border_color,
        fill=color,
        width=border_width
    )
# endfunc


def select_difficulty():
    def play_game():
        root.destroy()
        game = problem.TicTacToeProblem(depth_limit.get())
        game.gui.root.mainloop()    
    # endfunc
    root = tk.Tk()
    root.title("Difficulty")
    root.geometry("210x170")  # Set window size

    depth_limit = tk.IntVar()
    depth_limit.set(5)

    label = tk.Label(root, text="       Choose difficulty:", font=("Arial", 13, "bold"))
    label.grid(row=0, column=0, columnspan=3)  # Adjust label position

    radio_easy = tk.Radiobutton(root, text="Easy", variable=depth_limit, value=1, font=("Arial", 12, "bold"), fg="blue")
    radio_easy.grid(row=1, column=0, sticky='w')  # Place radio button on the grid

    radio_medium = tk.Radiobutton(root, text="Medium", variable=depth_limit, value=2, font=("Arial", 12, "bold"))
    radio_medium.grid(row=2, column=0, sticky='w')  # Place radio button on the grid

    radio_hard = tk.Radiobutton(root, text="HAL 9000", variable=depth_limit, value=5, font=("Arial", 12, "bold"), fg="red")
    radio_hard.grid(row=3, column=0, sticky='w')  # Place radio button on the grid

    canvas = tk.Canvas(root, width=120, height=40)
    canvas.grid(row=4, column=0, columnspan=3, pady=10,padx=32)  # Adjust canvas position and size

    # Get the center coordinates of the canvas
    canvas_center_x = canvas.winfo_reqwidth() / 2
    canvas_center_y = canvas.winfo_reqheight() / 2

    # Calculate the button dimensions and position to center it
    button_width = 110
    button_height = 30
    button_x1 = canvas_center_x - (button_width / 2)
    button_y1 = canvas_center_y - (button_height / 2)
    button_x2 = canvas_center_x + (button_width / 2)
    button_y2 = canvas_center_y + (button_height / 2)

    # Create the rounded rectangle button on the canvas
    create_rounded_rectangle(canvas, button_x1, button_y1, button_x2, button_y2, 10, "lightgrey", "black", 2)
    canvas.create_text(canvas_center_x, canvas_center_y, text="Play", font=("Arial", 10, "bold"), fill="black")

    canvas.bind("<Button-1>", lambda event: play_game())

    root.mainloop()
# endfunc

if __name__ == '__main__':
    select_difficulty()

    play_again = True
    while play_again:
        msg_box_root = tk.Tk()
        msg_box_root.title('Tic Tac T-ai')

        prompt = tk.Label(
            msg_box_root,
            text='Would you like to play again?',
            font=('normal', 16)
        )
        prompt.pack(padx=4, pady=8)

        def on_yes_click():
            global play_again
            play_again = True
            msg_box_root.destroy()
        # endfunc

        def on_no_click():
            global play_again
            play_again = False
            msg_box_root.destroy()
        # endfunc

        yes_button = tk.Button(msg_box_root, text='Yes', font=('normal', 12), command=on_yes_click)
        yes_button.pack(side=tk.RIGHT, padx=4, pady=4)

        no_button = tk.Button(msg_box_root, text='No', font=('normal', 12), command=on_no_click)
        no_button.pack(side=tk.RIGHT, padx=8, pady=4)

        msg_box_root.protocol("WM_DELETE_WINDOW", on_no_click)

        msg_box_root.mainloop()

        if play_again:
            select_difficulty()
        # endif
    # endwhile
# endmain