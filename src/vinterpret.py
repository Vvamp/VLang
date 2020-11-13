import sys, getopt 
version="0.0.1"
print("--Hello VLang--") 

class Token:
    def __init__(self, linenr, content):
        self.linenr = linenr 
        self.content = content 



def lex(all_lines):
   specialCharacters = ["}", "{", ")", "(", "\"", "\'", "//", ","] 
   tokens = []
   firsttoken = Token("-1", "check")
   current_line = 0
   for line in all_lines:
       # If line is empty, ignore the line
        if line == "":
           continue 
    
        # Increase line
        current_line = current_line + 1
        
        for word in line.split(" "): 
            currentlyInText=False
            for i in range(0, len(word)):
                if word[i] in specialCharacters:
                    print("letter is special <3")
                    if currentlyInText:
                        continue 
                    else:
                        tokens.append(Token(current_line, word[i]))
                        
                        print("Removing letter")
                else:
                    continue
              
            tokens.append(Token(current_line, word))


   # magic to decode
   # decode per line and write each line to tokens
   # if line is empty, ignore it!
   tokens.append(firsttoken)
   print(tokens)
   for token in tokens:
       print(f"- {token}\t{token.linenr}\t{token.content}")


def main(argv):
    for _file in argv:
        f = open(_file, "r")
        all_lines = []
        for line in f:
            all_lines.append(line)
            print("Command > " + line.strip("\n"))
            # lex(line)
        f.close()

        lex(all_lines)

if __name__ == "__main__":
    main(sys.argv[1:])
