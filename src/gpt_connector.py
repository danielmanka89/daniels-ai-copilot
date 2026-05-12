"""
Daniel's Clinical AI Copilot - Phase 4
GPT Connector for Clinical Summaries and ICD-10 Coding
"""

import openai
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class GPTConnector:
    def __init__(self):
        """Initialize the GPT connector"""
        self.model = "gpt-3.5-turbo"
    
    def summarize_clinical_note(self, clinical_note):
        """Generate a concise summary of a clinical note"""
        
        prompt = f"""
        You are a clinical AI assistant. Summarize the following patient discharge note in 3-4 sentences.
        Focus on: primary diagnosis, key risk factors, and discharge plan.
        
        Clinical Note:
        {clinical_note}
        
        Summary:
        """
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful clinical AI assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=200
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"
    
    def suggest_icd10_codes(self, clinical_note):
        """Suggest ICD-10 diagnosis codes based on clinical note"""
        
        prompt = f"""
        You are a clinical coding assistant. Based on the following discharge note,
        suggest 2-3 most appropriate ICD-10 diagnosis codes.
        Format each code as: Code - Description
        
        Clinical Note:
        {clinical_note}
        
        Suggested ICD-10 Codes:
        """
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a medical coding specialist."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=150
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"
    
    def flag_critical_symptoms(self, clinical_note):
        """Identify critical symptoms that need immediate attention"""
        
        prompt = f"""
        You are a clinical safety assistant. Review the following discharge note and
        flag any critical symptoms or red flags that require immediate medical attention.
        List them as bullet points. If none found, say "No critical symptoms identified."
        
        Clinical Note:
        {clinical_note}
        
        Critical Symptoms:
        """
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a clinical safety expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=150
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"


# ============================================
# TEST THE GPT CONNECTOR
# ============================================
if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("DANIEL'S CLINICAL AI COPILOT - PHASE 4")
    print("GPT Connector Test")
    print("=" * 50)
    
    if not openai.api_key:
        print("\n ERROR: OPENAI_API_KEY not found in .env file")
        print("Please add your API key to the .env file")
        exit(1)
    
    print("\n API key found!")
    
    gpt = GPTConnector()
    
    # Test clinical note
    test_note = """
    Patient is a 72-year-old male with history of heart failure.
    Presented with shortness of breath and leg swelling.
    Discharged on Lasix 40mg daily. Follow up in 1 week.
    """
    
    print("\n Test Clinical Note:")
    print(test_note)
    
    print("\n" + "=" * 50)
    print("1. CLINICAL SUMMARY")
    print("=" * 50)
    summary = gpt.summarize_clinical_note(test_note)
    print(summary)
    
    print("\n" + "=" * 50)
    print("2. ICD-10 CODE SUGGESTIONS")
    print("=" * 50)
    codes = gpt.suggest_icd10_codes(test_note)
    print(codes)
    
    print("\n" + "=" * 50)
    print("3. CRITICAL SYMPTOMS")
    print("=" * 50)
    symptoms = gpt.flag_critical_symptoms(test_note)
    print(symptoms)
    
    print("\n" + "=" * 50)
    print(" GPT CONNECTOR READY!")
    print("=" * 50)

