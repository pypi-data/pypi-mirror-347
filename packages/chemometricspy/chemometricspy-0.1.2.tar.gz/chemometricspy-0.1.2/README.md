# ChemometricsPy

**ChemometricsPy** is a modern, modular chemometrics library for Python, designed to support a wide range of multivariate methods in analytical chemistry, chemical engineering, and process optimization.

Currently, the package includes powerful tools for **Design of Experiments (DOE)** such as:
- Full factorial design
- Fractional factorial design with automatic resolution checking (III, IV, V)
- Central Composite Design (CCD) — rotatable and face-centered
- Box-Behnken Design (BBD)
- Built-in plotting functions and residual diagnostics

Future modules will include:
- Preprocessing (SNV, MSC, derivatives)
- Univariate and multivariate calibration (PLS, PCR, SVM)
- Exploratory analysis (PCA)
- Neural networks for chemometrics

## Installation

```bash
pip install chemometricspy
```

## Example

```python
from chemometricspy.doe import Factorial

f = Factorial(number_of_factors=3, factors_names=["pH", "Temp", "Conc"], center_points=4)
df = f.generate_codified_matrix()
print(df)
plan = f.generate_doe(factor_levels = [(4, 8), (25, 75), (0.25, 0.75)], center_levels = [6, 50, 0.50])
print(plan)
experimental = f.randomize(plan)
print(experimental)
f.calculate_effects(responses=[38.4, 66.1, 55.9, 69.8, 28.8, 39.6, 31.2, 28.8, 50.4, 51.6, 50.2, 48.3])
f.plot_pareto_effects(center_responses=[50.4, 51.6, 50.2, 48.3])
```

## Author

Developed by **Leonardo Guimarães**  
Email: leo.sguimaraes4@gmail.com

## Citation

If you use this library in your research or publication, please cite it as:

> Guimarães, L. (2025). *ChemometricsPy: A scientific Python library for chemometric modeling*. Version 0.1.0. https://pypi.org/project/chemometricspy

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.