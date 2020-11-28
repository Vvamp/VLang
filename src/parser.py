from typing import List, Tuple
import lexer, Token, copy


def check_location(tokenlist : List[str], current_line : int) -> Tuple[bool, List[Token.Token]]:
    """Checks if the given construction is of the type 'location'. If it is, the first value will return True and the second value will return a list of tokens. 
    If it isn't of the type 'location', the first value will return False and the second value wil return None.

    Args:
        tokenlist (List[str]): A list of strings consisting of an instruction and their parameters

    Returns:
        bool, List[Token.Token]: Returns a bool(whether the token is of this type) and a list of tokens, which is the instruction and the parameters.
    """
    if tokenlist.next() != 'location':
        return False, None 

    return True, [Token.Token('LOCATION', 'location', current_line), Token.Token('NAME', tokenlist.next(), current_line)] 
    
def check_goto(tokenlist : List[str], current_line : int) -> Tuple[bool, List[Token.Token]]:
    """Checks if the given construction is of the type 'goto'. If it is, the first value will return True and the second value will return a list of tokens. 
    If it isn't of the type 'goto', the first value will return False and the second value wil return None.

    Args:
        tokenlist (List[str]): A list of strings consisting of an instruction and their parameters

    Returns:
        bool, List[Token.Token]: Returns a bool(whether the token is of this type) and a list of tokens, which is the instruction and the parameters.
    """
    if tokenlist.next() != 'goto':
        return False, None 

    return True, [Token.Token('GOTO', 'goto', current_line), Token.Token('NAME', tokenlist.next(), current_line)]
    
def check_write(tokenlist : List[str], current_line : int) -> Tuple[bool, List[Token.Token]]:
    """Checks if the given construction is of the type 'goto'. If it is, the first value will return True and the second value will return a list of tokens. 
    If it isn't of the type 'goto', the first value will return False and the second value wil return None.

    Args:
        tokenlist (List[str]): A list of strings consisting of an instruction and their parameters

    Returns:
        bool, List[Token.Token]: Returns a bool(whether the token is of this type) and a list of tokens, which is the instruction and the parameters.
    """
    if tokenlist.next() != 'write':
        return False, None 

    allTokens = [] 
    nextToken = tokenlist.next()
    if nextToken == '"':
        # return False, None   
        text = []
        a = ""
        while a != '"':
            a = tokenlist.next()
            if a != '"':
                text.append(a) 
        #todo: functional
        allTokens.append(Token.Token('IO', 'write', current_line))
        allTokens.append(Token.Token('DELIM', '"', current_line))
        for textToken in text:
            allTokens.append(Token.Token('VALUE', textToken, current_line))
        allTokens.append(Token.Token('DELIM', '"', current_line))
    else: 
        allTokens.append(Token.Token('IO', 'write', current_line))
        allTokens.append(Token.Token('IDENTIFIER', nextToken, current_line))

    return True, allTokens
    
def check_writeln(tokenlist : List[str], current_line : int) -> Tuple[bool, List[Token.Token]]:
    """Checks if the given construction is of the type 'goto'. If it is, the first value will return True and the second value will return a list of tokens. 
    If it isn't of the type 'goto', the first value will return False and the second value wil return None.

    Args:
        tokenlist (List[str]): A list of strings consisting of an instruction and their parameters

    Returns:
        bool, List[Token.Token]: Returns a bool(whether the token is of this type) and a list of tokens, which is the instruction and the parameters.
    """
    if tokenlist.next() != 'writeLine':
        return False, None 

    allTokens = [] 
    nextToken = tokenlist.next()
    if nextToken == '"':
        # return False, None   
        text = []
        a = ""
        while a != '"':
            a = tokenlist.next()
            if a != '"':
                text.append(a) 
        #todo: functional
        allTokens.append(Token.Token('IO', 'writeline', current_line))
        allTokens.append(Token.Token('DELIM', '"', current_line))
        for textToken in text:
            allTokens.append(Token.Token('VALUE', textToken, current_line))
        allTokens.append(Token.Token('DELIM', '"', current_line))
    else: 
        allTokens.append(Token.Token('IO', 'writeline', current_line))
        allTokens.append(Token.Token('IDENTIFIER', nextToken, current_line))

    return True, allTokens


