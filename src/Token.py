from __future__ import annotations
from typing import List, Tuple

class Token:
    """A Token
    """
    def __init__(self, tokentype : str, symbol : str, linenr : int):
        """Initializes a Token object

        Args:
            tokentype (str): The type of the token(NAME, ASSIGNMENT, etc )
            symbol (str): The content of the token('x', 'y', 'i', etc)
            linenr (int): The line number of the instruction
        """
        self.tokentype = tokentype 
        self.symbol = symbol 
        self.line = linenr

class TokenList:
    def __init__(self, tokenlist : List[Token]):
        """Initializes a TokenList object based on a list of tokens

        Args:
            tokenlist (List(Token)): A list of tokens
        """
        self.tokenlist = tokenlist 

    def next(self) -> Tuple(Token, TokenList): 
        """Return the first token and a new TokenList without that token

        Returns:
            Tuple(Token, TokenList): A tuple of the next token in the list and a lsit without the token
        """

        return (self.tokenlist[0], TokenList(self.tokenlist[1:]))
        