# Disclaimer: Prof. Irfan is not responsible if this program crashes your computer :)

# How to run in terminal: python myParser.py tokens.txt

# Dylan Parsons (2017)
# Recursive-descent parser for CLite

# Input: A text file where each line has a token and the corresponding lexeme
# Output: True iff no syntax error

import sys
import operator

# Use global vars because it's well past midnight, otherwise it's a crime
iNextToken = 0  # Next token index
stack = []
tokenStream = []
lexemeStream = []  # not used for parsing
symTable = {}
stmtStart = ["print", "if", "while", "return", "id"]
literals = ["intLiteral", "boolLiteral", "floatLiteral", "charLiteral"]
operators = {  # easy transition from string to operator, no 'if x == "+" etc.' necessary
    '>': operator.gt,
    '>=': operator.ge,
    '<': operator.lt,
    '<=': operator.le,
    '+': operator.add,
    '-': operator.sub,
    '==': operator.eq,
    '!=': operator.ne,
    '*': operator.mul,
    '/': operator.truediv
}


def main(inputFileName):
    global tokenStream, lexemeStream, iNextToken
    tokenStream = []
    lexemeStream = []
    iNextToken = 0

    # Process the input file and build lists of tokens and lexemes
    inputFileObj = open(inputFileName, "r")
    bigStr = inputFileObj.read()
    bigList = bigStr.split()  # bigList is a list of tokens and lexemes (alternating)
    tokenStream = bigList[0::2]  # List of tokens sliced from bigList (even elements)
    lexemeStream = bigList[1::2]  # List of lexemes

    print("Tokens:", tokenStream)
    print("Lexemes:", lexemeStream)

    if len(tokenStream) < 6:  # must be at least type, main, (, ), {, }
        error()

    program()

    # consume final closing braces
    if iNextToken >= len(tokenStream):
        error()
    else:
        if tokenStream[iNextToken] == "}":
            iNextToken += 1

    print "Consumed " + str(iNextToken) + " of " + str(len(tokenStream)) + " tokens."

    if iNextToken < len(tokenStream):
        error()
    else:
        print("Valid Expression!")


def program():
    global iNextToken, stack
    stack.append("program")

    if tokenStream[:5] == ["type", "main", "(", ")", "{"]:  # program must start with these tokens, excepting imports or global var declarations
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
    id(True)
    while iNextToken < len(tokenStream) and tokenStream[iNextToken] == ",":
        iNextToken += 1
        # consume any following id, so long as it's preceded by ","
        id(True)

    closeStatement()
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


def id(isDeclaring):
    # isDeclaring will tell whether to store the variable in symTable (declaring) or check if it has already been declared (referencing)
    global iNextToken, stack, symTable

    stack.append("id")

    if iNextToken < len(tokenStream) and tokenStream[iNextToken] == "id":
        # consume an id
        varName = lexemeStream[iNextToken]

        if isDeclaring:
            # store the variable
            if varName in symTable:
                # rule 1: check if name is taken
                error("Variable name taken.")
            varType = lexemeStream[iNextToken - 1]

            symTable[varName] = [varType, None]

        else:
            if not lexemeStream[iNextToken] in symTable:
                # rule 2: check if declared
                declarationError(lexemeStream[iNextToken])

        iNextToken += 1
        stack.pop()
        return symTable[varName][1]
    else:
        error()


def statements():
    global iNextToken, stack

    stack.append("statements")

    while iNextToken < len(tokenStream) and tokenStream[iNextToken] in stmtStart:
        statement()

    stack.pop()

# source tells whether we've come from a while loop so we can act accordingly
def statement(execute=True):
    global iNextToken, stack, symTable

    stack.append("statement")

    if iNextToken >= len(tokenStream):
        error()

    if tokenStream[iNextToken] == "id":
        # check if declared
        if not lexemeStream[iNextToken] in symTable:
            declarationError(lexemeStream[iNextToken])
        name = lexemeStream[iNextToken]
        iNextToken += 1
        assignment(name, execute)
    elif tokenStream[iNextToken] == "print":
        iNextToken += 1
        printStmt()
    elif tokenStream[iNextToken] == "if":
        iNextToken += 1
        ifStmt(execute)
    elif tokenStream[iNextToken] == "while":
        iNextToken += 1
        whileStmt(execute)
    elif tokenStream[iNextToken] == "return":
        iNextToken += 1
        returnStmt()
    else:
        error()

    stack.pop()


