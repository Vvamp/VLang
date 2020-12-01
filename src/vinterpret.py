import sys, getopt 
import functools
import parser, lexer, ast_parser
import copy
from ast_nodes import Node, LocationNode, GotoNode, WriteNode, WriteLnNode, AssignmentNode, IfNode, ExitNode, AssignmentModNode, JumpNode
import memory
import Token
from typing import Union, List, Tuple
import time
# Dear Reader/Teacher,
#
# In the beginning of this course, I had a very small understanding of the structure of an interpreter. 
# I read in the reader that it began with a lexer and a parser. After that it was a little bit confusing to me, however.
# When I was looking around online, I stumbled upon two things I had to do: Parse and create an AST.
# Back then I thought they were two different things, so I created two different things: a parser and an ast parser. 
# I realize that I could/should merge them into 1 parser, but I felt like it served as a good learning point. 
# At this point, the regular parser server as a translation layer from the lexer's output to the AST parser's input.
# Completely useless, but I get reminded of how useless that step it everytime I look at the code. This is why I kept it. 
# When creating the compiler, assuming I have enough time, I'll merge the two. 
# I hope that's okay!
#
# Sincerely,
# Vincent van Setten, a person who thinks an interpreter has 5 steps



def interpret_node(ast_node : Node, mem : memory.Memory) -> Union[memory.Memory, None]: 
    """Interprets an ast node. creates a memory block and pushes the memory block to the memory

    Args:
        ast_node (Node): The AST node to interpret
        mem (memory.Memory): The current memory 

    Returns (either):
        - memory.Memory: The new memory with the interpreted ast
        - None: If the node could not be interpreted, None is returned
    """

    # print("Interpreting Node: {}".format(ast_node))
    if type(ast_node) is LocationNode:
        NewBlock = memory.LocationMemoryBlock(ast_node.rhs)
        # print("Location: {}".format(ast_node.rhs))
        return mem.push(NewBlock)

    elif type(ast_node) is GotoNode:
        NewBlock = memory.GotoMemoryBlock("", ast_node.rhs, copy.deepcopy(mem))
        # print("Goto: {}".format(ast_node.rhs))
        return mem.push(NewBlock)

    elif type(ast_node) is WriteNode:
        NewBlock = memory.WriteMemoryBlock("", ast_node.rhs, False, ast_node.isVariable, copy.deepcopy(mem))
        # print("Write: {}".format(ast_node.rhs))

        return mem.push(NewBlock)

    elif type(ast_node) is WriteLnNode:
        NewBlock = memory.WriteMemoryBlock("", ast_node.rhs, True, ast_node.isVariable, copy.deepcopy(mem))
        # print("WriteLn: {}".format(ast_node.rhs))

        return mem.push(NewBlock)

    elif type(ast_node) is AssignmentNode:
        NewBlock = memory.AssignmentMemoryBlock("", ast_node.lhs, ast_node.rhs, ast_node.asstype)
        # print("Assignment: {} {} = {}".format(ast_node.asstype, ast_node.lhs, ast_node.rhs))

        return mem.push(NewBlock)
    elif type(ast_node) is IfNode:
        NewBlock = memory.IfMemoryBlock("", ast_node.lhs, ast_node.rhs, ast_node.compare_operator, copy.deepcopy(mem))
        # print("If {} {} {}".format(ast_node.lhs, ast_node.compare_operator, ast_node.rhs))

        return mem.push(NewBlock)
    elif type(ast_node) is AssignmentModNode:
        NewBlock = memory.AssignmentModMemoryBlock("", ast_node.lhs, ast_node.rhs, ast_node.asstype, mem)
        
        return mem.push(NewBlock)
    elif type(ast_node) is ExitNode:
        NewBlock = memory.ExitMemoryBlock("__SYS__EXIT__")
        return mem.push(NewBlock)

    elif type(ast_node) is JumpNode:
        NewBlock = memory.JumpMemoryBlock("", ast_node.rhs, ast_node.isStatic)
        return mem.push(NewBlock)

    else:
        print("Error > Invalid node!")
    return None
    

def interpret_rec(ast : List[Node], mem : memory.Memory) -> memory.Memory:
    """Recursively interprets an AST tree into the given memory

    Args:
        ast (List): The AST tree to be loaded into memory
        mem (memory.Memory): The memory to load the AST in

    Returns:
        memory.Memory: The new memory with the AST loaded in
    """
    if len(ast) == 1:
        return interpret_node(ast[0], mem)
    elif len(ast) == 2:
        return interpret_node(ast[1], interpret_node(ast[0], mem))

    a = interpret_rec(ast[0:2], mem)
    return interpret_rec(ast[2:], a)

def interpret(ast : List[Node]) -> memory.Memory:
    """Interprets an AST Tree into a memory object

    Args:
        ast (List): An AST Tree

    Returns:
        memory.Memory: The memory object with the interpreted AST tree inside of it
    """
    
    mem = memory.Memory()
    return interpret_rec(ast, mem)

    

def check_errors(tokenmap : List[Token.Token], tokenlist : List[Token.Token]=[], errorlist : List[Token.Token]=[]) -> Tuple[List[Token.Token], List[Token.Token]]:
    """Checks for errors in a tokenmap and returns those errors in a seperate list

    Args:
        tokenmap (List(Token)): A tokenmap to check for errors 
        tokenlist (List(Token), optional): A list of regular tokens. Defaults to []
        errorlist (List(Token), optional): A list of error tokens. Defaults to []
    Returns:
        [Tuple]: A tuple of a regular list of tokens and a list of error tokens
    """

    if len(tokenmap) == 1:
        if tokenmap[0].tokentype == "ERROR":
            return (tokenlist, errorlist + ["Ln {}: {}".format(tokenmap[0].line, tokenmap[0].symbol)])
        else: 
            return (tokenlist + [tokenmap[0].symbol], errorlist) 
    current_token_tokenlist, current_token_errorlist = check_errors([tokenmap[0]], tokenlist, errorlist)
    next_tokens_tokenlist, next_tokens_errorlist = check_errors(tokenmap[1:], tokenlist, errorlist)
    return (current_token_tokenlist + next_tokens_tokenlist, current_token_errorlist + next_tokens_errorlist)

def run_interpreter(interpreted : memory.Memory) -> Union[memory.Memory, None]:
    """Runs the instructions in the memory

    Args:
        interpreted (memory.Memory): The memory to run

    Returns:
        memory.Memory : A memory without the current memory block 
        None          : Returns none after everything in the memory has been ran
    """
    
    if interpreted is None: 
        return None
    return run_interpreter(interpreted.run())

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
