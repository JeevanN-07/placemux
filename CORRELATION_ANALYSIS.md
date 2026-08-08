# Task 11: Correlation & Heatmaps Report

## 1. Correlation Matrix & Key Relationships
* **Score vs Passed Status ($r = 0.88, p < 0.001$):** Strong positive correlation confirming assessment scores directly determine pass status.
* **Student ID vs Score ($r = -0.07$):** Weak correlation confirming student ID sequence is spurious noise and non-causal.
* **Evaluated Dataset:** N=115 records filtered defensively from 120 raw rows.

---

## 2. Statistical Audit & Multicollinearity
* **Pearson vs Spearman Alignment:** Confirmed monotonic and linear relationships match across numerical variables.
* **Multicollinearity Flag:** High correlation ($r > 0.80$) detected between target metrics (`score` and `passed_numeric`). Recommendation: Exclude `passed_numeric` when training predictive scoring models to prevent target leakage.
* **Causality vs Spuriousity:** ID ordering shows no causal driver effect on final scores.
