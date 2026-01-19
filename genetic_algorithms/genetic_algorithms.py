import random
import numpy as np

class GeneticAlgorithm:
    def __init__(self, fitness_func, chromosome_length, population_size=50, crossover_rate=0.8, mutation_rate=0.1,
                 elitism=False, elitism_size=1, max_generations=100):
        self.fitness_func = fitness_func
        self.chromosome_length = chromosome_length
        self.population_size = population_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.elitism = elitism
        self.elitism_size = elitism_size
        self.max_generations = max_generations
        self.population = self._initialize_population()
        self.best_fitness_history = []
        self.average_fitness_history = []
    def _initialize_population(self):
        return [''.join(random.choice('01') for _ in range(self.chromosome_length)) for _ in range(self.population_size)]
    def _decode(self, chromosome):
        return int(chromosome, 2)
    def _evaluate_fitness(self, population):
        return [self.fitness_func(self._decode(chromosome)) for chromosome in population]
    def _select_parents(self, population, fitness_values):
        total_fitness = sum(fitness_values)
        if total_fitness == 0:
            probabilities = [1/len(population)] * len(population)
        else:
            probabilities = [fitness/total_fitness for fitness in fitness_values]
        parents = []
        for _ in range(len(population)):
            parents.append(random.choices(population, weights=probabilities, k=2))
        return parents
    def _crossover(self, parent1, parent2):
        if random.random() < self.crossover_rate:
            crossover_point = random.randint(1, len(parent1)-1)
            child1 = parent1[:crossover_point] + parent2[crossover_point:]
            child2 = parent2[:crossover_point] + parent1[crossover_point:]
            return child1, child2
        else:
            return parent1, parent2
    def _mutate(self, chromosome):
        mutated = list(chromosome)
        for i in range(len(mutated)):
            if random.random() < self.mutation_rate:
                mutated[i] = '1' if mutated[i] == '0' else '0'
        return ''.join(mutated)
    def _select_survivors(self, population, fitness_values, offspring, offspring_fitness):
        combined_population = population + offspring
        combined_fitness = fitness_values + offspring_fitness
        sorted_indices = np.argsort(combined_fitness)[::-1]
        new_population = [combined_population[i] for i in sorted_indices[:self.population_size]]
        return new_population
    def run(self):
        for generation in range(self.max_generations):
            fitness_values = self._evaluate_fitness(self.population)
            self.best_fitness_history.append(max(fitness_values))
            self.average_fitness_history.append(sum(fitness_values)/len(fitness_values))
            parents = self._select_parents(self.population, fitness_values)
            offspring = []
            for parent1, parent2 in parents:
                child1, child2 = self._crossover(parent1, parent2)
                offspring.extend([self._mutate(child1), self._mutate(child2)])
            offspring_fitness = self._evaluate_fitness(offspring)
            if self.elitism:
                elites = [self.population[i] for i in np.argsort(fitness_values)[::-1][:self.elitism_size]]
                self.population = self._select_survivors(self.population, fitness_values, offspring, offspring_fitness)
                for i, elite in enumerate(elites):
                    self.population[i] = elite
            else:
                self.population = self._select_survivors(self.population, fitness_values, offspring, offspring_fitness)
        final_fitness = self._evaluate_fitness(self.population)
        best_index = np.argmax(final_fitness)
        return {
            'best_chromosome': self.population[best_index],
            'best_fitness': final_fitness[best_index],
            'best_fitness_history': self.best_fitness_history,
            'average_fitness_history': self.average_fitness_history
        }
class ClassicGA(GeneticAlgorithm):
    def __init__(self, fitness_func, chromosome_length, population_size=50, crossover_rate=0.8, mutation_rate=0.1,
                 max_generations=100):
        super().__init__(fitness_func, chromosome_length, population_size, crossover_rate, mutation_rate,
                        elitism=False, max_generations=max_generations)
class ElitistGA(GeneticAlgorithm):
    def __init__(self, fitness_func, chromosome_length, population_size=50, crossover_rate=0.8, mutation_rate=0.1,
                 elitism_size=2, max_generations=100):
        super().__init__(fitness_func, chromosome_length, population_size, crossover_rate, mutation_rate,
                        elitism=True, elitism_size=elitism_size, max_generations=max_generations)
class SteadyStateGA(GeneticAlgorithm):
    def __init__(self, fitness_func, chromosome_length, population_size=50, crossover_rate=0.8, mutation_rate=0.1,
                 max_generations=100):
        super().__init__(fitness_func, chromosome_length, population_size, crossover_rate, mutation_rate,
                        elitism=False, max_generations=max_generations)
    def _select_survivors(self, population, fitness_values, offspring, offspring_fitness):
        new_population = population.copy()
        for child in offspring:
            worst_index = np.argmin(fitness_values)
            new_population[worst_index] = child
            fitness_values[worst_index] = self.fitness_func(self._decode(child))
        return new_population
    def run(self):
        for generation in range(self.max_generations):
            fitness_values = self._evaluate_fitness(self.population)
            self.best_fitness_history.append(max(fitness_values))
            self.average_fitness_history.append(sum(fitness_values)/len(fitness_values))
            parents = self._select_parents(self.population, fitness_values)
            offspring = []
            for parent1, parent2 in parents[:2]:
                child1, child2 = self._crossover(parent1, parent2)
                offspring.extend([self._mutate(child1), self._mutate(child2)])
            self.population = self._select_survivors(self.population, fitness_values, offspring, [])
        final_fitness = self._evaluate_fitness(self.population)
        best_index = np.argmax(final_fitness)
        return {
            'best_chromosome': self.population[best_index],
            'best_fitness': final_fitness[best_index],
            'best_fitness_history': self.best_fitness_history,
            'average_fitness_history': self.average_fitness_history
        }
class AdaptiveMutationGA(GeneticAlgorithm):
    def __init__(self, fitness_func, chromosome_length, population_size=50, crossover_rate=0.8, initial_mutation_rate=0.1,
                 elitism=False, elitism_size=1, max_generations=100):
        super().__init__(fitness_func, chromosome_length, population_size, crossover_rate, initial_mutation_rate,
                        elitism, elitism_size, max_generations)
        self.initial_mutation_rate = initial_mutation_rate
    def run(self):
        for generation in range(self.max_generations):
            fitness_values = self._evaluate_fitness(self.population)
            self.best_fitness_history.append(max(fitness_values))
            self.average_fitness_history.append(sum(fitness_values)/len(fitness_values))
            diversity = len(set(self.population)) / self.population_size
            self.mutation_rate = self.initial_mutation_rate * (1 + (1 - diversity) * 2)
            parents = self._select_parents(self.population, fitness_values)
            offspring = []
            for parent1, parent2 in parents:
                child1, child2 = self._crossover(parent1, parent2)
                offspring.extend([self._mutate(child1), self._mutate(child2)])
            offspring_fitness = self._evaluate_fitness(offspring)
            if self.elitism:
                elites = [self.population[i] for i in np.argsort(fitness_values)[::-1][:self.elitism_size]]
                self.population = self._select_survivors(self.population, fitness_values, offspring, offspring_fitness)
                for i, elite in enumerate(elites):
                    self.population[i] = elite
            else:
                self.population = self._select_survivors(self.population, fitness_values, offspring, offspring_fitness)
        final_fitness = self._evaluate_fitness(self.population)
        best_index = np.argmax(final_fitness)
        return {
            'best_chromosome': self.population[best_index],
            'best_fitness': final_fitness[best_index],
            'best_fitness_history': self.best_fitness_history,
            'average_fitness_history': self.average_fitness_history
        }