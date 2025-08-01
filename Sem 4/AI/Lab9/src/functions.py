import numpy as np
from typing import Tuple, Union


class BenchmarkFunction:
    
    def __init__(self, name: str, domain: Tuple[Tuple[float, float], Tuple[float, float]], 
                 global_minimum: Tuple[float, float], global_min_value: float):
        """
        Initialize benchmark function.
        
        Args:
            name: Function name
            domain: ((x_min, x_max), (y_min, y_max))
            global_minimum: (x_opt, y_opt) coordinates of global minimum
            global_min_value: Function value at global minimum
        """
        self.name = name
        self.domain = domain
        self.global_minimum = global_minimum
        self.global_min_value = global_min_value
    
    def __call__(self, x: Union[float, np.ndarray], y: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """Evaluate function at given coordinates."""
        raise NotImplementedError
    
    def evaluate(self, individual: np.ndarray) -> float:
        """Evaluate function for GA individual (x, y coordinates)."""
        return self(individual[0], individual[1])
    
    def is_in_domain(self, x: float, y: float) -> bool:
        """Check if coordinates are within function domain."""
        x_min, x_max = self.domain[0]
        y_min, y_max = self.domain[1]
        return x_min <= x <= x_max and y_min <= y <= y_max


class DropWaveFunction(BenchmarkFunction):
    """
    Drop-Wave Function implementation.
    
    Mathematical form:
    f(x, y) = -(1 + cos(12 * sqrt(x² + y²))) / (0.5 * (x² + y²) + 2)
    
    Domain: [-5.12, 5.12] × [-5.12, 5.12]
    Global minimum: f(0, 0) = -1
    """
    
    def __init__(self):
        super().__init__(
            name="Drop-Wave Function",
            domain=((-5.12, 5.12), (-5.12, 5.12)),
            global_minimum=(0.0, 0.0),
            global_min_value=-1.0
        )
    
    def __call__(self, x: Union[float, np.ndarray], y: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Evaluate Drop-Wave function.
        
        Args:
            x, y: Coordinates (can be scalars or arrays)
            
        Returns:
            Function value(s)
        """
        numerator = -(1 + np.cos(12 * np.sqrt(x**2 + y**2)))
        denominator = 0.5 * (x**2 + y**2) + 2
        return numerator / denominator


class LevyFunction(BenchmarkFunction):
    """
    Levy Function implementation.
    
    Mathematical form:
    f(x, y) = sin²(3πx) + (x-1)²[1 + sin²(3πy)] + (y-1)²[1 + sin²(2πy)]
    
    Domain: [-10, 10] × [-10, 10]
    Global minimum: f(1, 1) = 0
    """
    
    def __init__(self):
        super().__init__(
            name="Levy Function",
            domain=((-10.0, 10.0), (-10.0, 10.0)),
            global_minimum=(1.0, 1.0),
            global_min_value=0.0
        )
    
    def __call__(self, x: Union[float, np.ndarray], y: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Evaluate Levy function.
        
        Args:
            x, y: Coordinates (can be scalars or arrays)
            
        Returns:
            Function value(s)
        """
        term1 = np.sin(3 * np.pi * x)**2
        term2 = (x - 1)**2 * (1 + np.sin(3 * np.pi * y)**2)
        term3 = (y - 1)**2 * (1 + np.sin(2 * np.pi * y)**2)
        return term1 + term2 + term3


# Function instances for easy import
drop_wave = DropWaveFunction()
levy = LevyFunction()

# Dictionary for easy access
FUNCTIONS = {
    'drop_wave': drop_wave,
    'levy': levy
}


def get_function(name: str) -> BenchmarkFunction:
    """
    Get benchmark function by name.
    
    Args:
        name: Function name ('drop_wave' or 'levy')
        
    Returns:
        BenchmarkFunction instance
        
    Raises:
        ValueError: If function name is not recognized
    """
    if name not in FUNCTIONS:
        raise ValueError(f"Unknown function: {name}. Available: {list(FUNCTIONS.keys())}")
    return FUNCTIONS[name]


if __name__ == "__main__":
    print("Testing Drop-Wave Function:")
    print(f"f(0, 0) = {drop_wave(0, 0)} (expected: -1)")
    print(f"Domain: {drop_wave.domain}")
    
    print("\nTesting Levy Function:")
    print(f"f(1, 1) = {levy(1, 1)} (expected: 0)")
    print(f"Domain: {levy.domain}")
