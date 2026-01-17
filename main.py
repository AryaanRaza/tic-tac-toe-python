import tkinter as tk

# Main window setup
root = tk.Tk()
root.geometry("420x621")
root.title("Tic Tac Toe")
root.configure(bg="#E6E6FA")
root.resizable(False, False)

# Frames
frame1 = tk.Frame(root)
frame1.grid()

title_label = tk.Label(frame1, text="Tic Tac Toe game board", font=("Algerian", 22, "bold"), bg="#E6E6FA", fg="black", padx=4)
title_label.grid(row=0, column=0)

option_frame = tk.Frame(root, bg="grey")
option_frame.grid()

frame2 = tk.Frame(root, bg="#2F4F4F")
frame2.grid()

# Board state dictionary: keys are positions 1-9, values are " ", "X", or "O"
board = {i: " " for i in range(1, 10)}

turn = "X"
game_end = False
msg_label = None
mode = "single_player"

def change_mode_to_single_player():
    global mode
    mode = "single_player"
    single_player_button["bg"] = "#CD5C5C"
    multi_player_button["bg"] = "#F5F5DC"

def change_mode_to_multi_player():
    global mode
    mode = "multi_player"
    multi_player_button["bg"] = "#CD5C5C"
    single_player_button["bg"] = "#F5F5DC"

def check_for_win(player):
    win_conditions = [
        (1, 2, 3),
        (4, 5, 6),
        (7, 8, 9),
        (1, 4, 7),
        (2, 5, 8),
        (3, 6, 9),
        (1, 5, 9),
        (3, 5, 7)
    ]
    return any(all(board[pos] == player for pos in combo) for combo in win_conditions)

def check_for_draw():
    return all(board[pos] != " " for pos in board)

def restart_game():
    global game_end, turn, msg_label
    turn = "X"
    game_end = False
    for button in buttons:
        button["text"] = " "
    for key in board:
        board[key] = " "
    if msg_label is not None:
        msg_label.destroy()
        msg_label = None

def minimax(board_state, is_maximizing):
    if check_for_win("O"):
        return 1
    if check_for_win("X"):
        return -1
    if check_for_draw():
        return 0

    if is_maximizing:
        best_score = float('-inf')
        for key in board_state:
            if board_state[key] == " ":
                board_state[key] = "O"
                score = minimax(board_state, False)
                board_state[key] = " "
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for key in board_state:
            if board_state[key] == " ":
                board_state[key] = "X"
                score = minimax(board_state, True)
                board_state[key] = " "
                best_score = min(score, best_score)
        return best_score

def play_computer():
    best_score = float('-inf')
    best_move = None
    for key in board:
        if board[key] == " ":
            board[key] = "O"
            score = minimax(board, False)
            board[key] = " "
            if score > best_score:
                best_score = score
                best_move = key
    if best_move is not None:
        board[best_move] = "O"
        buttons[best_move - 1]["text"] = "O"

def play(event):
    global turn, game_end, msg_label
    if game_end:
        return
    button = event.widget
    clicked = buttons.index(button) + 1

    if button["text"] == " ":
        board[clicked] = turn
        button["text"] = turn

        if check_for_win(turn):
            msg_label = tk.Label(frame2, text=f"{turn} wins the game", font=("Comic Sans MS", 25), bg="#00008B", fg="#FFFF00", padx=4, pady=15, width=18)
            msg_label.grid(row=2, column=0, columnspan=3)
            game_end = True
        elif check_for_draw():
            msg_label = tk.Label(frame2, text="Game Draw", bg="#DC143C", fg="gold", font=("Comic Sans MS", 26), width=18, padx=4, pady=15)
            msg_label.grid(row=2, column=0, columnspan=3)
            game_end = True
        else:
            turn = "O" if turn == "X" else "X"
            if turn == "O" and mode == "single_player":
                play_computer()
                if check_for_win(turn):
                    msg_label = tk.Label(frame2, text=f"{turn} wins the game", font=("Comic Sans MS", 26), bg="#4B0082", fg="#FFD700", width=18, padx=4, pady=15)
                    msg_label.grid(row=2, column=0, columnspan=3)
                    game_end = True
                turn = "X"

# Mode Buttons
single_player_button = tk.Button(option_frame, text="SinglePlayer", width=13, height=1, font=("Arial", 15),
                                 bg="#F5F5DC", relief=tk.RAISED, borderwidth=5, command=change_mode_to_single_player)
single_player_button.grid(row=0, column=0, sticky=tk.NW)

multi_player_button = tk.Button(option_frame, text="Multiplayer", width=13, height=1, font=("Arial", 15),
                                bg="#F5F5DC", relief=tk.RAISED, borderwidth=5, command=change_mode_to_multi_player)
multi_player_button.grid(row=0, column=1, sticky=tk.NW)

# Tic Tac Toe Board Buttons
buttons = []
for r in range(1, 4):
    for c in range(3):
        btn = tk.Button(frame2, text=" ", width=4, height=2, font=("Cooper Black", 30), bg="#AFEEEE",
                        fg="#191970", relief=tk.GROOVE, borderwidth=8)
        btn.grid(row=r, column=c, padx=5, pady=5)
        btn.bind("<Button-1>", play)
        buttons.append(btn)

# Restart and Quit buttons
restart_button = tk.Button(frame2, text="Restart Game", width=10, height=3, font=("Helvetica", 10, "bold"),
                           bg="#32CD32", fg="black", relief=tk.RAISED, borderwidth=20, command=restart_game)
restart_button.grid(row=6, column=0)

quit_button = tk.Button(frame2, text="Quit Game", width=10, height=3, font=("Helvetica", 10, "bold"),
                        bg="#DC143C", fg="black", relief=tk.RAISED, borderwidth=20, command=root.destroy)
quit_button.grid(row=6, column=2)

root.mainloop()
