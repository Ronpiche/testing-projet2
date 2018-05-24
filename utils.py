import sys
import os

def read_file_lines(fileName):
    f= open(fileName,"r")
    data = f.readlines()
    f.close()
    return data

def read_file(fileName):
    f= open(fileName,"r")
    data = f.read()
    f.close()
    return data

def file_exist(file):
    try:
        f = open(file, "r")
        f.close()
    except:
        return False
    else:
        return True

def read_sudoku(fileName):
    file = read_file_lines(fileName)
    sudoku = [[1 for x in range(10)] for y in range(10)]

    isValid = True
    #check if the size is correct
    if (len(file) != 9):
        isValid = False
    else:
        for i in range( len(file) ):
            file[i] = file[i].replace("\n","")
            # check if the size is correct
            #if(len(file[i]) != 9):
                #isValid = False
    if (isValid):
        for x in range(1,10):
            for y in range(1, 10):
                sudoku[x][y] = int(file[x-1][y-1])
        return sudoku
    else:
        sys.exit("ERROR: invalide sudoku file")

def send_to_logic2cnf(rules):
    #save rule
    file = open("logic2cnf_data", "w")
    data = file.write(rules)
    file.close()
    #execute logic2cnf with our rule
    os.system("logic2cnf -c logic2cnf_data > logic2cnf_output")
    os.system("./minisat logic2cnf_output minisat_output")
    return

def get_var_ref_from_logic2cnf_output():
    f = open("logic2cnf_output", "r")
    data = f.readlines()
    f.close()
    refValue = dict()
    for i in range(len(data)):
        if ( "v" in data[i] ):
            temp = data[i][5:].split("=")
            refValue[temp[1].replace("\n","").replace(" ","")] =temp[0]
    #print(refValue)
    return  refValue

def get_var_value_from_minisat_output():
    try:	
	    f = open("minisat_output", "r")
	    data = f.readlines()
	    f.close()
	    varValue = dict()
	    temp = data[1].split(' ')
	    for i in range(len(temp)):
	        if ( "-" in temp[i]):
	            varValue[temp[i].replace("-","")] =False
	        else:
	            varValue[temp[i]] = True
    	    return varValue
    except:
	      sys.exit("\nSorry this sudoku can't be solved")

def write_solution(sudokuSoluce):
    n = ""
    for x in range(1,10):
        for y in range(1,10):
            n += sudokuSoluce[x][y]
        n +="\n"
    n =n[:-1]
    f =open("sudoku_solved.txt","w")
    f.write(n)
    f.close()

def solve_sudoku():
    refVal = get_var_ref_from_logic2cnf_output()
    varVal = get_var_value_from_minisat_output()
    get_var_value_from_minisat_output()
    sudokuVarSoluce = [[1 for x in range(10)] for y in range(10)]
    i =0
    for x in range(1,10):
        for y in range(1,10):
            for n in range(1,10):
                currentVar = "v"+str(x) +str(y) +str(n)
                if ( varVal[refVal[currentVar].replace(" ","")  ] == True):
                    sudokuVarSoluce[x][y] = currentVar[3:4]
                    i = i+1
    write_solution(sudokuVarSoluce)
    return sudokuVarSoluce

def create_solution_file(basicRules):
    text  = "===============================================================\n"\
            "Partie 2: specification au moyen de la logique propositionnelle\n"\
            "===============================================================\n"\
            "Vianney Guison\n"                                                 \
            "===============================================================\n"\
            "Le programme doit etre appele en executant la fonction main.py\n" \
            "vous devez fournir un fichier sudoku.txt dans le meme dossier \n" \
            "pour coder la grille de sudoku, ajouter -r pour recalculer les regles basic d'un sudoku.\n" \
            "Apres execution la solution se situera dans le fichier sudoku_solved.txt.\n" \
	    "===============================================================\n"\
            "La liste des variables propositionnelles qui modelisent le probleme sont:\n"
    var =""
    for x in range(1,10):
            for y in range(1, 10):
                for n in range(1, 10):
                    var += "v" + str(x) + str(y) + str(n) +" "
    text += var
    text +="\nChaque variable 'vxyn' represente une case possible de la grille\n" \
           "v: est la car logic2cnf n'accepte pas un nombre comme variable\n" \
           "x: Le premier nombre represente la position en x sur la grille\n" \
           "y: Le deuxieme nombre represente la position en y sur la grille\n" \
           "n: le troisieme nombre la valeur de la case\n" \
           "===============================================================\n" \
           "Les formules propositionnelles qui expriment les contraintes que doit respecter une grille correctement resolue sont:\n \n"
    text +=basicRules
    file = open("Solution.txt","w")
    file.write(text)
    file.close()
