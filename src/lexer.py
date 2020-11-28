from typing import List
import Token
import re

 
def flatten(unflattened_list : List[List[Token.Token]]) -> List[Token.Token]:
    """Makes a single depth list of Tokens from a nested list of Tokens

    Args:
        unflattened_list (List[List[Token.Token]]): 2D List of Tokens

    Returns:
        List[Token.Token]: A 1 dimensional list of Tokens
    """
    if len(unflattened_list) == 0:
        return []
    head, *tail = unflattened_list

    return head + flatten(tail)


def fixmylex(line):
    a = re.split('\s|(\")', line)
    a = filter(None, a) 
    return list( a )

def lex(lines : List[str]) -> List[str] : 
    """Generates a tokenized list of instructions from a valid .v file

    Args:
        lines (List[str]): A list of string lines, read from a valid .v file

    Returns:
        List[str]: A tokenized list of instructions in the .v file
    """
    # b = re.split('\s | \"', line)
    # a = list( map(lambda  line: re.split('\s|(\")', line), lines) )
    a = list( map(fixmylex, lines) )
    # b = list( filter(lambda word: word != '' and word != None, a) )
    # a = list( map(lambda line: (line.strip('\n').split(' ').split("\"")), lines ))
    print(a)
    return a


