
class Token:
    def __init__(self, tokentype : str, symbol : str):
        self.tokentype = tokentype 
        self.symbol = symbol 

# Probably not functional since it has a state. Maye return the new token list and the new token?
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