def check_assignment(tokenlist : List[str], current_line : int) -> Tuple[bool, List[Token.Token]]:
    """Checks if the given construction is of the type 'location'. If it is, the first value will return True and the second value will return a list of tokens. 
    If it isn't of the type 'location', the first value will return False and the second value wil return None.

    Args:
        tokenlist (List[str]): A list of strings consisting of an instruction and their parameters

    Returns:
        bool, List[Token.Token]: Returns a bool(whether the token is of this type) and a list of tokens, which is the instruction and the parameters.
    """
    variable_keywords = {
        "int": int
    }

    assignment_operators = ['=']
    variable_keyword = tokenlist.next()
    if variable_keyword not in variable_keywords:
        return False, None 

    name = tokenlist.next()
    assignment_operator = tokenlist.next()
    if assignment_operator not in assignment_operators:
        return False, None 

    value = tokenlist.next()

    if type(eval(value)) != variable_keywords[variable_keyword]:
        return False, [Token.Token('ERROR', 'Error: Value does not match type', current_line)]
    #todo: without append, just a singular list in 1 call
    tokens = []
    tokens.append(Token.Token('TYPE', variable_keyword, current_line))
    tokens.append(Token.Token('IDENTIFIER', name, current_line))
    tokens.append(Token.Token('ASSIGNMENT', assignment_operator, current_line))
    tokens.append(Token.Token('VALUE', value, current_line))

    return True, tokens

def parse_tokens(tokenlist : List[str], current_line : int) -> List[Token.Token]:
    """Creates tokens based on an instruction and their parameters

    Args:
        tokenlist (List[str]): A list of strings consisting of an instruction and their parameters
    Returns:
        List[Token.Token]: A list of tokens based on the instruction with the parameter
    """
    thetokenlist = Token.TokenList(tokenlist)

    # Check if the current instruction is a location statement
    result,checktokens = check_location(copy.deepcopy(thetokenlist), current_line)
    if result:
        return checktokens

    # Check if the current instruction is a goto statement
    result,checktokens = check_goto(copy.deepcopy(thetokenlist), current_line)
    if result:
        return checktokens
    
    # Check if the current instruction is a regular write statement
    result,checktokens = check_write(copy.deepcopy(thetokenlist), current_line)
    if result: 
        return checktokens
    
    # Check if the current instruction is a writeline statement
    result,checktokens = check_writeln(copy.deepcopy(thetokenlist), current_line)
    if result: 
        return checktokens

    # Check if the current instruction is an assignment 
    result,checktokens = check_assignment(copy.deepcopy(thetokenlist), current_line)
    if result:
        return checktokens

    # If the current instruction doesn't exist, return a NoneType
    # todo: result in check function becomes an int: 1 is true, 0 is false 2 is error
    return [Token.Token('ERROR', "Error: unknown instruction '{}'".format(copy.deepcopy(thetokenlist).next()), current_line)]


def parse_with_lines(tokenmap, current_line=1):
    # print(tokenmap)
    if len(tokenmap) == 1:
        return parse_tokens(tokenmap[0], current_line)
    
    return parse_with_lines([tokenmap[0]], current_line) + parse_with_lines(tokenmap[1:], current_line+1)
    


def parse(tokenmap : List[List[str]]) -> List[Token.Token]:
    """Generates a list of tokens from a tokenized list of instructions

    Args:
        tokenmap (List[str]): A tokenized list of instructions

    Returns:
        [type]: A list of tokens
    """
   
    return parse_with_lines(tokenmap)


# Debug Function, will not be used in final product
def printParsed(parsedmap):
    print(parsedmap)
    print('{:<15} {:<20}'.format("[Type]", "[Symbol]"))
    for token in parsedmap:
            print('{:<15} {:<20}'.format(token.tokentype, token.symbol))
