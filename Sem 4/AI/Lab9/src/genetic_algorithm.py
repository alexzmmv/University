"""
Genetic Algorithm implementation with multiple representations and crossover methods.

This module provides a flexible GA implementation supporting:
- Binary and real-valued representations
- Multiple crossover methods for each representation
- Configurable parameters (mutation rate, crossover rate, population size, generations)
"""

import numpy as np
import random
from typing import List, Tuple, Callable, Union, Dict, Any
from abc import ABC, abstractmethod
from .functions import BenchmarkFunction


class Individual:
    """Represents an individual in the population."""
    
    def __init__(self, genes: Union[List[int], np.ndarray], fitness: float = None):
        self.genes = genes
        self.fitness = fitness
        self.expression = None 
    
    def __str__(self):
        return f"Individual(genes={self.genes}, fitness={self.fitness})"


class Representation(ABC):
    """Abstract base class for different representations."""
    @abstractmethod
    def create_individual(self, domain: Tuple[Tuple[float, float], Tuple[float, float]]) -> Individual:
        """Create a random individual."""
        pass
    
    @abstractmethod
    def decode(self, individual: Individual) -> np.ndarray:
        """Decode individual to real values."""
        pass
    
    @abstractmethod
    def mutate(self, individual: Individual, mutation_rate: float) -> Individual:
        """Apply mutation to individual."""
        pass


class BinaryRepresentation(Representation):
    """Binary representation for GA."""
    
    def __init__(self, bits_per_variable: int = 16):
        self.bits_per_variable = bits_per_variable
        self.total_bits = 2 * bits_per_variable  
    
    def create_individual(self, domain: Tuple[Tuple[float, float], Tuple[float, float]]) -> Individual:
        """Create random binary number."""
        genes = [random.randint(0, 1) for _ in range(self.total_bits)]
        individual = Individual(genes)
        individual.expression = self.decode(individual, domain)
        return individual
    
    def decode(self, individual: Individual, domain: Tuple[Tuple[float, float], Tuple[float, float]]) -> np.ndarray:
        """Binary to real value"""
        x_bits = individual.genes[:self.bits_per_variable]
        y_bits = individual.genes[self.bits_per_variable:]
        
        # Convert binary to decimal
        x_decimal = sum(bit * (2 ** i) for i, bit in enumerate(reversed(x_bits)))
        y_decimal = sum(bit * (2 ** i) for i, bit in enumerate(reversed(y_bits)))
        
        # Scale to domain
        max_decimal = 2 ** self.bits_per_variable - 1
        x_min, x_max = domain[0]
        y_min, y_max = domain[1]
        
        x = x_min + (x_decimal / max_decimal) * (x_max - x_min)
        y = y_min + (y_decimal / max_decimal) * (y_max - y_min)
        
        return np.array([x, y])
    
    def mutate(self, individual: Individual, mutation_rate: float) -> Individual:
        mutated_genes = individual.genes.copy()
        for i in range(len(mutated_genes)):
            if random.random() < mutation_rate:
                mutated_genes[i] = 1 - mutated_genes[i]  # Flip bit
        
        mutated = Individual(mutated_genes)
        return mutated


class RealValuedRepresentation(Representation):
    
    def create_individual(self, domain: Tuple[Tuple[float, float], Tuple[float, float]]) -> Individual:
        x_min, x_max = domain[0]
        y_min, y_max = domain[1]
        x = random.uniform(x_min, x_max)
        y = random.uniform(y_min, y_max)
        individual = Individual(np.array([x, y]))
        individual.expression = individual.genes
        return individual
    
    def decode(self, individual: Individual) -> np.ndarray:
        return individual.genes
    
    def mutate(self, individual: Individual, mutation_rate: float, 
               domain: Tuple[Tuple[float, float], Tuple[float, float]], 
               mutation_strength: float = 0.1) -> Individual:
        """Apply Gaussian mutation."""
        mutated_genes = individual.genes.copy()
        x_min, x_max = domain[0]
        y_min, y_max = domain[1]
        
        for i in range(len(mutated_genes)):
            if random.random() < mutation_rate:
                # Gaussian mutation
                mutation_range = (x_max - x_min) if i == 0 else (y_max - y_min)
                mutation = np.random.normal(0, mutation_strength * mutation_range)
                mutated_genes[i] += mutation
                
                # Clamp to domain
                if i == 0:
                    mutated_genes[i] = np.clip(mutated_genes[i], x_min, x_max)
                else:
                    mutated_genes[i] = np.clip(mutated_genes[i], y_min, y_max)
        
        mutated = Individual(mutated_genes)
        mutated.expression = mutated_genes
        return mutated


