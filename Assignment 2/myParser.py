#Disclaimer: Prof. Irfan is not responsible if this program crashes your computer :)

#How to run in terminal: python parser_v1.py tokens1.txt

#Mohammad T. Irfan (2017)
#Recursive-descent parser for simple arithmetic expressions
#Example: intLiteral - intLiteral - intLiteral * intLiteral / intLiteral

#Grammar productions:
#   Expr -> Term {(+|-) Term}
#   Term -> Factor{(*|/) Factor}
#   Factor -> intLiteral

#Input: A text file where each line has a token and the corresponding lexeme
#Output: True iff no syntax error

import sys

#Use global vars because it's well past midnight, otherwise it's a crime
iNextToken = 0 #Next token index
tokenStream = []
lexemeStream = [] #not used for parsing
stmtStart = ["print", "if", "while", "return", "id"]
literals = ["intLiteral", "boolLiteral", "floatLiteral", "charLiteral"]

def main(inputFileName):
    global tokenStream, lexemeStream, iNextToken
    tokenStream = []
    lexemeStream = []
    iNextToken = 0
    
    #Process the input file and build lists of tokens and lexemes
    inputFileObj = open(inputFileName, "r")
    bigStr = inputFileObj.read()
    bigList = bigStr.split() #bigList is a list of tokens and lexemes (alternating)
    tokenStream = bigList[0::2] #List of tokens sliced from bigList (even elements)
    lexemeStream = bigList[1::2] #List of lexemes
    
    print("Tokens:", tokenStream)
    print("Lexemes:", lexemeStream)
    
    if len(tokenStream) < 6: # must be at least type, main, (, ), {, }
        error()

    program()

    # consume final closing braces
    if iNextToken >= len(tokenStream):
        error()
    else:
        if tokenStream[iNextToken] == "}":
            iNextToken += 1

    print iNextToken, len(tokenStream)
    #expr() #Start at the start symbol Expr
    if iNextToken < len(tokenStream):
        error() #Why?
    else:
        print("Valid Expression!")

def program():
    global iNextToken
    if tokenStream[:5] == ["type", "main", "(", ")", "{"]: # program must start with these tokens, excepting imports or global var declarations
        iNextToken += 5
        declarations()
        statements()
    else:
        error()

def declarations():
    global iNextToken
    # check if next token is a type
    while iNextToken < len(tokenStream) and tokenStream[iNextToken] == "type":
        iNextToken += 1
        # iteratively consume what's being declared
        declaration()

def declaration():
    global iNextToken
    #  consume an id
    id()
    while iNextToken < len(tokenStream) and tokenStream[iNextToken] == ",":
        iNextToken += 1
        # consume any following id, so long as it's preceded by ","
        id()
    closeStatement() # must end in semicolon

# consume a semicolon
def closeStatement():
    global iNextToken
    if iNextToken < len(tokenStream) and tokenStream[iNextToken] == ";":
        iNextToken += 1
        return
    else:
        error("Expected semicolon.")

def id():
    global iNextToken

    if iNextToken < len(tokenStream) and tokenStream[iNextToken] == "id":
        # consume an id
        iNextToken += 1
        return
    else:
        error()

def statements():
    global iNextToken
    
    while iNextToken < len(tokenStream) and tokenStream[iNextToken] in stmtStart:
        print iNextToken, len(tokenStream)
        statement()

def statement():
    global iNextToken

    if iNextToken >= len(tokenStream):
        error()

    if tokenStream[iNextToken] == "id":
        print "assnhi"
        iNextToken += 1
        assignment()
    elif tokenStream[iNextToken] == "print":
        print "printhi"
        iNextToken += 1
        printStmt()
    elif tokenStream[iNextToken] == "if":
        print "ifhi"
        iNextToken += 1
        ifStmt()
    elif tokenStream[iNextToken] == "while":
        print "whilehi"
        iNextToken += 1
        whileStmt()
    elif tokenStream[iNextToken] == "return":
        print "returnhi"
        iNextToken += 1
        returnStmt()
    else:
        error()

def assignment():
    global iNextToken
    if iNextToken < len(tokenStream) and tokenStream[iNextToken] == "assignOp":
        iNextToken += 1
        expr()
        closeStatement()
    else:
        error()

def printStmt():
    global iNextToken
    if iNextToken < len(tokenStream):
        expr()
        closeStatement()
    else:
        error()

def ifStmt():
    global iNextToken
    if iNextToken < len(tokenStream) and tokenStream[iNextToken] == "(":
        iNextToken += 1
    else:
        error("Incomplete if statement.")

    expr()

    if iNextToken < len(tokenStream) and tokenStream[iNextToken] == ")":
        iNextToken += 1
    else:
        error("Incomplete if statement")

    statement()

    if iNextToken < len(tokenStream) and tokenStream[iNextToken] == "else":
        # another statement!
        iNextToken += 1
        statement()

def whileStmt():
    global iNextToken

def returnStmt():
    global iNextToken
    if iNextToken < len(tokenStream):
        expr()
        closeStatement()
    else:
        error()

def expr():
    global iNextToken
    
    term() #Consume a Term first
    while iNextToken < len(tokenStream) and \
        (tokenStream[iNextToken] == "+" or tokenStream[iNextToken] == "-"):
        iNextToken += 1 #Consumed the + or - token
        term() #Consume another Term

def term():
    global iNextToken
    
    factor() #Consume a Factor
    while iNextToken < len(tokenStream) and \
        (tokenStream[iNextToken] == "*" or tokenStream[iNextToken] == "/"):
        iNextToken += 1 #Consumed the * or / token
        factor() #Consume another Factor

def factor():
    global iNextToken
    
    if iNextToken < len(tokenStream):
        if tokenStream[iNextToken] in literals:
            iNextToken += 1
            return
        else:
            id()

    else:
        error()

def error(message = ""):
    #print(iNextToken)
    if message != "":
        print("Error: " + message + "Error location: < " + tokenStream[iNextToken] + ", " + lexemeStream[iNextToken] + " >.")
    elif iNextToken < len(tokenStream):
        print("Error: Invalid expression. Error location: <" + tokenStream[iNextToken] + "," + lexemeStream[iNextToken] + ">.")
    else:
        print("Error: Incomplete expression. Expecting more terms.")
    exit()

#To take command line argument for the file name
if __name__ == "__main__":
    main(sys.argv[1])



#need:
"""
    Statement assignment
    (Expression) in factor
    Proper conjunction for expression
    Doesn't allow multiple functions?
    Doesn't allow declaration after statement
    
    """
