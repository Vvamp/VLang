
class Node(object):
    def __init__(self, parent):
        self.parent = parent 
    
class LocationNode(Node):
    def __init__(self, parent : Node, rhs : str):
        self.node = Node(parent)
        self.parent = self.node.parent 
        self.rhs = rhs

class GotoNode(Node):
    def __init__(self, parent : Node, rhs : str):
        self.node = Node(parent)
        self.parent = self.node.parent 
        self.rhs = rhs

class WriteNode(Node):
    def __init__(self, parent : Node, rhs : str, isVariable : bool):
        self.node = Node(parent)
        self.parent = self.node.parent 
        self.rhs = rhs
        self.isVariable = isVariable

class WriteLnNode(Node):
    def __init__(self, parent : Node, rhs : str, isVariable : bool):
        self.node = Node(parent)
        self.parent = self.node.parent 
        self.rhs = rhs
        self.isVariable = isVariable

class AssignmentNode(Node):
    def __init__(self, parent : Node, lhs : str, rhs, asstype : str):
        self.node = Node(parent)
        self.parent = self.node.parent 
        self.lhs = lhs 
        self.rhs = rhs
        self.asstype = asstype
