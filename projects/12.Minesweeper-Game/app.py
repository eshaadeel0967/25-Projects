import streamlit as st
import numpy as np
import random

# Board size
ROWS, COLS = 8, 8  
MINES = 10  

# Generate Minesweeper board
def create_board(rows, cols, mines):
    board = np.zeros((rows, cols), dtype=int)
    mine_positions = random.sample(range(rows * cols), mines)
    
    for pos in mine_positions:
        r, c = divmod(pos, cols)
        board[r][c] = -1  # -1 represents a mine
    
    # Fill board with numbers indicating adjacent mines
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == -1:
                continue
            count = sum((board[r+dr][c+dc] == -1) for dr, dc in 
                        [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
                        if 0 <= r+dr < rows and 0 <= c+dc < cols)
            board[r][c] = count
    return board

# Streamlit UI
st.title("💣 Minesweeper Game")

# Session state for game state
if "board" not in st.session_state:
    st.session_state.board = create_board(ROWS, COLS, MINES)
    st.session_state.revealed = np.full((ROWS, COLS), False)

# Display the board
def display_board():
    for r in range(ROWS):
        cols = st.columns(COLS)
        for c in range(COLS):
            if st.session_state.revealed[r][c]:
                if st.session_state.board[r][c] == -1:
                    cols[c].button("💥", key=f"{r}-{c}", disabled=True)  # Mine
                else:
                    cols[c].button(str(st.session_state.board[r][c]), key=f"{r}-{c}", disabled=True)
            else:
                if cols[c].button("⬜", key=f"{r}-{c}"):
                    reveal_cell(r, c)

# Reveal cells function
def reveal_cell(r, c):
    if st.session_state.board[r][c] == -1:
        st.error("Game Over! 💀")
        st.session_state.revealed[:, :] = True  # Reveal all cells
    else:
        st.session_state.revealed[r][c] = True
        if st.session_state.board[r][c] == 0:
            for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < ROWS and 0 <= nc < COLS and not st.session_state.revealed[nr][nc]:
                    reveal_cell(nr, nc)

# Display the board
display_board()

# Restart button
if st.button("🔄 Restart Game"):
    st.session_state.board = create_board(ROWS, COLS, MINES)
    st.session_state.revealed = np.full((ROWS, COLS), False)
    st.experimental_rerun()


st.write("💻 Minesweeper Game - A classic puzzle game where you clear a minefield without detonating any mines.")
st.write("🔹 Developed by Esha using Streamlit")