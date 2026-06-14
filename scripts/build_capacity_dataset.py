import pandas as pd
import numpy as np

# Load data
df = pd.read_csv('data/cleaned/atus_sleep_work_active.csv')

# Create derived variables
# Structural Work Load (capacity_proxy): the share of waking time already claimed
# by structurally imposed demands — work AND the commute it requires — before any
# recovery can happen.
df['waking_hours'] = 24 - df['sleep_hours']
df['capacity_proxy'] = (df['work_hours'] + df['commute_hours']) / df['waking_hours']
df['sleep_threshold_indicator'] = (df['sleep_hours'] < 7).astype(int)

# Drop invalid rows
df = df[df['waking_hours'] > 0]

# Drop extreme values (top 1%)
capacity_99th = df['capacity_proxy'].quantile(0.99)
df = df[df['capacity_proxy'] <= capacity_99th]

# Save cleaned dataset
df.to_csv('data/cleaned/capacity_model_dataset.csv', index=False)

# Print distribution statistics
print("Capacity Proxy Distribution:")
print(f"Mean: {df['capacity_proxy'].mean():.4f}")
print(f"Std: {df['capacity_proxy'].std():.4f}")
print(f"Min: {df['capacity_proxy'].min():.4f}")
print(f"Max: {df['capacity_proxy'].max():.4f}")
print(f"Median: {df['capacity_proxy'].median():.4f}")
print(f"\nTotal rows: {len(df)}")

# Check for anomalies
print("\nAnomaly Check:")
print(f"Rows with capacity_proxy > 1: {(df['capacity_proxy'] > 1).sum()}")
print(f"Rows with capacity_proxy < 0: {(df['capacity_proxy'] < 0).sum()}")
print(f"Rows with sleep_threshold_indicator = 1: {df['sleep_threshold_indicator'].sum()}")
