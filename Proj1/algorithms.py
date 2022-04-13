from formulation import *
import numpy as np

class Solution:
    def __init__(self, team):
        self.team = team
        self.solution = []
        for _ in range (team.n_projects):
            #self.solution.append([random.randint(0,1) for _ in range(team.n_members)])
            self.solution.append([0 for _ in range(team.n_members)])

    #(sum(solution[0]) + sum(solution[1]) + sum(solution[2]))
    def evaluate(self, solution) -> int:
        days = 0
        score = 0
        completed = 0
        counters = []
        started = 0

        no_projects = len(solution)
        no_members = len(solution[0])

        for i in range(no_projects):
            counters.append(0)

        #For each day
        while True:
            # If on the iteration 1, no project has started, break out of the loop
            if completed == no_projects:
                break

            days += 1

            #For each project
            for i in range(no_projects):
                project = self.team.projects[i]

                #Check whether it started or not
                if not project.has_started and not project.is_over:
                    project.has_started = project.check_requirements(self.team, i, solution[i])
                    if project.has_started:
                        print("Project " + str(i) + " has started!")
                        counters[i] += 1
                        started += 1

                else:
                    #If the project has ended
                    if counters[i] == project.duration:
                        score += project.score
                        completed += 1
                        project.is_over = True

                        #Unlock each member
                        #NEEDTO INCREMENT THE SKILL LEVEL
                        for k in range(no_members):
                            if self.team.members[k].working_on == i:
                                self.team.members[k].working_on = -1
                                self.team.members[k].on_project = False
                                #self.team.members[k].skills

                    #Otherwise, another day goes on
                    else:
                        counters[i] += 1

            if not started:
                return -1

        return days

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

