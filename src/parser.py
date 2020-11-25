from typing import List
import lexer, Token, copy


def check_location(tokenlist : List[str]) -> bool, List[Token.Token]:
    """Checks if the given construction is of the type 'location'. If it is, the first value will return True and the second value will return a list of tokens. 
    If it isn't of the type 'location', the first value will return False and the second value wil return None.

    Args:
        tokenlist (List[str]): A list of strings consisting of an instruction and their parameters

    Returns:
        bool, List[Token.Token]: Returns a bool(whether the token is of this type) and a list of tokens, which is the instruction and the parameters.
    """
    if tokenlist.next() != 'location':
        return False, None 
    # return True, (Token('a', 'b'), Token('b','c')
    return True, [Token.Token('LOCATION', 'location'), Token.Token('NAME', tokenlist.next())] 
    
def check_goto(tokenlist : List[str]) -> bool, List[Token.Token]:
     """Checks if the given construction is of the type 'goto'. If it is, the first value will return True and the second value will return a list of tokens. 
    If it isn't of the type 'goto', the first value will return False and the second value wil return None.

    Args:
        tokenlist (List[str]): A list of strings consisting of an instruction and their parameters

    Returns:
        bool, List[Token.Token]: Returns a bool(whether the token is of this type) and a list of tokens, which is the instruction and the parameters.
    """
    if tokenlist.next() != 'goto':
        return False, None 
    # return True, (Token.Token('a', 'b'), Token.Token('b','c')
    return True, [Token.Token('GOTO', 'goto'), Token.Token('NAME', tokenlist.next())]
    


def parse_tokens(tokenlist : List[str]) -> List[Token.Token]:
    """Creates tokens based on an instruction and their parameters

    Args:
        tokenlist (List[str]): A list of strings consisting of an instruction and their parameters
    Returns:
        List[Token.Token]: A list of tokens based on the instruction with the parameter
    """
    thetokenlist = Token.TokenList(tokenlist)

    # Check if the current instruction is a location statement
    result,checktokens = check_location(copy.deepcopy(thetokenlist))
    if result:
        return checktokens

    # Check if the current instruction is a goto statement
    result,checktokens = check_goto(copy.deepcopy(thetokenlist))
    if result:
        return checktokens

    # If the current instruction doesn't exist, return a NoneType
    # todo: return an error
    return [Token.Token('ERROR', 'NoneType')]


       
def parse(tokenmap : List[str]) -> List[Token.Token]:
    """Generates a list of tokens from a tokenized list of instructions

    Args:
        tokenmap (List[str]): A tokenized list of instructions

    Returns:
        [type]: A list of tokens
    """
   
    return lexer.flatten(list(map(parse_tokens, tokenmap)) )


# Debug Function, will not be used in final product
def printParsed(parsedmap):
    print(parsedmap)
    print('{:<15} {:<20}'.format("[Type]", "[Symbol]"))
    for token in parsedmap:
            print('{:<15} {:<20}'.format(token.tokentype, token.symbol))
