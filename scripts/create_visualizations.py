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


def style_axis(ax):
    """Apply the shared styling to an axis."""
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(COLOR_SECONDARY)
    ax.spines['bottom'].set_color(COLOR_SECONDARY)
    ax.tick_params(colors=COLOR_TEXT, labelsize=10)
    ax.grid(True, color=COLOR_SECONDARY, alpha=0.5, linewidth=0.5)


def r_squared(x, y):
    """R-squared from a simple OLS of y on x."""
    X = sm.add_constant(x)
    return sm.OLS(y, X).fit().rsquared


# Load data
df = pd.read_csv('data/cleaned/capacity_model_dataset.csv')

# ============================================================
# CHART 1: THE COLLAPSE — RAW WORK HOURS vs STRUCTURAL WORK LOAD
# Two panels sharing a sleep x-axis. The whole point of the study
# is the gap between these two R-squared values.
# ============================================================
r2_hours = r_squared(df['sleep_hours'], df['work_hours'])
r2_swl = r_squared(df['sleep_hours'], df['capacity_proxy'])

fig, (ax_left, ax_right) = plt.subplots(
    1, 2, figsize=(14, 6), facecolor=COLOR_BG
)

# --- LEFT PANEL: sleep vs raw work hours ---
ax_left.set_facecolor(COLOR_BG)
ax_left.scatter(df['sleep_hours'], df['work_hours'],
                color=COLOR_PRIMARY, alpha=0.3, s=20, edgecolors='none')
z = np.polyfit(df['sleep_hours'], df['work_hours'], 1)
p = np.poly1d(z)
sleep_sorted = np.sort(df['sleep_hours'])
ax_left.plot(sleep_sorted, p(sleep_sorted),
             color=COLOR_PRIMARY, alpha=0.9, linewidth=2)
style_axis(ax_left)
ax_left.set_xlabel('Sleep Hours', color=COLOR_TEXT, fontsize=11, fontname='Helvetica')
ax_left.set_ylabel('Daily Work Hours', color=COLOR_TEXT, fontsize=11, fontname='Helvetica')
ax_left.set_title('Raw Work Hours', color=COLOR_TEXT, fontsize=13,
                  fontweight='bold', fontname='Playfair Display', pad=10)
ax_left.text(0.95, 0.95, f'R² = {r2_hours:.3f}',
             transform=ax_left.transAxes, ha='right', va='top',
             color=COLOR_TEXT, fontsize=11, fontname='Helvetica', alpha=0.8)

# --- RIGHT PANEL: sleep vs Structural Work Load ---
ax_right.set_facecolor(COLOR_BG)
ax_right.scatter(df['sleep_hours'], df['capacity_proxy'],
                 color=COLOR_PRIMARY, alpha=0.3, s=20, edgecolors='none')
z2 = np.polyfit(df['sleep_hours'], df['capacity_proxy'], 1)
p2 = np.poly1d(z2)
ax_right.plot(sleep_sorted, p2(sleep_sorted),
              color=COLOR_PRIMARY, alpha=0.9, linewidth=2)
style_axis(ax_right)
ax_right.set_xlabel('Sleep Hours', color=COLOR_TEXT, fontsize=11, fontname='Helvetica')
ax_right.set_ylabel('Structural Work Load\n(work + commute) / waking hours',
                    color=COLOR_TEXT, fontsize=11, fontname='Helvetica')
ax_right.set_title('Structural Work Load', color=COLOR_TEXT, fontsize=13,
                   fontweight='bold', fontname='Playfair Display', pad=10)
ax_right.text(0.95, 0.95, f'R² = {r2_swl:.3f}',
              transform=ax_right.transAxes, ha='right', va='top',
              color=COLOR_TEXT, fontsize=11, fontname='Helvetica', alpha=0.8)

# Shared title + subtitle
fig.suptitle("Sleep's Explanatory Power Collapses for Structural Work Load",
             color=COLOR_TEXT, fontsize=17, fontweight='bold',
             fontname='Playfair Display', y=1.02)
