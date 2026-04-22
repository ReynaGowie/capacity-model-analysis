import pandas as pd
import numpy as np
import statsmodels.api as sm
from scipy import stats
import os

# Ensure output directory exists
os.makedirs('outputs/tables', exist_ok=True)

# ============================================================
# STEP 1: LOAD DATA
# ============================================================
print("=" * 60)
print("STEP 1: LOADING DATA")
print("=" * 60)

df = pd.read_csv('data/cleaned/capacity_model_dataset.csv')

# Confirm columns
required_columns = ['work_hours', 'sleep_hours', 'waking_hours', 'capacity_proxy', 'sleep_threshold_indicator']
missing_cols = [col for col in required_columns if col not in df.columns]
if missing_cols:
    raise ValueError(f"Missing required columns: {missing_cols}")

print(f"Data loaded successfully: {len(df)} rows")
print(f"Columns confirmed: {required_columns}")

# ============================================================
# STEP 2: DESCRIPTIVE STATS
# ============================================================
print("\n" + "=" * 60)
print("STEP 2: DESCRIPTIVE STATISTICS")
print("=" * 60)

variables = ['work_hours', 'sleep_hours', 'waking_hours', 'capacity_proxy']
desc_stats = []

for var in variables:
    var_data = df[var]
    q25 = var_data.quantile(0.25)
    q75 = var_data.quantile(0.75)
    
    desc_stats.append({
        'variable': var,
        'count': len(var_data),
        'mean': var_data.mean(),
        'median': var_data.median(),
        'std': var_data.std(),
        'min': var_data.min(),
        'q25': q25,
        'q75': q75,
        'max': var_data.max(),
        'iqr': q75 - q25
    })

desc_df = pd.DataFrame(desc_stats)
desc_df.to_csv('outputs/tables/capacity_descriptive_stats.csv', index=False)
print("Descriptive statistics saved to outputs/tables/capacity_descriptive_stats.csv")
print(desc_df.to_string(index=False))

# ============================================================
# STEP 3: CORRELATIONS
# ============================================================
print("\n" + "=" * 60)
print("STEP 3: CORRELATIONS")
print("=" * 60)

correlation_pairs = [
    ('sleep_hours', 'capacity_proxy'),
    ('waking_hours', 'capacity_proxy'),
    ('work_hours', 'sleep_hours')
]

correlations = []
for x, y in correlation_pairs:
    pearson_r, pearson_p = stats.pearsonr(df[x], df[y])
    spearman_r, spearman_p = stats.spearmanr(df[x], df[y])
    
    correlations.append({
        'variable_1': x,
        'variable_2': y,
        'pearson_r': pearson_r,
        'pearson_p': pearson_p,
        'spearman_r': spearman_r,
        'spearman_p': spearman_p
    })

corr_df = pd.DataFrame(correlations)
corr_df.to_csv('outputs/tables/capacity_correlations.csv', index=False)
print("Correlations saved to outputs/tables/capacity_correlations.csv")
print(corr_df.to_string(index=False))

# ============================================================
# STEP 4: MODEL COMPARISON
# ============================================================
print("\n" + "=" * 60)
print("STEP 4: MODEL COMPARISON")
print("=" * 60)

# Prepare data for modeling
X = df['sleep_hours']
X = sm.add_constant(X)
y = df['capacity_proxy']

# MODEL 1: capacity_proxy ~ sleep_hours
model1 = sm.OLS(y, X).fit()
print("\nMODEL 1: capacity_proxy ~ sleep_hours")
print(f"R-squared: {model1.rsquared:.4f}")
print(model1.summary().tables[1])

# MODEL 2: capacity_proxy ~ sleep_hours + sleep_threshold_indicator
X2 = df[['sleep_hours', 'sleep_threshold_indicator']]
X2 = sm.add_constant(X2)
model2 = sm.OLS(y, X2).fit()
print("\nMODEL 2: capacity_proxy ~ sleep_hours + sleep_threshold_indicator")
print(f"R-squared: {model2.rsquared:.4f}")
print(model2.summary().tables[1])

