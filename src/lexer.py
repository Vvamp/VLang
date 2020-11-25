from typing import List
import Token

 
def flatten(unflattened_list : List[List[Token.Token]]) -> List[Token.Token]:
    if len(unflattened_list) == 0:
        return []
    head, *tail = unflattened_list

    return head + flatten(tail)

def lex(lines):
    return list( map(lambda line: (line.strip('\n').split(' ')), lines ))


