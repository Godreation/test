import matplotlib.pyplot as plt
from genetic_algorithms import ClassicGA, ElitistGA, SteadyStateGA, AdaptiveMutationGA

def onemax_fitness(x):
    return x

def deceptive_fitness(x):
    binary_str = bin(x)[2:].zfill(10)
    ones_count = binary_str.count('1')
    if ones_count == 0:
        return 10
    elif ones_count == 10:
        return 20
    else:
        return 10 - ones_count

def quadratic_fitness(x):
    return - (x - 512) ** 2 + 512 ** 2

def test_algorithms():
    chromosome_length = 10
    max_generations = 50
    population_size = 50
    
    algorithms = {
        'Classic GA': ClassicGA(
            fitness_func=onemax_fitness,
            chromosome_length=chromosome_length,
            population_size=population_size,
            max_generations=max_generations
        ),
        'Elitist GA': ElitistGA(
            fitness_func=onemax_fitness,
            chromosome_length=chromosome_length,
            population_size=population_size,
            max_generations=max_generations
        ),
        'Steady-State GA': SteadyStateGA(
            fitness_func=onemax_fitness,
            chromosome_length=chromosome_length,
            population_size=population_size,
            max_generations=max_generations
        ),
        'Adaptive Mutation GA': AdaptiveMutationGA(
            fitness_func=onemax_fitness,
            chromosome_length=chromosome_length,
            population_size=population_size,
            max_generations=max_generations
        )
    }
    
    results = {}
    print("Running algorithms on OneMax problem...")
    for name, algorithm in algorithms.items():
        print(f"  Running {name}...")
        results[name] = algorithm.run()
    
    print("\nResults:")
    for name, result in results.items():
        print(f"{name}:")
        print(f"  Best Fitness: {result['best_fitness']}")
        print(f"  Best Chromosome: {result['best_chromosome']}")
        print(f"  Decoded Value: {int(result['best_chromosome'], 2)}")
        print()
    
    plt.figure(figsize=(12, 8))
    
    plt.subplot(2, 2, 1)
    for name, result in results.items():
        plt.plot(result['best_fitness_history'], label=name)
    plt.title('Best Fitness over Generations (OneMax)')
    plt.xlabel('Generation')
    plt.ylabel('Best Fitness')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(2, 2, 2)
    for name, result in results.items():
        plt.plot(result['average_fitness_history'], label=name)
    plt.title('Average Fitness over Generations (OneMax)')
    plt.xlabel('Generation')
    plt.ylabel('Average Fitness')
    plt.legend()
    plt.grid(True)
    
    algorithms_quadratic = {
        'Classic GA': ClassicGA(
            fitness_func=quadratic_fitness,
            chromosome_length=chromosome_length,
            population_size=population_size,
            max_generations=max_generations
        ),
        'Elitist GA': ElitistGA(
            fitness_func=quadratic_fitness,
            chromosome_length=chromosome_length,
            population_size=population_size,
            max_generations=max_generations
        ),
        'Steady-State GA': SteadyStateGA(
            fitness_func=quadratic_fitness,
            chromosome_length=chromosome_length,
            population_size=population_size,
            max_generations=max_generations
        ),
        'Adaptive Mutation GA': AdaptiveMutationGA(
            fitness_func=quadratic_fitness,
            chromosome_length=chromosome_length,
            population_size=population_size,
            max_generations=max_generations
        )
    }
    
    results_quadratic = {}
    print("Running algorithms on Quadratic problem...")
    for name, algorithm in algorithms_quadratic.items():
        print(f"  Running {name}...")
        results_quadratic[name] = algorithm.run()
    
    plt.subplot(2, 2, 3)
    for name, result in results_quadratic.items():
        plt.plot(result['best_fitness_history'], label=name)
    plt.title('Best Fitness over Generations (Quadratic)')
    plt.xlabel('Generation')
    plt.ylabel('Best Fitness')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(2, 2, 4)
    for name, result in results_quadratic.items():
        plt.plot(result['average_fitness_history'], label=name)
    plt.title('Average Fitness over Generations (Quadratic)')
    plt.xlabel('Generation')
    plt.ylabel('Average Fitness')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('ga_comparison.png')
    print("\nComparison chart saved as 'ga_comparison.png'")
    
    plt.figure(figsize=(12, 6))
    
    algorithms_deceptive = {
        'Classic GA': ClassicGA(
            fitness_func=deceptive_fitness,
            chromosome_length=chromosome_length,
            population_size=population_size,
            max_generations=100
        ),
        'Elitist GA': ElitistGA(
            fitness_func=deceptive_fitness,
            chromosome_length=chromosome_length,
            population_size=population_size,
            max_generations=100
        ),
        'Steady-State GA': SteadyStateGA(
            fitness_func=deceptive_fitness,
            chromosome_length=chromosome_length,
            population_size=population_size,
            max_generations=100
        ),
        'Adaptive Mutation GA': AdaptiveMutationGA(
            fitness_func=deceptive_fitness,
            chromosome_length=chromosome_length,
            population_size=population_size,
            max_generations=100
        )
    }
    
    results_deceptive = {}
    print("Running algorithms on Deceptive problem...")
    for name, algorithm in algorithms_deceptive.items():
        print(f"  Running {name}...")
        results_deceptive[name] = algorithm.run()
    
    plt.subplot(1, 2, 1)
    for name, result in results_deceptive.items():
        plt.plot(result['best_fitness_history'], label=name)
    plt.title('Best Fitness over Generations (Deceptive)')
    plt.xlabel('Generation')
    plt.ylabel('Best Fitness')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(1, 2, 2)
    for name, result in results_deceptive.items():
        plt.plot(result['average_fitness_history'], label=name)
    plt.title('Average Fitness over Generations (Deceptive)')
    plt.xlabel('Generation')
    plt.ylabel('Average Fitness')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('ga_comparison_deceptive.png')
    print("Comparison chart for deceptive problem saved as 'ga_comparison_deceptive.png'")
    
    print("\nDeceptive Problem Results:")
    for name, result in results_deceptive.items():
        print(f"{name}:")
        print(f"  Best Fitness: {result['best_fitness']}")
        print(f"  Best Chromosome: {result['best_chromosome']}")
        print(f"  Decoded Value: {int(result['best_chromosome'], 2)}")
        print()

if __name__ == "__main__":
    test_algorithms()