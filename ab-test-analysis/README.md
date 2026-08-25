# Marketing A/B Test Analysis: Ad vs PSA Conversion Impact

## Overview
Analysis of a marketing A/B test comparing a paid ad campaign against a public
service announcement (PSA / control group), measuring impact on user conversion
rate. Dataset: ~588,000 users (Marketing A/B Testing, Kaggle).

## Business Question
Does showing users an ad (vs a PSA) significantly increase conversion rate,
and is the effect consistent across days and hours?

## Method
- **Tools:** Python (pandas, scipy, seaborn, matplotlib), Power BI
- **Statistical tests:** Chi-square test of independence (conversion by group),
  Welch's t-test (confound check on ad exposure volume)
- **Effect size:** Absolute and relative lift, 95% CI for difference in proportions
- **Segmentation:** Conversion lift by day of week and hour of day
- **Multiple comparisons:** Bonferroni correction applied to day-level (n=7)
  and hour-level (n=24) significance tests, since running many tests inflates
  the false-positive rate (a naive 5% threshold across 7 tests carries ~30%
  risk of at least one false positive)

## Key Results
| Metric | Value |
|---|---|
| Ad conversion rate | 2.55% |
| PSA conversion rate | 1.79% |
| Absolute lift | 0.77 percentage points |
| Relative lift | 43.09% |
| 95% CI (absolute lift) | 0.60% – 0.94% |
| Overall significance | p < 0.00001 (chi-square) |

**Confound check:** No significant difference in total ads seen between
groups (p = 0.827), ruling out ad-volume as an explanation for the lift.

**Segment-level findings:** After Bonferroni correction (α = 0.00714 for
7 day-level tests), only **Monday–Wednesday** show individually significant
lift. Thursday–Sunday show positive lift in the raw data, but the difference
is not statistically distinguishable from random variation at this sample
size — reporting them as "significant" without correction would overstate
the finding.

## Repository Structure
- `ab-testing.py` — full analysis script
- `ab_test_summary.csv`, `ab_test_by_day.csv`, `ab_test_by_hour.csv` — outputs for Power BI
- `marketing_AB.csv` — original file for code
- `dashboard.pbix` — Power BI file
- `README.md` — this file

## Recommendation
Use the ad campaign — it produces a statistically significant, practically
meaningful lift in conversion overall. Day-level targeting claims should be
limited to Monday–Wednesday, where the effect is robust to multiple-testing
correction.
