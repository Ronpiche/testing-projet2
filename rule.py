import sys

def write_basic_rules ():
    case = [[[1 for x in range(10)] for y in range(10)]for n in range(10)]
    satRules =""
    #var declaration
    satVarDeclaration  ="def"

    #There is at least one number in each entry:
    satRulesNoEmptyCase ="#There is at least one number in each entry: \n"
    for x in range(1,10):
            for y in range(1, 10):
                singleRuleNoEmptyCase ="("
                for n in range(1, 10):
                    case[x][y][n] = "v" + str(x) + str(y) + str(n)
                    satVarDeclaration += " " + case[x][y][n]
                    singleRuleNoEmptyCase += "v"+ str(x) + str(y) + str(n) +"+"
                singleRuleNoEmptyCase = singleRuleNoEmptyCase[:-1]
                singleRuleNoEmptyCase += ")." +"\n"
                satRulesNoEmptyCase +=singleRuleNoEmptyCase

    #Each number appears at most once in each row:
    satRulesAppearAtMostRow ="#Each number appears at most once in each row: \n"
    #Each number appears at most once in each column:
    satRulesAppearAtMostColumn   ="#Each number appears at most once in each column: \n"
    #Each number appears at most once in each 3x3 sub-grid:
    satRulesApperAtMostSubGrid ="#Each number appears at most once in each 3x3 sub-grid: \n"
    for x in range(1,10):
            for y in range(1, 10):
                for n in range(1, 10):

                    #row appear at most rule
                    singleRuleAppearAtMostRow = "(" + case[x][y][n] + " => ("
                    for x2 in range(1, 10):
                        if (x2 !=x):
                            singleRuleAppearAtMostRow += "~" + "v" + str(x2) + str(y) + str(n) +"."

                    singleRuleAppearAtMostRow = singleRuleAppearAtMostRow[:-1]  # pop last point
                    singleRuleAppearAtMostRow += "))." +"\n"
                    satRulesAppearAtMostRow += singleRuleAppearAtMostRow

                    #column appear at most column
                    singleRuleAppearAtMostColumn = "(" + case[x][y][n] + " => ("
                    for y2 in range(1, 10):
                        if (y2 != y):
                            singleRuleAppearAtMostColumn += "~" + "v" + str(x) + str(y2) + str(n) +"."

                    singleRuleAppearAtMostColumn = singleRuleAppearAtMostColumn[:-1]  # pop last point
                    singleRuleAppearAtMostColumn += "))." +"\n"
                    satRulesAppearAtMostColumn += singleRuleAppearAtMostColumn

                    #subGrid appear at most
                    xStartSubGrid = get_starting_indice(x)
                    yStartSubGrid = get_starting_indice(y)
                    singleRuleAppearAtMostSubGrid = "(" + case[x][y][n] + " => ("

                    for x2 in range(xStartSubGrid, xStartSubGrid +3):
                        for y2 in range(yStartSubGrid, yStartSubGrid +3):
                            if ((x2 != x) or (y2 != y)):
                                singleRuleAppearAtMostSubGrid += "~" + "v" + str(x2) + str(y2) + str(n) +"."

                    singleRuleAppearAtMostSubGrid =singleRuleAppearAtMostSubGrid[:-1]#pop last point
                    singleRuleAppearAtMostSubGrid +="))." +"\n"
                    satRulesApperAtMostSubGrid += singleRuleAppearAtMostSubGrid

    # There is at most one number in each entry:
    satRulesAtMostOnePerCase = "#There is at most one number in each entry: \n"
    for x in range(1, 10):
        for y in range(1, 10):
            for n in range(1, 10):
                singleAtMostOnePerCase = "(" + "v" + str(x) + str(y) + str(n) + " => ("
                for n2 in range(1, 10):
                    if (n != n2):
                        singleAtMostOnePerCase += "~v" + str(x) + str(y) + str(n2) + "."
                singleAtMostOnePerCase = singleAtMostOnePerCase[:-1]
                singleAtMostOnePerCase += ") )." + "\n"
                satRulesAtMostOnePerCase += singleAtMostOnePerCase

    # Each number appears at least once in each row:
    satRulesAtLeastOnceRow ="# Each number appears at least once in each row: \n"
    # Each number appears at least once in each column:
    satRulesAtLeastOnceColumn = "# Each number appears at least once in each column: \n"
    # Each number appears at least once in each sub grid:
    satRulesAtLeastOnceSubGrid = "# Each number appears at least once in each sub grid: \n"
    for n in range(1, 10):
        #go through every column and row
        for a in range(1,10):
            singleRuleAtLeastOnceRow ="("
            singleRuleAtLeastOnceColumn = "("
            for b in range(1, 10):
                singleRuleAtLeastOnceRow += "v" + str(a) + str(b) + str(n) + "+"
                singleRuleAtLeastOnceColumn += "v" + str(b) + str(a) + str(n) + "+"

            singleRuleAtLeastOnceRow =singleRuleAtLeastOnceRow[:-1]#pop last +
            singleRuleAtLeastOnceRow +=")." +"\n"
            singleRuleAtLeastOnceColumn = singleRuleAtLeastOnceColumn[:-1]  # pop last +
            singleRuleAtLeastOnceColumn += ")." +"\n"
            satRulesAtLeastOnceRow += singleRuleAtLeastOnceRow
            satRulesAtLeastOnceColumn += singleRuleAtLeastOnceColumn
        #go through every sub grid
        for x in [1,4,7]:
            for y in [1,4,7]:
                singleRuleAtLeastOnceSubGrid ="("
                for x2 in range(x, x+3):
                    for y2 in range(y,y+3):
                        singleRuleAtLeastOnceSubGrid += "v" + str(x2) + str(y2) + str(n) + "+"
                singleRuleAtLeastOnceSubGrid = singleRuleAtLeastOnceSubGrid[:-1]
                singleRuleAtLeastOnceSubGrid += ")." +"\n"
                satRulesAtLeastOnceSubGrid += singleRuleAtLeastOnceSubGrid

    satVarDeclaration +=";"
    #satRulesApperAtMostSubGrid=satRulesApperAtMostSubGrid[:-2]#pop last point and \n of the last rule
    #combine our rule
    satRules = satVarDeclaration + "\n" + satRulesNoEmptyCase + "\n"
    satRules += satRulesAppearAtMostRow + "\n" + satRulesAppearAtMostColumn + "\n" + satRulesApperAtMostSubGrid + "\n"
    satRules += satRulesAtMostOnePerCase + "\n"
    satRules += satRulesAtLeastOnceRow +"\n" + satRulesAtLeastOnceColumn +"\n" + satRulesAtLeastOnceSubGrid
    #write our rule
    file = open("basic_rules.txt", "w")
    file.write(satRules)
    file.close()
    return 1

def create_sudoku_rules(sudoku):
    sudokuRules =""
    for x in range(1, 10):
        for y in range(1, 10):
            if (sudoku[x][y] != 0):
                sudokuRules += "v" + str(x)+str(y)+str(sudoku[x][y]) +"."
    return sudokuRules

def get_starting_indice(i):
    if (i in range(1,4)):
        return 1
    elif (i in range(4,7) ):
        return 4
    elif (i in range(7,10)):
        return 7

def read_basic_rules():
    file = open("basic_rules.txt", "r")
    data =file.read()
    file.close()
    return data