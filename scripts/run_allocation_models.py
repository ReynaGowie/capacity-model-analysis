import pandas as pd
import numpy as np
import statsmodels.api as sm
import os

# Ensure output directory exists
os.makedirs('outputs/tables', exist_ok=True)

# ============================================================
# LOAD DATA
# ============================================================
print("=" * 60)
print("LOADING DATA")
print("=" * 60)

df = pd.read_csv('data/cleaned/capacity_model_dataset.csv')
print(f"Data loaded: {len(df)} rows")
print(f"Columns: {df.columns.tolist()}")

# ============================================================
# STEP 1: MODEL WORK HOURS AS OUTCOME
# ============================================================
print("\n" + "=" * 60)
print("STEP 1: MODELING WORK HOURS AS OUTCOME")
print("=" * 60)

y = df['work_hours']

# Model A: work_hours ~ sleep_hours
X_a = df['sleep_hours']
X_a = sm.add_constant(X_a)
model_a = sm.OLS(y, X_a).fit()
print("\nModel A: work_hours ~ sleep_hours")
print(f"R-squared: {model_a.rsquared:.4f}")
print(model_a.summary().tables[1])

# Model B: work_hours ~ sleep_hours + waking_hours
X_b = df[['sleep_hours', 'waking_hours']]
X_b = sm.add_constant(X_b)
model_b = sm.OLS(y, X_b).fit()
print("\nModel B: work_hours ~ sleep_hours + waking_hours")
print(f"R-squared: {model_b.rsquared:.4f}")
print(model_b.summary().tables[1])

# Model C: work_hours ~ sleep_hours + sleep_threshold_indicator
X_c = df[['sleep_hours', 'sleep_threshold_indicator']]
X_c = sm.add_constant(X_c)
model_c = sm.OLS(y, X_c).fit()
print("\nModel C: work_hours ~ sleep_hours + sleep_threshold_indicator")
print(f"R-squared: {model_c.rsquared:.4f}")
print(model_c.summary().tables[1])

# Model D: work_hours ~ sleep_hours + sleep_hours^2
df['sleep_hours_squared'] = df['sleep_hours'] ** 2
X_d = df[['sleep_hours', 'sleep_hours_squared']]
X_d = sm.add_constant(X_d)
model_d = sm.OLS(y, X_d).fit()
print("\nModel D: work_hours ~ sleep_hours + sleep_hours^2")
print(f"R-squared: {model_d.rsquared:.4f}")
print(model_d.summary().tables[1])

# ============================================================
# STEP 2: OUTPUT
# ============================================================
print("\n" + "=" * 60)
print("STEP 2: SAVING RESULTS")
print("=" * 60)

results = []
for i, model in enumerate([model_a, model_b, model_c, model_d], 1):
    results.append({
        'model': f'Model {chr(64+i)}',
        'r_squared': model.rsquared,
        'adj_r_squared': model.rsquared_adj,
        'n_obs': int(model.nobs)
    })

results_df = pd.DataFrame(results)
results_df.to_csv('outputs/tables/allocation_model_results.csv', index=False)
print("Results saved to outputs/tables/allocation_model_results.csv")
print(results_df.to_string(index=False))

# ============================================================
# STEP 3: INTERPRETATION
# ============================================================
print("\n" + "=" * 60)
print("STEP 3: INTERPRETATION")
print("=" * 60)

print("\nSUMMARY OF FINDINGS:")
print("-" * 60)

# Does sleep significantly predict work_hours?
sleep_sig = model_a.pvalues['sleep_hours'] < 0.05
print(f"1. Sleep significantly predicts work_hours: {sleep_sig}")
if sleep_sig:
    print(f"   - Coefficient: {model_a.params['sleep_hours']:.4f} (p={model_a.pvalues['sleep_hours']:.4f})")
    direction = "positive" if model_a.params['sleep_hours'] > 0 else "negative"
    print(f"   - Direction: {direction}")

# Is the relationship strong or weak?
print(f"\n2. Relationship strength:")
print(f"   - R-squared (Model A): {model_a.rsquared:.4f}")
print(f"   - Interpretation: {'Strong' if model_a.rsquared > 0.3 else 'Moderate' if model_a.rsquared > 0.1 else 'Weak'}")

# Does the threshold (<7h) matter?
threshold_sig = model_c.pvalues['sleep_threshold_indicator'] < 0.05
print(f"\n3. Sleep threshold (<7h) significantly predicts work_hours: {threshold_sig}")
if threshold_sig:
    print(f"   - Coefficient: {model_c.params['sleep_threshold_indicator']:.4f} (p={model_c.pvalues['sleep_threshold_indicator']:.4f})")

# How much variance is explained?
print(f"\n4. Variance explained by each model:")
print(f"   - Model A (sleep only): {model_a.rsquared*100:.2f}%")
print(f"   - Model B (sleep + waking): {model_b.rsquared*100:.2f}%")
print(f"   - Model C (sleep + threshold): {model_c.rsquared*100:.2f}%")
print(f"   - Model D (sleep + quadratic): {model_d.rsquared*100:.2f}%")

# Quadratic term significance
quad_sig = model_d.pvalues['sleep_hours_squared'] < 0.05
print(f"\n5. Quadratic sleep term significant: {quad_sig}")
if quad_sig:
    print(f"   - Coefficient: {model_d.params['sleep_hours_squared']:.4f} (p={model_d.pvalues['sleep_hours_squared']:.4f})")

print("\n" + "=" * 60)
print("ANALYSIS COMPLETE")
print("=" * 60)
