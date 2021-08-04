class Node:
    def __init__(self):
        self.up = None
        self.down = None
        self.left = None
        self.right = None
        self.coord = [None, None]
    
class Sudoku:
    def __init__(self, grid):
        self.grid = [[0 for j in range(9)] for i in range(9)]
        for i in range(9):
            for j in range(9):
                self.grid[i][j] = grid[i][j]

class Cover:
    def __init__(self):
        self.matrix = [[0 for j in range(81 * 4)] for i in range(9 * 81)]
        for i, row in enumerate(self.matrix):
            cell_number = int((i - (i % 9))/9)
            row_number = int((i - (i % 81))/81)
            col_number = int(cell_number % 9)
            box_number = int((row_number - (row_number % 3)) + ((col_number - (col_number % 3))/3))

            #cell
            row[cell_number] = 1
            #row
            row[((row_number * 9) + (i % 9)) + 81] = 1
            #col
            row[(i % 81) + 81 * 2] = 1
            #box
            row[((box_number * 9) + (i % 9)) + 81 * 3] = 1

cover = Cover()

# for i, row in enumerate(cover.matrix):

#     if i < 81:
#         print(row[:81])

# input()
# print('\n\n\n')

# for i, row in enumerate(cover.matrix):

#     if i < 81:
#         print(row[81:162])

# input()
# print('\n\n\n')

# for i, row in enumerate(cover.matrix):

#     if i < 81:
#         print(row[162:243])

# input()
# print('\n\n\n')

# for i, row in enumerate(cover.matrix):

#     if i < 81:
#         print(row[243:324])        