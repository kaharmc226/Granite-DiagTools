# diagnostic_app.py

import os
import json
import streamlit as st
from datetime import datetime
from langchain_community.llms import Replicate

# Set up Replicate API
REPLICATE_API_KEY = st.secrets["REPLICATE_API_KEY"]
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_KEY

model = Replicate(
    model="ibm-granite/granite-3.3-8b-instruct",
    replicate_api_token=os.environ['REPLICATE_API_TOKEN'],
    model_kwargs={"max_tokens": 1024, "temperature": 0.7},
)

# Sample database of common hardware issues
HARDWARE_ISSUES = {
    "laptop": {
        "won't turn on": [
            "Faulty power adapter", "Dead battery", "Motherboard issue", "Power button failure"
        ],
        "overheating": [
            "Dust clogged fans", "Failed thermal paste", "Faulty cooling fan", "CPU overloading"
        ],
        "blue screen": [
            "Faulty RAM", "Hard drive failure", "Driver conflicts", "Operating system corruption"
        ]
    },
    "smartphone": {
        "rapid battery drain": [
            "Battery needs replacement", "Background apps consuming power", "Screen brightness too high"
        ],
        "cracked screen": [
            "Physical damage requiring screen replacement"
        ],
        "not charging": [
            "Faulty charging cable", "Charging port damage", "Battery failure"   
        ]
    },
    "printer": {
        "paper jams": [
            "Obstruction in paper path", "Worn pickup rollers", "Incorrect paper type"
        ],
        "poor print quality": [
            "Clogged print heads", "Low ink levels", "Incorrect printer settings"
        ]
    }
}

def analyze_with_ai(device_type, symptoms, description):
    """Use Replicate AI to analyze the described problem and suggest solutions"""

    prompt = f"""
    As an experienced hardware technician, analyze this device problem:

    Device Type: {device_type}
    Symptoms: {symptoms}
    Description: {description}

    Please provide:
    1. Likely causes (list 3-5 most probable issues)
    2. Recommended solutions for each potential issue
    3. Skill level required (beginner, intermediate, expert)
    4. Estimated repair time for each solution
    5. Any safety precautions

    Format your response as JSON with the following structure:
    {{
        "analysis": "brief overall analysis",
        "possible_issues": [
            {{
                "issue": "issue name",
                "likelihood": "high/medium/low",
                "solutions": ["step 1", "step 2", ...],
                "skill_level": "beginner/intermediate/expert",
                "repair_time": "estimated time",
                "precautions": ["precaution 1", ...],
                "parts_needed": ["part 1", ...]
            }}
        ]
    }}
    """

    try:
        # Call the Replicate model
        response = model(prompt)

        # Extract JSON from the response
        try:
            # Try to find JSON in the response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                return json.loads(json_str)
            else:
                # If no JSON found, return a structured error
                st.error("AI response didn't contain valid JSON. Showing raw response:")
                st.write(response)
                return {
                    "analysis": "Could not parse AI response. Please try again.",
                    "possible_issues": []
                }
        except json.JSONDecodeError as e:
            st.error(f"Failed to parse AI response as JSON: {e}")
            st.write("Raw response:", response)
            return {
                "analysis": "Error parsing AI response. Please try again.",      
                "possible_issues": []
            }

    except Exception as e:
        st.error(f"Error in AI analysis: {e}")
        return {
            "analysis": f"Error in analysis: {str(e)}",
            "possible_issues": []
        }

def main():
    st.title("🔧 Hardware Diagnostic Assistant")
    st.write("Describe your device issue and get AI-powered diagnosis and solutions")

    # Navigation
    st.sidebar.title("Navigation")

    # Input form
    with st.form("diagnosis_form"):
        col1, col2 = st.columns(2)

        with col1:
            device_type = st.selectbox(
                "Device Type",
                options=["laptop", "smartphone", "printer", "desktop computer", "tablet", "other"]
            )

            symptoms = st.multiselect(
                "Select all applicable symptoms",
                options=["Won't turn on", "Overheating", "Blue screen/errors", "Performance issues",
                         "Battery problems", "Display issues", "Connectivity problems", "Physical damage",
                         "Unusual noises", "Other"]
            )

        with col2:
            brand = st.text_input("Brand (optional)")
            model_input = st.text_input("Model (optional)")
            age = st.slider("Device age (years)", 0, 10, 2)

        description = st.text_area(
            "Please describe the problem in detail:",
            placeholder="Example: My laptop started making grinding noises yesterday, and today it won't turn on. The power light comes on for a second then turns off..."
        )

        submitted = st.form_submit_button("Analyze Problem")

    # Process form submission
    if submitted:
        if not description.strip():
            st.error("Please describe the problem in detail")
            return

        with st.spinner("Analyzing problem with AI..."):
            # Get AI analysis
            analysis_result = analyze_with_ai(device_type, symptoms, description)

            if analysis_result:
                st.success("Analysis complete!")

                # Display results
                st.subheader("Problem Analysis")
                st.write(analysis_result.get("analysis", ""))

                st.subheader("Possible Issues")
                for i, issue in enumerate(analysis_result.get("possible_issues", []), 1):
                    with st.expander(f"Issue {i}: {issue.get('issue', 'Unknown')} (Likelihood: {issue.get('likelihood', 'unknown')})"):
                        st.write(f"**Skill level required:** {issue.get('skill_level', 'Not specified')}")
                        st.write(f"**Estimated repair time:** {issue.get('repair_time', 'Not specified')}")

                        st.write("**Solutions:**")
                        for step in issue.get("solutions", []):
                            st.write(f"- {step}")

                # Save diagnosis history
                if 'history' not in st.session_state:
                    st.session_state.history = []

                
                st.session_state.history.append({
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),      
                    "device_type": device_type,
                    "symptoms": symptoms,
                    "analysis": analysis_result
                })

                # Feedback section
                st.subheader("Was this diagnosis helpful?")
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("👍 Yes", key="feedback_yes"):
                        st.success("Thank you for your feedback!")
                with col2:
                    if st.button("👎 No", key="feedback_no"):
                        st.info("We're sorry to hear that. We'll use your feedback to improve.")
                with col3:
                    if st.button("🤔 Partially", key="feedback_partial"):        
                        st.info("Thanks for the feedback. We're constantly working to improve our diagnostics.")

            else:
                st.error("Failed to analyze the problem. Please try again.")     

if __name__ == "__main__":
    main()