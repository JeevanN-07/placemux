# Task 15 — Time-Series Forecasting Document

## 1. Objective & Model Selection
* **Objective**: Deliver a validated seasonal time-series forecast with confidence intervals to drive operational planning and capacity decisions[cite: 1].
* **Model Selected**: SARIMA(1,1,1)x(1,1,1,7) — fitted to capture weekly seasonality (7-day period) alongside underlying trend progression[cite: 1].

## 2. Decomposition Summary
* **Trend Component**: Constant upward linear trajectory from index baseline 100 to 200 over 180 days[cite: 1].
* **Seasonal Component**: Strong 7-day cyclical weekly oscillation observed with peak amplitude variation[cite: 1].
* **Residual Component**: Normally distributed zero-mean noise variance[cite: 1].

## 3. Backtest & Model Validation
* **Validation Strategy**: Train/test split with rolling window backtest on 150 training vs. 30 test periods[cite: 1].
* **Naive Baseline RMSE**: Evaluated using simple last-known value baseline[cite: 1].
* **SARIMA RMSE**: Demonstrates significantly lower prediction error than Naive baseline, confirming true predictive uplift[cite: 1].

## 4. Drivers, Assumptions & Risk Periods
* **Key Drivers**: Weekly seasonal demand spikes combined with sustained long-term growth trend[cite: 1].
* **Assumptions**: Stationarity achieved via first-differencing; stable weekly seasonal pattern sustained into future periods[cite: 1].
* **Risk Periods**: Sudden external disruptions or unmodeled holiday/event anomalies that break the weekly cyclical cadence[cite: 1].
