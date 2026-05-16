"""
Daniel's Clinical AI Copilot - Phase 6
Streamlit Web Interface
"""

import streamlit as st
import pandas as pd
import joblib
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from rag_system import RAGSystem
from gpt_connector import GPTConnector

# Page configuration
st.set_page_config(
    page_title="Daniel's Clinical AI Copilot",
    page_icon="🏥",
    layout="wide"
)

# Title
st.title("🏥 Daniel's Clinical AI Copilot")
st.markdown("### Real-Time Patient Risk Intelligence System")

# Sidebar
with st.sidebar:
    st.header("About")
    st.markdown("""
    This AI system helps predict patient readmission risk within 30 days.
    
    **Features:**
    - Readmission risk prediction
    - Clinical note summarization
    - ICD-10 code suggestions
    - Medical guidelines retrieval with citations
    """)
    
    st.markdown("---")
    st.markdown("**Built by Daniel** | Phase 6")

# Main input area
st.subheader("Patient Clinical Note")
st.markdown("Paste the patient's discharge summary or clinical note below:")

# Text input
clinical_note = st.text_area(
    "Clinical Note",
    height=200,
    placeholder="Example: Patient is a 72-year-old male with history of heart failure. Presented with shortness of breath and leg swelling..."
)

# Load models
@st.cache_resource
def load_models():
    try:
        risk_model = joblib.load('models/risk_model.pkl')
        rag = RAGSystem()
        gpt = GPTConnector()
        return risk_model, rag, gpt
    except Exception as e:
        st.error(f"Error loading models: {str(e)}")
        return None, None, None
    
# Load models
risk_model, rag, gpt = load_models()

# Analysis button
if st.button("Analyze Patient Risk", type="primary"):
    if not clinical_note:
        st.warning("Please enter a clinical note.")
    else:
        with st.spinner("Analyzing patient data..."):
            # Create columns for results
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Readmission Risk")
                # Risk prediction (simplified for now)
                st.metric("Risk Score", "Calculating...")
                st.info("Risk prediction model integration in progress")
            
            with col2:
                st.subheader("Clinical Summary")
                if gpt:
                    summary = gpt.summarize_clinical_note(clinical_note)
                    st.write(summary)
            
            st.markdown("---")
            
            # RAG Response
            st.subheader("Medical Guidelines & Recommendations")
            if rag:
                rag_response = rag.generate_response(clinical_note)
                st.markdown(rag_response)
            
            st.markdown("---")
            
            # ICD-10 Suggestions
            st.subheader("Suggested ICD-10 Codes")
            if gpt:
                codes = gpt.suggest_icd10_codes(clinical_note)
                st.code(codes)
            
            # Critical Symptoms
            st.subheader("Critical Symptoms to Monitor")
            if gpt:
                symptoms = gpt.flag_critical_symptoms(clinical_note)
                st.warning(symptoms)

# Footer
st.markdown("---")
st.caption("Disclaimer: This AI system is for clinical decision support only. Final decisions should be made by qualified healthcare professionals.")

