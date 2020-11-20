import sys, getopt 
version="0.0.1"
print("--Hello VLang--") 

class Token:
    def __init__(self, linenr: int, tokentype: str, symbol: str):
        self.linenr = linenr 
        self.tokentype = tokentype 
        self.symbol = symbol 


def lexrec_words(words, linenr):
    keywords = ['location', 'goto', 'string']
    if len(words) == 1:
        if words[0] == keywords[0]:
            return [Token(linenr, keywords[0], words[0])]
        elif words[0] == keywords[1]:
            return [Token(linenr, keywords[1], words[0])]
        else:
            return [Token(linenr, keywords[2], words[0])]
    else:
        if len(words[1:]) > 1:
            # If there are more than 2 words or more left, besides index 0, then don't convert it to another list
            return lexrec_words([words[0]], linenr) + lexrec_words(words[1:], linenr)
        else:
            # If it's only one word, store it in a list so the function doesn't mess stuff up
            return lexrec_words([words[0]], linenr) + lexrec_words([words[1]], linenr)


def lexrec_line(line, linenr):
    """Lex a line 

    Args:
        line (string): A line of VLang code

    Returns:
        list: A list of tokens from a line
    """
    #todo: don't use a for loop
    tokens = []
    words = line.split(' ')
    tokens = lexrec_words(words, linenr)
    # for word in line.split(' '): 
    #     if word in keywords:
    #         myToken = Token(0, 0, word) 
    #         tokens.append(myToken)
    #     else:
    #         myToken = Token(0, 1, word)
    #         tokens.append(myToken)
    return tokens
            

    
    


def lexrec_lines(lines, linenr=1):
    """Creates a lexmap by recursively interpreting lines and returning them

    Args:
        lines (list): A list of lines of VLang code

    Returns:
        list: A list of tokened lines
    """
    if len(lines) == 1:
        return lexrec_line(lines[0], linenr)
    else:
        return lexrec_line(lines[0], linenr) + lexrec_lines(lines[1:], linenr+1)


def lex(lines):
    """Constructs a lexmap via the recursive lexrec_lines funcion

    Args:
        lines (list): A list of lines containing VLang code

    Returns:
        list: A list of tokened lines
    """
    lexlist = []
    all_tokens = lexrec_lines(lines)
    print(all_tokens)
    return all_tokens


def printTokens(lex):
    """Prints the tokens based on a lexmap

    Args:
        lex (list): A list of tokens
    """
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
