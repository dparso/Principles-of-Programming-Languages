import sys
import re

types = ["int", "bool", "float", "char"]
keywords = ["main", "if", "else", "while", "return", "print", ";", "(", ")", "{", "}", "[", "]", "\"", "\'"]
equOp = ["==", "!="]
relOp = ["<", "<=", ">", ">="]
addOp = ["+", "-"]
multOp = ["*", "/"]
boolLiterals = ["true", "false"]
tokens = []

def raiseError(error):
    print "Error: " + error
    sys.exit()

# match for any operation
def checkOp(word):
    # takes a word and returns it's type of operation, else None
    if word in equOp:
        return ("equOp", word)
    elif word in relOp:
        return ("relOp", word)
    elif word == "=":
        return ("assignOp", word)
    elif word in addOp:
        return ("addOp", word)
    elif word in multOp:
        return ("multOp", word)

# match for an ID
def checkID(word):
    # any number of letters followed by any digits (if other patterns follow this, not a problem -- the only restriction is no numbers to start)
    # (in that case, it probably suffices just to ensure word[0] is a letter, but this seems more complete and extendable)
    id = re.compile("^[a-zA-Z]+[\d+]?")
    # ^ indicates only matching the beginning of the string; the [\d+]? allows optional digits
    
    result = id.match(word, 0)
    if result:
        return ["id", word]

# match for literals (int, float, bool)
def checkLiteral(word):
    
    result = word.split(".")

    # this seems easier than passing each through a match for \d+, \d+\.\d+, etc.
    if len(result) == 1:
        try:
            value = int(word)
            return ("intLiteral", word)
        except ValueError:
            # not an integer
            pass

    # a float should only be split into 2 items
    if len(result) == 2:
        try:
            value = float(word)
            return ("floatLiteral", word)
        except ValueError:
            # not a float
            pass

    if word == "true" or word == "false":
        return ("boolLiteral", word)

# read and parse input
def regexRead():
    fileLines = open(sys.argv[1], 'r').readlines()
    # pattern matches a string to this pattern
    # note that a comment takes up the rest of the line, so //.* for anything following the //
    pattern = re.compile("\s*((//.*)|==|>=|<=|!=|=|(\d+\.\d+)|(\w+)|(.))")

    lines = []
    for line in fileLines:
        items = []
        pos = 0
        while 1:
            # get individual matches from a line
            result = pattern.match(line, pos)
            if not result:
                break
            pos = result.end()
            # put them into one array
            items.append(result.group(result.lastindex))
        # add each collection of lexemes to list
        lines.append(items)

    # now, go through them and classify each
    for index, line in enumerate(lines):
        typePresent = 0

        for word in line:
            # there shouldn't be more than one type per line
            if word in types:
                if typePresent:
                    raiseError("Invalid syntax: multiple types in one line.\n")
                tokens.append(["type", word])
                typePresent = 1
                continue
                
            result = checkOp(word)
            if result is not None:
                tokens.append(result)
                continue
                    
            if word in keywords:
                tokens.append([word, word])
                continue
        
            result = checkLiteral(word)
            if result:
                tokens.append(result)
                continue
            
            result = checkID(word)
            if result:
                tokens.append(result)
                continue
            
            if len(word) > 2:
                if word[0] == "/" and word[1] == "/":
                    tokens.append(["comment", word])
                    continue
            
            # if this has been reached, the lexeme doesn't match anything I've implemented
            raiseError("Invalid syntax: " + word)

# print and save results
def displayResults():
    file = open("token_output.txt", "w")

    for pair in tokens:
        output = pair[0] + "\t" + pair[1]
        print output
        file.write(output + "\n")
    file.close()

def main():
    regexRead()
    displayResults()


# potential improvements:
#   raising a syntax error if a line does not end in a semicolon (or {, (, etc.)
#   recognizing the entirety of the inside of a print("Hello world!") statement, instead of breaking it into print, (, ", id, id, etc.
#   I'm not sure where a char literal comes into play, but there don't seem to be any examples that fail or behave undesirably

main()

