from formulation import *

class Solution:
    def __init__(self, num_projs, num_colaborators):
        self.num_colaborators = num_colaborators
        self.num_projs = num_projs
        self.solution = [random.randint(0,1) for _ in range(num_projs * num_colaborators)]

    def evaluate(self, solution) -> int:
        return sum(solution) 

    def neighbour1(self, solution):
        """Change the value of one slot"""
        slot = random.randrange(len(solution))
        new_value = random.randint(0,1)
                
        solution[slot] = new_value
        
        return solution


    def neighbour2(self, solution):
        """Exchange the slots of two slots"""
        size = len(solution)
        slot1 = random.randrange(size)
        slot2 = random.randrange(size)

        new_value1 = random.randint(0,1)
        new_value2 = random.randint(0,1)

        solution[slot1], solution[slot2] = new_value1, new_value2
        
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
            neighbour = self.neighbour3(solution.copy())
            it += 1
            evaluation = self.evaluate(neighbour)
            ev.append(evaluation)

            if evaluation > self.evaluate(solution):
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
            T = self.T_schedule(T)
            neighbour = self.neighbour3(solution.copy())
            evaluation = self.evaluate(neighbour)
            delta = evaluation - self.evaluate(solution)
            it += 1
            ev.append(evaluation)

            if delta > 0 or exp(delta / T) > random.random():
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
            population.append([random.randint(0,1) for _ in range(self.num_projs * self.num_colaborators)])
            #population.append([])
            #for j in range(self.num_colaborators * self.num_projs): # n chromossomes for each project
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
        elite = population[index]   # actual element
        
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
                child = population[parent1][:round(total_population/2)] + population[parent2][round(total_population/2):]
                self.mutation(child)
                new_population.append(child)

        
        return new_population, top_fit


    def mutation(self, chromosome):
        percentage = 0.05
        for i in range(len(chromosome)):
            if random.random() < percentage:
                if(chromosome[i] == 1):
                    chromosome[i] = 0
                else:
                    chromosome[i] = 1