# MODEL 3: capacity_proxy ~ sleep_hours + work_hours + interaction
df['sleep_work_interaction'] = df['sleep_hours'] * df['work_hours']
X3 = df[['sleep_hours', 'work_hours', 'sleep_work_interaction']]
X3 = sm.add_constant(X3)
model3 = sm.OLS(y, X3).fit()
print("\nMODEL 3: capacity_proxy ~ sleep_hours + work_hours + interaction")
print(f"R-squared: {model3.rsquared:.4f}")
print(model3.summary().tables[1])

# MODEL 4: capacity_proxy ~ sleep_hours + sleep_hours^2
df['sleep_hours_squared'] = df['sleep_hours'] ** 2
X4 = df[['sleep_hours', 'sleep_hours_squared']]
X4 = sm.add_constant(X4)
model4 = sm.OLS(y, X4).fit()
print("\nMODEL 4: capacity_proxy ~ sleep_hours + sleep_hours^2")
print(f"R-squared: {model4.rsquared:.4f}")
print(model4.summary().tables[1])

# MODEL 5: capacity_proxy ~ sleep_hours + work_hours + sleep_threshold_indicator + interaction
X5 = df[['sleep_hours', 'work_hours', 'sleep_threshold_indicator', 'sleep_work_interaction']]
X5 = sm.add_constant(X5)
model5 = sm.OLS(y, X5).fit()
print("\nMODEL 5: capacity_proxy ~ sleep_hours + work_hours + sleep_threshold_indicator + interaction")
print(f"R-squared: {model5.rsquared:.4f}")
print(model5.summary().tables[1])

# Compile model results
model_results = []
for i, model in enumerate([model1, model2, model3, model4, model5], 1):
    model_results.append({
        'model': f'Model {i}',
        'r_squared': model.rsquared,
        'adj_r_squared': model.rsquared_adj,
        'n_obs': int(model.nobs)
    })

model_results_df = pd.DataFrame(model_results)
model_results_df.to_csv('outputs/tables/capacity_model_results.csv', index=False)
print("\nModel comparison saved to outputs/tables/capacity_model_results.csv")
print(model_results_df.to_string(index=False))

# ============================================================
# STEP 5: THRESHOLD ANALYSIS
# ============================================================
print("\n" + "=" * 60)
print("STEP 5: THRESHOLD ANALYSIS")
print("=" * 60)

low_sleep = df[df['sleep_hours'] < 7]
high_sleep = df[df['sleep_hours'] >= 7]

threshold_stats = []
for var in ['capacity_proxy', 'work_hours', 'waking_hours']:
    low_mean = low_sleep[var].mean()
    high_mean = high_sleep[var].mean()
    mean_diff = high_mean - low_mean
    pct_diff = (mean_diff / low_mean) * 100 if low_mean != 0 else np.nan
    
    threshold_stats.append({
        'variable': var,
        'sleep_lt_7_mean': low_mean,
        'sleep_gte_7_mean': high_mean,
        'mean_difference': mean_diff,
        'percent_difference': pct_diff
    })

threshold_df = pd.DataFrame(threshold_stats)
threshold_df.to_csv('outputs/tables/capacity_threshold_comparison.csv', index=False)
print("Threshold comparison saved to outputs/tables/capacity_threshold_comparison.csv")
print(threshold_df.to_string(index=False))

# ============================================================
# STEP 6: ROBUSTNESS CHECK
# ============================================================
print("\n" + "=" * 60)
print("STEP 6: ROBUSTNESS CHECK")
print("=" * 60)

# Create reduced dataset excluding extreme sleepers
df_reduced = df[(df['sleep_hours'] >= 4) & (df['sleep_hours'] <= 12)]
print(f"Reduced sample size: {len(df_reduced)} (excluded {len(df) - len(df_reduced)} extreme sleepers)")

# Re-run MODEL 1 on reduced sample
X_reduced = df_reduced['sleep_hours']
X_reduced = sm.add_constant(X_reduced)
y_reduced = df_reduced['capacity_proxy']
model1_reduced = sm.OLS(y_reduced, X_reduced).fit()

# Re-run MODEL 3 on reduced sample
df_reduced['sleep_work_interaction'] = df_reduced['sleep_hours'] * df_reduced['work_hours']
X3_reduced = df_reduced[['sleep_hours', 'work_hours', 'sleep_work_interaction']]
X3_reduced = sm.add_constant(X3_reduced)
model3_reduced = sm.OLS(y_reduced, X3_reduced).fit()

