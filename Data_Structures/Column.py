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