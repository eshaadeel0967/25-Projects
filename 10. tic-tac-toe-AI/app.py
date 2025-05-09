import streamlit as st
import numpy as np

# Tic-Tac-Toe board initialization
empty_board = [[' ' for _ in range(3)] for _ in range(3)]

# Function to check for a winner
def check_winner(board):
    for row in board:
        if row[0] == row[1] == row[2] != ' ':
            return row[0]
    
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != ' ':
            return board[0][col]
    
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return board[0][2]
    
    return None

# Function to check if the board is full
def is_draw(board):
    return all(board[row][col] != ' ' for row in range(3) for col in range(3))

# Minimax algorithm for AI player
def minimax(board, depth, is_maximizing):
    winner = check_winner(board)
    if winner == 'O':
        return 10 - depth
    elif winner == 'X':
        return depth - 10
    elif is_draw(board):
        return 0
    
    if is_maximizing:
        best_score = -np.inf
        for row in range(3):
            for col in range(3):
                if board[row][col] == ' ':
                    board[row][col] = 'O'
                    score = minimax(board, depth + 1, False)
                    board[row][col] = ' '
                    best_score = max(best_score, score)
        return best_score
    else:
        best_score = np.inf
        for row in range(3):
            for col in range(3):
                if board[row][col] == ' ':
                    board[row][col] = 'X'
                    score = minimax(board, depth + 1, True)
                    board[row][col] = ' '
                    best_score = min(best_score, score)
        return best_score

# AI Move function
def best_move(board):
    best_score = -np.inf
    move = None
    for row in range(3):
        for col in range(3):
            if board[row][col] == ' ':
                board[row][col] = 'O'
                score = minimax(board, 0, False)
                board[row][col] = ' '
                if score > best_score:
                    best_score = score
                    move = (row, col)
    return move

# Streamlit UI
st.title("🤖 Tic-Tac-Toe AI")

if 'board' not in st.session_state:
    st.session_state.board = [[' ' for _ in range(3)] for _ in range(3)]
    st.session_state.turn = 'X'
    st.session_state.game_over = False

st.write("### Current Board")
for row in range(3):
    cols = st.columns(3)
    for col in range(3):
        if st.session_state.board[row][col] == ' ' and not st.session_state.game_over:
            if cols[col].button(" ", key=f"{row}-{col}"):
                st.session_state.board[row][col] = 'X'
                winner = check_winner(st.session_state.board)
                if winner:
                    st.session_state.game_over = True
                elif is_draw(st.session_state.board):
                    st.session_state.game_over = True
                else:
                    ai_move = best_move(st.session_state.board)
                    if ai_move:
                        st.session_state.board[ai_move[0]][ai_move[1]] = 'O'
                        winner = check_winner(st.session_state.board)
                        if winner:
                            st.session_state.game_over = True
                        elif is_draw(st.session_state.board):
                            st.session_state.game_over = True

for row in st.session_state.board:
    st.write('|'.join(row))
    st.write("---")

if st.session_state.game_over:
    winner = check_winner(st.session_state.board)
    if winner:
        st.success(f"🎉 Player {winner} wins!")
    else:
        st.warning("😲 It's a draw!")

if st.button("🔄 Restart Game"):
    st.session_state.board = [[' ' for _ in range(3)] for _ in range(3)]
    st.session_state.turn = 'X'
    st.session_state.game_over = False

st.write("💻 AI-Powered Tic-Tac-Toe Game")
st.write("🔹 Developed by Esha")