def assignment(varName, execute=True):
    global iNextToken, stack
    # remaining is assignOp Expression
    stack.append("assignment")
    if iNextToken < len(tokenStream) and tokenStream[iNextToken] == "assignOp":
        iNextToken += 1
        value = expr()

        # this will be a string
        xType = symTable[varName][0]
        # so we convert it to Python's syntax for string comparison
        xStr = "<type '" + xType + "'>"

        # this will be a type of the form <type 'int'>, etc.
        yType = type(value)

        isError = False
        if xStr != str(yType):
            # any mismatch is an error except float = int
            isError = True
            # remember, we check a string, not a type
            if xType == 'float':
                    # float can be assigned an int
                    # here we use int rather than 'int', as yType was a type
                    if yType == int:
                        isError = False

        if isError:
            error("Type error. Invalid assignment.")


        if execute:
            symTable[varName][1] = value
        closeStatement()
        stack.pop()
        return
    else:
        error()


def printStmt():
    global iNextToken, stack

    stack.append("print")
    if iNextToken < len(tokenStream):
        result = expr()
        print result
        closeStatement()
        stack.pop()
        return
    else:
        error()


def ifStmt(execute=True):
    global iNextToken, stack

    # must include parentheses
    stack.append("if")
    if iNextToken < len(tokenStream) and tokenStream[iNextToken] == "(":
        iNextToken += 1
    else:
        error("Incomplete if statement.")

    result = expr()

    if iNextToken < len(tokenStream) and tokenStream[iNextToken] == ")":
        iNextToken += 1
    else:
        error("Incomplete if statement")

    """ careful with what's executed: an inner if might not run if its outer loop doesn't
    technically this doesn't matter here, as we can't have nested loops, but would be
    very important otherwise
    """
    if execute:
        statement(bool(result))
    else:
        # here, no matter what result was, this should not run, as its outer loop doesn't run
        statement(False)

    if iNextToken < len(tokenStream) and tokenStream[iNextToken] == "else":
        # another statement!
        iNextToken += 1
        statement()

    stack.pop()


def whileStmt(execute=True, restart=None):
    global iNextToken, stack

    if restart:
        # we're in the middle of the iteration of a loop: reset iNextToken
        iNextToken = restart

    # remember where we are so the next iteration can repeat
    startPoint = iNextToken

    stack.append("while")

    if iNextToken < len(tokenStream) and tokenStream[iNextToken] == "(":
        iNextToken += 1
    else:
        error("Incomplete while statement.")

    result = expr()

    if iNextToken < len(tokenStream) and tokenStream[iNextToken] == ")":
        iNextToken += 1
    else:
        error("Incomplete while statement")

    # see ifStmt for logic
    if execute:
        statement(bool(result))
        # should only repeat when the inner statement is executed
        whileStmt(bool(result), startPoint)
    else:
        statement(False)

    stack.pop()


def returnStmt():
    global iNextToken, stack

    stack.append("return")
    if iNextToken < len(tokenStream):
        result = expr()
        closeStatement()
    else:
        error()

    stack.pop()
    return result


def expr():
    global iNextToken, stack

    stack.append("expr")
    # consume single conjunction
    result = conjunction()
    while iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "||"):
        iNextToken += 1  # consume ||
        value = conjunction()  # consume another conjunction

        # rather than keeping track of the type all throughout the expression, we
        # can just make sure the operations being performed have compatiable types
        typeCheck(result, value)
        result = result or conjunction

    stack.pop()
    return result


