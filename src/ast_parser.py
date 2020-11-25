from typing import List
import lexer, Token

class Node(object):
    def __init__(self, parent, children):
        self.parent = parent 
        self.children = children 
    


class LocationNode(Node):
    def __init__(self, parent : Node, rhs : str):
        self.node = Node(parent, [rhs])

class GotoNode(Node):
    def __init__(self, parent : Node, rhs : str):
        self.node = Node(parent, [rhs])




def createAST(parsed_partmap, rootNode):
    if len(parsed_partmap) == 0:
        return []

    thisNode = None
    indexesUsed=1
    if parsed_partmap[0].tokentype == "LOCATION":
        indexesUsed=2
        thisNode = LocationNode(rootNode, parsed_partmap[1].symbol)
    elif parsed_partmap[0].tokentype == "GOTO":
        indexesUsed=2
        thisNode = GotoNode(rootNode, parsed_partmap[1].symbol)

        # Next one is also part of the AST node 
    return [thisNode] + createAST(parsed_partmap[indexesUsed:], rootNode)


def parse(parsedmap : List[Token.Token]):
    rootNode = Node(None, [])
    return createAST(parsedmap, rootNode)
    

        
