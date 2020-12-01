
class Node(object):
    def __init__(self, parent):
        """Initializes an empty node

        Args:
            parent (Node)): The parent node(or none if the current node is the rootnode)
        """
        self.parent = parent 
    
class LocationNode(Node):
    def __init__(self, parent : Node, rhs : str):
        """Initializes a location node

        Args:
            parent (Node): The node's parent
            rhs (str): The location label
        """
        self.node = Node(parent)
        self.parent = self.node.parent 
        self.rhs = rhs

class GotoNode(Node):
    def __init__(self, parent : Node, rhs : str):
        """Initializes a goto node

        Args:
            parent (Node): The node's parent
            rhs (str): The goto label
        """
        self.node = Node(parent)
        self.parent = self.node.parent 
        self.rhs = rhs

class WriteNode(Node):
    def __init__(self, parent : Node, rhs : str, isVariable : bool):
        """Initalizes a write node

        Args:
            parent (Node): The node's parent
            rhs (str): The (list of) string(s) to write, or the variable to write 
            isVariable (bool): Whether or not the RHS is a variable, or a string
        """
        self.node = Node(parent)
        self.parent = self.node.parent 
        self.rhs = rhs
        self.isVariable = isVariable

class WriteLnNode(Node):
    def __init__(self, parent : Node, rhs : str, isVariable : bool):
        """Initalizes a writeline node

        Args:
            parent (Node): The node's parent
            rhs (str): The (list of) string(s) to write, or the variable to write 
            isVariable (bool): Whether or not the RHS is a variable, or a string
        """
        self.node = Node(parent)
        self.parent = self.node.parent 
        self.rhs = rhs
        self.isVariable = isVariable

class AssignmentNode(Node):
    def __init__(self, parent : Node, lhs : str, rhs : str, asstype : str):
        """Initializes an assignment node

        Args:
            parent (Node): The node's parent
            lhs (str): The node's identifier
            rhs (str): The node's variable
            asstype (str): The node's type
        """
        self.node = Node(parent)
        self.parent = self.node.parent 
        self.lhs = lhs 
        self.rhs = rhs
        self.asstype = asstype

class IfNode(Node):
    def __init__(self, parent : Node, lhs : str, rhs : str, compare_operator : str):
        """Initializes an if node

        Args:
            parent (Node): The node's parent
            lhs (str): The left variable in the if statement
            rhs (str): The right variable in the if statement
            compare_operator (str): The compare operator to use, i.e == 
        """
        self.node = Node(parent)
        self.parent = self.node.parent 
        self.lhs = lhs 
        self.rhs = rhs 
        self.compare_operator = compare_operator

class AssignmentModNode(Node):
    def __init__(self, parent : Node, lhs : str, rhs : str, asstype : str):
        """Initializes an assignment node

        Args:
            parent (Node): The node's parent
            lhs (str): The node's identifier
            rhs (str): The node's variable
            asstype (str): The node's assignment, i.e. += or -=
        """
        self.node = Node(parent)
        self.parent = self.node.parent 
        self.lhs = lhs 
        self.rhs = rhs
        self.asstype = asstype


class ExitNode(Node):
    def __init__(self, parent : Node):
        """Initializes an exit node(quits the program)

        Args:
            parent (Node): The node's parent
        """
        self.node = Node(parent)
        self.parent = self.node.parent