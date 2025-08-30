import streamlit as st
import os
from datetime import datetime
import json

def main():
    st.title("📋 Diagnosis History")

    # Navigation
    st.sidebar.title("Navigation")
    
    # Check if history exists
    history_file = os.path.join("pages", "diagnosis_history.json")
    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            st.session_state.history = json.load(f)
        
        if st.session_state.history:
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
                        with open(history_file, 'w') as f:
                            json.dump(st.session_state.history, f, indent=4)     
                        st.rerun()
    else:
        st.info("No diagnosis history found. Go to the main page to analyze a device.")

    # Add a button to clear all history
    if st.button("Clear All History", type="primary"):
        st.session_state.history = []
        with open(history_file, 'w') as f:
            json.dump(st.session_state.history, f, indent=4)
        st.rerun()

if __name__ == "__main__":
    main()