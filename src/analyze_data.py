import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('data/patients.csv')
print("=" * 50)
print("DATA LOADED SUCCESSFULLY")
print("=" * 50)
print(f"Total patients: {len(df)}")
print("\nFirst 5 rows:")
print(df.head())

print("\n" + "=" * 50)
print("BASIC STATISTICS")
print("=" * 50)

print(f"\nAge Statistics:")
print(f"  Mean age: {df['age'].mean():.1f} years")
print(f"  Min age: {df['age'].min()} years")
print(f"  Max age: {df['age'].max()} years")

print(f"\nReadmission Rate: {df['readmitted_30_days'].mean():.1%}")

plt.figure(figsize=(10, 6))
plt.hist(df['age'], bins=20, edgecolor='black', color='skyblue')
plt.xlabel('Age (years)')
plt.ylabel('Number of Patients')
plt.title('Age Distribution of 500 Patients')
plt.savefig('screenshots/Phase01/Phase01_04_age_distribution.png', dpi=150)
plt.show()
print("Age chart saved!")

bins = [0, 30, 50, 65, 80, 100]
labels = ['<30', '30-50', '50-65', '65-80', '80+']
df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels)

readmission_by_age = df.groupby('age_group')['readmitted_30_days'].mean() * 100

plt.figure(figsize=(8, 6))
readmission_by_age.plot(kind='bar', color='coral', edgecolor='black')
plt.xlabel('Age Group')
plt.ylabel('Readmission Rate (%)')
plt.title('Readmission Rate by Age Group')
plt.savefig('screenshots/Phase01/Phase01_05_readmission_by_age.png', dpi=150)
plt.show()
print("Age group chart saved!")

conditions = ['has_heart_failure', 'has_diabetes', 'has_kidney_disease', 'has_copd']
condition_names = ['Heart Failure', 'Diabetes', 'Kidney Disease', 'COPD']
values = []

for condition in conditions:
    with_condition = df[df[condition] == 1]['readmitted_30_days'].mean() * 100
    without_condition = df[df[condition] == 0]['readmitted_30_days'].mean() * 100
    values.append(with_condition - without_condition)

plt.figure(figsize=(10, 6))
bars = plt.bar(condition_names, values, color='red', edgecolor='black')
plt.xlabel('Medical Condition')
plt.ylabel('Increase in Readmission Rate (%)')
plt.title('Impact of Each Condition on Readmission Risk')
plt.axhline(y=0, color='black', linestyle='-')
plt.savefig('screenshots/Phase01/Phase01_06_risk_factors.png', dpi=150)
plt.show()
print("Risk factor chart saved!")

print("\n" + "=" * 50)
print("DAY 3 ANALYSIS COMPLETE!")
print("=" * 50)
