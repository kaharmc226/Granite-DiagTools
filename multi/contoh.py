examples = [
	{
	"input" : '''
i want to make a program using AI generated code or AI integraion in it, the problem, there is so many options, i have a limited idea in these field. maybe its better to base this project in the filed that i know, because i can identify the problem and solution more clearly than other topic. lets see..
i very interested in hardware service, cause i work in there and its very fun to find a problem in the devices that most people dont know the cause of. but again, it can be a downside because that poor knowledge from the people often lead to confusion, distrust, and many other negative thing, and my poor communication skill makes it even worse. i can make a solution for this problem, maybe a diagnostic tool can help with it, we can provide the problems that happen, like some minor errors, unusual behaviour, and other information that can help to find the problem in this device. this information then thrown into AI to help summarize common problem that have similar symptoms. and it can provide brief information, recommended solution, and if it need a spesific spare parts, it can help us find it in the marketplace. sound neat right
oh yeah, for the AI, you can use this format to use Replicate API

import os
import streamlit as st
from langchain_community.llms import Replicate
import contoh_single as xp

REPLICATE_API_KEY = st.secrets["REPLICATE_API_KEY"]
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_KEY

model = Replicate(
    model="ibm-granite/granite-3.3-8b-instruct",
    replicate_api_token=os.environ['REPLICATE_API_TOKEN'],
    model_kwargs={"max_tokens":1024, "temperature":0.7},
)
''',
	"output" : '''
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
                            
                        if issue.get("precautions"):
                            st.write("**Safety precautions:**")
                            for precaution in issue.get("precautions", []):
                                st.write(f"- {precaution}")
                                
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
                    if st.button("👍 Yes"):
                        st.success("Thank you for your feedback!")
                with col2:
                    if st.button("👎 No"):
                        st.info("We're sorry to hear that. We'll use your feedback to improve.")
                with col3:
                    if st.button("🤔 Partially"):
                        st.info("Thanks for the feedback. We're constantly working to improve our diagnostics.")
            
            else:
                st.error("Failed to analyze the problem. Please try again.")

    # Display history if exists
    if 'history' in st.session_state and st.session_state.history:
        st.sidebar.subheader("Diagnosis History")
        for i, entry in enumerate(reversed(st.session_state.history)):
            if st.sidebar.button(f"{entry['timestamp']} - {entry['device_type']}", key=f"hist_{i}"):
                st.sidebar.write(f"Symptoms: {', '.join(entry['symptoms'])}")
                st.sidebar.write(f"Analysis: {entry['analysis'].get('analysis', '')}")

if __name__ == "__main__":
    main()
	'''	
    },

	{
		"input" : 'Make the diagnosis history saved locally as a JSON file in user storage, and when the program started, it reads the JSON file to display the content in diagnosis history. for easier loading, the JSON file is stored in same directory with the program file ',
		"output" : '''
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

                history_file = "diagnosis_history.json"
                if os.path.exists(history_file):
                    with open(history_file, 'r') as f:
                        st.session_state.history = json.load(f)

                st.session_state.history.append({
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "device_type": device_type,
                    "symptoms": symptoms,
                    "analysis": analysis_result
                })

                with open(history_file, 'w') as f:
                    json.dump(st.session_state.history, f, indent=4)

                # Feedback section
                st.subheader("Was this diagnosis helpful?")
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("👍 Yes"):
                        st.success("Thank you for your feedback!")
                with col2:
                    if st.button("👎 No"):
                        st.info("We're sorry to hear that. We'll use your feedback to improve.")
                with col3:
                    if st.button("🤔 Partially"):
                        st.info("Thanks for the feedback. We're constantly working to improve our diagnostics.")

            else:
                st.error("Failed to analyze the problem. Please try again.")

    # Display history if exists
    if 'history' in st.session_state and st.session_state.history:
        st.sidebar.subheader("Diagnosis History")
        for i, entry in enumerate(reversed(st.session_state.history)):
            if st.sidebar.button(f"{entry['timestamp']} - {entry['device_type']}", key=f"hist_{i}"):
                st.sidebar.write(f"Symptoms: {', '.join(entry['symptoms'])}")
                st.sidebar.write(f"Analysis: {entry['analysis'].get('analysis', '')}")      

if __name__ == "__main__":
    main()
'''
	},
	{
		"input" : "separate the input page and the history page into two different python file, both still run streamlit. but this way we can show two pages, using streamlit multipage feature by making an additional folder named pages",
		"output" : '''
MAIN PAGE

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
    st.sidebar.page_link("diagnostic_app.py", label="Home", icon="🏠")
    st.sidebar.page_link("pages/history.py", label="Diagnosis History", icon="📋")
    
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
                            
                        if issue.get("precautions"):
                            st.write("**Safety precautions:**")
                            for precaution in issue.get("precautions", []):
                                st.write(f"- {precaution}")
                
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
	
History Page (saved in pages/history.py)

import streamlit as st
from datetime import datetime

def main():
    st.title("📋 Diagnosis History")
    
    # Navigation
    st.sidebar.title("Navigation")
    st.sidebar.page_link("../diagnostic_app.py", label="Home", icon="🏠")
    st.sidebar.page_link("history.py", label="Diagnosis History", icon="📋")
    
    # Check if history exists
    if 'history' not in st.session_state or not st.session_state.history:
        st.info("No diagnosis history found. Go to the main page to analyze a device.")
        return
    
    st.write("Here's your diagnosis history:")
    
    # Display history in reverse chronological order (newest first)
    for i, entry in enumerate(reversed(st.session_state.history)):
        with st.expander(f"{entry['timestamp']} - {entry['device_type']}"):
            st.write(f"**Symptoms:** {', '.join(entry['symptoms'])}")
            
            st.write("**Analysis:**")
            st.write(entry['analysis'].get("analysis", ""))
            
            st.write("**Possible Issues:**")
            for j, issue in enumerate(entry['analysis'].get("possible_issues", []), 1):
                st.write(f"{j}. **{issue.get('issue', 'Unknown')}** (Likelihood: {issue.get('likelihood', 'unknown')})")
                
                st.write("   Solutions:")
                for step in issue.get("solutions", []):
                    st.write(f"   - {step}")
                
                if issue.get("precautions"):
                    st.write("   Safety precautions:")
                    for precaution in issue.get("precautions", []):
                        st.write(f"   - {precaution}")
                
                parts = issue.get("parts_needed", [])
                if parts:
                    st.write("   Possible parts needed:")
                    for part in parts:
                        st.write(f"   - {part}")
            
            # Add a button to delete this entry
            if st.button(f"Delete this entry", key=f"delete_{i}"):
                # Calculate the index in the original list (reverse of current index)
                original_index = len(st.session_state.history) - 1 - i
                del st.session_state.history[original_index]
                st.rerun()
    
    # Add a button to clear all history
    if st.button("Clear All History", type="primary"):
        st.session_state.history = []
        st.rerun()

if __name__ == "__main__":
    main()
'''
    },
	{
		"input" : "Make the history pages read the JSON file properly. make The visual similar to the elements in the input page",
		"output" : '''
## Code 1. (diagnostic_app.py)

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

                history_file = "diagnosis_history.json"
                if os.path.exists(history_file):
                    with open(history_file, 'r') as f:
                        st.session_state.history = json.load(f)     

                st.session_state.history.append({
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "device_type": device_type,
                    "symptoms": symptoms,
                    "analysis": analysis_result
                })

                with open(history_file, 'w') as f:
                    json.dump(st.session_state.history, f, indent=4)

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
	
## code.2 (pages/history.py)

import streamlit as st
from datetime import datetime
import os
import json

def main():
    st.title("📋 Diagnosis History")

    # Navigation
    st.sidebar.title("Navigation")
    
    # Check if history exists
    if 'history' not in st.session_state or not st.session_state.history:
        st.info("No diagnosis history found. Go to the main page to analyze a device.")
        return

    st.write("Here's your diagnosis history:")

    # Display history in reverse chronological order (newest first) 
    for i, entry in enumerate(reversed(st.session_state.history)):  
        with st.expander(f"{entry['timestamp']} - {entry['device_type']}"):
            st.write(f"**Symptoms:** {', '.join(entry['symptoms'])}")

            st.write("**Analysis:**")
            st.write(entry['analysis'].get("analysis", ""))

            st.write("**Possible Issues:**")
            for j, issue in enumerate(entry['analysis'].get("possible_issues", []), 1):
                st.write(f"{j}. **{issue.get('issue', 'Unknown')}** (Likelihood: {issue.get('likelihood', 'unknown')})")

                st.write("   Solutions:")
                for step in issue.get("solutions", []):
                    st.write(f"   - {step}")

                if issue.get("precautions"):
                    st.write("   Safety precautions:")
                    for precaution in issue.get("precautions", []): 
                        st.write(f"   - {precaution}")

                parts = issue.get("parts_needed", [])
                if parts:
                    st.write("   Possible parts needed:")
                    for part in parts:
                        st.write(f"   - {part}")

            # Add a button to delete this entry
            if st.button(f"Delete this entry", key=f"delete_{i}"):  
                # Calculate the index in the original list (reverse of current index)
                original_index = len(st.session_state.history) - 1 - i
                del st.session_state.history[original_index]        
                st.rerun()

    # Add a button to clear all history
    if st.button("Clear All History", type="primary"):
        st.session_state.history = []
        st.rerun()

if __name__ == "__main__":
    main()

'''
    },
	{
		"input" : 'make the diagnostic_app.py create the JSON file inside the pages folder',
		"output" : '''
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

                history_file = os.path.join("pages", "diagnosis_history.json")   
                if os.path.exists(history_file):
                    with open(history_file, 'r') as f:
                        st.session_state.history = json.load(f)

                st.session_state.history.append({
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),      
                    "device_type": device_type,
                    "symptoms": symptoms,
                    "analysis": analysis_result
                })

                with open(history_file, 'w') as f:
                    json.dump(st.session_state.history, f, indent=4)

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
'''
    }
]