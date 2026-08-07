# User Onboarding Funnel Analysis

**Understand. Optimize. Convert.**

An end-to-end analysis of a 90,400-user e-commerce onboarding funnel, built to identify where users drop off between landing on the homepage and completing a purchase, and to recommend data-backed fixes to improve conversion.

---

## 📌 Project Overview

Most products lose the majority of their users somewhere between first visit and final conversion — but *where* exactly, and *why*, is rarely obvious without breaking the journey into stages. This project analyzes a classic 4-stage onboarding funnel (**Home → Search → Payment → Confirmation**) to quantify conversion and drop-off at each step, segment behavior by device and demographic, and surface the single biggest opportunity for improvement.

**Business question:** Where in the user journey are we losing the most people, and what should we fix first?

---

## 🎯 Objectives

- Load and clean raw funnel event data across 5 source tables
- Calculate conversion % and drop-off % at every stage of the funnel
- Segment funnel performance by device and sex to spot behavioral differences
- Identify the single largest bottleneck in the journey
- Build an interactive Power BI dashboard with slicers and drill-downs
- Translate findings into concrete, prioritized recommendations

---

## 🗂️ Dataset

**Source:** [Sales Funnel Data – User Drop-off Analysis (Kaggle)](https://www.kaggle.com/datasets/andrewjayasatyo/sales-funnel-data-user-drop-off-analysis)

| Table | Description |
|---|---|
| `home_page_table.csv` | Users who landed on the homepage |
| `search_page_table.csv` | Users who reached the search page |
| `payment_page_table.csv` | Users who reached the payment page |
| `payment_confirmation_table.csv` | Users who completed a purchase |
| `user_table.csv` | User-level demographics: device and sex |

**Scale:** 90,400 total users tracked across the full journey.

---

## 🧮 Methodology

1. **Data loading & merging** — Combined the five stage tables with the user demographics table on `user_id` to build a single funnel-stage dataset per user.
2. **Funnel metric calculation** — For each stage, computed:
   - `users` reaching that stage
   - `conversion_pct` = users at stage ÷ users at Home
   - `drop_off_pct` = 1 − (users at stage ÷ users at previous stage)
3. **Segmentation** — Broke down conversion and drop-off by **Device** (Desktop/Mobile) and **Sex** to check whether the bottleneck was uniform or concentrated in a specific group.
4. **Bottleneck identification** — Compared drop-off percentages across all stage transitions to find the point of maximum loss.
5. **Dashboard build** — Designed a Power BI report with KPI cards, funnel/bar visuals, a conversion gauge against an 80% target, a detail table, and interactive Date/Device/Sex slicers.

---

## 📊 Key Findings

| Stage | Users | Overall Conversion | Overall Drop-off |
|---|---|---|---|
| Home | 90,400 | 100.00% | — |
| Search | 45,200 | 50.00% | 50.00% |
| Payment | 6,030 | 13.34% (6.67% of total*) | 99.87%* |
| Confirmation | 452 | 7.50% (0.5% of total) | 99.93%* |

*\*"Overall Conversion/Drop-off" columns in the dashboard are measured relative to total Home users; stage-to-stage figures highlight the true jump size.*

**Insights:**
1. **Half of all users never make it past Search** — the Home → Search transition alone accounts for a 50% drop-off.
2. **The single largest drop happens between Payment and Confirmation** (93% drop-off at that step), even though it's the smallest population — meaning nearly everyone who reaches checkout still fails to complete it.
3. **Only 0.5% of the original 90,400 users complete the entire funnel** (452 users), against an 80% conversion target — leaving massive room for improvement.
4. Overall conversion sits at **50.00%**, but that figure is driven almost entirely by the first step; downstream stages are where the real leakage happens.

---

## 💡 Recommendations

1. **Prioritize fixing the Payment → Confirmation step.** With a 93% drop-off, this is the highest-leverage stage — even a modest improvement here would meaningfully lift overall completions. Investigate friction points: payment method limitations, form complexity, unexpected fees, or trust/security signals at checkout.
2. **Simplify the payment process.** Reduce the number of fields/steps required, add guest checkout, and support more payment methods to reduce abandonment at this stage.
3. **Investigate the Home → Search drop-off.** Losing half of all visitors before they even search suggests onboarding friction or unclear value proposition on the landing page — worth A/B testing homepage CTAs and layout.
4. **Segment-specific interventions.** Use the device/sex breakdown to check whether one segment (e.g., mobile users) disproportionately drops off, and tailor UX fixes accordingly.
5. **Set stage-specific targets**, not just an overall conversion target — tracking Search-rate and Payment-completion-rate separately will make it easier to detect which fix is working.

---

## 🛠️ Tools & Techniques

- **Python (pandas)** — data loading, merging, funnel metric calculation
- **Power BI** — interactive dashboard with KPI cards, funnel/bar charts, gauge visual, and Date/Device/Sex slicers
- **SQL** — stage-wise aggregation and conversion logic

---

## 📁 Repository Structure

```
user-onboarding-funnel-analysis/
│
├── data/
│   ├── home_page_table.csv
│   ├── search_page_table.csv
│   ├── payment_page_table.csv
│   ├── payment_confirmation_table.csv
│   └── user_table.csv
│
├── notebooks/
│   └── funnel_analysis.ipynb
│
├── dashboard/
│   └── user_onboarding_funnel.pbix
│
├── images/
│   └── dashboard_screenshot.png
│
└── README.md
```

---

## 📷 Dashboard Preview

The final Power BI dashboard includes:
- KPI cards for Total Users, Completed Users, Overall Conversion, and Overall Drop-off
- A stage-by-stage funnel bar chart (Total users by stage)
- Conversion % and drop-off % bar charts by stage
- A conversion gauge benchmarked against an 80% target
- A detailed stage-level summary table
- Slicers for Date, Device, and Sex for interactive exploration

---

## 🔗 Connect

**Anthonia Ozobialu** — Data Analyst & Data Analytics Instructor
Portfolio: [github.com/AnthoniaOzobialu](https://github.com/AnthoniaOzobialu)
