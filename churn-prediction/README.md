# Telco Customer Churn Prediction
📄 [Read the 2-page case study](./Telco_Churn_Case_Study.pdf)

## Business Problem
Customer churn directly impacts recurring revenue for telecom providers. This project identifies which customers are most likely to churn and why, enabling targeted retention strategies before customers leave.

## Data
- Source: https://www.kaggle.com/datasets/blastchar/telco-customer-churn
- ~7,043 customers in the raw dataset (7,032 after cleaning), features covering demographics, services, contract, billing
- Target: Churn (Yes/No)

## Methodology
1. EDA — churn patterns by contract, tenure, payment method, internet service
2. Feature engineering & preprocessing
3. Models: Logistic Regression, Random Forest, XGBoost
4. Evaluation: Recall, F1, AUC-ROC (best: Logistic Regression, AUC-ROC 0.845)
5. SHAP for explainability

## Key Insights
- Month-to-month + fiber optic + electronic check = highest churn risk cluster
- 42.71% churn rate on month-to-month contracts vs 2.85% on two-year contracts
- Churn drops sharply after the 0-12 month tenure window

## Business Impact
- 1.87K customers flagged high-risk
- Estimated $120.8K/month at risk if no action taken
- Recommendation: auto-pay incentives + loyalty discounts for month-to-month segment

## How to Run
1. Clone this repo
2. Navigate to the `churn-prediction` folder
3. Install dependencies: `pip install -r requirements.txt`
4. Run the script: `python src/Tele-customer-churn.py`
5. Open `powerbi/TELCO_CHURN_PROJECT.pbix` in Power BI Desktop to view the dashboard
