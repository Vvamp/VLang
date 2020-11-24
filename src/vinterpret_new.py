import sys, getopt 
import copy
import functools

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


def check_location(tokenlist):
    if tokenlist.next() != 'location':
        return False, None 
    # return True, (Token('a', 'b'), Token('b','c')
    return True, (Token('LOCATION', 'location'), Token('NAME', tokenlist.next())) 
    
def check_goto(tokenlist):
    if tokenlist.next() != 'goto':
        return False, None 
    # return True, (Token('a', 'b'), Token('b','c')
    return True, (Token('GOTO', 'goto'), Token('NAME', tokenlist.next())) 
    


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

        

def parser(tokenmap):
    return list(map(parse_tokens, tokenmap))
    # return tokenmap 

def lexer(lines):
    return list( map(lambda line: (line.strip('\n').split(' ')), lines ))


def printParsed(parsedmap):
    print('{:<15} {:<20}'.format("[Type]", "[Symbol]"))
    for tokens in parsedmap:
        for token in tokens:
            # print("{token.tokentype}: {token.symbol}")
            print('{:<15} {:<20}'.format(token.tokentype, token.symbol))


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

if __name__ == "__main__":
    main(sys.argv[1:])