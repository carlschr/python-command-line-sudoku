

class Node:
    def __init__(self, value, row, col):
        self.value = value
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

    def add_below(self, node):
        node.down = self.down
        node.up = self
        self.down.up = node

    def add_right(self, node):
        node.right = self.right
        node.left = self
        self.right.left = node

    def add_left(self, node):
        node.left = self.left
        node.right = self
        self.left.right = node

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
        self.size += 1

    def __repr__(self):
        string = ''
        current_col = self.tail_col
    
        for i in range(self.size):
            string += str(current_col)
            string += '\n'
            current_col = current_col.left
        
        return string

# head_col = Column(Node('h', 0, 0))
# for i in range(1, 10):
#     head_col.add(Node(i, i, 0))

# col_list = ColumnList(head_col)
# for i in range(1, 10):
#     new_col = Column(Node(i, 0, i))
#     for j in range(1, 10):
#         new_col.add(Node(0, j, i))
#     col_list.add(new_col)

# print(col_list)

class Cover:
    def __init__(self):
        self.matrix = [[0 for j in range(81 * 4)] for i in range(9 * 81)]
        self.head = self.matrix[0][0]
        for i, row in enumerate(self.matrix):
            cell_number = int((i - (i % 9))/9)
            row_number = int((i - (i % 81))/81)
            col_number = int(cell_number % 9)
            box_number = int((row_number - (row_number % 3)) + ((col_number - (col_number % 3))/3))

            #cell
            cell_i = cell_number
            row[cell_i] = Node(1, i, cell_i)
            
            #row
            row_i = ((row_number * 9) + (i % 9)) + 81
            row[row_i] = Node(1, i, row_i)
         
            #col
            col_i = (i % 81) + 81 * 2
            row[col_i] = Node(1, i, col_i)
          
            #box
            box_i = ((box_number * 9) + (i % 9)) + 81 * 3
            row[box_i] = Node(1, i, box_i)

cover = Cover()

head_col = Column(Node('h', 0, 0))
for i in range(81 * 9):
    head_col.add(Node(i, i, 0))

col_list = ColumnList(head_col)
for i in range(81 * 4):
    new_col = Column(Node(i, 0, i))
    for j, row in enumerate(cover.matrix):
        if type(row[i]) is Node:
            new_col.add(row[i])
    col_list.add(new_col)

print(col_list)