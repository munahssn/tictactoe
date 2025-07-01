import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random

CELL_SIZE = 64
GRID_SIZE = 3

state = {"player": "X", "mode": "Player"}

def start_game(mode):
    state["mode"] = mode
    mode_window.destroy()
    run_tic_tac_toe()

def run_tic_tac_toe():
    window = tk.Tk()
    window.title("Tic Tac Toe")

    canvas = tk.Canvas(window, width=CELL_SIZE*GRID_SIZE, height=CELL_SIZE*GRID_SIZE)
    canvas.pack()

    waffle_img = Image.open("waffle.png").resize((CELL_SIZE*GRID_SIZE, CELL_SIZE*GRID_SIZE), Image.NEAREST)
    waffle_tk = ImageTk.PhotoImage(waffle_img)
    strawberry_img = Image.open("strawberry.png").resize((CELL_SIZE, CELL_SIZE), Image.NEAREST)
    strawberry_tk = ImageTk.PhotoImage(strawberry_img)
    banana_img = Image.open("banana.png").resize((CELL_SIZE, CELL_SIZE), Image.NEAREST)
    banana_tk = ImageTk.PhotoImage(banana_img)

    canvas.create_image(0, 0, anchor='nw', image=waffle_tk)

    board = [[" "]*GRID_SIZE for _ in range(GRID_SIZE)]
    piece_images = {"X": strawberry_tk, "O": banana_tk}

    def check_winner():
        for i in range(GRID_SIZE):
            if board[i][0] == board[i][1] == board[i][2] != " ":
                return board[i][0]
            if board[0][i] == board[1][i] == board[2][i] != " ":
                return board[0][i]
        if board[0][0] == board[1][1] == board[2][2] != " ":
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] != " ":
            return board[0][2]
        return None

    def is_full():
        return all(board[i][j] != " " for i in range(GRID_SIZE) for j in range(GRID_SIZE))

    def ai_move():
        empty = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if board[i][j] == " "]
        if empty:
            move = random.choice(empty)
            i, j = move
            board[i][j] = state["player"]
            canvas.create_image(j*CELL_SIZE, i*CELL_SIZE, anchor='nw', image=piece_images[state["player"]])
            winner = check_winner()
            if winner or is_full():
                end_game(winner)
            else:
                state["player"] = "O" if state["player"] == "X" else "X"

    def click(event):
        j = event.x // CELL_SIZE
        i = event.y // CELL_SIZE
        if board[i][j] == " ":
            board[i][j] = state["player"]
            canvas.create_image(j*CELL_SIZE, i*CELL_SIZE, anchor='nw', image=piece_images[state["player"]])
            winner = check_winner()
            if winner or is_full():
                end_game(winner)
                return
            state["player"] = "O" if state["player"] == "X" else "X"
            if state["mode"] == "AI" and state["player"] == "O":
                window.after(300, ai_move)

    def end_game(winner):
        if winner:
            fruit = "Strawberry" if winner == "X" else "Banana"
            messagebox.showinfo("Game Over", f"{fruit} wins!")
        else:
            messagebox.showinfo("Game Over", "It's a tie!")
        window.quit()

    canvas.bind("<Button-1>", click)
    window.mainloop()

mode_window = tk.Tk()
mode_window.title("Choose Game Mode")
mode_window.geometry("250x150")
label = tk.Label(mode_window, text="Select Game Mode:", font=("System", 14))
label.pack(pady=10)

ai_btn = tk.Button(mode_window, text="AI", font=("System", 12), width=10, command=lambda: start_game("AI"))
ai_btn.pack(pady=5)

pvp_btn = tk.Button(mode_window, text="PvP", font=("System", 12), width=10, command=lambda: start_game("Player"))
pvp_btn.pack(pady=5)

mode_window.mainloop()