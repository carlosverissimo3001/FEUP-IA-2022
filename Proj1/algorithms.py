from formulation import *

class Solution:
    def __init__(self, num_projs, num_collaborators):
        self.num_collaborators = num_collaborators
        self.num_projs = num_projs
        self.solution = []
        for _ in range (num_projs):
            self.solution.append([random.randint(0,1) for _ in range(num_collaborators)])

    def evaluate(self, solution) -> int:
        temp = ( sum(solution[0]) + sum(solution[1]) + sum(solution[2]) )
        return temp

    def neighbour1(self, solution):
        """Change the value of one slot"""
        proj = random.randrange(self.num_projs)
        collab = random.randrange(self.num_collaborators)

        if solution[proj][collab] == 1:
            solution[proj][collab] = 0
        else:
            solution[proj][collab] = 1
        
        return solution


    def neighbour2(self, solution):
        """Exchange the slots of two slots"""
        size = self.num_projs
        collabs_num = self.num_collaborators

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

    def genetic_algorithm(self, size_of_population):
        ev = []

        population = self.create_initial_population(size_of_population)

        it = 0
        while it < 100:
            it += 1

            population, current_best = self.generate_next_population(population)

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
            #population.append([random.randint(0,1) for _ in range(self.num_projs * self.num_collaborators)])
            temp = []
            for _ in range (self.num_projs):
                temp.append([random.randint(0,1) for _ in range(self.num_collaborators)])
            population.append(temp)
        
            #population.append([])
            #for j in range(self.num_collaborators * self.num_projs): # n chromossomes for each project
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

    def roulette_selection(fitness, population_size):
        return 5, 6


    #dar outro nome a crossover e criar outra funçao crossover para combinar os dois pais
    def generate_next_population(self, population):
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
                parent1, parent2 = self.select_parents(fitness, 1)  #mudar 2 argumento para input
                child = population[parent1][:round(self.num_projs/2)] + population[parent2][round(self.num_projs/2):]
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


