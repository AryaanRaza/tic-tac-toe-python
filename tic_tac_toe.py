import streamlit as st

# Initialize Game State
if 'board' not in st.session_state:
    st.session_state.board = {i: " " for i in range(1, 10)}
    st.session_state.turn = "X"
    st.session_state.game_end = False
    st.session_state.mode = "single_player"

def check_for_win(player, board):
    win_conditions = [(1,2,3), (4,5,6), (7,8,9), (1,4,7), (2,5,8), (3,6,9), (1,5,9), (3,5,7)]
    return any(all(board[pos] == player for pos in combo) for combo in win_conditions)

def check_for_draw(board):
    return all(board[pos] != " " for pos in board)

def minimax(board_state, is_maximizing):
    if check_for_win("O", board_state): return 1
    if check_for_win("X", board_state): return -1
    if check_for_draw(board_state): return 0

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
    for key in st.session_state.board:
        if st.session_state.board[key] == " ":
            st.session_state.board[key] = "O"
            score = minimax(st.session_state.board, False)
            st.session_state.board[key] = " "
            if score > best_score:
                best_score = score
                best_move = key
    if best_move:
        st.session_state.board[best_move] = "O"

def handle_click(i):
    if st.session_state.board[i] == " " and not st.session_state.game_end:
        st.session_state.board[i] = st.session_state.turn
        
        if check_for_win(st.session_state.turn, st.session_state.board):
            st.session_state.game_end = True
        elif check_for_draw(st.session_state.board):
            st.session_state.game_end = True
        else:
            if st.session_state.mode == "single_player":
                play_computer()
                if check_for_win("O", st.session_state.board):
                    st.session_state.game_end = True
            else:
                st.session_state.turn = "O" if st.session_state.turn == "X" else "X"

# --- UI Setup ---
st.set_page_config(page_title="Tic Tac Toe AI", layout="centered")
st.title("🎮 Tic Tac Toe Game Board")

# Mode Selection
mode = st.radio("Select Game Mode:", ["Single Player", "Multiplayer"], horizontal=True)
st.session_state.mode = "single_player" if mode == "Single Player" else "multi_player"

# Grid UI
st.write("---")
board_container = st.container()
for r in range(3):
    cols = st.columns(3)
    for c in range(3):
        index = r * 3 + c + 1
        button_label = st.session_state.board[index]
        if cols[c].button(button_label if button_label != " " else " ", key=f"btn{index}", use_container_width=True):
            handle_click(index)
            st.rerun()

# Messages
if st.session_state.game_end:
    if check_for_win("X", st.session_state.board):
        st.success("🎉 X wins the game!")
    elif check_for_win("O", st.session_state.board):
        st.error("🤖 O (Computer) wins the game!")
    else:
        st.info("🤝 It's a Draw!")

if st.button("Restart Game", type="primary"):
    st.session_state.board = {i: " " for i in range(1, 10)}
    st.session_state.game_end = False
    st.session_state.turn = "X"
    st.rerun()
