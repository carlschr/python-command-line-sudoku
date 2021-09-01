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

    def cover(self):
        self.down.up = self.up
        self.up.down = self.down

    def uncover(self):
        self.down.up = self
        self.up.down = self

    def __repr__(self) -> str:
        return f'[{self.row}, {self.col}]'
