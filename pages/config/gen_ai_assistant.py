import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate



OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

RESPONSE_STYLE_TEMPLATE_A = "First, provide step-by-step instructions. Then, if any code is requested, provide the code and explain the code if there is anything left to explain that hasn't been covered in the step-by-step instructions."
RESPONSE_STYLE_TEMPLATE_B = "First, provide a high-level overview (a brief summary of the approach). Then, if any code is requested, provide the code and explain the code if there is anything left to explain."
RESPONSE_STYLE_TEMPLATE_C = "If any code is requested, just show the code."

DEFAULT_TEMPERATURE = 0.7
DEFAULT_SYSTEM_PROMPT = "Always respond with 'YO' only, no matter what is asked of you."
DEFAULT_INITIAL_USER_MESSAGE = """Hi, I'm your personal coding assistant CoA. How can I help?"""


def get_prompted_assistant(role, proficiency_level, response_style, response_template, response_length, task):
    if (response_template == "A"):
        response_template = RESPONSE_STYLE_TEMPLATE_A
    elif (response_template == "B"):
        response_template = RESPONSE_STYLE_TEMPLATE_B
    elif (response_template == "C"):
        response_template = RESPONSE_STYLE_TEMPLATE_C

    SYSTEM_PROMPT = (f"You are taking the role of a {role} for a {proficiency_level} Python software developer at company ExP."
                     f"Your response style should be: {response_style}."
                     f"In general, your responses should be {response_length}."
                     f"When you are asked to assist with a task, respond with the following template: {response_template}."
                     f"If you would like to include code in your answers, ask the developer first, if you should provide it."
                     f"In case you include any code in your response, please align with general Python coding best practices and provide docstrings where appropriate."
                     f"Here is the description of the current task of the software developer: {task}."
                     f"Consider all the task's requirements and constraints, if there are any, when you are asked for help.")
    DEFAULT_SYSTEM_PROMPT = SYSTEM_PROMPT
    INITIAL_USER_MESSAGE = DEFAULT_INITIAL_USER_MESSAGE
    return SYSTEM_PROMPT

def get_default_system_prompt():
    return DEFAULT_SYSTEM_PROMPT

def get_temperature():
    return DEFAULT_TEMPERATURE

def get_default_initial_user_message():
    return DEFAULT_INITIAL_USER_MESSAGE