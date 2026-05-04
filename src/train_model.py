"""
Daniel's Clinical AI Copilot - Phase 2
Train Machine Learning Model to Predict Readmission Risk
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import joblib
import matplotlib.pyplot as plt

print("=" * 50)
print("DANIEL'S AI COPILOT - PHASE 2")
print("Training Readmission Prediction Model")
print("=" * 50)

# ============================================
# STEP 1: LOAD THE DATA
# ============================================
print("\n STEP 1: Loading patient data...")
df = pd.read_csv('data/patients.csv')
print(f"   Loaded {len(df)} patients")

# ============================================
# STEP 2: SELECT FEATURES FOR TRAINING
# ============================================
print("\n STEP 2: Selecting features...")

feature_columns = ['age', 'has_heart_failure', 'has_diabetes', 
                   'has_kidney_disease', 'has_copd', 
                   'prior_hospitalizations', 'length_of_stay']

target_column = 'readmitted_30_days'

X = df[feature_columns]
y = df[target_column]

print(f"   Features: {feature_columns}")
print(f"   Target: {target_column}")

# ============================================
# STEP 3: SPLIT DATA INTO TRAIN AND TEST
# ============================================
print("\n STEP 3: Splitting data...")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"   Training set: {len(X_train)} patients")
print(f"   Testing set: {len(X_test)} patients")

# ============================================
# STEP 4: TRAIN THE MODEL
# ============================================
print("\n STEP 4: Training Random Forest model...")

model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
model.fit(X_train, y_train)

print("   Model training complete!")

# ============================================
# STEP 5: MAKE PREDICTIONS
# ============================================
print("\n STEP 5: Making predictions...")

y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1]

# ============================================
# STEP 6: EVALUATE MODEL PERFORMANCE
# ============================================
print("\n STEP 6: Evaluating model...")

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_pred_proba)

print("\n" + "=" * 50)
print("MODEL PERFORMANCE METRICS")
print("=" * 50)
print(f"   Accuracy:  {accuracy:.2%}")
print(f"   Precision: {precision:.2%}")
print(f"   Recall:    {recall:.2%}")
print(f"   F1 Score:  {f1:.2%}")
print(f"   AUC Score: {auc:.2%}")
print("=" * 50)

# ============================================
# STEP 7: FEATURE IMPORTANCE (WHAT MATTERS MOST)
# ============================================
print("\n STEP 7: Feature importance...")

importance = model.feature_importances_
feature_importance = pd.DataFrame({
    'feature': feature_columns,
    'importance': importance
}).sort_values('importance', ascending=False)

print("\n   Most important factors for predicting readmission:")
for i, row in feature_importance.iterrows():
    print(f"   {i+1}. {row['feature']}: {row['importance']:.2%}")

# ============================================
# STEP 8: SAVE THE MODEL
# ============================================
print("\n STEP 8: Saving model...")

joblib.dump(model, 'models/risk_model.pkl')
print("   Model saved to: models/risk_model.pkl")

# ============================================
# STEP 9: CREATE FEATURE IMPORTANCE CHART
# ============================================
print("\n STEP 9: Creating feature importance chart...")

plt.figure(figsize=(8, 6))
plt.barh(feature_importance['feature'], feature_importance['importance'], color='steelblue')
plt.xlabel('Importance')
plt.title('What Predicts Readmission Risk?')
plt.gca().invert_yaxis()
plt.savefig('screenshots/Phase02/Phase02_01_feature_importance.png', dpi=150)
print("   Chart saved to: screenshots/Phase02/Phase02_01_feature_importance.png")

# ============================================
# COMPLETE
# ============================================
print("\n" + "=" * 50)
print(" DAY 4 COMPLETE!")
print("=" * 50)
print("\n Files created:")
print("   - models/risk_model.pkl (trained model)")
print("   - screenshots/Phase02/Phase02_01_feature_importance.png")
print("\n Your AI can now predict readmission risk!")
print("\n Model Accuracy: {:.1%}".format(accuracy))
print("=" * 50)