from Node import Node

class Column:
    def __init__(self, header):
        self.head = header
        self.tail = header
        header.parent = self
        self.right = self
        self.left = self
        self.size = 1

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

    def uncover(self):
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