class CrossoverMethod(ABC):    
    @abstractmethod
    def crossover(self, parent1: Individual, parent2: Individual) -> Tuple[Individual, Individual]:
        pass


class OnePointCrossover(CrossoverMethod):
    
    def crossover(self, parent1: Individual, parent2: Individual) -> Tuple[Individual, Individual]:
        point = random.randint(1, len(parent1.genes) - 1)
        
        child1_genes = parent1.genes[:point] + parent2.genes[point:]
        child2_genes = parent2.genes[:point] + parent1.genes[point:]
        
        return Individual(child1_genes), Individual(child2_genes)


class TwoPointCrossover(CrossoverMethod):
    """Two-point crossover for binary representation."""
    
    def crossover(self, parent1: Individual, parent2: Individual) -> Tuple[Individual, Individual]:
        """Perform two-point crossover."""
        length = len(parent1.genes)
        point1 = random.randint(1, length - 2)
        point2 = random.randint(point1 + 1, length - 1)
        
        child1_genes = (parent1.genes[:point1] + 
                       parent2.genes[point1:point2] + 
                       parent1.genes[point2:])
        child2_genes = (parent2.genes[:point1] + 
                       parent1.genes[point1:point2] + 
                       parent2.genes[point2:])
        
        return Individual(child1_genes), Individual(child2_genes)


class ArithmeticCrossover(CrossoverMethod):
    """Arithmetic crossover for real-valued representation."""
    
    def __init__(self, alpha: float = 0.5):
        self.alpha = alpha
    
    def crossover(self, parent1: Individual, parent2: Individual) -> Tuple[Individual, Individual]:
        """Perform arithmetic crossover."""
        child1_genes = self.alpha * parent1.genes + (1 - self.alpha) * parent2.genes
        child2_genes = (1 - self.alpha) * parent1.genes + self.alpha * parent2.genes
        
        child1 = Individual(child1_genes)
        child2 = Individual(child2_genes)
        child1.expression = child1_genes
        child2.expression = child2_genes
        
        return child1, child2


class BLXAlphaCrossover(CrossoverMethod):
    """BLX-α crossover for real-valued representation."""
    
    def __init__(self, alpha: float = 0.5):
        self.alpha = alpha
    
    def crossover(self, parent1: Individual, parent2: Individual) -> Tuple[Individual, Individual]:
        """Perform BLX-α crossover."""
        p1_genes = parent1.genes
        p2_genes = parent2.genes
        
        child1_genes = np.zeros_like(p1_genes)
        child2_genes = np.zeros_like(p1_genes)
        
        for i in range(len(p1_genes)):
            x_min = min(p1_genes[i], p2_genes[i])
            x_max = max(p1_genes[i], p2_genes[i])
            range_val = x_max - x_min
            
            lower_bound = x_min - self.alpha * range_val
            upper_bound = x_max + self.alpha * range_val
            
            child1_genes[i] = random.uniform(lower_bound, upper_bound)
            child2_genes[i] = random.uniform(lower_bound, upper_bound)
        
        child1 = Individual(child1_genes)
        child2 = Individual(child2_genes)
        child1.expression = child1_genes
        child2.expression = child2_genes
        
        return child1, child2


