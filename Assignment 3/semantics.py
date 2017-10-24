#Tasks:
#1) Type checking -- variable must be declared before use
#2) Semantic Analysis -- evaluate an expression

#Grammar productions
#Simplification: No main function; expressions without var; only type is int
#   Program     -> Declarations Statements
#   Declarations-> {Declaration}
#   Declaration -> {type id;}
#   type        -> int
#   Statements  -> {Statement}
#   Statement   -> print id; | id = Expr; 
#   Expr        -> Term {(+|-) Term}
#   Term        -> Factor{(*|/) Factor}
#   Factor      -> intLiteral

#Input: A text file where each line has a token and the corresponding lexeme
#Output: Type error (if any), output of print statements

import sys

#Global var
iNextToken = 0 #Next token index
tokenStream = []
lexemeStream = []
symTable = {} #empty dictionary/hash-map

def main(inputFileName):
    global tokenStream, lexemeStream, iNextToken
    #Initialize
    tokenStream = []
    lexemeStream = []
    iNextToken = 0
    symTable = {} #New

    #Process the input file and build lists of tokens and lexemes
    inputFileObj = open(inputFileName, "r")
    bigStr = inputFileObj.read()
    bigList = bigStr.split() #bigList is a list of tokens and lexemes (alternating)
    tokenStream = bigList[0: :2] #List of tokens sliced from bigList (even elements)
    lexemeStream = bigList[1: :2] #List of lexemes

    print("Tokens:", tokenStream)
    print("Lexemes:", lexemeStream)
    
    program() #Start at the start symbol Program
    if iNextToken < len(tokenStream): #had to stop early
        error()

def program():
    declarations()
    statements()

def declarations():
    while iNextToken < len(tokenStream) and \
          tokenStream[iNextToken] == 'type':
        declaration()

def declaration():
    global iNextToken, symTable
    if tokenStream[iNextToken] == 'type': #redundant
        iNextToken += 1
        if tokenStream[iNextToken] == 'id':
            varName = lexemeStream[iNextToken]
            varType = lexemeStream[iNextToken - 1]
            #Make a new dictionary entry: key = varName, value = [varType, initialValue]
            symTable[varName] = [varType, None]
            iNextToken += 1
            if tokenStream[iNextToken] == ';':
                iNextToken += 1
                return
    error()

def statements():
    while iNextToken < len(tokenStream) and \
          (tokenStream[iNextToken] == 'print' or tokenStream[iNextToken] == 'id'):
        statement()

def statement():
    global iNextToken, symTable
    
    if tokenStream[iNextToken] == 'print':
        iNextToken += 1
        if tokenStream[iNextToken] == 'id':
            if not exists(lexemeStream[iNextToken]): #var not declared?
                declarationError(lexemeStream[iNextToken])
            iNextToken += 1
            if tokenStream[iNextToken] == ';':
                iNextToken += 1
                printValue(lexemeStream[iNextToken - 2]) #argument: lexeme for id
                return #success
    elif tokenStream[iNextToken] == 'id':
        varName = lexemeStream[iNextToken] #for use later
        if not exists(lexemeStream[iNextToken]): #var not declared?
            declarationError(lexemeStream[iNextToken])
        iNextToken += 1
        if tokenStream[iNextToken] == '=':
            iNextToken += 1
            value = expr()
            if tokenStream[iNextToken] == ';':
                iNextToken += 1
                #save the new value in the symbol table
                #Note: the only type of var here is int.
                #For the assignment, you need to be more sophisticated with implicit type conversion.
                symTable[varName][1] = int(value) 
                return #success
    error()

def printValue(varName):
    print(varName, "=", symTable[varName][1],"\n")

def exists(varName):
    return varName in symTable
    
def expr():
    global iNextToken
   
    result = term() #Consume a Term first and save its result
    while iNextToken < len(tokenStream) and \
            (tokenStream[iNextToken] == "+" or tokenStream[iNextToken] == "-"):
        sign = 1 if tokenStream[iNextToken] == "+" else -1
        iNextToken += 1 #Consumed the + or - token
        v = term() #Consume another Term
        result = result + sign * v
    return result
    
def term():
    global iNextToken

    result = factor() #Consume a Factor
    while iNextToken < len(tokenStream) and \
            (tokenStream[iNextToken] == "*" or tokenStream[iNextToken] == "/"):
        exponent = 1 if tokenStream[iNextToken] == "*" else -1
        iNextToken += 1 #Consumed the * or / token
        v = factor() #Consume another Factor
        result = result * v ** exponent
    return result
    
def factor():
    global iNextToken

    if iNextToken < len(tokenStream) and tokenStream[iNextToken] == "intLiteral":
        iNextToken += 1
        return int(lexemeStream[iNextToken-1])
    error()

def error():
    print(iNextToken)
    if iNextToken < len(tokenStream):
        print("Error: Invalid expression. Error location: <",\
            tokenStream[iNextToken], ",", lexemeStream[iNextToken], ">.")
    else:
        print("Error: Incomplete expression. Expecting more terms.")
    exit()

def declarationError(varName):
    print("ERROR: Unknown variable", varName)
    exit()

#To take command line argument for the file name
if __name__ == "__main__":
    main(sys.argv[1])

