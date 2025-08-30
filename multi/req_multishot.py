import os
import streamlit as st
from langchain_community.llms import Replicate
import contoh as xp


REPLICATE_API_KEY = st.secrets["REPLICATE_API_KEY"]
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_KEY

model = Replicate(
    model="ibm-granite/granite-3.3-8b-instruct",
    replicate_api_token=os.environ['REPLICATE_API_TOKEN'],
    model_kwargs={"max_tokens":5000, "temperature":0.5},
)

def fewshot_prompt(context, examples):

    # Format the examples for the prompt
    formatted_examples = "\n\n".join(
        f"""
        Example {i+1}:
        User Input: {example['input']}
        Model Output: {example['output']}
        """
        for i, example in enumerate(examples)
    )

    # Construct the few-shot prompt
    prompt = f"""
    You are an experienced programmer with 15 years of experience writing full-stack applications and web development.
    Your task is to generate high-quality Python code for a Streamlit deployment using streamlit UI components
    based on the provided context and user question.

    Here are some examples of similar tasks you have completed successfully:
    {formatted_examples}

    Now, using these examples as a reference, generate code for the following task:

    Context: {context}

    Ensure that:
    - use the latest version of all resources
    - The code is well-structured and uses consistent styling, coloring, and formatting for all UI elements.
    - Output only the Python code.
    - if an example is used or mentioned in the code, include the code from examples in this code
    - if making more than one python file, separate it clearly
    """
    return prompt


def get_prompt(context, examples):
	prompt = fewshot_prompt(context, examples)
	result = model.invoke(prompt)
	return result

context = 'make the history.py checks first if the JSON file exists inside the pages folder, and show the content in the history page. with the option to delete entries that can delete the content of diagnosis_history.JSON as well.'
examples = xp.examples

result = get_prompt(context, examples)
print(f"Generated Code:\n {result}")