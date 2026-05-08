"""
Daniel's Clinical AI Copilot - Phase 3
Knowledge Base for Medical Guidelines
"""

import json
import os

class KnowledgeBase:
    def __init__(self, file_path='data/knowledge/clinical_guidelines.json'):
        """Load the clinical guidelines from JSON file"""
        self.file_path = file_path
        self.guidelines = self.load_guidelines()
    
    def load_guidelines(self):
        """Load guidelines from JSON file"""
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                return json.load(f)
        else:
            print(f"Error: File {self.file_path} not found")
            return {}
    
    def search(self, condition):
        """Search for guidelines by condition name"""
        condition_lower = condition.lower()
        
        # Match keywords to guideline topics
        if 'heart' in condition_lower or 'cardiac' in condition_lower:
            return self.guidelines.get('heart_failure', {})
        elif 'copd' in condition_lower or 'lung' in condition_lower or 'breathing' in condition_lower:
            return self.guidelines.get('copd', {})
        elif 'pneumonia' in condition_lower or 'lung infection' in condition_lower:
            return self.guidelines.get('pneumonia', {})
        else:
            return self.guidelines.get('general', {})
    
    def get_all_topics(self):
        """Return list of all available guideline topics"""
        return list(self.guidelines.keys())
    
    def display_guideline(self, condition):
        """Print guideline for a given condition"""
        result = self.search(condition)
        
        print("=" * 50)
        print(f"CLINICAL GUIDELINE: {result.get('title', 'Not Found')}")
        print("=" * 50)
        print(f"Source: {result.get('source', 'Unknown')}")
        print(f"Readmission Risk: {result.get('readmission_risk', 'Unknown')}")
        print("\nKey Points:")
        for point in result.get('key_points', []):
            print(f"  • {point}")
        print("\nRed Flags (Warning Signs):")
        for flag in result.get('red_flags', []):
            print(f"  • {flag}")
        print("=" * 50)
        
        return result


# ============================================
# TEST THE KNOWLEDGE BASE
# ============================================
if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("DANIEL'S CLINICAL AI COPILOT - PHASE 3")
    print("Knowledge Base Test")
    print("=" * 50)
    
    # Create knowledge base instance
    kb = KnowledgeBase()
    
    print(f"\nAvailable topics: {kb.get_all_topics()}")
    
    # Test search for heart failure
    print("\nSearching for: 'heart failure'")
    kb.display_guideline("heart failure")
    
    # Test search for COPD
    print("\nSearching for: 'COPD'")
    kb.display_guideline("COPD")
    
    # Test search for pneumonia
    print("\nSearching for: 'pneumonia'")
    kb.display_guideline("pneumonia")
    
    print("\n" + "=" * 50)
    print("PHASE 3 - KNOWLEDGE BASE READY!")
    print("=" * 50)