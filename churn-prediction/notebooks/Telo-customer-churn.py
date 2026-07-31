import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from xgboost import plot_importance
from sklearn.metrics import roc_curve

#Load the dataset
df = pd.read_csv(r'c:\Users\user\Downloads\WA_Fn-UseC_-Telco-Customer-Churn.csv')

#Explore
print(df.head()) # first 5 rows
print(df.shape)  # how many rows and columns
print(df.dtypes) # data types
print(df.info()) # overview

# Checking missing values
print(df.isnull().sum())
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
print(df.isnull().sum())
pd.set_option('display.max_columns',None)

#Summary statistics
print(df.describe())

# Churn distribution
sns.countplot(x='Churn', data = df)
plt.title("Churn Distribution")
plt.gca().bar_label(plt.gca().containers[0], label_type='edge')
plt.show()

#Percentage
print(df['Churn'].value_counts(normalize=True) * 100)

# Churn by Contract type
sns.countplot(x='Contract', data=df, hue='Churn')
plt.title("Churn by Contract Type")
plt.show()

# Churn by Internet Service
sns.countplot(x='InternetService', data=df, hue='Churn')
plt.title("Churn By Internet Service")
plt.show()

# Churn by tenure
sns.histplot(data=df, x='tenure', hue='Churn', bins=30, multiple='dodge')
plt.title('Tenure vs Churn')
plt.show()

# Momthly Charges vs Churn
sns.boxplot(x='Churn', y ='MonthlyCharges', data= df)
plt.title("Monthly Charges vs Churn")
plt.show()

# Correlation Heatmap
numeric_df = df[['tenure', 'MonthlyCharges', 'TotalCharges']]
sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm')

plt.title('Correlation Heatmap')
plt.show()

# Feature Enineering and Processing
print(df.dtypes)
print(df['Churn'].value_counts())
df.drop('customerID', axis=1, inplace=True) # Delete customerID column
df.dropna(subset=['TotalCharges'], inplace=True) # Delete rows with null values of TotalCharge
df['Churn'] = df['Churn'].map({"Yes": 1, "No": 0}) # Convert Churn from Yes/No to 1/0
print(df['SeniorCitizen'].value_counts())
#Encode binary columns(Yes/No to 1/0)
binary_cols= ['Partner', 'Dependents', 'PhoneService', 'PaperlessBilling']
for col in binary_cols:
    df[col] = df[col].map({"Yes": 1, "No":0})
# Encode columns with more than 2 categories
multi_cols = ['MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV',
              'StreamingMovies', 'Contract', 'PaymentMethod', 'gender']
df = pd.get_dummies(df, columns = multi_cols, drop_first= True)
print(df.shape)
print(df.head())
print(df.dtypes)

# Split into features and target:
X = df.drop('Churn', axis=1)
y = df['Churn']

print(X.shape)
print(y.value_counts())

#Scale the numeric columns
scaler = StandardScaler()
X[['tenure', 'MonthlyCharges', 'TotalCharges']] = scaler.fit_transform(
    X[['tenure', 'MonthlyCharges', 'TotalCharges']]
)
# Split into train and test sets:
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f'Training set: {X_train.shape}')
print(f'Test set: {X_test.shape}')

# Logistic Regression
lr_model = LogisticRegression(max_iter=1000, random_state=42)
lr_model.fit(X_train, y_train)
lr_pred = lr_model.predict(X_test)

print("=== Logistic Regression ===")
print(classification_report(y_test, lr_pred))
print("AUC-ROC:", roc_auc_score(y_test, lr_model.predict_proba(X_test)[:,1]))

# Random Forest
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
rf_pred = rf_model.predict(X_test)

print("=== Random Forest ===")
print(classification_report(y_test, rf_pred))
print("AUC-ROC:", roc_auc_score(y_test, rf_model.predict_proba(X_test)[:,1]))

# XGBoost
xgb_model = XGBClassifier(random_state = 42, eval_metric='logloss')
xgb_model.fit(X_train, y_train)
xgb_pred = xgb_model.predict(X_test)

print("=== XGBoost ===")
print(classification_report(y_test, xgb_pred))
print("AUC-ROC:", roc_auc_score(y_test, xgb_model.predict_proba(X_test)[:,1]))

# Comparing all three with Cross Validation
models = {
    'Logistic Regression': lr_model,
    'Random Forest': rf_model,
    'XGBoost': xgb_model
}

print("=== Cross Validation Scores ===")
for name, model in models.items():
    scores = cross_val_score(model, X, y, cv=5, scoring='roc_auc')
    print(f"{name}: {scores.mean():.3f} (+/- {scores.std():.3f})")
    
# Visualize Confusion Matrix for Best Model
# Use XGBoost confusion matrix
cm = confusion_matrix(y_test, xgb_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['No Churn', 'Churn'],
            yticklabels=['No Churn', 'Churn'])
plt.title("XGBoost Confusion Matrix")
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.show()

plot_importance(xgb_model, max_num_features=15)
plt.title('Top 15 Most Important Features')
plt.tight_layout()
plt.show()

# Feature importance
importance = pd.DataFrame({
    'Feature': X_train.columns,
    'Importance': xgb_model.feature_importances_
})

importance = importance.sort_values(
    'Importance', ascending = False
).head(15)

plt.figure(figsize=(10, 6))
sns.barplot(x=importance['Importance'], y = importance['Feature'] )
plt.title('Top 15 Most Important Features - XGBoost')
plt.tight_layout()
plt.show()

# ROC Curve Plot
fpr, tpr, thresholds = roc_curve(
    y_test, xgb_model.predict_proba(X_test)[:,1]
)

plt.figure(figsize=(8,6))
plt.plot(fpr, tpr, color = 'blue', label = f'XGBoost (AUC = 0.819)')
plt.plot([0,1], [0,1], color='red', linestyle='--', label='Random Guess')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend()
plt.show()

df.to_csv('telco_churn_cleaned.csv', index = False)
