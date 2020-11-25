import lexer
import Token
import copy


def check_location(tokenlist):
    if tokenlist.next() != 'location':
        return False, None 
    # return True, (Token('a', 'b'), Token('b','c')
    return True, [Token.Token('LOCATION', 'location'), Token.Token('NAME', tokenlist.next())] 
    
def check_goto(tokenlist):
    if tokenlist.next() != 'goto':
        return False, None 
    # return True, (Token.Token('a', 'b'), Token.Token('b','c')
    return True, [Token.Token('GOTO', 'goto'), Token.Token('NAME', tokenlist.next())]
    


def parse_tokens(tokenlist):
    thetokenlist = Token.TokenList(tokenlist)

    # head, *tail = tokenlist
    # tokens = []
    result,checktokens = check_location(copy.deepcopy(thetokenlist))
    if result:
        return checktokens

    result,checktokens = check_goto(copy.deepcopy(thetokenlist))
    if result:
        return checktokens
    # return tokens

    return [Token.Token('ERROR', 'NoneType')]


       
def parse(tokenmap):
    parsedmap = list(map(parse_tokens, tokenmap))
    return lexer.flatten(parsedmap)

def printParsed(parsedmap):
    print(parsedmap)
    print('{:<15} {:<20}'.format("[Type]", "[Symbol]"))
    for token in parsedmap:
            print('{:<15} {:<20}'.format(token.tokentype, token.symbol))