fig.text(0.5, 0.965, 'Sleep predicts raw work hours, but almost none of how much '
         'of the waking day is claimed by work and commuting',
         ha='center', color=COLOR_TEXT, fontsize=10, fontname='Helvetica')

plt.tight_layout()
plt.savefig('outputs/figures/sleep_vs_work.png', dpi=300,
            facecolor=COLOR_BG, edgecolor='none', bbox_inches='tight')
plt.close()
print("Saved: outputs/figures/sleep_vs_work.png")

# ============================================================
# CHART 2: STRUCTURAL WORK LOAD DISTRIBUTION
# ============================================================
fig, ax = plt.subplots(figsize=(10, 6), facecolor=COLOR_BG)
ax.set_facecolor(COLOR_BG)

ax.hist(df['capacity_proxy'], bins=50, color=COLOR_PRIMARY,
        alpha=0.8, edgecolor='none')

style_axis(ax)
ax.grid(True, color=COLOR_SECONDARY, alpha=0.5, linewidth=0.5, axis='y')

ax.set_xlabel('Structural Work Load', color=COLOR_TEXT, fontsize=11, fontname='Helvetica')
ax.set_ylabel('Frequency', color=COLOR_TEXT, fontsize=11, fontname='Helvetica')
ax.set_title('Structural Work Load Varies Widely Across Individuals',
             color=COLOR_TEXT, fontsize=16, fontweight='bold',
             fontname='Playfair Display', pad=20)

ax.text(0.5, 1.02, 'Share of waking time claimed by work and commuting',
        transform=ax.transAxes, ha='center', color=COLOR_TEXT,
        fontsize=10, fontname='Helvetica')

plt.tight_layout()
plt.savefig('outputs/figures/capacity_distribution.png', dpi=300,
            facecolor=COLOR_BG, edgecolor='none', bbox_inches='tight')
plt.close()
print("Saved: outputs/figures/capacity_distribution.png")

# ============================================================
# CHART 3: PREDICTED VS ACTUAL (raw work-hours model from sleep)
# ============================================================
X = df['sleep_hours']
X = sm.add_constant(X)
model = sm.OLS(df['work_hours'], X).fit()
df['predicted_work_hours'] = model.predict(X)

fig, ax = plt.subplots(figsize=(10, 6), facecolor=COLOR_BG)
ax.set_facecolor(COLOR_BG)

ax.scatter(df['predicted_work_hours'], df['work_hours'],
           color=COLOR_PRIMARY, alpha=0.3, s=20, edgecolors='none')

max_val = max(df['predicted_work_hours'].max(), df['work_hours'].max())
ax.plot([0, max_val], [0, max_val],
        color=COLOR_SECONDARY, alpha=0.8, linewidth=2, linestyle='--')

style_axis(ax)

ax.set_xlabel('Predicted Work Hours', color=COLOR_TEXT, fontsize=11, fontname='Helvetica')
ax.set_ylabel('Actual Work Hours', color=COLOR_TEXT, fontsize=11, fontname='Helvetica')
ax.set_title('Sleep Explains Only a Small Portion of Daily Work Hours',
             color=COLOR_TEXT, fontsize=16, fontweight='bold',
             fontname='Playfair Display', pad=20)

ax.text(0.5, 1.02, f'Sleep-only model of raw work hours (R² = {model.rsquared:.3f})',
        transform=ax.transAxes, ha='center', color=COLOR_TEXT,
        fontsize=10, fontname='Helvetica')

plt.tight_layout()
plt.savefig('outputs/figures/model_fit.png', dpi=300,
            facecolor=COLOR_BG, edgecolor='none', bbox_inches='tight')
plt.close()
print("Saved: outputs/figures/model_fit.png")

print("\nAll visualizations saved successfully.")
print(f"  Raw work hours ~ sleep:        R² = {r2_hours:.4f}")
print(f"  Structural Work Load ~ sleep:  R² = {r2_swl:.4f}")
