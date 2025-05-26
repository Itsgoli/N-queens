import random

class GeneticSolver:
    POP_SIZE = 200  
    MUTATION_RATE = 0.1
    MAX_GENERATIONS = 2000
    RETRY_LIMIT = 10  

    def __init__(self, n):
        self.n = n

    def fitness(self, individual):
        n = len(individual)
        non_attacks = 0
        for i in range(n):
            for j in range(i + 1, n):
                if individual[i] != individual[j] and abs(individual[i] - individual[j]) != abs(i - j):
                    non_attacks += 1
        return non_attacks

    def crossover(self, parent1, parent2):
        n = len(parent1)
        point = random.randint(0, n - 1)
        return parent1[:point] + parent2[point:]

    def mutate(self, individual):
        n = len(individual)
        if random.random() < self.MUTATION_RATE:
            i = random.randint(0, n - 1)
            individual[i] = random.randint(0, n - 1)
        return individual

    def solve(self):
        max_fitness = (self.n * (self.n - 1)) // 2

        for attempt in range(self.RETRY_LIMIT):
            population = [[random.randint(0, self.n - 1) for _ in range(self.n)] for _ in range(self.POP_SIZE)]

            for generation in range(self.MAX_GENERATIONS):
                population.sort(key=self.fitness, reverse=True)

                if self.fitness(population[0]) == max_fitness:
                    return population[0]

                new_population = population[:10]
                while len(new_population) < self.POP_SIZE:
                    parent1, parent2 = random.choices(population[:50], k=2)
                    child = self.crossover(parent1, parent2)
                    child = self.mutate(child)
                    new_population.append(child)

                population = new_population

        return None
