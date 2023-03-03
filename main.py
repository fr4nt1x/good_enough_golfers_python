from GeneticSolver import GeneticSolver
# import timeit


def call():
    solver = GeneticSolver(
        numberOfGroups=10, sizeOfGroups=5, numberOfRounds=5)
    result = solver.solve()
    print(result)


if __name__ == "__main__":
    # result = timeit.timeit(
    #     stmt="call()", setup="from __main__ import call", number=5)
    # print(result)
    call()
