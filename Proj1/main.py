from algorithms import *


if __name__ == "__main__":

    sol = Solution(3, 3)

    print(sol.solution)

    sol1, hill_evals = sol.hill_climbing()
    print("Last value with hill climbing was ", sol1)

    sol2, annealing_evals = sol.simulated_annealing()
    print("Last value with simulated annealing was ", sol2)

    sol3, genetic_evals = sol.genetic_algorithm()


    plt.plot(hill_evals, 'g', label='Hill Climbing')
    plt.plot(annealing_evals, 'b', label='Simulated Annealing')
    plt.plot(genetic_evals, 'r', label='Genetic Algorithm')

    #plt.title('Title')

    plt.xlabel('iteration')

    plt.ylabel('cost')

    plt.legend()

    plt.show()

    
