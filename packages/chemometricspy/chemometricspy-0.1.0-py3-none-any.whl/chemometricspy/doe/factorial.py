import pandas as pd
import numpy as np
import itertools
from itertools import combinations
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import t, norm
import warnings
from pandas.errors import PerformanceWarning

warnings.simplefilter(action='ignore', category=PerformanceWarning)

class Factorial:

    """
    Factorial
    ---------
    Generates a full two-level factorial design matrix with optional center points.

    This class supports the construction of complete 2^k factorial designs and their conversion to real-world levels.

    Parameters:
    - number_of_factors (int): Number of factors in the experiment.
    - factors_names (list of str): Names of the factors.
    - center_points (int): Number of center points (default is 0).

    Attributes:
    - codified_matrix (pd.DataFrame): The matrix with coded levels (-1, +1, and 0).
    - real_matrix (pd.DataFrame): Design matrix converted to real levels.
    - effects (dict): Stores calculated effects from experimental data.

    Methods:
    - generate_codified_matrix(): Generates the factorial matrix with ±1 levels and optional center points.
    - generate_doe(): Converts the codified matrix to real experimental levels.
    - calculate_effects(): Computes the main and interaction effects from responses.
    - plot_effects(): Bar chart of effect magnitudes.
    - plot_effects_percentage(): Plots the contribution percentage of each effect.
    - plot_effects_probability(): QQ-style plot for determining significant effects.
    - plot_effect_diagrams(): Main and interaction plots for exploratory visualization.
    - plot_pareto_effects(): Horizontal Pareto chart of effects for significance evaluation.
    """

    def __init__(self, number_of_factors, factors_names, center_points=0):
        if len(factors_names) != number_of_factors:
            raise ValueError("The number of factor names must match the number of factors.")
        self.number_of_factors = number_of_factors
        self.factors_names = factors_names
        self.center_points = center_points
        self.codified_matrix = None
        self.real_matrix = None
        self.effects = None

    def generate_codified_matrix(self):

        """
        Generates the codified (normalized) factorial design matrix.

        Returns:
        - pandas.DataFrame: A matrix with levels -1 and +1 for each factor.
        If center_points > 0, rows with level 0 are also included.

        Notes:
        - The matrix is saved internally as self.codified_matrix.
        - Each factor is varied across two levels: -1 (low) and +1 (high).
        - Center points are optional and are placed at level 0 for all factors.
            
        """
        
        k = len(self.factors_names)
        n_runs = 2 ** k
        matrix = []

        for i in range(n_runs):
            row = []
            for j in range(k):
                block_size = 2 ** j
                val = -1 if (i // block_size) % 2 == 0 else 1
                row.append(val)
            matrix.append(row)

            design_matrix = pd.DataFrame(matrix, columns=self.factors_names)
        

        if self.center_points > 0:
            center_row = pd.DataFrame([[0] * self.number_of_factors] * self.center_points,
                                      columns=self.factors_names)
        design_matrix = pd.concat([design_matrix, center_row], ignore_index=True)
        self.codified_matrix = design_matrix
        return self.codified_matrix
        

    def generate_doe(self, factor_levels, center_levels):
        
        """
        Converts the codified matrix to a real matrix using the specified factor levels.

        Parameters:
        - factor_levels: list of tuples (low, high) for each factor.
            Example: [(3.0, 7.0), (40, 80), (0.1, 0.9)]
        - center_levels: list of center values for each factor.
            Example: [5.0, 60, 0.5]

        Returns:
        - pandas.DataFrame: Real-world matrix with actual factor levels.

        Notes:
        - Requires self.codified_matrix to exist; generates it if not.
        - Replaces -1, 0, +1 in the codified matrix with corresponding real values.
        - Result is saved as self.real_matrix.
        
        """
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

    def calculate_effects(self, responses, display=True):
        """
        Calculates factorial effects manually without using DataFrame .prod().
        Uses only factorial points (±1), ignoring center points (0).

        Parameters:
        - responses: list of response values (same order as self.matrix)
        - display: whether to print the effects

        Stores:
        - self.effects: dict of effects { "A": value, "A*B": value, ... }
        """
        if self.codified_matrix is None:
            raise ValueError("Design matrix not found. Assign it to self.matrix first.")
        
        y = np.array(responses)
        X = self.codified_matrix.copy()

        # Remove center points (all zero)
        is_center = (X == 0).all(axis=1)
        X = X.loc[~is_center].reset_index(drop=True)
        y = y[~is_center]
        n = len(y)

        factor_names = list(X.columns)
        effects = {}

        # Main effects
        for name in factor_names:
            x = X[name].values
            effects[name] = (x * y).sum() / (n / 2)

        # Interactions
        for r in range(2, len(factor_names) + 1):
            for combo in combinations(factor_names, r):
                interaction_name = "*".join(combo)
                interaction_vector = np.ones(len(y))
                for factor in combo:
                    interaction_vector *= X[factor].values
                effects[interaction_name] = (interaction_vector * y).sum() / (n / 2)

        self.effects = {k: round(v, 3) for k, v in effects.items()}

        if display:
            print("\nCalculated effects:")
            for term, value in self.effects.items():
                print(f"{term:<20} → {value:.4f}")

        

    def plot_effects(self, color='#8dd3c7'):
        df_effects = pd.DataFrame.from_dict(self.effects, orient='index', columns=['Value']).reset_index()
        df_effects.columns = ['Effect', 'Value']
        df_effects_order = df_effects.sort_values(by='Value', ascending=True).reset_index(drop=True)
        df_effects_order = df_effects_order.set_index('Effect',drop=True)
        df_effects_order = df_effects_order.astype({'Value': np.float32})
        df_effects_order.plot(kind='bar', color=color)
        for i, v in enumerate(df_effects_order['Value']):
            if v < 0:
                plt.text(i, v, np.float32(round(v, 2)), ha='center', va='top')
            else:
                plt.text(i, v, np.float32(round(v, 2)), ha='center', va='bottom')
        plt.xlabel('Effects')
        plt.ylabel('Magnitude')
        plt.xticks(rotation=90)
        plt.title('Magnitude of Effects')
        plt.tight_layout()
        plt.show()

    def plot_effects_percentage(self, color='#8dd3c7'):
        df_effects = pd.DataFrame.from_dict(self.effects, orient='index', columns=['Value']).reset_index()
        df_effects.columns = ['Effect', 'Value']
        df_effects = df_effects.astype({'Value': np.float32})
        square_effects = df_effects['Value'] **2
        sum_effects = square_effects.sum()
        porcentage = (square_effects / sum_effects) * 100
        df_effects['Percentage'] = porcentage
        df_effects = df_effects.sort_values(by='Percentage', ascending=True)
        df_effects = df_effects.set_index('Effect')
        df_effects = df_effects.drop(columns='Value')
        df_effects.plot(kind='bar', color=color)

        for i, v in enumerate(df_effects['Percentage']):
            plt.text(i, v, f"{round(v, 2)}", ha='center', va='top' if v < 0 else 'bottom')

        plt.xlabel('Effects')
        plt.ylabel('Percentage of Contribution (%)')
        plt.xticks(rotation=90)
        plt.title('Percentage of Contribution of Effects')
        plt.tight_layout()
        plt.show()

    def plot_effects_probability(self, center_responses):
        """
        Plots probability plot of effects from self.effects using center point replicates.

        Parameters:
        - center_responses: list of replicate response values at center points
        """
        if not hasattr(self, "effects") or not self.effects:
            raise ValueError("No effects found. Run calculate_effects_direct() first.")

        df = pd.DataFrame(self.effects.items(), columns=["Effect", "Value"])
        df = df.sort_values(by="Value", ascending=True).reset_index(drop=True)

        z_scores = norm.ppf([(i + 0.5) / len(df) for i in range(len(df))])
        df["Z-score"] = z_scores

        std_r = np.std(center_responses, ddof=1)
        k = int(np.log2(len(self.effects)))
        denominator = np.sqrt(4 * (2 ** k))
        effect_error = (2 * std_r) / denominator
        gl = len(center_responses) - 1
        t_critical = t.ppf(1 - 0.05 / 2, df=gl)
        margin = effect_error * t_critical

        palette = dict(zip(df["Effect"], sns.color_palette("husl", len(df))))

        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=df, x="Value", y="Z-score", hue="Effect", palette=palette, s=100)
        plt.axvline(x=0, color='blue', linestyle='--')
        plt.axvline(x=margin, color='red', linestyle='--')
        plt.axvline(x=-margin, color='red', linestyle='--')
        plt.xlabel("Effects")
        plt.ylabel("Z-score")
        plt.title("Probability Plot of Effects")
        plt.legend(fontsize='small', loc='lower left', bbox_to_anchor=(1, 0.25))
        plt.tight_layout()
        plt.show()

    def plot_effect_diagrams(self, responses, effect="primary"):
        """
        Plots effect diagrams for primary effects and secondary interactions only.

        Parameters:
        - responses: list of response values (same length as self.matrix)
        - effect: "primary" or "secondary"

        Requires:
        - self.matrix: codified design matrix with ±1 and 0 levels
        """

        if self.codified_matrix is None:
            raise ValueError("Matrix not found. Assign self.matrix first.")

        X = self.codified_matrix.copy()
        y = np.array(responses)

        # Remove center points (all zero)
        is_center = (X == 0).all(axis=1)
        X = X.loc[~is_center].reset_index(drop=True)
        y = y[~is_center]

        factor_names = list(X.columns)

        if effect == "primary":
            n = len(factor_names)
            n_rows = (n + 1) // 2
            fig, axes = plt.subplots(n_rows, 2, figsize=(12, 4 * n_rows))
            axes = axes.flatten()
            for i, var in enumerate(factor_names):
                df = pd.DataFrame({var: X[var], 'Response': y})
                means = df.groupby(var)['Response'].mean()
                sns.pointplot(x=means.index, y=means.values, ax=axes[i])
                axes[i].set_title(f'Effect of {var}')
                axes[i].set_xlabel(f'{var} level')
                axes[i].set_ylabel('Mean Response')

            for j in range(i + 1, len(axes)):
                axes[j].axis('off')

            plt.tight_layout()
            plt.subplots_adjust(hspace=0.4, wspace=0.3)
            plt.show()

        elif effect == "secondary":
            if len(factor_names) < 2:
                raise ValueError("At least 2 factors required for secondary interactions.")

            combos = list(combinations(factor_names, 2))
            n_rows = (len(combos) + 2) // 3
            fig, axes = plt.subplots(n_rows, 3, figsize=(18, 5 * n_rows))
            axes = axes.flatten()

            for idx, combo in enumerate(combos):
                df = X[list(combo)].copy()
                df["Response"] = y
                means = df.groupby(list(combo))['Response'].mean()
                means = means.unstack()

                means.plot(marker='o', ax=axes[idx])
                axes[idx].set_title(f'Interaction: {combo[0]} x {combo[1]}')
                axes[idx].set_xlabel(combo[0])
                axes[idx].set_ylabel('Mean Response')
                axes[idx].legend(title=combo[1])

            for j in range(idx + 1, len(axes)):
                axes[j].axis('off')

            plt.tight_layout()
            plt.subplots_adjust(hspace=0.4, wspace=0.3)
            plt.show()

        else:
            raise ValueError("Invalid effect type. Choose 'primary' or 'secondary'.")
        
    def plot_pareto_effects(self, center_responses=None, alpha=0.05):
        """
        Plots a Pareto chart of effects sorted by absolute magnitude.
        
        Parameters:
        - center_responses: list of center point responses, required for significance threshold
        - alpha: significance level (default = 0.05)

        Requires:
        - self.effects: dict with effect names and values
        """
        
        if not hasattr(self, "effects") or not self.effects:
            raise ValueError("No effects found. Use calculate_effects first.")

        df = pd.DataFrame(self.effects.items(), columns=["Effect", "Value"])
        df["AbsValue"] = df["Value"].abs()
        df = df.sort_values(by="AbsValue", ascending=False).reset_index(drop=True)

        # Calcular limiar de significância se pontos centrais forem fornecidos
        if center_responses is not None:
            std_r = np.std(center_responses, ddof=1)
            n_effects = len(self.effects)
            k = int(np.log2(n_effects))
            denominator = np.sqrt(4 * (2 ** k))
            effect_error = (2 * std_r) / denominator
            gl = len(center_responses) - 1
            t_critical = t.ppf(1 - alpha / 2, df=gl)
            margin = t_critical * effect_error
        else:
            margin = None

        # Gráfico de barras (Pareto)
        plt.figure(figsize=(10, 6))
        bars = plt.bar(df["Effect"], df["AbsValue"], color="#8dd3c7")
        
        if margin:
            plt.axhline(y=margin, color="red", linestyle="--", label=f"Significance limit ({alpha*100:.0f}%)")

        plt.xticks(rotation=90)
        plt.ylabel("Absolute Effect")
        plt.title("Pareto Chart of Effects")
        plt.tight_layout()
        if margin:
            plt.legend()
        plt.show()