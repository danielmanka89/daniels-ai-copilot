"""
Daniel's Clinical AI Copilot - Patient Data Generator
Phase 1: Creates synthetic patient data for training the AI model

This script generates realistic patient records including:
- Demographics (age, gender)
- Medical conditions (heart failure, diabetes, kidney disease)
- Hospital history (prior admissions, length of stay)
- Clinical notes (doctor's notes)
- Readmission outcomes (whether patient returned within 30 days)
"""

import pandas as pd
import random
from datetime import datetime, timedelta

def create_one_patient(patient_number):
    """
    Creates ONE patient record with all clinical information.
    
    Parameters:
    patient_number (int): Unique identifier for the patient
    
    Returns:
    dict: Complete patient record with demographics, conditions, and outcomes
    """
    
    # ============================================
    # DEMOGRAPHICS
    # ============================================
    age = random.randint(18, 95)  # Age between 18 and 95 years
    
    # ============================================
    # MEDICAL CONDITIONS (Risk Factors)
    # 1 = has the condition, 0 = does not have it
    # ============================================
    has_heart_failure = random.choice([0, 1])      # #1 readmission risk factor
    has_diabetes = random.choice([0, 1])           # Common comorbidity
    has_kidney_disease = random.choice([0, 1])     # Increases readmission risk
    has_copd = random.choice([0, 1])               # Lung disease
    
    # ============================================
    # HOSPITAL HISTORY
    # ============================================
    prior_hospitalizations = random.randint(0, 4)  # How many times in last year
    length_of_stay = random.randint(1, 20)         # Days in hospital this time
    
    # ============================================
    # CALCULATE READMISSION RISK SCORE (0-100)
    # Based on medical literature risk factors
    # ============================================
    risk_score = 0
    
    # Age risk (older patients have higher risk)
    if age > 65:
        risk_score += 20
    if age > 80:
        risk_score += 15
        
    # Medical condition risks
    if has_heart_failure:
        risk_score += 25      # Heart failure is HIGHEST risk factor
    if has_diabetes:
        risk_score += 10
    if has_kidney_disease:
        risk_score += 15
    if has_copd:
        risk_score += 10
        
    # Hospital history risks
    if prior_hospitalizations >= 2:
        risk_score += 20
    elif prior_hospitalizations == 1:
        risk_score += 10
        
    # Length of stay risks (longer stays = sicker patients)
    if length_of_stay > 7:
        risk_score += 15
    elif length_of_stay > 4:
        risk_score += 5
    
    # Cap risk score at 95 (never 100% certain)
    risk_score = min(risk_score, 95)
    
    # ============================================
    # DETERMINE IF PATIENT GETS READMITTED
    # Higher risk score = higher chance of readmission
    # ============================================
    if risk_score > 50:
        # High risk patients: 70% chance of readmission
        will_be_readmitted = random.random() < 0.70
    else:
        # Low risk patients: 20% chance of readmission
        will_be_readmitted = random.random() < 0.20
    
    # ============================================
    # GENERATE REALISTIC CLINICAL NOTE
    # This simulates what a doctor would write
    # ============================================
    
    # Select gender randomly for the note
    gender = 'male' if random.random() > 0.5 else 'female'
    
    # Build symptoms based on conditions
    symptoms = []
    if has_heart_failure:
        symptoms.extend(["shortness of breath", "leg swelling", "fatigue"])
    if has_copd:
        symptoms.extend(["cough", "wheezing", "sputum production"])
    if has_diabetes:
        symptoms.extend(["increased thirst", "frequent urination"])
    
    if not symptoms:
        symptoms = ["stable", "no acute distress"]
    
    clinical_note = f"""
HOSPITAL DISCHARGE SUMMARY
Patient ID: PT-{patient_number:05d}
Age: {age} years
Gender: {gender}
Admission Date: {(datetime.now() - timedelta(days=length_of_stay)).strftime('%Y-%m-%d')}
Discharge Date: {datetime.now().strftime('%Y-%m-%d')}

PRINCIPAL DIAGNOSES:
{'- Heart failure' if has_heart_failure else '- No heart failure'}
{'- Diabetes mellitus type 2' if has_diabetes else '- No diabetes'}
{'- Chronic kidney disease' if has_kidney_disease else '- Normal renal function'}
{'- COPD' if has_copd else '- No lung disease'}

HOSPITAL COURSE:
The patient presented with {symptoms[0]}. 
During the {length_of_stay}-day admission, the patient {'required ICU care' if length_of_stay > 10 else 'was managed on general medicine floor'}.
Vital signs stabilized with treatment.

MEDICATIONS AT DISCHARGE:
{'- Lisinopril 10mg daily' if has_heart_failure else '- No cardiac medications'}
{'- Metformin 500mg twice daily' if has_diabetes else '- No diabetes medications'}
{'- Albuterol inhaler as needed' if has_copd else '- No respiratory medications'}

DISCHARGE PLAN:
- Follow up with primary care within 7 days
{'- Cardiology follow-up scheduled' if has_heart_failure else ''}
{'- Diabetes education provided' if has_diabetes else ''}
- Patient {'lives alone' if random.random() > 0.5 else 'has family support'}

DISCHARGE DISPOSITION:
Discharged to home.
"""
    
    # ============================================
    # RETURN COMPLETE PATIENT RECORD
    # ============================================
    return {
        'patient_id': f'PT-{patient_number:05d}',
        'age': age,
        'gender': gender,
        'has_heart_failure': has_heart_failure,
        'has_diabetes': has_diabetes,
        'has_kidney_disease': has_kidney_disease,
        'has_copd': has_copd,
        'prior_hospitalizations': prior_hospitalizations,
        'length_of_stay': length_of_stay,
        'risk_score_calculated': risk_score,
        'readmitted_30_days': will_be_readmitted,
        'clinical_note': clinical_note
    }


