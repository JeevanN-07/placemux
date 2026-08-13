import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# 1. Load Data / Create Representative Arrays
np.random.seed(42)
n_samples = 250

# Generate distinct data distributions (Normal, Skewed, Uniform)
score_array = np.random.normal(loc=68, scale=12, size=n_samples)
time_spent_array = np.random.exponential(scale=25, size=n_samples) # Right-skewed
submissions_array = np.random.poisson(lam=3, size=n_samples)      # Discrete skewed

df = pd.DataFrame({
    'score': np.clip(score_array, 0, 100),
    'time_spent': time_spent_array,
    'submission_count': submissions_array
})

# Save clean copy
df.to_csv('data/distribution_review_data.csv', index=False)

# 2. Distribution Review & Summary Statistics
summary_stats = df.describe().T
summary_stats['skewness'] = df.skew()
summary_stats['kurtosis'] = df.kurtosis()

print("=== ARRAY DISTRIBUTION SUMMARY ===")
print(summary_stats[['mean', 'std', 'min', '50%', 'max', 'skewness', 'kurtosis']])

# 3. Normality Testing (Shapiro-Wilk Test)
print("\n=== NORMALITY TESTING (Shapiro-Wilk) ===")
normality_results = {}
for col in df.columns:
    stat, p_val = stats.shapiro(df[col])
    is_normal = p_val > 0.05
    normality_results[col] = {'stat': stat, 'p_value': p_val, 'is_normal': is_normal}
    print(f"Column: {col:18} | Stat: {stat:.4f} | p-value: {p_val:.4e} | Normal: {is_normal}")

# 4. Data Transformations (Log & Scaling)
df['time_spent_log'] = np.log1p(df['time_spent']) # Handle right-skew

scaler_standard = StandardScaler()
scaler_minmax = MinMaxScaler()

df_scaled = pd.DataFrame(
    scaler_standard.fit_transform(df[['score', 'time_spent_log']]),
    columns=['score_zscore', 'time_spent_log_zscore']
)

# 5. Visualizations (Histograms & Box Plots)
fig, axes = plt.subplots(3, 2, figsize=(12, 10))
fig.suptitle("Task 14 — Data Array Distribution & Transformation Review", fontsize=14, fontweight='bold')

# Score Distribution
sns.histplot(df['score'], kde=True, ax=axes[0, 0], color='#2563eb')
axes[0, 0].set_title("Score Array (Near-Normal)")
sns.boxplot(x=df['score'], ax=axes[0, 1], color='#60a5fa')
axes[0, 1].set_title("Score Array Spread & Outliers")

# Time Spent (Raw Skewed)
sns.histplot(df['time_spent'], kde=True, ax=axes[1, 0], color='#dc2626')
axes[1, 0].set_title("Time Spent Array (Right-Skewed)")
sns.boxplot(x=df['time_spent'], ax=axes[1, 1], color='#f87171')
axes[1, 1].set_title("Time Spent Spread & Extreme Outliers")

# Log-Transformed & Standardized
sns.histplot(df['time_spent_log'], kde=True, ax=axes[2, 0], color='#16a34a')
axes[2, 0].set_title("Log-Transformed Time Spent (Normalized)")
sns.histplot(df_scaled['time_spent_log_zscore'], kde=True, ax=axes[2, 1], color='#059669')
axes[2, 1].set_title("Standardized Z-Score Scaled (Mean=0, Std=1)")

plt.tight_layout()
plt.savefig("distribution_review_plots.png")
plt.close()

print("\nDistribution analysis complete! Plots saved as 'distribution_review_plots.png'.")
