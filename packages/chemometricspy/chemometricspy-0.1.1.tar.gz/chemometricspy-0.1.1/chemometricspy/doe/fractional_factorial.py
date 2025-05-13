import numpy as np
import pandas as pd
from itertools import product
from chemometricspy.doe import Factorial
import warnings
from pandas.errors import PerformanceWarning

warnings.simplefilter(action='ignore', category=PerformanceWarning)

class FractionalFactorial(Factorial):
    """
    FractionalFactorial
    -------------------
    Generates fractional factorial designs 2^(k-p) with specified resolution.

    Allows construction of classical fractional factorial matrices based on generators and resolution constraints.

    Parameters:
    - number_of_factors (int): Number of factors (k).
    - resolution (str): Desired resolution of the design ("III", "IV", "V").
    - generators (dict, optional): Dictionary of manually specified generators.

    Attributes:
    - design_matrix (pd.DataFrame): Codified design matrix for fractional factorial plan.
    - generators (dict): Generator equations used in construction.
    - resolution (str): Actual resolution used.

    Methods:
    - _get_classical_designs(): Returns predefined designs for common (k, resolution) combinations.
    - generate_matrix(): Generates the design matrix based on resolution and number of factors.
    - describe_plan(): Describes the structure and generators of the current fractional design.
    """

    def __init__(self):
        self.codified_matrix = None
        self.factors_names = []
        self._base_factors = None
        self._generators = None
        self._n_runs = None
        self.number_of_factors = None

    def _get_classical_designs(self):
        """
        Returns a dictionary of classical fractional factorial designs.
        Keys are tuples (number of factors, resolution), values are tuples:
        (number of runs, base factors, generators)
        """
        return {
            # Resolution V
            (7, 'V'): (64, ['A', 'B', 'C', 'D', 'E'], {'F': ['A', 'B', 'C'], 'G': ['B', 'C', 'D']}),
            (6, 'V'): (64, ['A', 'B', 'C'], {'D': ['A', 'B', 'C'], 'E': ['A', 'C', 'B'], 'F': ['B', 'C', 'A']}),

            # Resolution IV
            (6, 'IV'): (32, ['A', 'B', 'C', 'D'], {'E': ['A', 'B'], 'F': ['C', 'D']}),
            (7, 'IV'): (32, ['A', 'B', 'C', 'D'], {'E': ['A', 'B'], 'F': ['A', 'C'], 'G': ['A', 'D']}),
            (8, 'IV'): (64, ['A', 'B', 'C', 'D', 'E'], {'F': ['A', 'B'], 'G': ['A', 'C'], 'H': ['B', 'C']}),
            (9, 'IV'): (64, ['A', 'B', 'C', 'D', 'E'], {'F': ['A', 'B'], 'G': ['A', 'C'], 'H': ['A', 'D'], 'I': ['B', 'C']}),
            (10, 'IV'): (64, ['A', 'B', 'C', 'D', 'E', 'F'], {
                'G': ['A', 'B'], 'H': ['A', 'C'], 'I': ['A', 'D'], 'J': ['B', 'C']
            }),

            # Resolution III
            (7, 'III'): (16, ['A', 'B', 'C', 'D'], {'E': ['A', 'B'], 'F': ['A', 'C'], 'G': ['A', 'D']}),
            (8, 'III'): (16, ['A', 'B', 'C', 'D'], {'E': ['A', 'B'], 'F': ['A', 'C'], 'G': ['B', 'D']}),
            (9, 'III'): (16, ['A', 'B', 'C', 'D'], {'E': ['A', 'B'], 'F': ['A', 'C'], 'G': ['A', 'D'], 'H': ['B', 'C'], 'I': ['B', 'D']}),
            (10, 'III'): (32, ['A', 'B', 'C', 'D', 'E'], {'F': ['A', 'B'], 'G': ['A', 'C'], 'H': ['A', 'D'], 'I': ['B', 'C'], 'J': ['B', 'D']}),
            (11, 'III'): (32, ['A', 'B', 'C', 'D', 'E'], {'F': ['A', 'B'], 'G': ['A', 'C'], 'H': ['A', 'D'], 'I': ['B', 'C'], 'J': ['B', 'D'], 'K': ['C', 'D']}),
            (12, 'III'): (32, ['A', 'B', 'C', 'D', 'E'], {'F': ['A', 'B'], 'G': ['A', 'C'], 'H': ['A', 'D'], 'I': ['B', 'C'], 'J': ['B', 'D'], 'K': ['C', 'D'], 'L': ['A', 'E']}),
            (13, 'III'): (64, ['A', 'B', 'C', 'D', 'E', 'F'], {'G': ['A', 'B'], 'H': ['A', 'C'], 'I': ['A', 'D'], 'J': ['B', 'C'], 'K': ['B', 'D'], 'L': ['C', 'D'], 'M': ['A', 'E']}),
            (14, 'III'): (64, ['A', 'B', 'C', 'D', 'E', 'F'], {'G': ['A', 'B'], 'H': ['A', 'C'], 'I': ['A', 'D'], 'J': ['B', 'C'], 'K': ['B', 'D'], 'L': ['C', 'D'], 'M': ['A', 'E'], 'N': ['B', 'E']}),
            (15, 'III'): (64, ['A', 'B', 'C', 'D', 'E', 'F'], {'G': ['A', 'B'], 'H': ['A', 'C'], 'I': ['A', 'D'], 'J': ['B', 'C'], 'K': ['B', 'D'], 'L': ['C', 'D'], 'M': ['A', 'E'], 'N': ['B', 'E'], 'O': ['C', 'E']}),
        }

    def generate_matrix(self, n_factors, factors_names, resolution='V'):
        """
        Generate the factorial design matrix.

        Parameters:
            n_factors (int): Number of factors.
            factor_names (list): List of factor names (length must match n_factors).
            resolution (str): Desired resolution ('III', 'IV', or 'V').
        """
        resolution = resolution.upper()
        key = (n_factors, resolution)
        table = self._get_classical_designs()

        if key not in table:
            available = [r for (k, r) in table if k == n_factors]
            raise ValueError(f"No classical design found for {n_factors} factors with resolution {resolution}. "
                             f"Available resolutions: {available}")

        self._n_runs, self._base_factors, self._generators = table[key]

        if len(factors_names) != n_factors:
            raise ValueError("The number of factor names must match the number of factors.")

        runs = np.array(list(product([-1, 1], repeat=len(self._base_factors))))[:, ::-1]
        df = pd.DataFrame(runs, columns=self._base_factors)

        for alias, equation in self._generators.items():
            df[alias] = np.prod([df[f] for f in equation], axis=0)

        df.columns = factors_names
        self.factors_names = factors_names
        self.codified_matrix = df
        self.number_of_factors = n_factors
        return self.codified_matrix

    
    def describe_plan(self):
        """
        Describes the current factorial design: number of runs, base factors, and generator aliases.
        """
        if self._base_factors is None or self._generators is None:
            raise ValueError("No plan has been generated yet.")
        description = f"\n→ Number of runs: {self._n_runs}\n→ Base factors: {self._base_factors}\n→ Generators:"
        for alias, equation in self._generators.items():
            description += f"\n    {alias} = {' * '.join(equation)}"
        return description
