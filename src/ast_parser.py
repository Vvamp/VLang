from typing import List
import lexer, Token
from ast_nodes import LocationNode, GotoNode, Node



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
    

        
