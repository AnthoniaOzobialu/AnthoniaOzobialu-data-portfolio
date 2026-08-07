# USER FUNNEL DROP-OFF ANALYSIS
#Part 1: Data Loading & Cleaning
# Author: Anthonia Ozobialu


# Import Libraries
import pandas as pd
import matplotlib.pyplot as plt

# Load Datasets
home= pd.read_csv(r"data\home_page_table.csv")
search = pd.read_csv(r"data\search_page_table.csv")
payment = pd.read_csv(r"data\payment_page_table.csv")
confirm = pd.read_csv(r"data\payment_confirmation_table.csv")
users  = pd.read_csv(r"data\user_table.csv")

# Convert Date Column
users['date'] = pd.to_datetime(users['date'])

# Store DateFrames in Dictionary
datasets = {
    "Users": users,
    "Home": home,
    "Search": search,
    "Payment": payment,
    "Confirmation": confirm
}

# Explore the Data
print("\nDATASET OVERVIEW")

for name, df in datasets.items():
    print(f"\n {name.upper()}")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")
    print("\nFirst Five Rows")
    print(df.head())
    print("\nData Types")
    print(df.dtypes)
    
# Missing Values
print("\nMissing Values")

for name, df in datasets.items():    
    duplicates = df.duplicated().sum()
    print(f"{name}: {duplicates}")
# No Duplicate Rows Found

# Standardize Column Names
home.columns = home.columns.str.lower().str.strip()
search.columns = search.columns.str.lower().str.strip()
payment.columns = payment.columns.str.lower().str.strip()
confirm.columns = confirm.columns.str.lower().str.strip()
users.columns = users.columns.str.lower().str.strip()

# Fill Missing Values
if "sex" in users.columns:
    users["sex"] = users["sex"].fillna("Unknown")
if "device" in users.columns:
    users["device"] = users["device"].fillna("Unknown")
    
# Dataset Summary

print("Data Summary")
print(f"Total Users: {users['user_id'].nunique():,}")
print(f"Users on Home Page: {home['user_id'].nunique():,}")
print(f"Users on Search Page: {search['user_id'].nunique():,}")
print(f"Users on Payment Page: {payment['user_id'].nunique():,}")
print(f"Users who Completed Payment: {confirm['user_id'].nunique():,}")
print("\nData cleaning completed successfully!")

# Save Cleaned User Table
users.to_csv("clean_users.csv", index=False)
print("\nCleaned user table exported.")


#PART 2: FUNNEL ANALYSIS
print("\nUSER FUNNEL ANALYSIS")
# Count Users at Each Funnel Stage
home_users = home["user_id"].nunique()
search_users = search["user_id"].nunique()
payment_users = payment["user_id"].nunique()
confirm_users = confirm["user_id"].nunique()

print(f"Home Page Users: {home_users:,}")
print(f"Search Page Users: {search_users:,}")
print(f"Payment Page Users: {payment_users:,}")
print(f"Payment Confirmation Users: {confirm_users:,}")

# Create Funnel Summary Table
funnel = pd.DataFrame({
    "Stage": ["Home","Search","Payment","Confirmation"],
    "Users": [home_users, search_users, payment_users, confirm_users]
    })

# Stage-to-Stage Conversion Rate
conversion = [100]

for i in range(1, len(funnel)):
    rate = (
        funnel.loc[i, "Users"] / funnel.loc[i-1, "Users"]
    ) * 100
    conversion.append(round(rate, 2))
funnel["Stage Conversion (%)"] = conversion

# Overall Conversion Rate
overall_conversion = []
for users_at_stage in funnel["Users"]:
    overall_conversion.append(
        round((users_at_stage / home_users) * 100, 2)
    )
    
funnel["Overall Conversion (%)"] = overall_conversion

# Drop-off Rate
drop_off = [0]
for i in range(1, len(funnel)):
    drop = 100 - conversion[i]
    drop_off.append(round(drop, 2))
    
funnel["Drop-off (%)"] = drop_off

print("\nFUNNEL SUMMARY")
print(funnel)

# Biggest Drop-off Stage
largest_drop = funnel.iloc[1:]
worst_stage = largest_drop.loc[largest_drop["Drop-off (%)"].idxmax()]

print("\nLargest Drop-off Stage")
print("-----------------------")
print(
    f"{worst_stage['Stage']} "
    f"({worst_stage['Drop-off (%)']}%)"
)

# Overall Funnel Conversion
overall = (confirm_users / home_users) * 100

print(f"\nOverall Funnel Conversion: {overall:.2f}%")

# Overall Funnel Drop-off
overall_drop = 100 - overall

print(f"Overall Funnel Drop-off: {overall_drop: .2f}%")

# Business Insights
print("Business Insights")
print(f"• {home_users:,} users entered the website.")
print(f"• {confirm_users:,} users completed payment.")
print(f"• Overall conversion rate is "f"{overall_drop:.2f}%.")

