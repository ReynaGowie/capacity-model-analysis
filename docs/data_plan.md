# Data Plan: Human Capacity Modeling

## Objective
Compare whether work hours alone explain capacity allocation, or whether sleep and behavioral factors improve explanatory power.

## Variables

### Predictors
- **work_hours**: Daily hours spent on work tasks
- **sleep_hours**: Daily hours of sleep
- **work_variability**: Standard deviation of work hours (optional)
- **sleep_variability**: Standard deviation of sleep hours (optional)

### Outcome
- **capacity_proxy**: ratio of work hours to available waking hours

Definition:
```
capacity_proxy = work_hours / (24 - sleep_hours)
```

Explanation:
- Represents how much available capacity is allocated to work
- Incorporates both time and biological constraint (sleep)
- Serves as a proxy for effective capacity utilization

Alternative formulations:
- `work_hours / sleep_hours`
- Threshold-based versions (e.g., sleep < 7 hours)

## Models to Test

1. `capacity_proxy ~ sleep_hours`
2. `capacity_proxy ~ sleep_hours + interaction with work_hours`
3. `capacity_proxy ~ sleep_hours + work_variability + sleep_variability`
4. `capacity_proxy ~ sleep_hours + nonlinear terms`
5. Optional: residual analysis from baseline model

### Baseline Comparison

A baseline model using work_hours alone is not included directly due to mechanical dependence with the outcome.

Instead, analysis focuses on whether sleep and behavioral factors explain variation in capacity allocation beyond time constraints.

## Interpretation

This analysis does NOT measure true productivity. It models **capacity allocation under constraints**. The goal is to test whether biological and behavioral constraints (such as sleep) explain variation in capacity allocation beyond time-based measures.

## Data Source

- American Time Use Survey (ATUS)
- Cross-sectional daily time allocation data

## Limitations

- capacity_proxy is a constructed measure, not direct productivity
- Cross-sectional data limits causal interpretation
- Results reflect population-level patterns, not individual behavior over time
- capacity_proxy includes work_hours in its construction, which may introduce mechanical relationships if not modeled carefully
