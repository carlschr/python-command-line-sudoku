class Node:
    def __init__(self, value=None):
        self.up = None
        self.down = None
        self.left = None
        self.right = None
        self.coord = [None, None]
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

class CircularDoublyLinkedList:
    def __init__(self, direction):
        self.central_node = None
        self.tail = None
        self.size = 0
        self.direction = direction
    
    def get_central_node(self):
        return self.central_node
    def get_tail(self):
        return self.tail

    def set_central_node(self, node):
        self.central_node = node
    def set_tail(self, node):
        self.tail = node

    def add_node(self, value):
        node = Node(value)
        if self.size == 0:
            self.set_central_node(node)
            self.set_tail(node)
            self.size = 1
            return node

        central_node = self.get_central_node()
        tail = self.get_tail()

        if self.direction:
            tail.set_down(node)
            node.set_down(central_node)
            node.set_up(tail)
            central_node.set_up(node)
            node.set_col(central_node.get_col())
        else:
            tail.set_right(node)
            node.set_right(central_node)
            node.set_left(tail)
            central_node.set_left(node)
            node.set_row(central_node.get_row())

        self.set_tail(node)
        self.size += 1
        return node
    
    def __repr__(self) -> str:
        string = ''
        central_node = self.get_central_node()

        if central_node:
            current_node = central_node.get_down() if self.direction else central_node.get_right()
            if current_node:
                while current_node is not central_node:
                    string += str(current_node.value)
                    string += '\n'
                    current_node = current_node.get_down() if self.direction else current_node.get_right()

        return string

h = CircularDoublyLinkedList(0)
h.add_node('h')
for i in range(81 * 4):
    h.add_node(i)

v = CircularDoublyLinkedList(1)
v.add_node('v')
for j in range(81 * 9):
    v.add_node(j)

print(v)


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