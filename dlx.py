class Node:
    def __init__(self, value=None, coord=None):
        self.up = None
        self.down = None
        self.left = None
        self.right = None
        self.coord = coord
        self.value = value
    
    def set_right(self, node):
        self.right = node
    def set_left(self, node):
        self.left = node
    def set_up(self, node):
        self.up = node
    def set_down(self, node):
        self.down = node

    def get_right(self):
        return self.right
    def get_left(self):
        return self.left
    def get_up(self):
        return self.up
    def get_down(self):
        return self.down
    
    def set_row(self, row):
        self.coord[0] = row
    def set_col(self, col):
        self.coord[1] = col

    def get_row(self):
        return self.coord[0]
    def get_col(self):
        return self.coord[1]

class TwoDimensionalLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    

def create_rows_cols(head_node):
    # creates columns
    current_node = head_node
    for i in range(81*4):
        temp = Node(i)
        current_node.set_right(temp)
        temp.set_left(current_node)
        current_node = temp
        if i == 323:
            temp.set_right(head_node)
            head_node.set_left(temp)
    
    # creates rows
    current_node = head_node
    for i in range(81*9):
        temp = Node(i)
        current_node.set_down(temp)
        temp.set_up(current_node)
        current_node = temp
        if i == 728:
            temp.set_down(head_node)
            head_node.set_up(temp)

def index_to_coord(i, row_len):
    row = (i - (i % row_len))/row_len
    col = i % row_len
    return [row, col]

def coord_to_index(row, col, row_len):
    return int(row * row_len + col)


            
class Sudoku:
    def __init__(self, grid):
        self.grid = [[0 for j in range(9)] for i in range(9)]
        for i in range(9):
            for j in range(9):
                self.grid[i][j] = grid[i][j]

class Cover:
    def __init__(self):
        self.matrix = [[Node(0, [i, j]) for j in range(81 * 4)] for i in range(9 * 81)]
        self.head = self.matrix[0][0]
        for i, row in enumerate(self.matrix):
            cell_number = int((i - (i % 9))/9)
            row_number = int((i - (i % 81))/81)
            col_number = int(cell_number % 9)
            box_number = int((row_number - (row_number % 3)) + ((col_number - (col_number % 3))/3))

            #cell
            cell_i = cell_number
            row[cell_i].value = 1
            self.connect_one_above(i, cell_i)
            self.connect_one_left(i, cell_i)

            #row
            row_i = ((row_number * 9) + (i % 9)) + 81
            row[row_i].value = 1
            self.connect_one_above(i, row_i)
            self.connect_one_left(i, row_i)

            #col
            col_i = (i % 81) + 81 * 2
            row[col_i].value = 1
            self.connect_one_above(i, col_i)
            self.connect_one_left(i, col_i)

            #box
            box_i = ((box_number * 9) + (i % 9)) + 81 * 3
            row[box_i].value = 1
            self.connect_one_above(i, box_i)
            self.connect_one_left(i, box_i)

    def connect_one_above(self, i, j):
        n = i - 1
        while n > 0:
            if self.matrix[n][j].value:
                current = self.matrix[i][j]
                found = self.matrix[n][j]
                current.up = found
                found.down = current
                return found.value
            n += 1
        return 0

    def connect_one_left(self, i, j):
        n = j - 1
        while n > 0:
            if self.matrix[i][n].value:
                current = self.matrix[i][j]
                found = self.matrix[i][n]
                current.left = found
                found.right = current
                return found.value
            n += 1
        return 0

cover = Cover()

my_arr = cover.matrix
