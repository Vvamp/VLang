import sys, getopt 
import functools
import parser, lexer, ast_parser
import copy
from ast_nodes import Node, LocationNode, GotoNode, WriteNode, WriteLnNode, AssignmentNode, IfNode, ExitNode, AssignmentModNode, JumpNode, WaitNode
import memory
import Token
from typing import Union, List, Tuple
import time

def printWelcome():
    """Prints the welcome screen to the terminal
    """
    version="1.0.0"
    print("VLang {} (Git Version)".format(version))
    print("Created by Vincent van Setten", end="\n=======================\n\n")

def main(argv : List[str]) -> Tuple[int, List[Token.Token]]:
    """The main function

    Args:
        argv (List(str)): A list of arguments
    Returns:
        Tuple(int, List(Token.Token)): A tuple of an exit code(int) and a list of errors

    """
    # Show welcome message
    printWelcome()

    # Load file
    f = open(argv[0], "r")
    all_lines = f.readlines()
    f.close()
   
    # Create a variable lookup table
    table = memory.LookUpTable()
    # table = table.addVariable("___memcheck___", 0)

    # Tokenize the text
    tokenmap = lexer.lex(all_lines)

    # Parse the tokenized list 
    parsedmap = parser.parse(tokenmap)

    #Check for errors 
    tokens,errors = check_errors(parsedmap)
    if len(errors) >= 1: 
        return 1, errors

    # Create an AST tree from the tokenized list 
    ast = ast_parser.parse(parsedmap)


    # Run the interpreter
    ## Note: I used a while loop here due to a recursion depth error 
    ## Below I have the function call that makes it work recursively. 
    ## It changes nothing to the code's behaviour, but recursive limtis the program to 1000 memory blocks due to recursion depth.
    interpreted = interpret(ast)
    while interpreted != None:
        results = interpreted.run(table)
        if results is None:
            break
        interpreted,table = results

    # Recursive: 
    # run_interpreter(interpreted)

    return 0, []

if __name__ == "__main__":
    """Calls the main function and prints the exit code and errors(if present)
    """
    result, errors = main(sys.argv[1:])
    print("\n=======================")
    print("Program Exit Code: {}".format(result))
    if result == 1:
        for error in errors: 
            print(error)
