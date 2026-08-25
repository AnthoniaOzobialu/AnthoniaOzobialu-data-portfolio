import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 
from scipy.stats import chi2_contingency
from scipy.stats import ttest_ind
from scipy.stats import norm

#Load data
df = pd.read_csv("marketing_AB.csv")
print(df.head()) # Print first five rows
print(df.dtypes) # Print the datatype of each column
print(df.describe()) # Print the numeric summary 
print(df.info()) # Print datatype and checks for null
print(df.isna().sum()) # Check for columns containing null values
print(df.duplicated().sum())

# Remove any stray whitespace from headers
df.columns = df.columns.str.strip()

# Remove leftover index column
df = df.drop(columns=['Unnamed: 0'])
print(df.head())
group_counts = df['test group'].value_counts()
conversion_by_group = df.groupby('test group')['converted'].mean() * 100
print(group_counts)
print(conversion_by_group)

# Visualize Bar chart of conversion rate comparison.
plt.figure(figsize=(6, 4))
sns.barplot(x=conversion_by_group.index, y=conversion_by_group.values)
plt.title('Conversion Rate: Ad vs PSA')
plt.ylabel('Conversion Rate (%)')
plt.xlabel('Test Group')
plt.show()

# Visualize total ads seen, distribution by group.
plt.figure(figsize=(6,4))
# showfliers=False hides extreme outliers so the box isn't squashed...
# total ads seen is usually heavily right_skewed(e.g. A user saw 2000+ ads)
sns.boxplot(x='test group', y='total ads', data=df, showfliers=False)
plt.title('Total Ads Seen by Group (outliers hidden)')
plt.show()

# Visualize conversion by day of week (bonus context for segmentation later)
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
plt.figure(figsize=(8,4))
sns.barplot(x='most ads day', y ='converted', hue='test group', data=df, order=day_order, estimator=np.mean, errorbar=None)
plt.title('Conversion Rate by Day and Group')
plt.ylabel('Conversion Rate')
plt.xticks(rotation=45)
plt.show()

# Build the contingency table using Chi-square test
contingency = pd.crosstab(df['test group'], df['converted'])
print(contingency)

chi2, p_value_overall, dof, expected = chi2_contingency(contingency)
print(f"Chi-square statistic: {chi2:.4f}")
print(f"P-value_overall: {p_value_overall:.10f}")
print(f"Degrees of freedom: {dof}")

# To interpret it
alpha = 0.05
if p_value_overall < alpha:
    print("Reject HO: conversion rate differs significantly between ad and psa groups.")
else:
    print("Fail to reject HO: no significant difference detected.")

ad_group = df[df['test group'] == 'ad']['total ads']
psa_group = df[df['test group'] == 'psa']['total ads']

t_stat, p_val_ttest = ttest_ind(ad_group, psa_group, equal_var=False)
print(f"T-statistic: {t_stat:.4f}")
print(f"p-value: {p_val_ttest:.10f}")

ad_conv = df[df['test group'] == 'ad']['converted'].mean()
psa_conv = df[df['test group'] == 'psa']['converted'].mean()
n_ad = df[df['test group'] == 'ad'].shape[0]
n_psa =df[df['test group'] == 'psa'].shape[0]

print(f"Ad conversion rate: {ad_conv:.4%}")
print(f"PSA conversion rate: {psa_conv:.4%}")
print(f"Ad group size: {n_ad}, PSA group size: {n_psa}")
print(df.shape)

# To calculate lift(practical size of the effect)
absolute_lift = ad_conv - psa_conv
if psa_conv != 0:
    relative_lift = ((ad_conv - psa_conv) / psa_conv) * 100
else:
    relative_lift = np.nan
print(f"Absolute lift: {absolute_lift:.4%}")
print(f"Relative lift: {relative_lift:.2f}%")

