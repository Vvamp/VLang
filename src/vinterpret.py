import sys, getopt 
version="0.0.1"
print("--Hello VLang--") 

class Token:
    def __init__(self, linenr: int, tokentype: int, symbol: str):
        self.linenr = linenr 
        self.tokentype = tokentype 
        self.symbol = symbol 


def lexrec_word(word):
    return

def lexrec_line(line):
    """
    Return a list of tokens from a line
    """
    #todo: don't fix this
    keywords = ['location', 'goto']
    tokens = []
    for word in line.split(' '): 
        if word in keywords:
            myToken = Token(0, 0, word) 
            tokens.append(myToken)
        else:
            myToken = Token(0, 1, word)
            tokens.append(myToken)
    return tokens
            

    
    


def lexrec_lines(lines):
    """
    Return a list of tokens from all lines
    """
    if len(lines) == 1:
        return lexrec_line(lines[0])
    else:
        return lexrec_line(lines[0]) + lexrec_lines(lines[1:])


def lex(lines):
    """
    Should output a list of Tokens
    """
    lexlist = []
    all_tokens = lexrec_lines(lines)
    print(all_tokens)
    return all_tokens


def printTokens(lex):
    print("Tokens:")
    for i in range(0, len(lex)):
        print(f'ID: {i} Line: {lex[i].linenr} Type: {lex[i].tokentype} Symbol: {lex[i].symbol}')



# install docstring extension

def main(argv):
    #todo: read multiple files
    f = open(argv[0], "r")
    all_lines = f.readlines()
    f.close()
    lexmap = lex(all_lines)
    
    printTokens(lexmap)


if __name__ == "__main__":
    main(sys.argv[1:])
