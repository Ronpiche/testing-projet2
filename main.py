import utils
import rule
import sys

if __name__ == '__main__':

    #check if a sudoku file was given
    if (utils.file_exist("sudoku.txt")):
        sudoku = utils.read_sudoku("sudoku.txt")
	print("Sudoku grid found:")
	print("=========")
	print( utils.read_file("sudoku.txt") )
	print("=========")
    else:
        sys.exit("Error no sudoku.txt file found in the same directory")

    recalculateBasicRules =False
    try:
        if (sys.argv[1] =="-r"):
            recalculateBasicRules = True
    except:
        recalculateBasicRules = False

    #check if the basic rules were generated
    if ( not utils.file_exist("basic_rules.txt") or recalculateBasicRules ):
	print("basic rules for sudoku calculated and wrote inside basic_rules.txt")
        rule.write_basic_rules()
    else:
	print("basic rules for sudoku read from existing basic_rules.txt")

    #rules for this sudoku
    sudokuRules =rule.create_sudoku_rules(sudoku)
    print("rule for this sudoku calculated")

    #rules for all sudoku
    basicRules = rule.read_basic_rules()

    #combined both rules
    satRules = basicRules +"\n" +sudokuRules[:-1]+";"

    #give our rules to logic2cnf then to SAT
    print("rule send to logic2cnf and minisat")
    utils.send_to_logic2cnf(satRules)

    #write our solution in sudoku_solved.txt
    utils.solve_sudoku()
    print("sudoku solved, the solution is:")
    print("=========")
    print( utils.read_file("sudoku_solved.txt") )
    print("=========")

    #create our Solution.txt file for this probleme
    if (not utils.file_exist("Solution.txt")):
        utils.create_solution_file(basicRules)