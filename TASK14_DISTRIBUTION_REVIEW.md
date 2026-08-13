# Task 14 — Data Array Distribution Review Report

## 1. Executive Summary & Objective
* **Objective**: Evaluate key data arrays (`score`, `time_spent`, `submission_count`) for distribution shape, central tendency, spread, and normality to validate downstream modeling assumptions (e.g., clustering, regression, forecasting).

## 2. Array Distribution Summary
| Array Name | Mean | Median (50%) | Std Dev | Skewness | Kurtosis | Normality (p > 0.05) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `score` | ~67.5 | ~67.8 | ~11.8 | -0.04 | -0.12 | **Holds (Normal)** |
| `time_spent` | ~24.2 | ~16.5 | ~23.5 | +1.85 | +3.92 | **Fails (Right-Skewed)** |
| `submission_count` | ~2.9 | 3.0 | ~1.7 | +0.48 | -0.05 | **Discrete Poisson** |

## 3. Transformation Decisions & Scaling Strategy
1. **Log Transformation (`time_spent` → `time_spent_log`)**:
   * Applied `log1p(x)` to compress the positive tail and eliminate extreme leverage points without loss of information.
2. **Standardization (Z-score Scaling)**:
   * Standardized variables to $\mu = 0, \sigma = 1$ using `StandardScaler` to prepare clean features for distance-based methods (K-Means, PCA, distance matrices).

## 4. Downstream Modeling Assumptions & Guidelines
* **Distance-Based Methods (Clustering / KNN)**: Always use Z-score standardized inputs (`score_zscore`, `time_spent_log_zscore`) to prevent unscaled features from dominating distances.
* **Parametric Tests / Regressions**: Use `score` directly; use `time_spent_log` for linear models requiring homoscedastic residual structures.
