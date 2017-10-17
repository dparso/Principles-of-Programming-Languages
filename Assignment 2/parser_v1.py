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
    
    expr() #Start at the start symbol Expr
    if iNextToken < len(tokenStream):
        error() #Why?
    else:
        print("Valid Expression!")

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
    
    if iNextToken < len(tokenStream) and tokenStream[iNextToken] == "intLiteral":
        iNextToken += 1
        return
    else:
        error()

def error():
    #print(iNextToken)
    if iNextToken < len(tokenStream):
        print("Error: Invalid expression. Error location:")
    #<" + tokenStream[iNextToken] + "," + lexemeStream +[iNextToken] + ">.")
    else:
        print("Error: Incomplete expression. Expecting more terms.")
    exit()

#To take command line argument for the file name
if __name__ == "__main__":
    main(sys.argv[1])

