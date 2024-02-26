import argparse
import json
import sys
import logging

import sympy
from fractions import Fraction
import random

def generateMatrix(seed):
    logging.info("Beggining generation of matrix")
    eigval = sympy.Array([Fraction(random.randint(-5,5), Fraction(random.randint(1,2))), 
                          Fraction(random.randint(-5,5), Fraction(random.randint(1,2))), 
                          Fraction(random.randint(-5,5), Fraction(random.randint(1,2)))])
    D = sympy.diag(*eigval)
    logging.info("generateMatrix | Generated D matrix : " + str(D))

    P = sympy.randMatrix(3, 3, seed=seed, min=-5, max=5)
    while (sympy.det(P) == 0):
        P = sympy.simplify(P + sympy.eye(3))
    logging.info("generateMatrix | Generated P matrix : " + str(P))

    Pinv = P.inv()

    M = P * D * Pinv

    logging.info("generateMatrix | Generated M matrix : " + str(M))

    # Test pour réduire les valeurs des éléments de M en dessous de 100

    # Créer une matrice non diag

    logging.info("generateMatrix | Returning generation of matrix")
    return P, D, M

def isDiag(M):
    return (sympy.det(M) != 0)

# On renvoie la correction élément par élément (que ce soient valeurs propres ou vecteurs propres), dans le même format que l'entrée
# Si la valeur est bonne, un None se trouve à la place de la valeur ; sinon la valeur correcte

def matchInputWithEigen(input, P, D):
    logging.info("Beggining match")
    logging.info("matchInputWithEigen | Input value : " +  str(input))

    correct = {}
    for i in range(len(D.tolist())):
        if (D[i,i] in correct.keys()):
            old_entry = correct[D[i,i]]
            correct.update({D[i,i] : old_entry + [P.row(i).tolist()[0]]})
        else :
            correct.update({D[i,i] : [P.row(i).tolist()[0]]})
    logging.info("matchInputWithEigen | Real answer built : " +  str(correct))

    ans = {}
    for eigval in correct.keys():
        if eigval in input.keys(): 
            for vect in input[eigval] :
                if (eigval in ans.keys()):
                    old_entry = ans[eigval]
                    ans.update({eigval : (True, old_entry + [(vect, vect in correct[eigval])])})
                else :
                    ans.update({eigval : (True, [(vect, vect in correct[eigval])])})
        else :
            ans.update({eigval : (False, correct[eigval])})
        
    logging.info("matchInputWithEigen | Returning correction : " + str(ans))

    return ans
    

#--------------------------------
#-------- Main Section ----------
#--------------------------------
    
def parse_arguments():
    parser = argparse.ArgumentParser(description="Manipulation de matrices")

    # Argument d'état
    parser.add_argument("state", choices=["start", "step1", "step2"], help="État du programme")

    # Arguments pour l'état step1
    parser.add_argument("--seed", type=int, help="Seed pour l'état step1")

    parser.add_argument("--is_diag", action="store_true", help="Booléen pour l'état step1")

    # Arguments pour l'état step2
    parser.add_argument("--eigen", help="Dictionnaire JSON pour l'état step2")

    args = parser.parse_args()

    if args.state == "step1":
        if args.seed is None or args.is_diag is None:
            parser.error("--seed est requis pour l'état step1")
    elif args.state == "step2":
        if args.seed is None or args.eigen is None:
            parser.error("--eigen est requis pour l'état step2")

    return args

def main():
    logging.basicConfig(filename='matrixDiag.log', encoding='utf-8', level=logging.DEBUG)
    args = parse_arguments()
    
    if args.state == "start":
        seed = random.randint(0, 999999)
        logging.info("Generating matrix diag with seed " + str(seed))

        P,D,M = generateMatrix(args.seed)

        matrixAsList = M.tolist()
        matrixAsList = list(map((lambda vect : 
                                list(map((lambda frac : [frac.numerator, frac.denominator]),
                                    vect))
                            ),
                            matrixAsList 
                        ))
        print({"seed" : str(seed),
                "matrix" : matrixAsList})
        sys.stdout.flush()

    elif args.state == "step1":
        logging.info("Solving step 1 of matrix diag with seed " + str(args.seed))
        logging.info("Input : is diag = " + str(args.is_diag))
        # random.seed(args.seed)
        random.seed(random.randint(0, 9999))

        P,D,M = generateMatrix(args.seed)
        val = (isDiag(M) == args.is_diag)

        print(args.seed)
        print(sympy.det(M))
        print(val)
        sys.stdout.flush()


    elif args.state == "step2":
        logging.info("Solving step 2 of matrix diag with seed " + str(args.seed))
        logging.info("Input : eigens = " + str(args.eigen))
        eigen_input = json.loads(args.eigen)
        eigen_input = {int(k):v for k,v in eigen_input.items()}
        random.seed(args.seed)

        P,D,M = generateMatrix(args.seed)
        ans = matchInputWithEigen(eigen_input, P, D)

        print(ans)
        print(args.seed)
        sys.stdout.flush()

if __name__ == "__main__":
    main()