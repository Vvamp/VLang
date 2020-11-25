import sys, getopt 
import functools
import parser
import lexer
import ast_parser

def main(argv):
    #todo: read multiple files
    f = open(argv[0], "r")
    all_lines = f.readlines()
    f.close()
    tokenmap = lexer.lex(all_lines)
    print(f"Token Map: {tokenmap}")

    parsedmap = parser.parse(tokenmap)
    print(f"Parsed List: ")
    parser.printParsed(parsedmap)

    # print(ast_parser.)

    print(ast_parser.parse(parsedmap))

if __name__ == "__main__":
    main(sys.argv[1:])