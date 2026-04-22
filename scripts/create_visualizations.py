import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import statsmodels.api as sm
import os

# Ensure output directory exists
os.makedirs('outputs/figures', exist_ok=True)

# Color palette
COLOR_BG = '#FFFFFF'
COLOR_PRIMARY = '#640520'
COLOR_TEXT = '#111111'
COLOR_SECONDARY = '#EAEAEA'

# Load data
df = pd.read_csv('data/cleaned/capacity_model_dataset.csv')

# ============================================================
# CHART 1: SLEEP VS WORK SCATTER
# ============================================================
fig, ax = plt.subplots(figsize=(10, 6), facecolor=COLOR_BG)
ax.set_facecolor(COLOR_BG)

# Scatter with transparency
ax.scatter(df['sleep_hours'], df['work_hours'], 
           color=COLOR_PRIMARY, alpha=0.3, s=20, edgecolors='none')

# Add trend line
z = np.polyfit(df['sleep_hours'], df['work_hours'], 1)
p = np.poly1d(z)
ax.plot(df['sleep_hours'], p(df['sleep_hours']), 
        color=COLOR_PRIMARY, alpha=0.8, linewidth=2)

# Styling
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(COLOR_SECONDARY)
ax.spines['bottom'].set_color(COLOR_SECONDARY)
ax.tick_params(colors=COLOR_TEXT, labelsize=10)
ax.grid(True, color=COLOR_SECONDARY, alpha=0.5, linewidth=0.5)

# Labels and title
ax.set_xlabel('Sleep Hours', color=COLOR_TEXT, fontsize=11, fontname='Helvetica')
ax.set_ylabel('Work Hours', color=COLOR_TEXT, fontsize=11, fontname='Helvetica')
ax.set_title('Sleep Has a Limited Relationship with Work Allocation', 
             color=COLOR_TEXT, fontsize=16, fontweight='bold', 
             fontname='Playfair Display', pad=20)

# Subtitle
ax.text(0.5, 1.02, 'Daily time-use data (ATUS)', 
        transform=ax.transAxes, ha='center', color=COLOR_TEXT, 
        fontsize=10, fontname='Helvetica')

# Annotation
ax.text(0.95, 0.05, 'R² ≈ 0.11', 
        transform=ax.transAxes, ha='right', color=COLOR_TEXT, 
        fontsize=10, fontname='Helvetica', alpha=0.7)

plt.tight_layout()
plt.savefig('outputs/figures/sleep_vs_work.png', dpi=300, 
            facecolor=COLOR_BG, edgecolor='none', bbox_inches='tight')
plt.close()

print("Saved: outputs/figures/sleep_vs_work.png")

# ============================================================
# CHART 2: CAPACITY DISTRIBUTION HISTOGRAM
# ============================================================
fig, ax = plt.subplots(figsize=(10, 6), facecolor=COLOR_BG)
ax.set_facecolor(COLOR_BG)

# Histogram
ax.hist(df['capacity_proxy'], bins=50, color=COLOR_PRIMARY, 
        alpha=0.8, edgecolor='none')

# Styling
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(COLOR_SECONDARY)
ax.spines['bottom'].set_color(COLOR_SECONDARY)
ax.tick_params(colors=COLOR_TEXT, labelsize=10)
ax.grid(True, color=COLOR_SECONDARY, alpha=0.5, linewidth=0.5, axis='y')

# Labels and title
ax.set_xlabel('Capacity Proxy', color=COLOR_TEXT, fontsize=11, fontname='Helvetica')
ax.set_ylabel('Frequency', color=COLOR_TEXT, fontsize=11, fontname='Helvetica')
ax.set_title('Capacity Allocation Varies Widely Across Individuals', 
             color=COLOR_TEXT, fontsize=16, fontweight='bold', 
             fontname='Playfair Display', pad=20)

# Subtitle
ax.text(0.5, 1.02, 'Share of waking time allocated to work', 
        transform=ax.transAxes, ha='center', color=COLOR_TEXT, 
        fontsize=10, fontname='Helvetica')

plt.tight_layout()
plt.savefig('outputs/figures/capacity_distribution.png', dpi=300, 
            facecolor=COLOR_BG, edgecolor='none', bbox_inches='tight')
plt.close()

print("Saved: outputs/figures/capacity_distribution.png")

# ============================================================
# CHART 3: PREDICTED VS ACTUAL (OPTIONAL)
# ============================================================
# Fit simple model to get predictions
X = df['sleep_hours']
X = sm.add_constant(X)
model = sm.OLS(df['work_hours'], X).fit()
df['predicted_work_hours'] = model.predict(X)

fig, ax = plt.subplots(figsize=(10, 6), facecolor=COLOR_BG)
ax.set_facecolor(COLOR_BG)

# Scatter with transparency
ax.scatter(df['predicted_work_hours'], df['work_hours'], 
           color=COLOR_PRIMARY, alpha=0.3, s=20, edgecolors='none')

# Add diagonal reference line
max_val = max(df['predicted_work_hours'].max(), df['work_hours'].max())
ax.plot([0, max_val], [0, max_val], 
        color=COLOR_SECONDARY, alpha=0.8, linewidth=2, linestyle='--')

# Styling
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(COLOR_SECONDARY)
ax.spines['bottom'].set_color(COLOR_SECONDARY)
ax.tick_params(colors=COLOR_TEXT, labelsize=10)
ax.grid(True, color=COLOR_SECONDARY, alpha=0.5, linewidth=0.5)

# Labels and title
ax.set_xlabel('Predicted Work Hours', color=COLOR_TEXT, fontsize=11, fontname='Helvetica')
ax.set_ylabel('Actual Work Hours', color=COLOR_TEXT, fontsize=11, fontname='Helvetica')
ax.set_title('Sleep Explains Only a Small Portion of Work Behavior', 
             color=COLOR_TEXT, fontsize=16, fontweight='bold', 
             fontname='Playfair Display', pad=20)

# Subtitle
ax.text(0.5, 1.02, 'Model fit remains weak despite statistical significance', 
        transform=ax.transAxes, ha='center', color=COLOR_TEXT, 
        fontsize=10, fontname='Helvetica')

plt.tight_layout()
plt.savefig('outputs/figures/model_fit.png', dpi=300, 
            facecolor=COLOR_BG, edgecolor='none', bbox_inches='tight')
plt.close()

print("Saved: outputs/figures/model_fit.png")

print("\nAll visualizations saved successfully.")
