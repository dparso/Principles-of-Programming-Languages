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
stack = []
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
        print("Valid Syntax!")

def program():
    global iNextToken, stack
    stack.append("program")
    if tokenStream[:5] == ["type", "main", "(", ")", "{"]: # program must start with these tokens, excepting imports or global var declarations
        iNextToken += 5
        declarations()
        statements()
    else:
        error()
    stack.pop()

def declarations():
    global iNextToken, stack
    
    stack.append("declarations")
    # check if next token is a type
    while iNextToken < len(tokenStream) and tokenStream[iNextToken] == "type":
        iNextToken += 1
        # iteratively consume what's being declared
        declaration()
    stack.pop()

def declaration():
    global iNextToken, stack
    
    stack.append("declaration")
    #  consume an id
    id()
    while iNextToken < len(tokenStream) and tokenStream[iNextToken] == ",":
        iNextToken += 1
        # consume any following id, so long as it's preceded by ","
        id()
    closeStatement() # must end in semicolon
    stack.pop()

# consume a semicolon
def closeStatement():
    global iNextToken, stack
    
    stack.append("closeStmt")
    if iNextToken < len(tokenStream) and tokenStream[iNextToken] == ";":
        iNextToken += 1
        stack.pop()
        return
    else:
        error("Expected semicolon.")

def id():
    global iNextToken, stack
    
    stack.append("id")

    if iNextToken < len(tokenStream) and tokenStream[iNextToken] == "id":
        # consume an id
        iNextToken += 1
        stack.pop()
        return
    else:
        error()

def statements():
    global iNextToken, stack
    
    stack.append("statements")
    
    while iNextToken < len(tokenStream) and tokenStream[iNextToken] in stmtStart:
        statement()

    stack.pop()

def statement():
    global iNextToken, stack
    
    stack.append("statement")

    if iNextToken >= len(tokenStream):
        error()

    if tokenStream[iNextToken] == "id":
        iNextToken += 1
        assignment()
    elif tokenStream[iNextToken] == "print":
        iNextToken += 1
        printStmt()
    elif tokenStream[iNextToken] == "if":
        iNextToken += 1
        ifStmt()
    elif tokenStream[iNextToken] == "while":
        iNextToken += 1
        whileStmt()
    elif tokenStream[iNextToken] == "return":
        iNextToken += 1
        returnStmt()
    else:
        error()

    stack.pop()

def assignment():
    global iNextToken, stack
    # remaining is assignOp Expression
    stack.append("assignment")
    if iNextToken < len(tokenStream) and tokenStream[iNextToken] == "assignOp":
        iNextToken += 1
        expr()
        closeStatement()
        stack.pop()
        return
    else:
        error()

def printStmt():
    global iNextToken, stack
    
    stack.append("print")
    if iNextToken < len(tokenStream):
        expr()
        closeStatement()
        stack.pop()
        return
    else:
        error()

def ifStmt():
    global iNextToken, stack
    
    # must include parentheses
    stack.append("if")
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

    stack.pop()

def whileStmt():
    global iNextToken, stack
    
    stack.append("while")
    
    if iNextToken < len(tokenStream) and tokenStream[iNextToken] == "(":
        iNextToken += 1
    else:
        error("Incomplete while statement.")
    
    expr()

    if iNextToken < len(tokenStream) and tokenStream[iNextToken] == ")":
        iNextToken += 1
    else:
        error("Incomplete while statement")

    statement()

    stack.pop()

def returnStmt():
    global iNextToken, stack
    
    stack.append("return")
    if iNextToken < len(tokenStream):
        expr()
        closeStatement()
    else:
        error()

    stack.pop()

def expr():
    global iNextToken, stack
    
    stack.append("expr")
    # consume single conjunction
    conjunction()
    while iNextToken < len(tokenStream) and \
        (tokenStream[iNextToken] == "||"):
        iNextToken += 1 # consume ||
        conjunction() # consume another conjunction
    stack.pop()

def conjunction():
    global iNextToken, stack

    stack.append("conjunction")
    equality()
    # as many equalities as separated by &&
    while iNextToken < len(tokenStream) and tokenStream[iNextToken] == "&&":
        iNextToken += 1
        equality()
    stack.pop()

def equality():
    global iNextToken, stack

    stack.append("equality")
    relation()

    if iNextToken < len(tokenStream) and tokenStream[iNextToken] == "equOp":
        iNextToken += 1
        relation()
    stack.pop()

def relation():
    global iNextToken, stack
    stack.append("relation")
    addition()

    if iNextToken < len(tokenStream) and tokenStream[iNextToken] == "relOp":
        iNextToken += 1
        addition()
    stack.pop()

def addition():
    global iNextToken, stack
    
    stack.append("addition")
    
    term() #Consume a Term first
    while iNextToken < len(tokenStream) and \
        (tokenStream[iNextToken] == "addOp"):
        iNextToken += 1 #Consumed the + or - token
        term() #Consume another Term
    stack.pop()

def term():
    global iNextToken, stack
    
    stack.append("term")
    
    factor() #Consume a Factor
    while iNextToken < len(tokenStream) and \
        (tokenStream[iNextToken] == "multOp"):
        iNextToken += 1 #Consumed the * or / token
        factor() #Consume another Factor
    stack.pop()

def factor():
    global iNextToken, stack
    
    stack.append("factor")
    
    if iNextToken < len(tokenStream):
        # check if any literal (char not implemented)
        if tokenStream[iNextToken] in literals:
            iNextToken += 1
            stack.pop()
            return
        elif tokenStream[iNextToken] == "(":
            # beginning of (Expression)
            iNextToken += 1
            expr()
            if iNextToken < len(tokenStream) and tokenStream[iNextToken] == ")":
                iNextToken += 1
            else:
                error("Expected closing parenthesis.")
        else:
            id()
    else:
        error()
    stack.pop()

def error(message = ""):
    if message != "":
        print("Error: " + message + " Error location: < " + tokenStream[iNextToken] + ", " + lexemeStream[iNextToken] + " >.")
    elif iNextToken < len(tokenStream):
        print("Error: Invalid syntax. Error location: < " + tokenStream[iNextToken] + "," + lexemeStream[iNextToken] + " >.")
    else:
        print("Error: Incomplete expression. Expecting more terms.")
    print "\nStack is:"
    for i in stack:
        print i + "->",
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
