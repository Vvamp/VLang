import sys, getopt 
import functools
import parser, lexer, ast_parser
import copy
from ast_nodes import Node, LocationNode, GotoNode, WriteNode, WriteLnNode
import memory

def interpret_node(ast_node, mem):
    print("Interpreting Node: {}".format(ast_node))
    if type(ast_node) is LocationNode:
        NewBlock = memory.LocationMemoryBlock(ast_node.rhs)
        print("Location: {}".format(ast_node.rhs))
        return mem.push(NewBlock)

    elif type(ast_node) is GotoNode:
        NewBlock = memory.GotoMemoryBlock("", ast_node.rhs, copy.deepcopy(mem))
        print("Goto: {}".format(ast_node.rhs))
        return mem.push(NewBlock)

    elif type(ast_node) is WriteNode:
        NewBlock = memory.WriteMemoryBlock("", ast_node.rhs, False)
        print("Write: {}".format(ast_node.rhs))

        return mem.push(NewBlock)

    elif type(ast_node) is WriteLnNode:
            NewBlock = memory.WriteMemoryBlock("", ast_node.rhs, True)
            print("WriteLn: {}".format(ast_node.rhs))

            return mem.push(NewBlock)
    else:
        print("Error > Invalid node!")
    return
    

def interpret(ast):
    print(ast)
    mem = memory.Memory()

    # a = map(interpret_node, mem, ast)  
    a = mem   
    #todo no for loops
    for node in ast:
        a = interpret_node(node, a)
    # print('returning {}'.format(a))
    return a

    

def check_errors(tokenmap, tokenlist = [], errorlist = []):
    if len(tokenmap) == 1:
        if tokenmap[0].tokentype == "ERROR":
            return (tokenlist, errorlist + ["Ln {}: {}".format(tokenmap[0].line, tokenmap[0].symbol)])
        else: 
            return (tokenlist + [tokenmap[0].symbol], errorlist) 
    current_token_tokenlist, current_token_errorlist = check_errors([tokenmap[0]], tokenlist, errorlist)
    next_tokens_tokenlist, next_tokens_errorlist = check_errors(tokenmap[1:], tokenlist, errorlist)
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
    interpreted = interpret(ast)
    while interpreted != None:
        interpreted = interpreted.run()
    # print(interpreted)

    return 0, []

if __name__ == "__main__":
    result, errors = main(sys.argv[1:])
    print("Program Exit Code: {}".format(result))
    if result == 1:
        for error in errors: 
            print(error)
