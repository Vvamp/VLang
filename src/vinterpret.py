import sys, getopt 
version="0.0.1"
print("--Hello VLang--") 

class Token:
    def __init__(self, linenr: int, tokentype: int, symbol: str):
        self.linenr = linenr 
        self.tokentype = tokentype 
        self.symbol = symbol 

def addTokenToLexmap(lexmap, token):
    tokens = lexmap.append(token)
    return tokens 


def isToken(word, typestocheck):
    if len(typestocheck) == 1:
        return word == typestocheck[0]
    else:
        return (word == typestocheck[0]) | isToken(word, typestocheck[1:])

def tokenise(line):
    lorem = ['goto', 'location']
    if isToken("int", prim_types):
        print("TOKEN!")
    return [line, line]


def lexrec(lines, tokenedlines = []):
    if len(lines) == 1:
        tokenedlines = tokenedlines + tokenise(lines[0])
        return tokenedlines
    else:
        tokenedlines = tokenedlines + tokenise(lines[0])
        tokenedlines = tokenedlines + lexrec(lines[1:])
        return tokenedlines

def lex(lines):
    lexlist = []
    all_test = lexrec(lines)
    print(all_test)
    a = Token(1, 2, "HI")
    b = Token(2, 4, "Hey")
    return [a,b]


def printTokens(lex):
    print("Tokens:")
    for i in range(0, len(lex)):
        print(f'ID: {i} Line: {lex[i].linenr} Type: {lex[i].tokentype} Symbol: {lex[i].symbol}')



def main(argv):
    #todo: read multiple files
    f = open(argv[0], "r")
    all_lines = f.readlines()
    f.close()
    lexmap = lex(all_lines)
    
    printTokens(lexmap)


if __name__ == "__main__":
    main(sys.argv[1:])
