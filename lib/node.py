class Node:
    def __init__(self):
        self.next = None
        self.prev = None
        self.parent = None


class CompositeNode(Node):

    first: any
    last: any

    def __init__(self):
        super().__init__()
        self.first = None
        self.last = None

    def append(self, node: Node):
        node.parent = self
        if self.last:
            self.last.next = node
            node.prev = self.last
        else:
            self.first = node

        self.last = node

    def insert(self, node: Node):
        node.parent = self
        if self.first:
            node.next = self.first
            self.first.prev = node
        else:
            self.last = node

        self.first = node
        
    def remove(self, node: Node):
        if node == self.first:
            self.first = None

        if node == self.last:
            self.last = None

        prev = node.prev()
        next = node.next()

        if prev:
            prev.next = next

        if next:
            next.prev = prev

        node.next = None
        node.prev = None
        node.parent = None
