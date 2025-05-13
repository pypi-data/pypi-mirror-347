from itertools import combinations
import numpy as np
import pandas as pd

class BoxBehnkenDesign:

    """
    BoxBehnkenDesign
    ----------------
    Generates Box-Behnken designs for response surface experiments.

    Useful for avoiding extreme experimental conditions by combining midpoints of factor ranges.

    Parameters:
    - factors_names (list of str): List of factor names.
    - center_points (int): Number of center point replicates.

    Attributes:
    - codified_matrix (pd.DataFrame): Design matrix in coded values (-1, 0, +1).

    Methods:
    - generate_codified_matrix(): Generates the Box-Behnken design in coded levels.
    - generate_doe(): Converts the codified matrix to real-world levels using factor boundaries.
    """

    def __init__(self):
        self.codified_matrix = None
        self.number_of_factors = None
        self.factors_names = None

    def generate_codified_matrix(self, number_of_factors, factor_names, center_points=3):
        """
        Generates a Box-Behnken matrix in canonical execution order.

        Parameters:
        - number_of_factors: int ≥ 3
        - factor_names: list of str, optional
        - center_points: int

        Stores:
        - self.codified_matrix
        """
        if number_of_factors < 3:
            raise ValueError("Box-Behnken design requires at least 3 factors.")

        if factor_names is None:
            factor_names = [f"X{i+1}" for i in range(number_of_factors)]
        elif len(factor_names) != number_of_factors:
            raise ValueError("Length of factor_names must match number_of_factors.")

        design_rows = []
        pairs = list(combinations(range(number_of_factors), 2))  # ex: (0,1), (0,2), (1,2)

        for i, j in pairs:
            for level_j in [-1, 1]:  # ← fator j varia mais devagar
                for level_i in [-1, 1]:  # ← fator i varia mais rápido
                    row = [0] * number_of_factors
                    row[i] = level_i
                    row[j] = level_j
                    design_rows.append(row)

        # Adiciona pontos centrais
        center_block = [[0] * number_of_factors for _ in range(center_points)]

        full_matrix = design_rows + center_block
        df = pd.DataFrame(full_matrix, columns=factor_names)
        self.codified_matrix = df
        self.number_of_factors = number_of_factors
        self.factors_names = factor_names
        return df
    
    def generate_doe(self, factor_levels, center_levels):
        if len(factor_levels) != self.number_of_factors or len(center_levels) != self.number_of_factors:
            raise ValueError("factor_levels and center_levels must match the number of factors.")
        if self.codified_matrix is None:
            self.generate_codified_matrix()
        real_matrix = self.codified_matrix.copy()
        for i, name in enumerate(self.factors_names):
            low, high = factor_levels[i]
            center = center_levels[i]
            real_matrix[name] = real_matrix[name].replace({-1: low, 1: high, 0: center})
        self.real_matrix = real_matrix
        return real_matrix