def conjunction():
    global iNextToken, stack

    stack.append("conjunction")
    result = equality()
    # as many equalities as separated by &&
    while iNextToken < len(tokenStream) and tokenStream[iNextToken] == "&&":
        iNextToken += 1
        value = equality()
        typeCheck(result, value)
        result = result and value

    stack.pop()
    return result


def equality():
    global iNextToken, stack

    stack.append("equality")
    result = relation()

    if iNextToken < len(tokenStream) and tokenStream[iNextToken] == "equOp":
        op = lexemeStream[iNextToken]
        iNextToken += 1
        value = relation()
        typeCheck(result, value)
        result = operators[op](result, value)

    stack.pop()
    return result


def relation():
    global iNextToken, stack
    stack.append("relation")
    result = addition()

    if iNextToken < len(tokenStream) and tokenStream[iNextToken] == "relOp":
        compare = lexemeStream[iNextToken]
        iNextToken += 1
        value = addition()
        result = operators[compare](result, value)

    stack.pop()
    return result


def addition():
    global iNextToken, stack

    stack.append("addition")

    result = term()  # Consume a Term first
    while iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "addOp"):
        op = lexemeStream[iNextToken]
        iNextToken += 1  # Consumed the + or - token
        value = term()  # Consume another Term
        typeCheck(result, value)
        result = operators[op](result, value)

    stack.pop()
    return result


def term():
    global iNextToken, stack

    stack.append("term")

    result = factor()  # Consume a Factor
    while iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "multOp"):
            op = lexemeStream[iNextToken]
            iNextToken += 1  # Consumed the * or / token
            value = factor()  # Consume another Factor
            typeCheck(result, value)
            result = operators[op](result, value)

    stack.pop()
    return result


def factor():
    global iNextToken, stack

    stack.append("factor")

    if iNextToken < len(tokenStream):
        # check if any literal (char not implemented)
        if tokenStream[iNextToken] == "intLiteral":
            iNextToken += 1
            stack.pop()
            return int(lexemeStream[iNextToken - 1])
        elif tokenStream[iNextToken] == "boolLiteral":
            iNextToken += 1
            stack.pop()
            return lexemeStream[iNextToken - 1]  # might need to convert?
        elif tokenStream[iNextToken] == "floatLiteral":
            iNextToken += 1
            stack.pop()
            return float(lexemeStream[iNextToken - 1])
        elif tokenStream[iNextToken] == "charLiteral":
            iNextToken += 1
            stack.pop()
            return lexemeStream[iNextToken - 1]
        elif tokenStream[iNextToken] == "(":
            # beginning of (Expression)
            iNextToken += 1
            value = expr()
            if iNextToken < len(tokenStream) and tokenStream[iNextToken] == ")":
                iNextToken += 1
                stack.pop()
                return value
            else:
                error("Expected closing parenthesis.")
        else:
            # id
            value = id(False)
            stack.pop()
            return value
    else:
        error()


def error(message=""):
    if message != "":
        print("Error: " + message + " Error location: < " + tokenStream[iNextToken] + ", " + lexemeStream[iNextToken] + " >.")
    elif iNextToken < len(tokenStream):
        print("Error: Invalid expression. Error location: < " + tokenStream[iNextToken] + "," + lexemeStream[iNextToken] + " >.")
    else:
        print("Error: Incomplete expression. Expecting more terms.")
    print "\nStack is:"
    for i in stack:
        print i + "->",
    exit()


def declarationError(varName):
    print("ERROR: Variable not declared: " + varName)
    exit()


# raise an error if the types of arguments are incompatible
def typeCheck(a, b):
    nums = [int, float]
    other = [bool, str]

    if type(a) in nums:
        if type(b) in other:
            error("Type error. Mismatched types.")
    elif type(b) in nums:
        error("Type error. Mismatched types.")


# To take command line argument for the file name
if __name__ == "__main__":
    main(sys.argv[1])

# Note that the execute parameter doesn't need to be passed to
# functions like printStmt & returnStmt, as they only deal with expressions,
# and expressions are not assignments, so nothing can be changed

# need:
"""
    some sort of flag to indicate if a given line should actually be executed (like if it's in the false part of an if statement)
    """
