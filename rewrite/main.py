from lex import lex 
from lexToken import *
from typing import List
import sys


# Put parse and run in seperate files. These are dummy funcs
def parse():
    pass 

def run():
    pass

def main(argv : List[str]):
    # Load file
    f = open(argv[0], "r")
    all_lines = f.readlines()
    f.close()

    # Make tokens(a list of words with indentation etc)
    print(lex(all_lines))

    # Combine tokens into parsed nodes. A node can have children and acts witht hose children
    # i.e. A fcuntion, which can contain an if, which can contain code, etc
    parse()

    # Run the parsed tree
    run()

    # COmpiler: Instead of run, read compile.pdf


if __name__ == "__main__":
    """Calls the main function and prints the exit code and errors(if present)
    """
    result, errors = main(sys.argv[1:])