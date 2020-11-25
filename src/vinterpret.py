import sys, getopt 
import functools
import parser, lexer, ast_parser
import copy
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

    

def check_errors(tokenmap, tokenlist = [], errorlist = [], linenr=1):
    # calc real linenr 
    #todo: is this allowed? idk but in the future I want this to do in the token object, so it still works after a goto.. 
    thelinenr = int((linenr+1)/2)  # Because for each line above 1, the function gets called twice. Once to call the [1:] and then to seperate it with [0]
        

    if len(tokenmap) == 1:
        if tokenmap[0].tokentype == "ERROR":
            return (tokenlist, errorlist + [tokenmap[0].symbol + " at line {}".format(thelinenr)])
        else: 
            return (tokenlist + [tokenmap[0].symbol], errorlist) 
    current_token_tokenlist, current_token_errorlist = check_errors([tokenmap[0]], tokenlist, errorlist, linenr)
    next_tokens_tokenlist, next_tokens_errorlist = check_errors(tokenmap[1:], tokenlist, errorlist, linenr+1)
    return (current_token_tokenlist + next_tokens_tokenlist, current_token_errorlist + next_tokens_errorlist)


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

    #Check for errors 
    tokens,errors = check_errors(parsedmap)
    if len(errors) >= 1: 
        return 1, errors

    print(f"Parsed List: ")
    parser.printParsed(parsedmap)

    # Create an AST tree from the tokenized list 
    ast = ast_parser.parse(parsedmap)

    # Run the interpreter
    interpreted = list(interpret(ast))

    return 0, []

if __name__ == "__main__":
    result, errors = main(sys.argv[1:])
    print("Program Exit Code: {}".format(result))
    if result == 1:
        for error in errors: 
            print(error)
