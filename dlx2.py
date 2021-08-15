# global sudoku variables
DIGITS = 9
ROW_SIZE = DIGITS
COL_SIZE = DIGITS
BOX_ROW_SIZE = int(ROW_SIZE ** .5)
BOX_COL_SIZE = int(COL_SIZE ** .5)
CELL_COUNT = ROW_SIZE * COL_SIZE
CONSTRAINTS = 4

class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.up = self
        self.down = self
        self.right = self
        self.left = self
    
    def add_above(self, node):
        node.up = self.up
        node.down = self
        self.up.down = node
        self.up = node

    def add_below(self, node):
        node.down = self.down
        node.up = self
        self.down.up = node
        self.down = node

    def add_right(self, node):
        node.right = self.right
        node.left = self
        self.right.left = node
        self.right = node

    def add_left(self, node):
        node.left = self.left
        node.right = self
        self.left.right = node
        self.left = node

    def __repr__(self) -> str:
        return f'[{self.row}, {self.col}]'

class Column:
    def __init__(self, header):
        self.head = header
        self.tail = header
        self.right = self
        self.left = self
        self.size = 1

    def add(self, node):
        node.up = self.tail
        node.down = self.tail.down
        self.tail.down = node
        self.tail = node
        self.head.up = node
        self.size += 1

    def __repr__(self):
        string = ''
        current_node = self.head
        for i in range(self.size):
            string += str(current_node)
            current_node = current_node.down
        return string

class ColumnList:
    def __init__(self, head_col):
        self.head_col = head_col
        self.tail_col = head_col
        self.size = 1

    def add(self, col):
        col.right = self.tail_col.right
        col.left = self.tail_col
        self.tail_col.right = col
        self.tail_col = col
        self.head_col.left = col
        self.size += 1

    def __repr__(self):
        string = ''
        current_col = self.tail_col
    
        for i in range(self.size):
            string += str(current_col)
            string += '\n'
            current_col = current_col.left
        
        return string

# Class for a sudoku cover matrix 729 by 324
# Each row represents a choice (e.g. 4 in cell 9, 5 in cell 80, 9 in cell 32, etc.)
# Rows follow this order: cell 1 (guesses 1-9), cell 2 (guesses 1-9), etc.
# Columns are used to eliminate conflicting choices
# Columns 1-81 ensure that all other choices for a cell are eliminated after the first choice has been made
# Columns 82-162 ensure that a digit may only be guessed once per sudoku row
# Columns 163-243 ensure that a digit may only be guessed once per sudoku column
# Columns 244-324 ensure that a digit may only be guessed once per box
class Cover:
    def __init__(self, grid=[[0 for j in range(ROW_SIZE)] for i in range(COL_SIZE)]):
        # initializes empty matrix
        self.matrix = [[0 for j in range(CELL_COUNT * CONSTRAINTS)] for i in range(CELL_COUNT * DIGITS)]
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
            if grid[row_number][col_number] != 0:
                i = (cell_number * DIGITS) + grid[row_number][col_number] - 1

            # cell constraint gets placed in the corresponding column for the cell number 1-81
            cell_i = cell_number
            row[cell_i] = Node(i, cell_i)

            # row constraint gets placed in 9 by 9 diagonals that are offset by 9 times the row number (0 through 8)
            # the whole row constraint grid is offset by 81
            ROW_CONSTRAINT_OFFSET = 1 * CELL_COUNT
            row_i = ((row_number * DIGITS) + (i % DIGITS)) + ROW_CONSTRAINT_OFFSET
            row[row_i] = Node(i, row_i)
         
            # col constraint gets placed in 81 by 81 diagonals that repeat without an additional offset
            # the whole col constraint grid is offset by 162
            COL_CONSTRAINT_OFFSET = 2 * CELL_COUNT
            col_i = (i % (ROW_SIZE * DIGITS)) + COL_CONSTRAINT_OFFSET
            row[col_i] = Node(i, col_i)
          
            # box constraint gets placed in 9 by 9 diagonals that are offset by 9 times the box number (0 through 8)
            # the box constraint grid is offset by 243
            BOX_CONSTRAINT_OFFSET = 3 * CELL_COUNT
            box_i = ((box_number * BOX_COL_SIZE * BOX_ROW_SIZE) + (i % DIGITS)) + BOX_CONSTRAINT_OFFSET
            row[box_i] = Node(i, box_i)


#Tomfoolery below this line... beware!
#-----------------------------------------------------------------
sudoku = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
          [6, 0, 0, 1, 9, 5, 0, 0, 0],
          [0, 9, 8, 0, 0, 0, 0, 6, 0],
          [8, 0, 0, 0, 6, 0, 0, 0, 3],
          [4, 0, 0, 8, 0, 3, 0, 0, 1],
          [7, 0, 0, 0, 2, 0, 0, 0, 6],
          [0, 6, 0, 0, 0, 0, 2, 8, 0],
          [0, 0, 0, 4, 1, 9, 0, 0, 5],
          [0, 0, 0, 0, 8, 0, 0, 7, 9]]

cover = Cover(sudoku)

# create header column
head_col = Column(Node(-1, -1))
for i in range(81 * 9):
    head_col.add(Node(i, -1))

# create header row
col_list = ColumnList(head_col)
for i in range(81 * 4):
    new_col = Column(Node(-1, i))
    for j, row in enumerate(cover.matrix):
        if type(row[i]) is Node:
            new_col.add(row[i])
    col_list.add(new_col)

# list to cycle through columns in parallel started with all column heads
parallel_nodes = []
current_col = col_list.head_col
for i in range(col_list.size):
    parallel_nodes.append(current_col.head)
    current_col = current_col.right

# starts at -1 as headers have -1 as row/col
current_row = -1
def filter_function(i, el):
    # lists traverse only if the current node will be linked in the next chunk of code
    if el.row == current_row:
        parallel_nodes[i] = parallel_nodes[i].down
        return True

# loops through all rows
while current_row != 729:
    # list of nodes on the current row
    row_nodes = [node for i, node in enumerate(parallel_nodes) if filter_function(i, node)]

    # links each rows nodes
    for i, node in enumerate(row_nodes):
        if i != len(row_nodes) - 1:
            node.add_right(row_nodes[i + 1])

    current_row += 1

for i, row in enumerate(cover.matrix):
    if i < 9:
        print(row)