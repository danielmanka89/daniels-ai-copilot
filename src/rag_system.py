"""
Daniel's Clinical AI Copilot - Phase 5
RAG System (Retrieval-Augmented Generation)
Combines Knowledge Base + GPT for cited answers
"""

import json
import openai
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class RAGSystem:
    def __init__(self, knowledge_base_path='data/knowledge/clinical_guidelines.json'):
        """Load the knowledge base"""
        with open(knowledge_base_path, 'r') as f:
            self.knowledge_base = json.load(f)
    
    def retrieve_guidelines(self, condition):
        """Retrieve relevant guidelines based on condition"""
        condition_lower = condition.lower()
        
        if 'heart' in condition_lower or 'cardiac' in condition_lower:
            return self.knowledge_base.get('heart_failure', {})
        elif 'copd' in condition_lower or 'lung' in condition_lower:
            return self.knowledge_base.get('copd', {})
        elif 'pneumonia' in condition_lower:
            return self.knowledge_base.get('pneumonia', {})
        else:
            return self.knowledge_base.get('general', {})
    
    def generate_response(self, patient_note):
        """Generate response with citations using retrieved guidelines"""
        
        # Step 1: Detect condition from patient note
        condition = "general"
        if 'heart' in patient_note.lower() or 'cardiac' in patient_note.lower():
            condition = "heart_failure"
        elif 'copd' in patient_note.lower() or 'lung' in patient_note.lower():
            condition = "copd"
        elif 'pneumonia' in patient_note.lower():
            condition = "pneumonia"
        
        # Step 2: Retrieve relevant guidelines
        guidelines = self.retrieve_guidelines(condition)
        
        # Step 3: Build prompt with retrieved context
        prompt = f"""
You are a clinical AI assistant. Use the following medical guidelines to answer.

SOURCE: {guidelines.get('source', 'Medical Guidelines')}
GUIDELINES:
{chr(10).join(guidelines.get('key_points', ['No specific guidelines found']))}

PATIENT NOTE:
{patient_note}

Please provide:
1. Readmission risk assessment
2. Relevant guidelines (cite the source)
3. Key recommendations

Remember to cite the source in your answer.
"""

        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a clinical AI assistant. Always cite your sources."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            result = response.choices[0].message.content
            # Add citation footer
            result += f"\n\n---\n📚 Source: {guidelines.get('source', 'Medical Guidelines')}"
            return result
            
        except Exception as e:
            return f"Error: {str(e)}"


# ============================================
# TEST THE RAG SYSTEM
# ============================================
if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("DANIEL'S CLINICAL AI COPILOT - PHASE 5")
    print("RAG System Test")
    print("=" * 50)
    
    rag = RAGSystem()
    
    # Test Case 1: Heart Failure Patient
    print("\n" + "=" * 50)
    print("TEST CASE 1: Heart Failure Patient")
    print("=" * 50)
    
    patient_note_1 = """
    Patient is 72-year-old male with history of heart failure.
    Presented with shortness of breath and leg swelling.
    Discharged on Lasix 40mg daily.
    """
    
    print(f"Patient Note: {patient_note_1}")
    print("\nRAG Response:")
    response_1 = rag.generate_response(patient_note_1)
    print(response_1)
    
    # Test Case 2: COPD Patient
    print("\n" + "=" * 50)
    print("TEST CASE 2: COPD Patient")
    print("=" * 50)
    
    patient_note_2 = """
    Patient is 65-year-old female with COPD.
    Presented with wheezing and increased sputum production.
    Discharged on albuterol inhaler and prednisone.
    """
    
    print(f"Patient Note: {patient_note_2}")
    print("\nRAG Response:")
    response_2 = rag.generate_response(patient_note_2)
    print(response_2)
    
    print("\n" + "=" * 50)
    print("RAG SYSTEM READY!")
    print("=" * 50)