from Node import Node
from Sudoku import Sudoku

class Cover:
    def __init__(self, sudoku_string):
        sudoku = Sudoku(sudoku_string)
        CELL_COUNT = sudoku.size ** 2
        CONSTRAINTS = 4
        DIGITS = ROW_SIZE = COL_SIZE = sudoku.size
        BOX_COL_SIZE = BOX_ROW_SIZE = int(sudoku.size ** .5)

        # initializes empty matrix
        self.matrix = [[0 for _ in range(CELL_COUNT * CONSTRAINTS)] for _ in range(CELL_COUNT * DIGITS)]
        # loops through rows to assign constraints
        for index, row in enumerate(self.matrix):
            i = index
            # cells change every 9 rows
            cell_number = int(i//DIGITS)
            # sudoku rows change every 81 rows
            row_number = int(i//(DIGITS * ROW_SIZE))
            # sudoku columns change for every cell and reset every 9 cells
            col_number = cell_number % COL_SIZE
            # sudoku boxes are calculated by taking the lower row of the box (0,3, or 6) plus the column grouping (1,2, or 3)
            # result is one of nine boxes (0 through 8)
            box_number = int(row_number - (row_number % BOX_COL_SIZE) + col_number//BOX_ROW_SIZE)

            # if the sudoku cell is given, the 9 rows for the cell will all be the same
            # this ensures that the given cells will be part of the solution
            if sudoku.grid[row_number][col_number] != 0:
                i = (cell_number * DIGITS) + sudoku.grid[row_number][col_number] - 1

            # cell constraint gets placed in the corresponding column for the cell number 1-81
            cell_i = cell_number
            cell_node = Node(index, cell_i)
            row[cell_i] = cell_node

            # row constraint gets placed in 9 by 9 diagonals that are offset by 9 times the row number (0 through 8)
            # the whole row constraint grid is offset by 81
            ROW_CONSTRAINT_OFFSET = 1 * CELL_COUNT
            row_i = ((row_number * DIGITS) + (i % DIGITS)) + ROW_CONSTRAINT_OFFSET
            row_node = Node(index, row_i)
            row[row_i] = row_node
         
            # col constraint gets placed in 81 by 81 diagonals that repeat without an additional offset
            # the whole col constraint grid is offset by 162
            COL_CONSTRAINT_OFFSET = 2 * CELL_COUNT
            col_i = (i % (ROW_SIZE * DIGITS)) + COL_CONSTRAINT_OFFSET
            col_node = Node(index, col_i)
            row[col_i] = col_node
          
            # box constraint gets placed in 9 by 9 diagonals that are offset by 9 times the box number (0 through 8)
            # the box constraint grid is offset by 243
            BOX_CONSTRAINT_OFFSET = 3 * CELL_COUNT
            box_i = ((box_number * BOX_COL_SIZE * BOX_ROW_SIZE) + (i % DIGITS)) + BOX_CONSTRAINT_OFFSET
            box_node = Node(index, box_i)
            row[box_i] = box_node

            head_node = Node(index, -1)
            head_node.add_right(cell_node)
            cell_node.add_right(row_node)
            row_node.add_right(col_node)
            col_node.add_right(box_node)
            # print(f'{head_node.right}, {head_node.right.right}, {head_node.right.right.right}, {head_node.right.right.right.right}, {head_node.right.right.right.right.right}')

    def __repr__(self):
        r = ''
        for i in range(len(self.matrix)):
            row = ''
            for j in range(len(self.matrix[0])):
                current =  self.matrix[i][j]
                if current != 0:
                    row += str(current)
            r += f'\n{row}'
        return r

if __name__ == '__main__':
    test_cover = Cover('530070000600195000098000060800060003400803001700020006060000280000419005000080079')
    print(f'Test Cover Matrix: {test_cover}')