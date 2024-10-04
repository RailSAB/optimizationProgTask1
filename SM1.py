import math

MAX_RATIO = 10 ** 7


def solve_llp(C: list, A: list, b: list, eps= 1e-3, res="max"):
    print_optimization_problem(C, A, b, res)
    tableau = initialize_tableau(C, A, b, res)
    try:
        solution, answers = simplex_method(tableau, b, eps)
        print(solution if res=="max" else -1*solution, answers, sep="\n")
    except Exception as e:
        print(repr(e))


def print_optimization_problem(C: list, A: list, b: list, res):
    # Print objective function
    objectiveFunction = f"{res} z = "
    for i, c in enumerate(C):
        if i != 0:
            objectiveFunction += f"+ {c}*x{i + 1} " if c >= 0 else f"- {c * -1}*x{i + 1} "
        else:
            objectiveFunction += f"{c}*x{i + 1} " if c >= 0 else f"{c}*x{i + 1} "
    print(objectiveFunction)
    # Print constraints
    print("subject to the constraints:")
    for i, a in enumerate(A):
        line = ""
        for k, c in enumerate(a):
            if k != 0:
                line += f"+ {c}*x{k + 1} " if c >= 0 else f"- {-1 * c}*x{k + 1} "
            else:
                line += f"{c}*x{k + 1} " if c >= 0 else f"{c}*x{k + 1} "
        line += f"<= {b[i]}"
        print(line)


def initialize_tableau(C, A, b, res):
    if res == "max":
        C = list(map(lambda x: x * -1, C))
    tableau = [C]
    tableau[0] += [0] * (len(b))

    for i in range(len(b)):
        tableau.append(A[i])
        tableau[-1] += [0] * i + [1] + [0] * (len(b) - i - 1)
        # tableau[-1] += [b[i]]
    return tableau


def simplex_method(tableau: list, b: list, eps):
    positionOfVariables = [0 for _ in range(len(tableau[0]) - len(b))]
    canIterate = False
    minimalCoefficient, position = find_min(tableau[0])
    if minimalCoefficient < 0:
        canIterate = True
    solution = 0

    while canIterate:
        # Finding leaving variable
        smallestRatio = MAX_RATIO
        leavingRow = 0
        for i in range(1, len(tableau)):
            ratio = b[i - 1] / tableau[i][position] if tableau[i][position] != 0 else -1
            if smallestRatio > ratio >= 0:
                smallestRatio = ratio
                leavingRow = i
        if smallestRatio == MAX_RATIO:
            raise ValueError("The method is not applicable!")
        # Change pivot row
        if position < len(positionOfVariables):
            positionOfVariables[position] = leavingRow
        k = tableau[leavingRow][position]
        tableau[leavingRow] = list(map(lambda x: x / k, tableau[leavingRow]))
        b[leavingRow - 1] /= k
        # Changing rows using triangle rule
        for i in range(len(tableau)):
            if i != leavingRow:
                coefficient = tableau[i][position] / tableau[leavingRow][position]
                tableau[i] = [tableau[i][k] - coefficient * tableau[leavingRow][k] for k in range(len(tableau[i]))]
                if i == 0:
                    solution -= coefficient * b[leavingRow - 1]
                else:
                    b[i - 1] -= coefficient * b[leavingRow - 1]

        minimalCoefficient, position = find_min(tableau[0])
        canIterate = True if minimalCoefficient < 0 else False


    x = []
    for i in positionOfVariables:
        x += [round(b[i-1], int(-1*math.log10(eps)))] if i != 0 else [0]
    return round(solution, int(-1*math.log10(eps))), x


def find_min(row: list):
    m = row[0]
    pos = 0
    for i in range(len(row)):
        if row[i] < m:
            m = row[i]
            pos = i
    return m, pos


# 1
# C = [5, 4]
# A = [[6, 4], [1, 2], [-1, 2], [0, 1]]
# b = [24, 6, 1, 2]
# solve_llp(C, A, b)
#Answer
# max z = 5*x1 + 4*x2
# subject to the constraints:
# 6*x1 + 4*x2 <= 24
# 1*x1 + 2*x2 <= 6
# -1*x1 + 2*x2 <= 1
# 0*x1 + 1*x2 <= 2
# 21.0
# [3.0, 1.5]

#2
# C = [10, 20]
# A = [[-1, 2], [1, 1], [5, 3]]
# b = [15, 12, 45]
# solve_llp(C, A, b)
#Answer
# max z = 10*x1 + 20*x2
# subject to the constraints:
# -1*x1 + 2*x2 <= 15
# 1*x1 + 1*x2 <= 12
# 5*x1 + 3*x2 <= 45
# 210.0
# [3.0, 9.0]


#3
# C = [9, 10, 16]
# A = [[18, 15, 12], [6, 4, 8], [5, 3, 3]]
# b = [360, 192, 180]
# solve_llp(C, A, b)
# Answer
# max z = 9*x1 + 10*x2 + 16*x3
# subject to the constraints:
# 18*x1 + 15*x2 + 12*x3 <= 360
# 6*x1 + 4*x2 + 8*x3 <= 192
# 5*x1 + 3*x2 + 3*x3 <= 180
# 400.0
# [0, 8.0, 20.0]


#4
# C = [-2, 2, -6]
# A = [[2, 1, -2], [1, 2, 4], [1, -1, 2]]
# b = [24, 23, 10]
# solve_llp(C, A, b, res="min")
# Answer
# min z = -2*x1 + 2*x2 - 6*x3
# subject to the constraints:
# 2*x1 + 1*x2 - 2*x3 <= 24
# 1*x1 + 2*x2 + 4*x3 <= 23
# 1*x1 - 1*x2 + 2*x3 <= 10
# -30.75
# [0, 0.75, 5.375]


