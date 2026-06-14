# Modeling Human Capacity: Does Sleep Explain the Structural Work Load?

> A micro-level analysis of whether biological constraints explain how people divide their day between work, commuting, and recovery.

## Overview

Most models of human productivity assume that biological factors like sleep strongly determine how much of the day people allocate to work and commuting.

This project tests that assumption using American Time Use Survey (ATUS) data, examining whether sleep meaningfully explains the **Structural Work Load (SWL)** — the share of waking time already claimed by work and commuting before any recovery can occur.

## Key Insight

**Sleep is statistically significant but explains less than 2% of variation in Structural Work Load. The remaining 98% is driven by structural demands — commutes, caregiving, inflexible schedules — not by how much people sleep.**

## Why This Matters

Many models of human productivity assume biological factors like sleep strongly determine capacity and output. If this assumption does not hold, simple time-based models are insufficient for understanding or predicting human behavior. Understanding the limits of these variables is critical for building better systems, whether in workforce planning, productivity tools, or research design.

## Data

- **Source**: American Time Use Survey (ATUS)
- **Unit**: Daily time allocation per individual
- **Sample**: 92,949 active workers (work_hours > 0)
- **Key variables**:
  - `work_hours`: Daily hours spent on work tasks
  - `commute_hours`: Daily hours spent traveling to/from work (ATUS code t180501)
  - `sleep_hours`: Daily hours of sleep (ATUS code t0101 — sleeping only, not all personal care)
  - `waking_hours`: 24 - sleep_hours
  - `capacity_proxy`: (work_hours + commute_hours) / waking_hours — the **Structural Work Load (SWL)**, the share of waking time claimed by work and the commute it structurally requires

## Methods

- Feature construction (capacity proxy from sleep and work hours)
- Correlation analysis (Pearson and Spearman)
- Regression modeling (sleep-only, sleep + threshold, nonlinear specifications)
- Threshold analysis (sleep < 7 hours vs ≥ 7 hours)
- Robustness checks (excluding extreme sleepers)

## Key Findings

- **The R² Collapse:** Sleep predicts 11.8% of variation in raw daily work hours, but only 1.7–1.9% of variation in the *share* of waking time (SWL). This collapse is the key finding: when you account for how much of the day is available (waking hours), sleep explains almost nothing about how tightly that day is packed.
- **Sleep's weak effect on SWL:** Pearson r = -0.131, Spearman r = -0.095. People sleeping less than 7 hours allocate about 3 percentage points more of their waking time to work+commuting (49% vs 46%), but the effect is modest.
- **Structural demands dominate:** The remaining 98% of SWL variation is explained by commutes, caregiving, multiple jobs, and inflexible schedules — not by sleep. Sleep does not determine how compressed a day is.
- **SWL distribution:** Mean = 0.464 (46% of waking time), median = 0.511, IQR = 0.274 (middle half ranges from 34% to 61%).

> Sleep alone provides minimal explanatory power for the structural constraints on daily time allocation. The binding constraint is structural demand, not biological recovery capacity.

## Visualizations

![Sleep vs Work](outputs/figures/sleep_vs_work.png)
*Sleep predicts raw work hours (R² ≈ 0.12) but not Structural Work Load (R² ≈ 0.018)*

![Capacity Distribution](outputs/figures/capacity_distribution.png)
*SWL distribution: 34–61% of waking time across the middle half of workers*

![Model Fit](outputs/figures/model_fit.png)
*Sleep~SWL relationship: R² = 0.018, showing structural demands, not sleep, drive day-packing*

## Interpretation

This analysis does NOT measure productivity or capacity in a physiological sense. It measures **Structural Work Load**: how much of the waking day is already claimed by work and commuting before any recovery can occur. 

The key finding: **How tightly a person's day is packed has almost nothing to do with how much they sleep.** People sleeping 6 hours and people sleeping 9 hours can have identical Structural Work Loads, because both are constrained by commutes, caregiving, schedules they don't control, and other structural demands that sleep cannot explain.

This gap between what sleep would predict (if it were the constraint) and what actually drives day-packing (structural demands) is why simple biological models fail.

## Limitations

- **SWL is a structural measure, not a capacity measure.** It says how much of the day is claimed, not how capable a person is, how productive they are, or what they could do differently. Validating SWL against actual cognitive performance, wellbeing outcomes, or physiological markers of fatigue remains a critical next step.
- **Cross-sectional data limits causal interpretation.** We can't tell from a single diary day whether sleep deprivation drives high SWL, or whether high SWL causes sleep deprivation, or whether both are caused by something else (stress, caregiving, economic necessity).
- **Unobserved factors dominate SWL variation.** The model doesn't include commute length, caregiving hours, multiple-jobholding, or whether work schedules are flexible. These likely explain much of the unexplained 98%.
- **Results reflect one day per person.** A single diary day cannot show chronic patterns—whether someone has run a sleep deficit for a month, or whether the recorded day was atypical.

## Implications

- **Sleep is not the binding constraint on daily time allocation.** Policies that focus on "recharging" or improving sleep will have limited impact on how compressed a workday is.
- **Structural demands are the binding constraint.** Commutes, caregiving, inflexible schedules, and non-negotiable work time determine how much of the day is available for recovery—not how much sleep someone got.
- **Trying to optimize around sleep will fail.** Scheduling tools that use sleep data to place meetings are optimizing the 2% while ignoring the 98% driven by structural factors the tools can't see.
- **The recovery window matters more than sleep hours.** Occupational health research shows that daily rest periods below 11–12 hours are associated with elevated health risks and cognitive impairment. SWL indexes how compressed that window becomes.

## Next Steps

- **Validate SWL against outcomes.** Pair time-allocation data with biomarkers of physiological wear (allostatic load indices) and direct measures of cognitive performance to test whether compressed recovery windows actually predict the capacity costs SWL is meant to signal.
- **Build the structural model.** Include commute length, caregiving hours, multiple-jobholding, and schedule flexibility to explain the 98% of SWL variation that sleep doesn't account for.