print(
    f"• The biggest loss of users occurs at the "
    f"{worst_stage['Stage']} stage "
    f"with a drop-off of "
    f"{worst_stage['Drop-off (%)']:.2f}%."
)
# FUNNEL VISUALIZATION

plt.figure(figsize=(8,5))
plt.plot(funnel["Stage"],funnel["Users"],marker="o",linewidth=3)
for x, y in zip(funnel["Stage"], funnel["Users"]):
    plt.text(x, y,f"{y:,}",ha="center",va="bottom")

plt.title("User Funnel")
plt.xlabel("Funnel Stage")
plt.ylabel("Number of Users")
plt.grid(axis="y")
plt.tight_layout()
plt.savefig("funnel_trend.png", dpi=300)
plt.show()

# BAR CHART
plt.figure(figsize=(8,5))

plt.bar(funnel["Stage"], funnel["Users"])

plt.title("Users at Each Funnel Stage")
plt.xlabel("Stage")
plt.ylabel("Users")
plt.tight_layout()
plt.savefig("funnel_bar_chart.png", dpi=300)
plt.show()
# EXPORT SUMMARY
funnel.to_csv("funnel_summary.csv", index=False)
print("\nFunnel summary exported successfully.")


# Part 3: Segmentation Analysis
home_users = home.merge(users, on="user_id", how='left')
search_users = search.merge(users, on="user_id", how="left")
payment_users = payment.merge(users, on="user_id", how="left")
confirm_users = confirm.merge(users, on="user_id", how="left")

# Device Analysis
print("\nDevice Analysis")
device_summary = pd.DataFrame()
device_summary['Home'] = (home_users.groupby("device")["user_id"].nunique())
device_summary['Search'] = (search_users.groupby("device")["user_id"].nunique())
device_summary["Payment"] = (payment_users.groupby("device")["user_id"].nunique())
device_summary["Confirmation"] = (confirm_users.groupby("device")["user_id"].nunique())

device_summary = device_summary.fillna(0).astype(int)

device_summary["Overall Conversion (%)"] = round(
    device_summary["Confirmation"] / device_summary["Home"] * 100, 2
)

print(device_summary)

# Device Bar Chart

device_summary[["Home", "Confirmation"]].plot(kind="bar", figsize=(8,5))
plt.title("Device Performance")
plt.ylabel("Users")
plt.tight_layout()
plt.savefig("device_analysis.png", dpi = 300)
plt.show()

# Gender Analysis
print("\nGender Analysis")
gender_summary = pd.DataFrame()
gender_summary["Home"] = (home_users.groupby("sex")["user_id"].nunique())
gender_summary["Search"] = (search_users.groupby("sex")["user_id"].nunique())
gender_summary["Payment"] = (payment_users.groupby("sex")["user_id"].nunique())
gender_summary["Confirmation"] = (confirm_users.groupby("sex")["user_id"].nunique())
gender_summary = gender_summary.fillna(0).astype(int)
gender_summary["Overall Conversion (%)"] = round(
    gender_summary["Confirmation"] / gender_summary["Home"] * 100, 2
)
print(gender_summary)

# Gender Chart
gender_summary[["Home", "Confirmation"]].plot(kind="bar", figsize=(8,5))
plt.title("Gender Performace")
plt.ylabel("Users")
plt.tight_layout()
plt.savefig("gender_analysis.png", dpi=300)
plt.show()

# Country Analysis
if "country" in users.columns:
    print("\nCountry Analysis")
    country_home = (home_users.groupby("country")["user_id"].nunique())
    country_confirm = (confirm_users.groupby("country")["user_id"].nunique())
    country_summary = pd.concat([country_home, country_confirm], axis=1)
    country_summary.columns = ["Home", "Confirmation"]
    country_summary = (country_summary.fillna(0).astype(int))
    country_summary["Conversion (%)"] = round(
        country_summary["Confirmation"] / country_summary["Home"] * 100, 2
    )
    print(country_summary.sort_values(
        "Conversion (%)", ascending = False
    ))
    
# Browser Analysis
if "browser" in users.columns:
    print("\nBrowser Analysis")
    browser_home = (home_users.groupby("browser")["user_id"].nunique())
    browser_confirm = (confirm_users.groupby("browser")["user_id"].nunique())
    browser_summary = pd.concat([browser_home, browser_confirm], axis=1)
    browser_summary.columns=["Home", "Confirmation"]
    browser_summary = (browser_summary.fillna(0).astype(int))
    browser_summary["Conversion (%)"] = round(
        browser_summary["Confirmation"] / browser_summary["Home"]*100,2
    )
    print(browser_summary)
    
