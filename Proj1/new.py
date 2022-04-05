from formulation import *

class Solution:
    def __init__(self, num_projs, num_colaborators):
        self.num_colaborators = num_colaborators
        self.num_projs = num_projs
        self.solution = [random.randint(0,1) for _ in range(num_projs * num_colaborators)]

    def evaluate(self, solution) -> int:
        return sum(solution) * math.sqrt(solution[3]) / 1.7

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

        while it < 100:
            neighbour = self.neighbour3(solution.copy())
            it += 1
            evaluation = self.evaluate(neighbour)
            ev.append(evaluation)

            if evaluation > self.evaluate(solution):
                solution = neighbour
                it = 0

        return solution, ev

    def simulated_annealing(self):
        ev = []

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

        return solution, ev

    def T_schedule(self, T):
        return 0.90 * T

    def genetic_algorithm(self):
        ev = []
        size_of_population = 8

        population = self.create_initial_population(size_of_population)

        it = 0
        while it < 100:
            it += 1
            fitness = self.evaluate_fitness(population)
            x, y = self.select_parents(population)

            index = fitness.index(max(fitness)) # most fit element
            elite = population[index]

            ev.append(max(fitness))


            population = self.crossover(population, x, y, elite)

            #self.mutation(population, size_of_population)

        return elite, ev



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

    def select_parents(self, fitness):
        #choose elements for tournament
        el1 = random.randrange(0, 7)
        el2 = random.randrange(0, 7)
        el3 = random.randrange(0, 7)
        el4 = random.randrange(0, 7)

        if fitness[el1] > fitness[el2]:
            parent1 = el1
        else:
            parent1 = el2

        if fitness[el3] > fitness[el4]:
            parent2 = el3
        else:
            parent2 = el4

        return parent1, parent2


    def crossover(self, population, parent1, parent2, elite):
        new_population = []
        new_population.append(elite)
        new_population.append(population[random.randrange(0,7)])
        new_population.append(population[parent1][:4] + population[parent2][4:])
        new_population.append(population[parent2][:4] + population[parent1][4:])
        new_population.append(population[parent1][:6] + population[parent2][6:])
        new_population.append(population[parent2][:6] + population[parent1][6:])
        new_population.append(population[parent1][:2] + population[parent2][2:])
        new_population.append(population[parent2][:2] + population[parent1][2:])

        return new_population


    def mutation(self, population, size):
        percentage = 0.05
        for i in range(size):
            if random.random() > percentage:
                population[i][random.randrange(0, 7)] = random.randrange(2, 10)

