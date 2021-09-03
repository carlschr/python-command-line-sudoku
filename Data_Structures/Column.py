from Node import Node

class Column:
    def __init__(self, header):
        self.head = header
        self.tail = header
        header.parent = self
        self.right = self
        self.left = self
        self.size = 1

    def add_right(self, column):
        column.right = self.right
        column.left = self
        self.right.left = column
        self.right = column

    def add(self, node):
        node.parent = self
        node.up = self.tail
        node.down = self.tail.down
        self.tail.down = node
        self.tail = node
        self.head.up = node
        self.size += 1

    def cover(self):
        self.right.left = self.left
        self.left.right = self.right
        current = self.head.down
        while current != self.head:
            row_node = current.right
            while row_node != current:
                row_node.cover()
                self.size -= 1
                row_node = row_node.right
            current = current.down

    def uncover(self):
        current = self.head.up
        while current != self.head:
            row_node = current.left
            while row_node != current:
                row_node.uncover()
                self.size += 1
                row_node = row_node.left
            current = current.up
        self.right.left = self
        self.left.right = self

    def __repr__(self):
        string = ''
        current_node = self.head
        for _ in range(self.size):
            string += str(current_node)
            current_node = current_node.down
        return string

if __name__ == '__main__':
    test_head = Node(0, 0)
    test_column = Column(test_head)
    for i in range(1, 9):
        new_node = Node(i, 0)
        test_column.add(new_node)
    print(f'Test Column: {test_column}')
    print(f'Test Column Head: {test_column.head}')