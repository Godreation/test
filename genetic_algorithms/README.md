# Genetic Algorithms Implementation

This project implements several classic genetic algorithms and their variants in Python, along with a test script to compare their performance on benchmark problems.

## Genetic Algorithms Overview

Genetic Algorithms (GAs) are search and optimization algorithms inspired by the process of natural selection. They work by evolving a population of candidate solutions through operations like selection, crossover, and mutation over multiple generations.

## Implemented Algorithms

### 1. Classic Genetic Algorithm (Classic GA)

**Concept:** The basic form of genetic algorithm that follows the standard evolutionary cycle.

**Principles:**
- **Initialization:** Randomly generate an initial population
- **Selection:** Select parents based on fitness using roulette wheel selection
- **Crossover:** Combine parent chromosomes to create offspring with a certain probability
- **Mutation:** Randomly flip bits in offspring chromosomes with a certain probability
- **Survivor Selection:** Replace the entire population with the best individuals from parents and offspring

**Suitable Problem Types:**
- General optimization problems
- Problems with smooth fitness landscapes
- Where diversity maintenance is not the primary concern

### 2. Elitist Genetic Algorithm (Elitist GA)

**Concept:** An extension of Classic GA that preserves the best individuals (elites) from one generation to the next.

**Principles:**
- Same as Classic GA, but with an additional elitism step
- The top N individuals from each generation are directly passed to the next generation
- Prevents loss of good solutions due to genetic drift

**Suitable Problem Types:**
- Problems where maintaining good solutions is critical
- Optimization problems with rugged fitness landscapes
- When convergence to optimal solutions is more important than exploration

### 3. Steady-State Genetic Algorithm (Steady-State GA)

**Concept:** A variant where only a few individuals are replaced in each generation, rather than the entire population.

**Principles:**
- Select a small number of parents (usually 2)
- Create offspring through crossover and mutation
- Replace the worst individuals in the population with the new offspring
- Maintains higher population diversity compared to Classic GA

**Suitable Problem Types:**
- Problems where population diversity is important
- Large-scale optimization problems
- Problems prone to premature convergence

### 4. Adaptive Mutation Genetic Algorithm (Adaptive Mutation GA)

**Concept:** A GA variant where the mutation rate adapts based on population diversity.

**Principles:**
- Same as Classic GA, but with dynamic mutation rate
- Monitors population diversity (measured as the percentage of unique individuals)
- Increases mutation rate when diversity is low to encourage exploration
- Decreases mutation rate when diversity is high to focus on exploitation

**Suitable Problem Types:**
- Problems with complex fitness landscapes
- Problems where balancing exploration and exploitation is challenging
- Dynamic optimization problems where the landscape changes over time

## Installation

1. Ensure you have Python 3.7+ installed
2. Install required dependencies:
   ```bash
   pip install matplotlib numpy
   ```

## Usage

### Running the Test Script

The test script compares all algorithms on three benchmark problems:
- **OneMax:** Simple problem where fitness is the number of 1s in the binary string
- **Quadratic:** A quadratic function with a single maximum
- **Deceptive:** A problem designed to trick simple GAs by rewarding intermediate solutions

```bash
python test_ga.py
```

### Using the Algorithms in Your Own Code

```python
from genetic_algorithms import ClassicGA, ElitistGA, SteadyStateGA, AdaptiveMutationGA

# Define your fitness function
def your_fitness_function(x):
    # x is the decoded integer value
    return - (x - 100) ** 2 + 10000

# Create and run an algorithm
algorithm = ElitistGA(
    fitness_func=your_fitness_function,
    chromosome_length=10,  # Length of binary chromosome
    population_size=50,     # Number of individuals in population
    max_generations=100     # Maximum number of generations
)

result = algorithm.run()

# Access results
print(f"Best fitness: {result['best_fitness']}")
print(f"Best chromosome: {result['best_chromosome']}")
print(f"Decoded value: {int(result['best_chromosome'], 2)}")
```

## Test Results

The test script generates two comparison charts:
- `ga_comparison.png`: Comparison on OneMax and Quadratic problems
- `ga_comparison_deceptive.png`: Comparison on Deceptive problem

## Algorithm Comparison

| Algorithm | Convergence Speed | Diversity Maintenance | Robustness | Best For |
|-----------|-------------------|-----------------------|------------|----------|
| Classic GA | Medium | Medium | Medium | General optimization |
| Elitist GA | Fast | Low | High | Convergence to optima |
| Steady-State GA | Slow | High | Medium | Maintaining diversity |
| Adaptive Mutation GA | Medium | High | High | Complex landscapes |

## Features

- Object-oriented implementation for easy extension
- Support for different fitness functions
- Configurable parameters for each algorithm
- Fitness history tracking for analysis
- Visual comparison of algorithm performance

## Benchmark Problems

### OneMax

A simple problem where the fitness of a binary string is the number of 1s it contains. The optimal solution is a string of all 1s.

### Quadratic

A quadratic function with a single maximum at the center. This represents a smooth fitness landscape.

### Deceptive

A challenging problem where intermediate solutions have higher fitness than they should, making it difficult for simple GAs to find the global optimum.

## Extending the Code

You can extend this implementation by:

1. Adding new selection methods
2. Implementing different crossover operators
3. Adding new mutation strategies
4. Creating new algorithm variants
5. Testing on your own optimization problems

## License

MIT License