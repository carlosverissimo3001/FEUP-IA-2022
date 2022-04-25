import copy

class HillClimbing:
    def __init__(self, first_solution, neighbour_function, evaluation_function):
        self.solution = first_solution
        self.neighbour_function = neighbour_function
        self.evaluation_function = evaluation_function

    def run(self):
        ev = []
        solution = self.solution.copy()
        best_sol = []
        best_sol_eval = 0

        it = 0
        while it < 100:
            it += 1

            neighbour = self.neighbour_function(copy.deepcopy(solution))
            evaluation = self.evaluation_function(neighbour)

            if evaluation > self.evaluation_function(solution):
                solution = neighbour
                #it = 0
                if evaluation > best_sol_eval:
                    #all time best
                    best_sol = neighbour
                    best_sol_eval = evaluation

            ev.append(self.evaluation_function(solution))

        return best_sol, ev