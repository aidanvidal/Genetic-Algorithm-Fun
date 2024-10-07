import numpy as np

BOARD_SIZE = 9  # 9x9 Sudoku

given_board = [0, 8, 9, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 9, 0, 4, 0,
               3, 5, 0, 0, 0, 0, 0, 0, 0,
               1, 0, 0, 9, 0, 0, 3, 8, 4,
               0, 2, 0, 0, 0, 4, 7, 9, 0,
               0, 0, 0, 0, 0, 0, 2, 0, 0, 
               0, 4, 7, 0, 3, 0, 5, 0, 0,
               0, 0, 0, 8, 0, 0, 0, 2, 0,
               0, 1, 0, 0, 0, 5, 8, 0, 0]
given_values = np.array(given_board).reshape(BOARD_SIZE, BOARD_SIZE)

# Check if a number can be placed in a cell
def is_valid(board, row, col, num):
    # Check row
    if num in board[row]:
        return False
    
    # Check column
    if num in board[:, col]:
        return False
    
    # Check 3x3 box
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    if num in board[box_row:box_row+3, box_col:box_col+3]:
        return False
    
    return True

# Finds the next empty cell in the board
def find_empty(board):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i, j] == 0:
                return i, j
    return None

# Solves the Sudoku board using backtracking
def solve_sudoku(board):
    # Find the next empty cell
    empty = find_empty(board)
    # If the board is full, return True
    if not empty:
        return True
    
    row, col = empty

    # Try placing numbers 1-9 in the empty cell
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row, col] = num
            
            if solve_sudoku(board):
                return True
            
            board[row, col] = 0
    
    return False

def main():
    board = given_values.copy()
    print("Original board:")
    print(board)
    print("\nSolving...\n")
    
    if solve_sudoku(board):
        print("Solved board:")
        print(board)
    else:
        print("No solution exists")

if __name__ == "__main__":
    main()