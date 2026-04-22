import pandas as pd
import numpy as np

# Load ATUS data
print("Loading ATUS data...")
df = pd.read_csv('data/raw/atussum-0324/atussum_0324.dat')

print(f"Total observations: {len(df)}")
print(f"Total variables: {len(df.columns)}")

# Define activity code groups based on ATUS coding lexicon
# Sleep activities (01xxxx codes - personal care, including sleeping)
sleep_codes = [col for col in df.columns if col.startswith('t01')]

# Work activities (05xxxx codes - work and work-related activities)
work_codes = [col for col in df.columns if col.startswith('t05')]

print(f"Sleep activity codes: {len(sleep_codes)}")
print(f"Work activity codes: {len(work_codes)}")

# Calculate total minutes for each category
df['sleep_minutes'] = df[sleep_codes].sum(axis=1)
df['work_minutes'] = df[work_codes].sum(axis=1)

# Convert to hours
df['sleep_hours'] = df['sleep_minutes'] / 60
df['work_hours'] = df['work_minutes'] / 60

# Filter to active workers (people with work_hours > 0)
df_active = df[df['work_hours'] > 0].copy()

print(f"\nActive workers (work_hours > 0): {len(df_active)}")
print(f"Sleep hours - Mean: {df_active['sleep_hours'].mean():.2f}, Std: {df_active['sleep_hours'].std():.2f}")
print(f"Work hours - Mean: {df_active['work_hours'].mean():.2f}, Std: {df_active['work_hours'].std():.2f}")

# Select relevant columns for analysis
output_columns = ['sleep_hours', 'work_hours']
df_output = df_active[output_columns].copy()

# Remove any rows with missing or invalid values
df_output = df_output.dropna()
df_output = df_output[(df_output['sleep_hours'] > 0) & (df_output['sleep_hours'] < 24)]
df_output = df_output[(df_output['work_hours'] >= 0) & (df_output['work_hours'] < 24)]

print(f"\nFinal dataset size: {len(df_output)}")

# Save to cleaned data
df_output.to_csv('data/cleaned/atus_sleep_work_active.csv', index=False)
print("Saved to data/cleaned/atus_sleep_work_active.csv")

# Print summary statistics
print("\nSummary Statistics:")
print(df_output.describe())
