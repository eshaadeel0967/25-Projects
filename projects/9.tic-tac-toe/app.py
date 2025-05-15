import streamlit as st
import numpy as np

def check_winner(board):
    # Check rows, columns, and diagonals for a winner
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != "":
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != "":
            return board[0][i]
    
    if board[0][0] == board[1][1] == board[2][2] != "":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != "":
        return board[0][2]
    
    return None

def is_board_full(board):
    return all(cell != "" for row in board for cell in row)

st.title("🎲 Tic-Tac-Toe Game")

# Initialize session state
if "board" not in st.session_state:
    st.session_state.board = [["" for _ in range(3)] for _ in range(3)]
    st.session_state.current_player = "X"
    st.session_state.winner = None

st.write(f"Current Player: {st.session_state.current_player}")

# Create the board UI
for row in range(3):
    cols = st.columns(3)
    for col in range(3):
        if cols[col].button(st.session_state.board[row][col] or " ", key=f"{row}-{col}"):
            if st.session_state.board[row][col] == "" and st.session_state.winner is None:
                st.session_state.board[row][col] = st.session_state.current_player
                winner = check_winner(st.session_state.board)
                if winner:
                    st.session_state.winner = winner
                    st.success(f"🎉 Player {winner} wins!")
                elif is_board_full(st.session_state.board):
                    st.session_state.winner = "Draw"
                    st.warning("🤝 It's a Draw!")
                else:
                    st.session_state.current_player = "O" if st.session_state.current_player == "X" else "X"

# Reset button
if st.button("🔄 Restart Game"):
    st.session_state.board = [["" for _ in range(3)] for _ in range(3)]
    st.session_state.current_player = "X"
    st.session_state.winner = None
st.write("🔹 Developed by Esha using Streamlit")