class GeneticAlgorithm:
    """Genetic Algorithm implementation."""
    
    def __init__(self, 
                 representation: Representation,
                 crossover_method: CrossoverMethod,
                 population_size: int = 100,
                 mutation_rate: float = 0.01,
                 crossover_rate: float = 0.8,
                 elitism: int = 2):
        """
        Initialize GA.
        
        Args:
            representation: Representation method (binary or real-valued)
            crossover_method: Crossover method
            population_size: Size of population
            mutation_rate: Probability of mutation
            crossover_rate: Probability of crossover
            elitism: Number of best individuals to preserve
        """
        self.representation = representation
        self.crossover_method = crossover_method
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elitism = elitism
        
        self.population = []
        self.best_fitness_history = []
        self.mean_fitness_history = []
        self.function_evaluations = 0
    
    def initialize_population(self, function: BenchmarkFunction) -> None:
        """Initialize random population."""
        self.population = []
        for _ in range(self.population_size):
            individual = self.representation.create_individual(function.domain)
            self.population.append(individual)
    
    def evaluate_population(self, function: BenchmarkFunction) -> None:
        """Evaluate fitness of all individuals."""
        for individual in self.population:
            if individual.fitness is None:
                # Decode to real values if needed
                if hasattr(self.representation, 'decode') and isinstance(self.representation, BinaryRepresentation):
                    individual_representation = self.representation.decode(individual, function.domain)
                else:
                    individual_representation = individual.expression

                individual.fitness = function.evaluate(individual_representation)
                self.function_evaluations += 1
    
    def tournament_selection(self, tournament_size: int = 3) -> Individual:
        """Tournament selection."""
        tournament = random.sample(self.population, tournament_size)
        return min(tournament, key=lambda x: x.fitness)  # Minimization
    
    def evolve_generation(self, function: BenchmarkFunction) -> None:
        """Evolve one generation."""
        # Sort population by fitness (minimization)
        self.population.sort(key=lambda x: x.fitness)
        
        # Record statistics
        fitnesses = [ind.fitness for ind in self.population]
        self.best_fitness_history.append(min(fitnesses))
        self.mean_fitness_history.append(np.mean(fitnesses))
        
        # Create new population
        new_population = []
        
        # Elitism: keep best individuals
        new_population.extend(self.population[:self.elitism])
        
        # Generate offspring
        while len(new_population) < self.population_size:
            parent1 = self.tournament_selection()
            parent2 = self.tournament_selection()
            
            # Crossover
            if random.random() < self.crossover_rate:
                child1, child2 = self.crossover_method.crossover(parent1, parent2)
            else:
                child1, child2 = Individual(parent1.genes.copy()), Individual(parent2.genes.copy())
            
            # Mutation
            if isinstance(self.representation, BinaryRepresentation):
                child1 = self.representation.mutate(child1, self.mutation_rate)
                child2 = self.representation.mutate(child2, self.mutation_rate)
                child1.expression = self.representation.decode(child1, function.domain)
                child2.expression = self.representation.decode(child2, function.domain)
            else:
                child1 = self.representation.mutate(child1, self.mutation_rate, function.domain)
                child2 = self.representation.mutate(child2, self.mutation_rate, function.domain)
            
            new_population.extend([child1, child2])
        
        # Trim to exact population size
        self.population = new_population[:self.population_size]
    
    def run(self, function: BenchmarkFunction, generations: int) -> Dict[str, Any]:
        """
        Run the genetic algorithm.
        
        Args:
            function: Benchmark function to optimize
            generations: Number of generations to run
            
        Returns:
            Dictionary with results
        """
        self.function_evaluations = 0
        self.best_fitness_history = []
        self.mean_fitness_history = []
        
        # Initialize population
        self.initialize_population(function)
        self.evaluate_population(function)
        
        # Evolution loop
        for generation in range(generations):
            self.evolve_generation(function)
            self.evaluate_population(function)
        
        # Find best individual
        best_individual = min(self.population, key=lambda x: x.fitness)
        
        if isinstance(self.representation, BinaryRepresentation):
            best_expression = self.representation.decode(best_individual, function.domain)
        else:
            best_expression = best_individual.expression
        
        return {
            'best_fitness': best_individual.fitness,
            'best_solution': best_expression,
            'best_fitness_history': self.best_fitness_history,
            'mean_fitness_history': self.mean_fitness_history,
            'function_evaluations': self.function_evaluations,
            'generations': generations
        }


# Factory functions for easy configuration
def create_ga_config(representation_type: str, crossover_type: str, **kwargs) -> GeneticAlgorithm:
    """
    Create GA configuration.
    
    Args:
        representation_type: 'binary' or 'real'
        crossover_type: For binary: '1point', '2point'. For real: 'arithmetic', 'blx_alpha'
        **kwargs: Additional GA parameters
        
    Returns:
        Configured GeneticAlgorithm instance
    """
    # Create representation
    if representation_type == 'binary':
        representation = BinaryRepresentation(kwargs.get('bits_per_variable', 16))
        if crossover_type == '1point':
            crossover = OnePointCrossover()
        elif crossover_type == '2point':
            crossover = TwoPointCrossover()
        else:
            raise ValueError(f"Unknown binary crossover type: {crossover_type}")
    
    elif representation_type == 'real':
        representation = RealValuedRepresentation()
        if crossover_type == 'arithmetic':
            crossover = ArithmeticCrossover(kwargs.get('alpha', 0.5))
        elif crossover_type == 'blx_alpha':
            crossover = BLXAlphaCrossover(kwargs.get('alpha', 0.5))
        else:
            raise ValueError(f"Unknown real crossover type: {crossover_type}")
    
    else:
        raise ValueError(f"Unknown representation type: {representation_type}")
    
    # Create GA
    return GeneticAlgorithm(
        representation=representation,
        crossover_method=crossover,
        population_size=kwargs.get('population_size', 100),
        mutation_rate=kwargs.get('mutation_rate', 0.01),
        crossover_rate=kwargs.get('crossover_rate', 0.8),
        elitism=kwargs.get('elitism', 2)
    )