# Confidence interval for difference in proportions to 
# Estimate the likely range of the true advertising effect
p1, p2 = ad_conv, psa_conv
se = np.sqrt((p1*(1-p1))/n_ad + (p2*(1-p2))/n_psa)
z=norm.ppf(0.975) # 95% CI, two-tailed
margin = z*se
ci_lower = absolute_lift - margin
ci_upper = absolute_lift + margin
print(f"95% CI for absolute lift: ({ci_lower:.4%}, {ci_upper:.4%})")
print(f"Statistically significant (p<0.05): {p_value_overall < 0.05}")
print(f"Absolute lift: {absolute_lift:.4%} (practically meaningful? - you decide based on business context)")

# Segmentation Analysis
# Conversion rate and lift by day of week

day_pivot = df.groupby(['most ads day', 'test group'])['converted'].mean().unstack() * 100
day_pivot = day_pivot.reindex(day_order)
day_pivot['lift_pp']=day_pivot['ad']-day_pivot['psa']
day_pivot['relative_lift_%'] = (day_pivot['ad'] - day_pivot['psa'])/day_pivot['psa'] *100
print(day_pivot)

# Convert rate and lift by hour
hour_pivot = df.groupby(['most ads hour', 'test group'])['converted'].mean().unstack() *100
hour_pivot['lift_pp'] = hour_pivot['ad'] - hour_pivot['psa']
hour_pivot['relative_lift_%'] = (hour_pivot['ad'] - hour_pivot['psa']) / hour_pivot['psa'] *100
print(hour_pivot.sort_values('lift_pp', ascending=False).head(5))
print(hour_pivot.sort_values('lift_pp', ascending=True).head(5))

# Visualize lift by day
plt.figure(figsize=(8,4))
sns.barplot(x=day_pivot.index, y=day_pivot['lift_pp'])
plt.title('Absolute Lift (percentage points) by Day')
plt.ylabel('Lift (pp)')
plt.xticks(rotation = 45)
plt.show()

# Visualize lift by hour
plt.figure(figsize=(10,4))
sns.lineplot(x=hour_pivot.index,y=hour_pivot['lift_pp'], marker='o')
plt.title('Absolute Lift (percentage points) by Hour of Day')
plt.xlabel('Hour')
plt.ylabel('Lift (pp)')
plt.xticks(range(0,24))
plt.show()

# statistical significance per segment
alpha_corrected = 0.05 / len(day_order)
print(f"Bonferroni-corrected alpha: {alpha_corrected:.5f}")

for day in day_order:
    day_subset = df[df['most ads day'] == day]
    contingency_table = pd.crosstab(day_subset['test group'], day_subset['converted'])
    chi2, p, dof, expected_counts = chi2_contingency(contingency_table)
    verdict = "SIGNIFICANT" if p < alpha_corrected else "not significant"
    print(f"{day}: p-value = {p:.5f} {verdict} (corrected threshold: {alpha_corrected:.5f})")
    
    
print("\nBUSINESS SUMMARY")
print(f"Ad conversion: {ad_conv:.2%}")
print(f"PSA conversion: {psa_conv:.2%}")
print(f"Lift: {absolute_lift:.2%}")
print(f"P-value_overall: {p_value_overall:.5f}")

if p_value_overall < 0.05:
    print("Recommendation: Use advertisements because they significantly improve conversion.")
else:
    print("Recommendation: No evidence that ads improve conversion.")
    
    
# Overal summary table for Power BI
summary = pd.DataFrame({
    'group': ['ad', 'psa'],
    'conversion_rate': [ad_conv, psa_conv],
    'sample_size': [n_ad, n_psa]
})
summary.to_csv('ab_test_summary.csv', index=False)

# Day-level segmentation table
day_pivot.to_csv('ab_test_by_day.csv')

# Hour-level segmentation table
hour_pivot.to_csv('ab_test_by_hour.csv')

# Raw cleaned dataset (optional, if you want Power BI to compute independently)
df.to_csv('marketing_AB_cleaned.csv', index=False)