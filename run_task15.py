import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error

# 1. Generate Synthetic Daily Time-Series Data with Seasonality & Trend
np.random.seed(42)
dates = pd.date_range(start="2024-01-01", periods=180, freq="D")
trend = np.linspace(100, 200, 180)
seasonality = 15 * np.sin(2 * np.pi * dates.dayofweek / 7)
noise = np.random.normal(0, 5, 180)
values = trend + seasonality + noise

df = pd.DataFrame({"ds": dates, "y": values}).set_index("ds")

# 2. Decompose Time Series
decomposition = seasonal_decompose(df["y"], model="additive", period=7)

fig = decomposition.plot()
fig.set_size_inches(10, 8)
plt.suptitle("Time-Series Decomposition (Trend, Seasonality, Residuals)", fontsize=12)
plt.tight_layout()
plt.savefig("time_series_decomposition.png")
plt.close()

# 3. Rolling Window Backtest: SARIMA vs Naive Baseline
train_size = 150
train, test = df.iloc[:train_size], df.iloc[train_size:]

naive_preds = [train["y"].iloc[-1]] + list(test["y"].iloc[:-1].values)

model = SARIMAX(train["y"], order=(1,1,1), seasonal_order=(1,1,1,7))
results = model.fit(disp=False)

forecast_res = results.get_forecast(steps=len(test))
sarima_preds = forecast_res.predicted_mean
conf_int = forecast_res.conf_int()

naive_rmse = np.sqrt(mean_squared_error(test["y"], naive_preds))
sarima_rmse = np.sqrt(mean_squared_error(test["y"], sarima_preds))

print(f"--- VALIDATION RESULTS ---")
print(f"Naive Baseline RMSE: {naive_rmse:.2f}")
print(f"SARIMA Model RMSE:    {sarima_rmse:.2f}")

# 4. Plot Final Forecast with Confidence Intervals
plt.figure(figsize=(12, 6))
plt.plot(train.index, train["y"], label="Historical Train")
plt.plot(test.index, test["y"], label="Actual Test Data", color="black", alpha=0.7)
plt.plot(test.index, sarima_preds, label="SARIMA Forecast", color="red", linestyle="--")
plt.fill_between(test.index, conf_int.iloc[:, 0], conf_int.iloc[:, 1], color="red", alpha=0.2, label="95% Confidence Interval")
plt.title("Task 15: Seasonal Time-Series Forecast with SARIMA")
plt.xlabel("Date")
plt.ylabel("Metric / Demand")
plt.legend()
plt.grid(True)
plt.savefig("forecast_plot.png")
plt.close()

print("Task 15 Python script executed successfully!")
