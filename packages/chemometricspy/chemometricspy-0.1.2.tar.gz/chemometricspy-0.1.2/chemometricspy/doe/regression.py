import pandas as pd
import numpy as np
from itertools import combinations
import matplotlib.pyplot as plt
import seaborn as sns


class RegressionAnalysis:

    """
    RegressionAnalysis
    ------------------
    Performs regression analysis (linear or quadratic) on coded design matrices.

    Supports visualization of regression diagnostics and model predictions.

    Attributes:
    - matrix (pd.DataFrame): Full X matrix used in regression.
    - coefficients (dict): Estimated regression coefficients.
    - y_pred (np.array): Predicted Y values.
    - residuals (np.array): Vector of residuals.
    - model_type (str): Type of regression ("linear" or "quadratic").
    - y_actual (np.array): Original response values used for fitting.

    Methods:
    - fit(): Builds the regression model based on matrix and responses.
    - regression_equation(): Prints the formatted regression model as an equation.
    - plot_residual_distribution(): KDE plot of residuals to assess normality.
    - plot_residuals_vs_predicted(): Scatter plot of residuals vs predicted values.
    - plot_predicted_vs_actual(): Scatter plot of predicted vs actual responses with R² annotation.
    """
    
    def __init__(self):
        self.matrix = None
        self.coefficients = None
        self.y_pred = None
        self.residuals = None
        self.model_type = None
        self.y_actual = None

    def fit(self, matrix, responses, model_type="linear", display=True):
        """
        Builds a regression model from a given design matrix and response vector.

        Parameters:
        - matrix: codified design matrix (DataFrame)
        - responses: list or array of Y values
        - model_type: "linear" or "quadratic"

        Saves:
        - self.matrix: full matrix X used for regression
        - self.coefficients: dict of estimated coefficients
        - self.y_pred: predicted values
        - self.residuals: residuals (Y - Ŷ)
        """
        if matrix is None or not isinstance(matrix, pd.DataFrame):
            raise ValueError("Matrix must be a pandas DataFrame.")
        
        matrix = matrix.copy().reset_index(drop=True).dropna()
        responses = np.array(responses).ravel()

        if len(matrix) != len(responses):
            raise ValueError("Response vector length must match matrix rows.")

        X_base = matrix.copy()
        y = np.array(responses)
        X = pd.DataFrame(index=X_base.index)

        # Intercept
        X["Intercept"] = 1

        # Main effects
        for col in X_base.columns:
            X[col] = X_base[col]

        # Interaction terms (2 to k)
        k = len(X_base.columns)
        for r in range(2, k + 1):
            for combo in combinations(X_base.columns, r):
                name = "*".join(combo)
                X[name] = X_base[list(combo)].prod(axis=1)

        # Quadratic terms (X1^2, X2^2, ...)
        if model_type == "quadratic":
            for col in X_base.columns:
                name = f"{col}²"
                X[name] = X_base[col] ** 2

        # Regression equation
        XT = X.T.values
        coef = np.linalg.inv(XT @ X.values) @ XT @ y
        y_pred = X @ coef
        residuals = y - y_pred

        self.matrix = X
        self.model_type = model_type
        self.coefficients = dict(zip(X.columns, coef))
        self.y_pred = y_pred
        self.residuals = residuals
        self.y_actual = y

        print("\nRegression Coefficients:\n")
        for name, value in self.coefficients.items():
            print(f"{name:<20} → {round(value, 4)}")
        
    def regression_equation(self, decimals=3):
        """
        Prints the regression equation based on self.model_coefficients.
        Uses proper formatting for quadratic terms (e.g., X1²).

        Parameters:
        - decimals: int, number of decimal places for coefficients
        """
        if not hasattr(self, "coefficients") or not self.coefficients:
            raise ValueError("No model coefficients found. Run regression() first.")

        terms = []
        for term, coef in self.coefficients.items():
            coef = round(coef, decimals)

            if term == "Intercept":
                terms.insert(0, f"{coef}")
            else:
                # Formatar termo quadrático se terminar com '²'
                formatted_term = term.replace("**2", "²").replace("^2", "²")
                sign = "+" if coef >= 0 else "-"
                terms.append(f" {sign} {abs(coef)}*{formatted_term}")

        equation = "Y = " + "".join(terms)
        print("\nRegression Equation:")
        print(equation)
        return equation
    
    def plot_residual_distribution(self):
        """
        Plots only the KDE (density curve) of residuals, without histogram.
        """

        if not hasattr(self, "residuals") or self.residuals is None:
            raise ValueError("No residuals found. Run regression() first.")

        plt.figure(figsize=(8, 5))
        sns.kdeplot(self.residuals, fill=True, color="#8dd3c7", linewidth=2)
        plt.title("Residual Distribution")
        plt.xlabel("Residuals")
        plt.ylabel("Density")
        plt.tight_layout()
        plt.show()

    def plot_residuals_vs_predicted(self, color="#4682B4"):
        """
        Plots residuals versus predicted Y values.
        """

        if not hasattr(self, "residuals") or self.residuals is None:
            raise ValueError("No residuals found. Run regression() first.")
        if not hasattr(self, "y_pred") or self.y_pred is None:
            raise ValueError("No predicted values found. Run regression() first.")

        plt.figure(figsize=(8, 5))
        sns.scatterplot(x=self.y_pred, y=self.residuals, color=color, s=80)
        plt.axhline(y=0, color="red", linestyle="--")
        plt.title("Residuals vs Predicted")
        plt.xlabel("Predicted Y")
        plt.ylabel("Residuals")
        plt.tight_layout()
        plt.show()

    def plot_predicted_vs_actual(self):
        """
        Plots a scatterplot of predicted vs actual values.
        Uses self.y_pred and self.y_real from the last regression.
        """
        import matplotlib.pyplot as plt
        import seaborn as sns
        import numpy as np

        if not hasattr(self, "y_pred") or self.y_pred is None:
            raise ValueError("No predicted values found. Run regression() first.")
        if not hasattr(self, "y_actual") or self.y_actual is None:
            raise ValueError("No actual values found. Run regression() first.")

        plt.figure(figsize=(7.5, 6))
        sns.scatterplot(x=self.y_actual, y=self.y_pred, color="#1F4E79", s=100)

        # Linha y = x (linha ideal)
        min_val = min(min(self.y_actual), min(self.y_pred))
        max_val = max(max(self.y_actual), max(self.y_pred))
        plt.plot([min_val, max_val], [min_val, max_val], '--', color="gray", linewidth=1.5)

        # R²
        SSr = np.sum((self.y_actual - self.y_pred) ** 2)
        SST = np.sum((self.y_actual - np.mean(self.y_actual)) ** 2)
        r2 = 1 - (SSr / SST)

        # Anotação R²
        plt.text(min_val + 0.05 * (max_val - min_val), 
                max_val - 0.1 * (max_val - min_val),
                f"$R^2$ = {r2:.4f}", fontsize=12, color="#1F4E79")

        plt.xlabel("Actual Values", fontsize=12)
        plt.ylabel("Predicted Values", fontsize=12)
        plt.title("Predicted vs Actual", fontsize=14)
        plt.grid(alpha=0.3)
        plt.tight_layout()
        plt.show()
        