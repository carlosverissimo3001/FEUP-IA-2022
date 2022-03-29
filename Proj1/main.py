import math

import numpy as np
import matplotlib.pyplot as plt

import copy
import random
from math import exp


class Semaphore:
    def __init__(self):
        self.greenTime = random.randrange(2, 10)
        self.redTime = random.randrange(2, 10)
        self.waitingCars = random.randrange(0, 30)
        self.increasingRate = random.randrange(1, 4)  # number of cars arriving to the semaphore per second


class Roundabout:
    def __init__(self):
        self.semaphores = []
        self.cars = 7
        self.number_semaphores = 4

    def add_to_list(self, semaphore):
        self.semaphores.append(semaphore)







class Solution:
    def __init__(self, sp1, sp2, sp3, sp4):
        
        self.solution = [sp1.greenTime, sp1.redTime, sp2.greenTime, sp2.redTime, sp3.greenTime, 
                         sp3.redTime, sp4.greenTime, sp4.redTime]

    def evaluate(self, solution) -> int:
        return sum(solution) * math.sqrt(solution[3]) / 1.7

    def neighbour1(self, rb, solution):
        """Change the value of one slot"""
        slot = random.randrange(rb.number_semaphores * 2)
        new_value = random.randrange(2, 10)
                
        solution[slot] = new_value
        
        return solution


    def neighbour2(self, rb, solution):
        """Exchange the slots of two slots"""
        slot1 = random.randrange(rb.number_semaphores * 2)
        slot2 = random.randrange(rb.number_semaphores * 2)

        new_value1 = random.randrange(2, 10)
        new_value2 = random.randrange(2, 10)

        solution[slot1], solution[slot2] = new_value1, new_value2
        
        return solution

    def neighbour3(self, rb, solution):
        """Change a discipline from slot or exchange the slots of two disciplines"""

        if random.choice([True, False]):
            return self.neighbour1(rb, solution)

        else:
            return self.neighbour2(rb, solution)

    def hill_climbing(self, rb):
        ev = []
        solution = self.solution.copy()
        it = 0

        while it < 100:
            neighbour = self.neighbour3(rb, solution.copy())
            it += 1
            evaluation = self.evaluate(neighbour)
            ev.append(evaluation)

            if evaluation > self.evaluate(solution):
                solution = neighbour
                it = 0

        return solution, ev

    def simulated_annealing(self, rb):
        ev = []

        solution = self.solution.copy()
        it = 0
        T = 1000

        while it < 100:
            T = self.T_schedule(T)
            neighbour = self.neighbour3(rb, solution.copy())
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
            population.append([])
            for j in range(8): # 8 chromosomes, two for each semaphore
                population[i].append(random.randrange(2, 10))

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




if __name__ == "__main__":
    semaphore1 = Semaphore()
    semaphore2 = Semaphore()
    semaphore3 = Semaphore()
    semaphore4 = Semaphore()

    roundabout = Roundabout()
    roundabout.add_to_list(semaphore1)
    roundabout.add_to_list(semaphore2)
    roundabout.add_to_list(semaphore3)
    roundabout.add_to_list(semaphore4)

    sol = Solution(semaphore1, semaphore2, semaphore3, semaphore4)

    print(sol.solution)

    sol1, hill_evals = sol.hill_climbing(roundabout)
    print("Last value with hill climbing was ", sol1)

    sol2, annealing_evals = sol.simulated_annealing(roundabout)
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

    