robustness_results = [
    {
        'model': 'Model 1 (full sample)',
        'r_squared': model1.rsquared,
        'sleep_coef': model1.params['sleep_hours'],
        'sleep_se': model1.bse['sleep_hours'],
        'sleep_pval': model1.pvalues['sleep_hours']
    },
    {
        'model': 'Model 1 (reduced sample)',
        'r_squared': model1_reduced.rsquared,
        'sleep_coef': model1_reduced.params['sleep_hours'],
        'sleep_se': model1_reduced.bse['sleep_hours'],
        'sleep_pval': model1_reduced.pvalues['sleep_hours']
    },
    {
        'model': 'Model 3 (full sample)',
        'r_squared': model3.rsquared,
        'sleep_coef': model3.params['sleep_hours'],
        'sleep_se': model3.bse['sleep_hours'],
        'sleep_pval': model3.pvalues['sleep_hours']
    },
    {
        'model': 'Model 3 (reduced sample)',
        'r_squared': model3_reduced.rsquared,
        'sleep_coef': model3_reduced.params['sleep_hours'],
        'sleep_se': model3_reduced.bse['sleep_hours'],
        'sleep_pval': model3_reduced.pvalues['sleep_hours']
    }
]

robustness_df = pd.DataFrame(robustness_results)
robustness_df.to_csv('outputs/tables/capacity_robustness.csv', index=False)
print("Robustness check saved to outputs/tables/capacity_robustness.csv")
print(robustness_df.to_string(index=False))

# ============================================================
# STEP 7: INTERPRETATION
# ============================================================
print("\n" + "=" * 60)
print("STEP 7: INTERPRETATION")
print("=" * 60)

print("\nSUMMARY OF FINDINGS:")
print("-" * 60)

# 1. Is sleep_hours significantly associated with capacity_proxy?
sleep_sig = model1.pvalues['sleep_hours'] < 0.05
print(f"1. Sleep hours significantly associated with capacity_proxy: {sleep_sig}")
if sleep_sig:
    print(f"   - Coefficient: {model1.params['sleep_hours']:.4f} (p={model1.pvalues['sleep_hours']:.4f})")
    direction = "positive" if model1.params['sleep_hours'] > 0 else "negative"
    print(f"   - Direction: {direction}")

# 2. Does the sleep threshold (< 7 hours) matter?
threshold_sig = model2.pvalues['sleep_threshold_indicator'] < 0.05
print(f"\n2. Sleep threshold (< 7 hours) significantly associated: {threshold_sig}")
if threshold_sig:
    print(f"   - Coefficient: {model2.params['sleep_threshold_indicator']:.4f} (p={model2.pvalues['sleep_threshold_indicator']:.4f})")

# 3. Does adding work_hours and interaction improve explanatory power?
r2_improvement = model3.rsquared - model1.rsquared
print(f"\n3. Adding work_hours and interaction improves R-squared by {r2_improvement:.4f}")
print(f"   - Model 1 R-squared: {model1.rsquared:.4f}")
print(f"   - Model 3 R-squared: {model3.rsquared:.4f}")
interaction_sig = model3.pvalues['sleep_work_interaction'] < 0.05
print(f"   - Interaction term significant: {interaction_sig}")

# 4. Evidence that biological constraints help explain capacity allocation
print(f"\n4. Evidence for biological constraints:")
print(f"   - Sleep hours alone explains {model1.rsquared*100:.2f}% of variance in capacity allocation")
print(f"   - Full model with interaction explains {model3.rsquared*100:.2f}% of variance")
if r2_improvement > 0.05:
    print(f"   - Substantial improvement when accounting for work-sleep interaction")
else:
    print(f"   - Limited improvement beyond sleep alone")

# 5. Robustness
coef_change = abs(model1.params['sleep_hours'] - model1_reduced.params['sleep_hours'])
print(f"\n5. Robustness after excluding extreme sleepers:")
print(f"   - Sleep coefficient change: {coef_change:.4f}")
print(f"   - Model 1 R-squared change: {abs(model1.rsquared - model1_reduced.rsquared):.4f}")
print(f"   - Results appear {'robust' if coef_change < 0.01 else 'sensitive to sample restrictions'}")

print("\n" + "=" * 60)
print("ANALYSIS COMPLETE")
print("=" * 60)
print("\nAll outputs saved to outputs/tables/")
