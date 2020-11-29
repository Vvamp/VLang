from typing import List, Union
import lexer, Token
from ast_nodes import LocationNode, GotoNode, Node, WriteNode, WriteLnNode, AssignmentNode, IfNode, ExitNode

def checkIndexByType(results : List(int)) -> Union(int, None): 
    """Recursively find the first index that is not none

    Args:
        results (List(int)): A list of indexes and none's

    Returns:
        int: The index of the first matching element 
        None: If the element type was not found, it returns None
    """
    if len(results) == 0:
        return None
    if results[0] != None:
        return results[0]
    return checkIndexByType(results[1:])

def findIndexByType(thelist : List(Token.Token), thetype : str) -> Union(int, None) :
    """Find index of an element based on its type

    Args:
        thelist (List(Token.Token)): The token list to search in
        thetype (str): The tokentype to find

    Returns:
        int: The index of the element 
        None: If the element type was not found, it returns None
    """
    results = list( map(lambda element: thelist.index(element) if element.tokentype == thetype else None, thelist) ) 
    return checkIndexByType(results)
 

def createAST(parsed_partmap : List[Token.Token], rootNode : Node) -> List[Node]:
    """Creates an AST from a list of tokens

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
    # Checks what token type it is and creates an AST node for that
    if parsed_partmap[0].tokentype == "LOCATION":
        indexesUsed=2
        thisNode = LocationNode(rootNode, parsed_partmap[1].symbol)
    elif parsed_partmap[0].tokentype == "GOTO":
        indexesUsed=2
        thisNode = GotoNode(rootNode, parsed_partmap[1].symbol)
    elif parsed_partmap[0].tokentype == "IO" and parsed_partmap[0].symbol == "write":
        indexesUsed = 0 

        if parsed_partmap[1].tokentype != "DELIM" and parsed_partmap[1].tokentype != "IDENTIFIER":
            # Throw error: Invaid argument 
            return 
        if parsed_partmap[1].tokentype == "DELIM":
            otherdelimIndex = findIndexByType(parsed_partmap[2:], "DELIM") +2
            indexesUsed = otherdelimIndex+1 # The call + first delim + the rest
            beginIndex = 2
            isVariable = False
        else: 
            otherdelimIndex = 1+1
            beginIndex = 1
            indexesUsed = 2
            isVariable = True

        valNodes = []
        for node in parsed_partmap[beginIndex:otherdelimIndex]:
            valNodes.append(node.symbol)
    
        
        thisNode = WriteNode(rootNode, valNodes, isVariable)
    
    elif parsed_partmap[0].tokentype == "IO" and parsed_partmap[0].symbol == "writeline":
        indexesUsed = 0 

        if parsed_partmap[1].tokentype != "DELIM" and parsed_partmap[1].tokentype != "IDENTIFIER":
            # Throw error: Invaid argument 
            return 

        if parsed_partmap[1].tokentype == "DELIM":
            otherdelimIndex = findIndexByType(parsed_partmap[2:], "DELIM") +2
            indexesUsed = otherdelimIndex+1 # The call + first delim + the rest
            beginIndex = 2
            isVariable = False
        else: 
            otherdelimIndex = 1+1
            beginIndex = 1
            indexesUsed = 2
            isVariable = True

        valNodes = []
        for node in parsed_partmap[beginIndex:otherdelimIndex]:
            valNodes.append(node.symbol)

        thisNode = WriteLnNode(rootNode, valNodes, isVariable)

    elif parsed_partmap[0].tokentype == "TYPE":
        indexesUsed = 4 # Change for str 
        thisNode = AssignmentNode(rootNode, parsed_partmap[1].symbol, parsed_partmap[3].symbol,parsed_partmap[0].symbol)

    elif parsed_partmap[0].tokentype == "EXIT":
        indexesUsed = 1 # Change for str 
        thisNode = ExitNode(rootNode)

    elif parsed_partmap[0].tokentype == "CONDITIONAL":
        indexesUsed = 4
        thisNode = IfNode(rootNode, parsed_partmap[1].symbol, parsed_partmap[3].symbol, parsed_partmap[2].symbol)

        # Next one is also part of the AST node 
    elif parsed_partmap[0].tokentype == "IGNORE":
        indexesUsed = 1
        return  createAST(parsed_partmap[indexesUsed:], rootNode)
    return [thisNode] + createAST(parsed_partmap[indexesUsed:], rootNode)


def parse(parsedmap : List[Token.Token]) -> List[Node]:
    """Creates an AST tree based on a list of tokens

    Args:
        parsedmap (List[Token.Token]): A list of tokens

    Returns:
        List[Node]: A list of AST Nodes
    """
    # Create a rootnode and pass it to the createAST function
    return createAST(parsedmap, Node(None))
    

        
