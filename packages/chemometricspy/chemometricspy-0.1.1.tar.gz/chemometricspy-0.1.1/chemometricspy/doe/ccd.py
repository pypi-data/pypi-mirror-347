import numpy as np
import pandas as pd
from itertools import product

class CentralCompositeDesign:

    """
    CentralCompositeDesign (CCD)
    ----------------------------
    Generates Central Composite Designs for response surface modeling.

    Supports both rotatable and face-centered CCD configurations. Includes factorial, axial and center points.

    Parameters:
    - factors_names (list of str): Names of the experimental factors.
    - center_points (int): Number of center points to include.
    - alpha_type (str): Type of axial distance ('rotatable' or 'face-centered').

    Attributes:
    - codified_matrix (pd.DataFrame): Matrix including factorial, axial and center points in coded form.

    Methods:
    - _alpha_rotatable(): Computes rotatable alpha value for the number of factors.
    - generate_codified_matrix(): Generates a rotatable CCD matrix.
    - generate_codified_matrix_fc(): Generates a face-centered CCD matrix (α = 1).
    - generate_doe(): Converts the codified CCD matrix to real experimental levels.
    """

    def __init__(self):
        self.matrix = None

    def _alpha_rotatable(self, k):
        return (2 ** k) ** 0.25

    def generate_codified_matrix(self, n_factors, factor_names, center_points=3):
        if len(factor_names) != n_factors:
            raise ValueError("Number of factor names must match number of factors.")

        # Factorial Part
        factorial_part = np.array(list(product([-1, 1], repeat=n_factors)))[:, ::-1]

        # Axial Part
        alpha = self._alpha_rotatable(n_factors)
        axial_part = []
        for i in range(n_factors):
            for sign in [-1, 1]:
                point = [0] * n_factors
                point[i] = sign * alpha
                axial_part.append(point)
        axial_part = np.array(axial_part)

        # Center points
        center_part = np.zeros((center_points, n_factors))

        # Dataframe with every parts together
        full_matrix = np.vstack([factorial_part, axial_part, center_part])
        df = pd.DataFrame(full_matrix, columns=factor_names)

        self.matrix = df
        return df
    
    def generate_codified_matrix_fc(self, n_factors, factor_names, center_points=1):
        """
        Generates a face-centered central composite design (CCD) matrix.
        All design points have coded levels of -1, 0, or +1.

        Parameters:
        - n_factors (int): number of factors
        - factor_names (list[str]): list of factor names
        - center_points (int): number of replicates at the center

        Returns:
        - pd.DataFrame: design matrix with coded levels
        """
        if len(factor_names) != n_factors:
            raise ValueError("Number of factor names must match number of factors.")

        # Factorial part
        factorial_part = np.array(list(product([-1, 1], repeat=n_factors)))[:, ::-1]
        df_factorial = pd.DataFrame(factorial_part.astype(int), columns=factor_names)

        # Axial points. Alpha = 1
        axial_part = []
        for i in range(n_factors):
            for sign in [-1, 1]:
                point = [0] * n_factors
                point[i] = sign
                axial_part.append(point)
        df_axial = pd.DataFrame(axial_part, columns=factor_names).astype(int)

        # Center points
        center_part = np.zeros((center_points, n_factors), dtype=int)
        df_center = pd.DataFrame(center_part, columns=factor_names)

        # Dataframe with everything together
        df = pd.concat([df_factorial, df_axial, df_center], ignore_index=True)

        self.matrix = df
        return df
    
    def generate_doe(self, factor_levels, center_levels):
        """
        Converts the codified matrix into real values using linear transformation:
        real = center + x * (high - low)/2

        Parameters:
        - factor_levels: list of tuples [(low1, high1), ..., (lowk, highk)]
        - center_levels: list of center points [c1, c2, ..., ck]

        Returns:
        - pd.DataFrame: real-valued design matrix
        """
        if self.matrix is None:
            raise ValueError("You must first generate a codified matrix.")

        if len(factor_levels) != self.matrix.shape[1] or len(center_levels) != self.matrix.shape[1]:
            raise ValueError("factor_levels and center_levels must match the number of factors.")

        # Converte tudo para float (para lidar com α como string formatada)
        coded = self.matrix.copy().astype(float)
        real = coded.copy()

        for i, name in enumerate(real.columns):
            low, high = factor_levels[i]
            center = center_levels[i]
            scale = (high - low) / 2
            real[name] = center + coded[name] * scale

        self.real_matrix = real
        return real

