import sys, getopt 
import functools
import parser, lexer, ast_parser
from ast_nodes import Node, LocationNode, GotoNode

def interpret_node(ast_node):
    if type(ast_node) is LocationNode:
        print("Location: {}".format(ast_node.rhs))
        # Set a label at specific pc 
    elif type(ast_node) is GotoNode:
        print("Goto: {}".format(ast_node.rhs))
        # Search for the label and go to it
    else:
        print("Error > Invalid node!")
    return
    

def interpret(ast):
    return map(interpret_node, ast)     


def main(argv):
    #todo: read multiple files
    f = open(argv[0], "r")
    all_lines = f.readlines()
    f.close()

    # Tokenize the text
    tokenmap = lexer.lex(all_lines)
    print(f"Token Map: {tokenmap}")

    # Parse the tokenized list 
    parsedmap = parser.parse(tokenmap)
    print(f"Parsed List: ")
    parser.printParsed(parsedmap)

    # Create an AST tree from the tokenized list 
    ast = ast_parser.parse(parsedmap)

    # Run the interpreter
    interpreted = list(interpret(ast))

if __name__ == "__main__":
    main(sys.argv[1:])