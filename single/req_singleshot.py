import os
import streamlit as st
from langchain_community.llms import Replicate
import contoh_single as xp


REPLICATE_API_KEY = st.secrets["REPLICATE_API_KEY"]
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_KEY

model = Replicate(
    model="ibm-granite/granite-3.3-8b-instruct",
    replicate_api_token=os.environ['REPLICATE_API_TOKEN'],
    model_kwargs={"max_tokens":5000, "temperature":0.8},
)

def fewshot_prompt(question, examples):

    # Construct the few-shot prompt
    prompt = f"""
    You are an experienced programmer with 15 years of experience writing full-stack applications and web development.
    Your task is to generate high-quality Python code for a Streamlit deployment using streamlit UI components
    based on the provided context and user question.

    Now, generate a complete python code that suits for the user input:

    User input: {question}
    Ensure that:
    - The code is well-structured and uses consistent styling, coloring, and formatting for all UI elements.
    - Output only the Python code.
    """
    return prompt


def get_prompt(question, examples):
	prompt = fewshot_prompt (question, examples)
	result = model.invoke(prompt)
	return result

question = '''
i want to make a program using AI generated code or AI integration in it, the problem, there is so many options, i have a limited idea in these field. maybe its better to base this project in the filed that i know, because i can identify the problem and solution more clearly than other topic. lets see..
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

'''
examples = xp.example

result = get_prompt( question, examples)
print(f"Generated Code:\n {result}")