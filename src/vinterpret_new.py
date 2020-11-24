import sys, getopt 
import copy
import functools
from typing import List

class Token:
    def __init__(self, tokentype : str, symbol : str):
        self.tokentype = tokentype 
        self.symbol = symbol 

class TokenList:
    def __init__(self, tokenlist):
        self.tokenlist = tokenlist 

    def next(self) -> Token: 
        """Return the first token and remove it

        Returns:
            Token: The next token in the list
        """
        theToken = self.tokenlist[0]
        self.tokenlist = self.tokenlist[1:] # pop 
        return theToken

class ASTNode:
    def __init__(self, nodetype: str, LHS: str, RHS: str):
        self.nodetype = nodetype 
        self.LHS = LHS 
        self.RHS = RHS 



def check_location(tokenlist):
    if tokenlist.next() != 'location':
        return False, None 
    # return True, (Token('a', 'b'), Token('b','c')
    return True, [Token('LOCATION', 'location'), Token('NAME', tokenlist.next())] 
    
def check_goto(tokenlist):
    if tokenlist.next() != 'goto':
        return False, None 
    # return True, (Token('a', 'b'), Token('b','c')
    return True, [Token('GOTO', 'goto'), Token('NAME', tokenlist.next())]
    


def parse_tokens(tokenlist):
    thetokenlist = TokenList(tokenlist)

    # head, *tail = tokenlist
    # tokens = []
    result,checktokens = check_location(copy.deepcopy(thetokenlist))
    if result:
        return checktokens

    result,checktokens = check_goto(copy.deepcopy(thetokenlist))
    if result:
        return checktokens
    # return tokens

    return [Token('ERROR', 'NoneType')]

        

def flatten(unflattened_list : List[List[Token]]) -> List[Token]:
    if len(unflattened_list) == 0:
        return []
    head, *tail = unflattened_list

    return head + flatten(tail)

def parser(tokenmap):
    parsedmap = list(map(parse_tokens, tokenmap))
    return flatten(parsedmap)
    # return tokenmap 

def lexer(lines):
    return list( map(lambda line: (line.strip('\n').split(' ')), lines ))


def printParsed(parsedmap):
    print(parsedmap)
    print('{:<15} {:<20}'.format("[Type]", "[Symbol]"))
    for token in parsedmap:
            print('{:<15} {:<20}'.format(token.tokentype, token.symbol))

def astMaker(parsedmap):
    

def main(argv):
    #todo: read multiple files
    f = open(argv[0], "r")
    all_lines = f.readlines()
    f.close()
    tokenmap = lexer(all_lines)
    print(f"Token Map: {tokenmap}")

    parsedmap = parser(tokenmap)
    print(f"Parsed List: ")
    printParsed(parsedmap)

    astMaker(parsedmap)

if __name__ == "__main__":
    main(sys.argv[1:])