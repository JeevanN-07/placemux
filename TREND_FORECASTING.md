# Task 9: Trend Forecasting Report

## 1. Model Performance vs Baseline
* **Baseline (Naive Last Value) MAE:** 23.56
* **Exponential Smoothing Model MAE:** 20.97
* **Evaluated Records:** N=115 cleaned daily submissions (filtered from 120 raw records)

---

## 2. Forecast & Uncertainty Bounds
* **7-Day Projection:** Score trend projected forward with a 95% confidence interval ($\pm{1.96 	imes 	ext{std\_err}}$).
* **Assumptions:** Stationarity in evaluation grading logic without unannounced syllabus shifts.
