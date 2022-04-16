from formulation import *
import numpy as np

class Solution:
    def __init__(self, team):
        self.team = team
        self.solution = []
        for _ in range (team.n_projects):
            #self.solution.append([random.randint(0,1) for _ in range(team.n_members)])
            self.solution.append([0 for _ in range(team.n_members)])

    def evaluate(self, solution) -> int:
        print("NEIGHBOUR: ", solution)
        #return (sum(solution[0]) + sum(solution[1]) + sum(solution[2]) + sum(solution[3]))
        
        project_timer = []
        #Initialization
        for i in range(len(solution)):
            project_timer.append(0)

        days = 0                # Number of days passed 
        score = 0               # Score of the completed projects
        delta = 0               # Time passed without a project starting
        completed_projects = 0  # Number of completed projects
        unfinished_projects = 0 # Number of unfinished projects
        started_projects = 0    # Number of started projects
        solution_members = []   # Members that were chosen to test a given project requirements
        penalties = 0           # Score penalties
        
        i = 0         
        while True:
            delta += 1
            days += 1

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
                        print(project.name, "has started!")
                        #print("-------------------------\n")
                        project_timer[i] += 1
                        started_projects += 1
                        unfinished_projects += 1
                        delta = 0

                # If the project has started start the timers
                else:
                    project_timer[i] += 1
                    # If the project's duration is over
                    if project_timer[i] == project.duration:
                        project.is_over = True
                        project.has_started = False
                        score += project.score
                        unfinished_projects -= 1
                        completed_projects += 1

                        #Unlocking members
                        for member in solution_members:
                            if member.working_on == i:
                                member.reset()
            
            # If all projects get completed
            if completed_projects == self.team.n_projects:
                break
            
            # In case a new project doesn't start in a few days, stop
            elif delta > 5 and not unfinished_projects:
                break
        
        self.team.reset()
        #print("Score: ", score, " Days: ", days, "Penalties:", penalties, "Total:", 1000 + score/days + penalties)
        return 1000 - score/days + penalties

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
                ev.append(evaluation)
                solution = neighbour
                it = 0
                if evaluation > best_sol_eval:
                    #all time best
                    best_sol = neighbour
                    best_sol_eval = evaluation

        return best_sol, ev

    def simulated_annealing(self):
        ev = []

        best_sol = []
        best_sol_eval = 0

        solution = self.solution.copy()
        it = 0
        T = 1000

        while it < 100:
            it += 1

            T = self.T_schedule(T)
            neighbour = self.neighbour3(copy.deepcopy(solution))
            evaluation = self.evaluate(neighbour)
            delta = evaluation - self.evaluate(solution)

            if delta > 0 or exp(delta / T) > random.random():
                ev.append(evaluation)
                solution = neighbour
                if evaluation > best_sol_eval:
                    #all time best
                    best_sol = neighbour
                    best_sol_eval = evaluation

        return best_sol, ev

    def T_schedule(self, T):
        return 0.90 * T

    def genetic_algorithm(self, size_of_population, parents_algorithm):
        ev = []

        population = self.create_initial_population(size_of_population)

        it = 0
        while it < 100:
            it += 1

            population, current_best = self.generate_next_population(population, parents_algorithm)

            ev.append(current_best)

        #check the best of the final solution
        fitness = self.evaluate_fitness(population)

        top_fit = max(fitness)  # value of the fittest element
        index = fitness.index(top_fit) # most fit element index
        all_time_best = population[index]   # actual element

        ev.append(top_fit)

        return all_time_best, ev

    def tabu_tenure(self):
        return 3

    def tabu_search(self):
        tabu_list = []
        counters = []
        ev = []
        iteration = 0

        solution = self.solution.copy()
        neighbour = self.neighbour3(copy.deepcopy(solution))
        best_sol = neighbour
        ev.append(self.evaluate(best_sol))


        while iteration < 100:
            iteration += 1
            neighbour = self.neighbour3(copy.deepcopy(neighbour))
            evaluation = self.evaluate(neighbour)
            ev.append(evaluation)

            if neighbour not in tabu_list:
                tabu_list.append(neighbour)
                counters.append([neighbour.copy(), self.tabu_tenure()])
                if evaluation > self.evaluate(best_sol):
                    best_sol = neighbour

            else:
                for k in range(len(counters)):
                    counters[k][1] -= 1
                    if counters[k][1] == 0:
                        tabu_list.remove(counters[k][0])

        return best_sol, ev


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
    def generate_next_population(self, population, parents_algorithm):
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
                child = population[parent1][:round(self.team.n_projects/2)] + population[parent2][round(self.team.n_projects/2):]
                self.mutation(child)
                new_population.append(child)


        return new_population, top_fit


    def mutation(self, chromosome):
        percentage = 0.05
        for i in range(len(chromosome)):
            for j in range (len(chromosome[0])):
                if random.random() < percentage:
                    if(chromosome[i][j] == 1):
                        chromosome[i][j] = 0
                    else:
                        chromosome[i][j] = 1