print("Automatic Insights")
best_device = device_summary["Overall Conversion (%)"].idxmax()
worst_device = device_summary["Overall Conversion (%)"].idxmin()
print(f"Best performing device: " f"{best_device}")
print(f"Lowest performing device: " f"{worst_device}")
best_gender = gender_summary["Overall Conversion (%)"].idxmax()
worst_gender = gender_summary["Overall Conversion (%)"].idxmin()
print(f"Highest converting gender: " f"{best_gender}")
print(f"Lowest converting gender: " f"{worst_gender}")

print("\nBusiness Recommendations")
print("- Improve the onboarding experience for the lowest-performing device.")
print("- Investigate the stage where users abandon the funnel most frequently.")
print("- Optimize the user experience for segments with lower conversion rates. ")
print("- Conduct A/B testing on landing and payment pages.")
print("- Monitor conversion rates regularly after implementing improvements.")

# Export Results
device_summary.to_csv("device_summary.csv")
gender_summary.to_csv("gender_summary.csv")
print("\nSegmentation results exported successfully.")


# ============================================
# PART 4: EXPORTS, DASHBOARD DATA & REPORT
# ============================================

print("\n" + "="*50)
print("POWER BI EXPORT")
print("="*50)

# --------------------------------------------
# Assign Highest Stage Reached
# --------------------------------------------

home["Stage"] = "Home"
search["Stage"] = "Search"
payment["Stage"] = "Payment"
confirm["Stage"] = "Confirmation"

all_stages = pd.concat([
    home[["user_id","Stage"]],
    search[["user_id","Stage"]],
    payment[["user_id","Stage"]],
    confirm[["user_id","Stage"]]
])

stage_order = {
    "Home":1,
    "Search":2,
    "Payment":3,
    "Confirmation":4
}

all_stages["Stage_Order"] = all_stages["Stage"].map(stage_order)

furthest_stage = all_stages.loc[
    all_stages.groupby("user_id")["Stage_Order"].idxmax()
]

powerbi_data = users.merge(
    furthest_stage,
    on="user_id",
    how="left"
)

powerbi_data["Stage"] = powerbi_data["Stage"].fillna("No Visit")
powerbi_data["Stage_Order"] = powerbi_data["Stage_Order"].fillna(0)
powerbi_data.to_csv(
    "powerbi_funnel_dataset.csv",
    index=False
)
print("Power BI dataset exported successfully.")

# Executive KPI Table
executive_summary = pd.DataFrame({
    "Metric":[
        "Total Users",
        "Home Users",
        "Search Users",
        "Payment Users",
        "Completed Payments",
        "Overall Conversion (%)",
        "Overall Drop-off (%)"
    ],
    "Value":[
        users.user_id.nunique(),
        home.user_id.nunique(),
        search.user_id.nunique(),
        payment.user_id.nunique(),
        confirm.user_id.nunique(),
        round(overall,2),
        round(overall_drop,2)
    ]
})
print("\nExecutive Summary")
print(executive_summary)
executive_summary.to_csv("outputs/executive_summary.csv", index=False)
 
# Funnel Conversion Chart
plt.figure(figsize=(9,5))
plt.bar(funnel["Stage"], funnel["Stage Conversion (%)"])
plt.title("Stage Conversion Rate")
plt.ylabel("Conversion (%)")
plt.ylim(0,110)

for x,y in zip(funnel["Stage"], funnel["Stage Conversion (%)"]):
    plt.text(x, y+2, f"{y:.1f}%")

plt.tight_layout()
plt.savefig("outputs/stage_conversion.png", dpi=300)
plt.show()

# Overall Conversion Chart

plt.figure(figsize=(9,5))
plt.bar(funnel["Stage"], funnel["Overall Conversion (%)"])
plt.title("Overall Funnel Conversion")
plt.ylabel("Overall Conversion (%)")
plt.ylim(0,110)

for x,y in zip(funnel["Stage"], funnel["Overall Conversion (%)"]):

    plt.text(x, y+2, f"{y:.1f}%")

plt.tight_layout()
plt.savefig("outputs/overall_conversion.png", dpi=300)
plt.show()

# Export All Analysis
funnel.to_csv("outputs/funnel_table.csv", index=False)

print("\nFunnel table exported.")

# Final Report
print("FINAL PROJECT REPORT")
print(f"""
PROJECT: USER FUNNEL DROP-OFF ANALYSIS

Business Problem
----------------
The objective of this project was to identify where users
leave the sales funnel and determine opportunities to
improve conversion.

Key Findings
------------
• Total Users: {users.user_id.nunique():,}
• Users Reaching Confirmation: {confirm.user_id.nunique():,}
• Overall Conversion: {overall:.2f}%
• Overall Drop-off: {overall_drop:.2f}%
• Largest Drop-off Stage: {worst_stage['Stage']}

Recommendations
---------------
1. Improve the stage with the highest abandonment.
2. Optimize the lowest-performing device.
3. Simplify the payment process.
4. Perform A/B testing on critical pages.
5. Monitor funnel performance regularly.
Project Completed Successfully.
""")
print("All files saved in the outputs folder.")
print("Ready for Power BI dashboard creation.")
