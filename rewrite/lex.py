from typing import List 



def lexWord(word : str):
    if word == None or word == "":
        return ""
    print("Token -> \"", word, "\"")
    return word

def lexLine(line : str):
    print("> Line: \"", line, "\"")
    lineLength = len(line.split(' '))
    if lineLength == 1:
        return lexWord(line.split(' ')[0])
    elif lineLength == 2:
        return lexWord(line.split(' ')[0]) + lexWord(line.split(' ')[1])
    print("Not 2, but ", lineLength)
    firstWord = line.split(' ')[0]
    firstWordLength = len(firstWord)
    restOfTheString = line[firstWordLength:]
    return lexLine(firstWord) + lexLine(restOfTheString)

def lexRemoveTrailingSpaces(line : str) -> str:
    """Recursively remove trailing spaces from a string

    Args:
        line (str): [description]

    Returns:
        str: [description]
    """
    if line[-1] == " ":
        return lexRemoveTrailingSpaces(line[:-1])
    return line


def lexRec(lines : List[str]):

    if len(lines) == 1:
        # Attempt to find comments
        anyComments = lines[0].find("//")
        if anyComments != -1:
            print(f"Line without comments: \"{lexRemoveTrailingSpaces(lines[0][:anyComments])}\"")
            return lexLine(lexRemoveTrailingSpaces(lines[0][:anyComments])) # Leave out the comments
        print(f"Clean line: \"{lines[0]}\"")
        return lexLine(lines[0])
    
    return lexRec(lines[0]) + lexRec(lines[1:])


def lex(fileInput : List[str]):
    lexRec(fileInput)


