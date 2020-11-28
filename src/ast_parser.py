from typing import List
import lexer, Token
from ast_nodes import LocationNode, GotoNode, Node, WriteNode, WriteLnNode

def findIndexByType(thelist, thetype):
    print("Searching list: {}".format(thelist))
    #todo functional
    for elem in thelist:
        if elem.tokentype == thetype:
            return  thelist.index(elem)
    return False

def createAST(parsed_partmap : List[Token.Token], rootNode : Node) -> List[Node]:
    """[summary]

    Args:
        parsed_partmap (List[Token.Token]): A (subset of) a list of tokens
        rootNode (Node): The root of the tree, which is usually a regular empty node

    Returns:
        List[Node]: A list of AST nodes
    """
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
    elif parsed_partmap[0].tokentype == "IO" and parsed_partmap[0].symbol == "write":
        indexesUsed = 0 
        # [write, delim, hallo, caro, delim]
        if parsed_partmap[1].tokentype != "DELIM":
            # Errror 
            return 
        otherdelimIndex = findIndexByType(parsed_partmap[2:], "DELIM") +2
        indexesUsed = otherdelimIndex+1 # The call + first delim + the rest

        valNodes = []
        for node in parsed_partmap[2:otherdelimIndex]:
            valNodes.append(node.symbol)
        
        thisNode = WriteNode(rootNode, valNodes)
    
    elif parsed_partmap[0].tokentype == "IO" and parsed_partmap[0].symbol == "writeline":
        indexesUsed = 0 
        # [write, delim, hallo, caro, delim]
        if parsed_partmap[1].tokentype != "DELIM":
            # Errror 
            return 
        otherdelimIndex = findIndexByType(parsed_partmap[2:], "DELIM") +2
        indexesUsed = otherdelimIndex+1 # The call + first delim + the rest

        valNodes = []
        for node in parsed_partmap[2:otherdelimIndex]:
            valNodes.append(node.symbol)
        
        thisNode = WriteLnNode(rootNode, valNodes)

        # Next one is also part of the AST node 
    return [thisNode] + createAST(parsed_partmap[indexesUsed:], rootNode)


def parse(parsedmap : List[Token.Token]) -> List[Node]:
    """Creates an AST tree based on a list of tokens

    Args:
        parsedmap (List[Token.Token]): A list of tokens

    Returns:
        List[Node]: A list of AST Nodes
    """
    return createAST(parsedmap, Node(None))
    

        
