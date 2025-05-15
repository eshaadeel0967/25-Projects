import streamlit as st
import numpy as np

# Sudoku board size
SIZE = 9

# Function to check if a number is valid in a given position
def is_valid(board, row, col, num):
    for i in range(SIZE):
        if board[row][i] == num or board[i][col] == num:
            return False
    
    start_row, start_col = (row // 3) * 3, (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
                
    return True

# Backtracking function to solve Sudoku
def solve_sudoku(board):
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True

# Streamlit UI
st.title("🧩 Sudoku Solver")

# Sudoku grid input
st.write("Enter the Sudoku puzzle (use 0 for empty cells):")
grid = np.zeros((SIZE, SIZE), dtype=int)

for i in range(SIZE):
    cols = st.columns(SIZE)
    for j in range(SIZE):
        grid[i][j] = int(cols[j].text_input(f"Cell {i+1},{j+1}", "0"))

# Solve button
if st.button("Solve Sudoku"):
    if solve_sudoku(grid):
        st.success("🎉 Solution Found!")
        for i in range(SIZE):
            cols = st.columns(SIZE)
            for j in range(SIZE):
                cols[j].text(str(grid[i][j]))
    else:
        st.error("❌ No solution exists for this Sudoku.")

# Reset button
if st.button("🔄 Reset Grid"):
    st.experimental_rerun()

st.write("📌 Sudoku Solver using Backtracking Algorithm")
st.write("🔹 Developed by Esha using Streamlit")