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


def lexLine(line):
    if line == "\n":
        return ["\n"]
    elif line.startswith('#'):
        return ["#"]
    
    splittedList = re.split('\s|(\")', line)
    filteredList = filter(None, splittedList) 
    return list( filteredList )

def lex(lines : List[str]) -> List[str] : 
    """Generates a tokenized list of instructions from a valid .v file

    Args:
        lines (List[str]): A list of string lines, read from a valid .v file

    Returns:
        List[str]: A tokenized list of instructions in the .v file
    """
  
    lexed = list( map(lexLine, lines) )
   
    print(lexed)
    return lexed