def generate_patient_dataset(number_of_patients=500):
    """
    Generate multiple patient records by calling create_one_patient repeatedly.
    
    Parameters:
    number_of_patients (int): How many patients to generate (default: 500)
    
    Returns:
    DataFrame: Pandas DataFrame containing all patient records
    """
    
    print("=" * 60)
    print("DANIEL'S CLINICAL AI COPILOT - PHASE 1")
    print("Patient Data Generator")
    print("=" * 60)
    print(f"\nGenerating {number_of_patients} synthetic patients...")
    print("This will take a few seconds...\n")
    
    all_patients = []
    
    # Create patients one by one
    for i in range(number_of_patients):
        patient = create_one_patient(i)
        all_patients.append(patient)
        
        # Show progress every 100 patients
        if (i + 1) % 100 == 0:
            print(f"   ✓ Created {i + 1} patients...")
    
    # Convert list of dictionaries to pandas DataFrame
    df = pd.DataFrame(all_patients)
    
    return df


def show_statistics(df):
    """
    Display summary statistics about the generated dataset.
    
    Parameters:
    df (DataFrame): The patient dataset
    """
    
    print("\n" + "=" * 60)
    print("DATASET STATISTICS")
    print("=" * 60)
    
    print(f"\nTotal patients: {len(df)}")
    print(f"Average age: {df['age'].mean():.1f} years")
    print(f"Gender distribution: {df['gender'].value_counts().to_dict()}")
    print(f"\nMedical conditions prevalence:")
    print(f"   - Heart failure: {df['has_heart_failure'].mean():.1%}")
    print(f"   - Diabetes: {df['has_diabetes'].mean():.1%}")
    print(f"   - Kidney disease: {df['has_kidney_disease'].mean():.1%}")
    print(f"   - COPD: {df['has_copd'].mean():.1%}")
    
    print(f"\nHospital statistics:")
    print(f"   - Average length of stay: {df['length_of_stay'].mean():.1f} days")
    print(f"   - Average prior hospitalizations: {df['prior_hospitalizations'].mean():.1f}")
    
    print(f"\nREADMISSION RATE: {df['readmitted_30_days'].mean():.1%}")
    print(f"Average risk score: {df['risk_score_calculated'].mean():.1f}")


# ============================================
# MAIN EXECUTION - This runs when you run the script
# ============================================

if __name__ == "__main__":
    # Generate 500 patients
    patients_df = generate_patient_dataset(500)
    
    # Save to CSV file
    patients_df.to_csv('data/patients.csv', index=False)
    print(f"\nData saved to: data/patients.csv")
    
    # Show statistics
    show_statistics(patients_df)
    
    # Show sample of first 5 patients
    print("\n" + "=" * 60)
    print("SAMPLE DATA - FIRST 5 PATIENTS")
    print("=" * 60)
    print(patients_df[['patient_id', 'age', 'has_heart_failure', 'length_of_stay', 'readmitted_30_days']].head())
    
    print("\n" + "=" * 60)
    print("PHASE 1 COMPLETE!")
    print("=" * 60)
    print("\nFiles created:")
    print("   - data/patients.csv (500 patient records)")
    print("\nNext: Phase 2 - Build Risk Prediction Model")
    print("=" * 60)