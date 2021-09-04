from dlx2 import Node, Column, ColumnList, LinkedGrid
cover_matrix = [[1,0,0,1,0,0,1],
                [1,0,0,1,0,0,0],
                [0,0,0,1,1,0,1],
                [0,0,1,0,1,1,0],
                [0,1,1,0,0,1,1],
                [0,1,0,0,0,0,1]]

head_col = Column(Node(-1,-1))
for i in range(6):
    head_col.add(Node(i, -1))

cl = ColumnList(head_col)
for i in range(7):
    new_node = Node(-1, i)
    new_col = Column(new_node)
    cl.add(new_col)

current_col = cl.head_col.right
for i in range(cl.size - 1):
    for j, row in enumerate(cover_matrix):
        if row[i] == 1:
            current_col.add(Node(j, i))
    current_col = current_col.right

current_row = -1
parallel_nodes = []
current_col = cl.head_col
for i in range(cl.size):
    parallel_nodes.append(current_col.head)
    current_col = current_col.right

def filter(i, node):
    if node.row == current_row:
        parallel_nodes[i] = node.down
        return True

for i in range(cl.head_col.size):
    row_nodes = [node for j, node in enumerate(parallel_nodes) if filter(j, node)]
    print(row_nodes)
    for j, node in enumerate(row_nodes):
        if j != len(row_nodes) - 1:
            node.add_right(row_nodes[j + 1])
    current_row += 1


#----------------------------------


grid = LinkedGrid(cl)
solution = []

def cover(node):
    column = node.parent
    column.right.left = column.left
    column.left.right = column.right

    next_node = node.down
    while next_node != column.head:
        next_node.up.down = next_node.down
        next_node.down.up = next_node.up

        current_node = next_node.right
        while current_node != next_node:
            current_node.up.down = current_node.down
            current_node.down.up = current_node.up

            current_node = current_node.right

        next_node = next_node.down

def uncover(node):
    column = node.parent
    column.right.left = column
    column.left.right = column

    left_node = node.left
    while left_node != node:
        left_node.up.down = left_node.down
        left_node.down.up = left_node.up
        left_node = left_node.left

def remove_solution(node):
    cover(node)
    current_node = node.right
    while current_node != node:
        if not (current_node.col == -1 or current_node.row == -1):
            cover(current_node)
        
        current_node = current_node.right

def insert_solution(node):
    current_node = node.left
    while current_node != node:
        if current_node.col != -1:
            uncover(current_node)
        
        current_node = current_node.left

    uncover(node)


remove_solution(grid.head.right.head.down)