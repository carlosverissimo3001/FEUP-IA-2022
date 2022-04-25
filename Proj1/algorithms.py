from formulation import *
import numpy as np

class Solution:
    def __init__(self, team):
        self.team = team
        self.solution = []
        for _ in range (team.n_projects):
            self.solution.append([random.randint(0,1) for _ in range(team.n_members)])
            #self.solution.append([0 for _ in range(team.n_members)])

    def evaluate(self, solution):
        if len(solution) == 0:
            return 0
        
       # print("NEIGHBOUR: ", solution)
        #return (sum(solution[0]) + sum(solution[1]) + sum(solution[2]) + sum(solution[3]))
        
        project_timer = []
        #Initialization
        for i in range(len(solution)):
            project_timer.append(0)

        score = 0               # Score of the completed projects
        unfinished_projects = 0 # Number of unfinished projects
        solution_members = []   # Members that were chosen to test a given project requirements
        penalties = 0           # Score penalties
        
        i = 0         
        while True:
            for i in range(self.team.n_projects):
                project = self.team.projects[i]
                solution_members.clear()

                if project.is_over:
                    continue
                
                for k in range(len(solution[i])):
                    if solution[i][k]:
                        solution_members.append(self.team.members[k])

                # Check if the project meets the requirements to start
                if not project.has_started:
                    #print(project.name, "has not started yet.")
                    penalties += project.check_requirements(i, solution_members)
                    if project.has_started:
                        project_timer[i] += 1
                        unfinished_projects += 1

                # If the project has started increment the timers
                else:
                    project_timer[i] += 1
                    # If the project's duration is over
                    if project_timer[i] == project.duration:
                        #print(project.name, "has ended in day: ", days)
                        project.is_over = True
                        project.has_started = False
                        score += project.score
                        unfinished_projects -= 1

                        #Unlocking members
                        for member in solution_members:
                            if member.working_on == i:
                                member.reset()
            
            # If all projects get completed
            if unfinished_projects == 0:
                break

        self.team.reset()
        #print("Score: ", score, "Penalties: ", penalties, "Total:", score - penalties)
        return score - penalties

    def neighbour1(self, solution):
        """Change the value of one slot"""
        proj = random.randrange(self.team.n_projects)
        collab = random.randrange(self.team.n_members)

        if solution[proj][collab] == 1:
            solution[proj][collab] = 0
        else:
            solution[proj][collab] = 1

        return solution

    def neighbour2(self, solution):
        """Exchange the slots of two slots"""
        size = self.team.n_projects
        collabs_num = self.team.n_members

        proj1 = random.randrange(size)
        proj2 = random.randrange(size)

        collab1 = random.randrange(collabs_num)
        collab2 = random.randrange(collabs_num)


        if solution[proj1][collab1] == 1:
            solution[proj1][collab1] = 0
        else:
            solution[proj1][collab1] = 1


        if solution[proj2][collab2] == 1:
            solution[proj2][collab2] = 0
        else:
            solution[proj2][collab2] = 1

        return solution

    def neighbour3(self, solution):
        """Change a discipline from slot or exchange the slots of two disciplines"""

        if random.choice([True, False]):
            return self.neighbour1(solution)

        else:
            return self.neighbour2(solution)


    def hill_climbing(self):
        ev = []
        solution = self.solution.copy()
        it = 0
        best_sol = []
        best_sol_eval = 0

        while it < 100:
            it += 1

            neighbour = self.neighbour3(copy.deepcopy(solution))
            evaluation = self.evaluate(neighbour)

            if evaluation > self.evaluate(solution):
                solution = neighbour
                #it = 0
                if evaluation > best_sol_eval:
                    #all time best
                    best_sol = neighbour
                    best_sol_eval = evaluation

            ev.append(self.evaluate(solution))

        return best_sol, ev

    def simulated_annealing(self, cooling_algorithm):
        ev = []

        best_sol = []
        best_sol_eval = 0

        solution = self.solution.copy()
        it = 0
        T0 = 50

        while it < 100:
            T = self.T_schedule(T0, it, cooling_algorithm)
            neighbour = self.neighbour3(copy.deepcopy(solution))
            evaluation = self.evaluate(neighbour)
            delta = float(evaluation - self.evaluate(solution))

            #print(delta / T, 'and', T, 'and', delta)

            it += 1
            
            if delta > 0 or random.random() < exp(delta / T):
                solution = neighbour
                if evaluation > best_sol_eval:
                    #all time best
                    best_sol = neighbour
                    best_sol_eval = evaluation

            ev.append(self.evaluate(solution))

        return best_sol, ev

    def T_schedule(self, T0, it, cooling_option):
        if(cooling_option == 1):
            return T0 * 0.80 ** it
        elif(cooling_option == 2):
            return T0 / (1 + 2 * math.log(1 + it))
        elif(cooling_option == 3):
            return T0 / (1 + 1 * it) 
        else:
            return T0 / (1 + 0.5 * it ** 2) 
        
    def tabu_tenure(self):
        return 10

    def tabu_neighbourhood(self, solution, tabus):
        neighbourhood = []
        for i in range(10):
            neighbour = self.neighbour3(copy.deepcopy(solution))
            while neighbour in neighbourhood:
                neighbour = self.neighbour3(copy.deepcopy(solution))
            
            #If the generated neighbour is not in the tabu list, add it
            if str(neighbour) not in tabus and neighbour not in neighbourhood:
                neighbourhood.append(neighbour)

        return neighbourhood
            

    def tabu_search(self):
        tabus = {}
        ev = []

        solution = self.solution.copy()
        best_sol = self.neighbour3(copy.deepcopy(solution))
        candidate_solution = best_sol
        ev.append(self.evaluate(best_sol))

        it = 0
        while it < 100: 
            # Generates a neighbourhood around the current best solution
            neighbourhood = self.tabu_neighbourhood(best_sol, tabus)
            
            # Searches the neighbourhood for a better solution than the one so far
            for temp_neighbour in neighbourhood:
                evaluation = self.evaluate(temp_neighbour)
                #print("Candidate: ", best_sol, evaluation, " Current: ", self.evaluate(best_sol))
                if evaluation > self.evaluate(candidate_solution):
                    candidate_solution = temp_neighbour

            # Checks if the local optima is greater than the global one
            evaluation = self.evaluate(candidate_solution)
            ev.append(evaluation)
            if evaluation > self.evaluate(best_sol):
                best_sol = candidate_solution
            
            # Decrements the counters for each tabu
            old_tabus = []
            for sol in tabus:
                tabus[str(sol)] -= 1
                if tabus[str(sol)] == 0:
                    old_tabus.append(str(sol))

            # Removes the null tabus
            for old in old_tabus:
                del tabus[old]

            old_tabus.clear()

            # Adds the new best neighbour of the neighbourhood to the tabu list
            tabus[str(candidate_solution)] = self.tabu_tenure()

            it += 1
            
        return best_sol, ev

    def genetic_algorithm(self, size_of_population, parents_algorithm, crossover_algortithm):
        ev = []

        population = self.create_initial_population(size_of_population)

        it = 0
        while it < 100:
            it += 1

            population, current_best = self.generate_next_population(population, parents_algorithm, crossover_algortithm)

            ev.append(current_best)

        #check the best of the final solution
        fitness = self.evaluate_fitness(population)

        top_fit = max(fitness)  # value of the fittest element
        index = fitness.index(top_fit) # most fit element index
        all_time_best = population[index]   # actual element

        ev.append(top_fit)

        return all_time_best, ev

    def create_initial_population(self, size):
        population = []

        for i in range(size):
            #population.append([random.randint(0,1) for _ in range(self.team.n_projects * self.team.n_members)])
            temp = []
            for _ in range (self.team.n_projects):
                temp.append([random.randint(0,1) for _ in range(self.team.n_members)])
            population.append(temp)

            #population.append([])
            #for j in range(self.team.n_members * self.team.n_projects): # n chromossomes for each project
            #    population[i].append(random.randint(0,1))

        return population

    def evaluate_fitness(self, population):
        fitness = []
        for i in range(len(population)):
            fitness.append(self.evaluate(population[i]))

        return fitness

    def select_parents(self, fitness, option):

        population_size = len(fitness)

        if(option == 1):
            return self.tournament_selection(fitness, population_size)
        else:
            return self.roulette_selection(fitness, population_size)


    def tournament_selection(self, fitness, population_size):

        #choose elements for tournament
        el1 = random.randrange(population_size)
        el2 = random.randrange(population_size)
        el3 = random.randrange(population_size)
        el4 = random.randrange(population_size)

        if fitness[el1] > fitness[el2]:
            parent1 = el1
        else:
            parent1 = el2

        if fitness[el3] > fitness[el4]:
            parent2 = el3
        else:
            parent2 = el4

        return parent1, parent2 # index of the parents

    def roulette_selection(self, fitness, population_size):

        # Computes the totallity of the population fitness
        population_fitness = sum(fitness)

        # Computes for each chromosome the probability
        chromosome_probabilities = [fitness[chromosome]/population_fitness for chromosome in range (population_size)]

        # Selects two elements of the fitness list based on the computed probabilities
        fit1 = np.random.choice(fitness, p=chromosome_probabilities)
        fit2 = np.random.choice(fitness, p=chromosome_probabilities)

        #finds the index of the parents
        parent1 = fitness.index(fit1)
        parent2 = fitness.index(fit2)

        return parent1, parent2


    #criar outra funçao crossover para combinar os dois pais
    def generate_next_population(self, population, parents_algorithm, crossover_algorithm):
        total_population = len(population)
        new_population = []


        fitness = self.evaluate_fitness(population)

        top_fit = max(fitness)  # value of the fittest element
        index = fitness.index(top_fit) # most fit element index
        elite = copy.deepcopy(population[index])   # actual element

        new_population.append(elite)


        for i in range (total_population - 1):
            if random.random() < 0.2:
                # randomly selected element passes to next generation
                parent = population[random.randrange(total_population)]
                self.mutation(parent)
                new_population.append(parent)
            else:
                #crossover between 2 parents
                parent1, parent2 = self.select_parents(fitness, parents_algorithm)
                # child = population[parent1][:round(self.team.n_projects/2)] + population[parent2][round(self.team.n_projects/2):]
                child = self.select_crossover(population[parent1], population[parent2], crossover_algorithm)
                self.mutation(child)
                new_population.append(child)


        return new_population, top_fit

    def select_crossover(self, parent1, parent2, choice):
        if choice == 1:
            return self.crossover1(parent1, parent2)
        elif choice == 2:
            return self.crossover2(parent1, parent2)
        else:
            return self.crossover3(parent1, parent2)


    def crossover1(self, parent1, parent2):
        return parent1[:round(self.team.n_projects/2)] + parent2[round(self.team.n_projects/2):]

    def crossover2(self, parent1, parent2):
        return parent2[:round(self.team.n_projects/2)] + parent1[round(self.team.n_projects/2):]

    def crossover3(self, parent1, parent2):
        if random.choice([True, False]):
            return self.crossover1(parent1, parent2)
        else:
            return self.crossover2(parent1, parent2)

    def mutation(self, chromosome):
        percentage = 0.05
        for i in range(len(chromosome)):
            for j in range (len(chromosome[0])):
                if random.random() < percentage:
                    if(chromosome[i][j] == 1):
                        chromosome[i][j] = 0
                    else:
                        chromosome[i][j] = 1

