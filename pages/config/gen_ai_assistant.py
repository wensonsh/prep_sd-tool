import streamlit as st

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

RESPONSE_STYLE_TEMPLATE_A = "Just show the code and nothing else"
RESPONSE_STYLE_TEMPLATE_B = "First, provide step-by-step instructions. Then, provide the code and explain the code if there is anything left to explain that hasn't been covered in the step-by-step instructions"
RESPONSE_STYLE_TEMPLATE_C = "First, provide a high-level overview (a brief summary of the approach). Then, provide the code and explain the code if there is anything left to explain"


DEFAULT_TEMPERATURE = 0.7
DEFAULT_INITIAL_USER_MESSAGE = """Hi, I'm your personal coding assistant CoA. I already know your task. \n\n Feel free to adjust the interaction and response settings first (see expander above this chat), before we start to collaborate on the task. Let's get started! 🚀"""
INITIAL_USER_MESSAGE_WITHOUT_TASK = """Hi, I'm your personal coding assistant CoA. \n\n Feel free to adjust the interaction and response settings first (see expander above this chat), before we get started."""

def get_prompted_assistant(role, proficiency_level, response_style, response_template, response_length, code_correction_style, task):
    if response_template == "Code only":
        response_template = RESPONSE_STYLE_TEMPLATE_A
    elif response_template == "Step-by-step instructions + code block":
        response_template = RESPONSE_STYLE_TEMPLATE_B
    elif response_template == "High-level overview + code block + explanation":
        response_template = RESPONSE_STYLE_TEMPLATE_C
    if response_style == "Flowtext":
        response_style = "flowtext. Avoid any bullet points or lists in that case"

    system_prompt = (f"You are taking the role of a {role} for a {proficiency_level} Python software developer who is conducting an experiment with your assistance."
                     f"While interacting with the software developer, your responses should be as {response_style}."
                     f"In general, your responses should be {response_length}."
                     f"If the developer asks you to provide code, do so. If you would like to include code in your answers, without the developer explicitly asking for code before, ask the developer first, if you should provide it."
                     f"In case you include any code in your response, do so in the following template: {response_template}. Also, align with general Python coding best practices and provide docstrings where appropriate."
                     f"In case you adjust or correct any code that you already have provided or that is provided to you, {code_correction_style}"
                     f"Here is the description of the current task of the software developer: {task}."
                     f"The developer can see that same task description and all the requirements in the sidebar on the experiment page that can be opened and closed."
                     f"Consider all the task's requirements and constraints, if there are any, when you are asked for help.")
    return system_prompt


def get_prompted_assistant_without_task(role, proficiency_level, response_style, response_template, response_length, code_correction_style):
    if response_template == "Code only":
        response_template = RESPONSE_STYLE_TEMPLATE_A
    elif response_template == "Step-by-step instructions + code block":
        response_template = RESPONSE_STYLE_TEMPLATE_B
    elif response_template == "High-level overview + code block + explanation":
        response_template = RESPONSE_STYLE_TEMPLATE_C
    if response_style == "Flowtext":
        response_style = "flowtext. Avoid any bullet points or lists in that case"
    system_prompt = (
        f"You are taking the role of a {role} for a {proficiency_level} Python software developer who is conducting an experiment with your assistance."
        f"While interacting with the software developer, your responses should be as {response_style}."
        f"In general, your responses should be {response_length}."
        f"If the developer asks you to provide code, do so. If you would like to include code in your answers, without the developer explicitly asking for code before, ask the developer first, if you should provide it."
        f"In case you include any code in your response, do so in the following template: {response_template}. Also, align with general Python coding best practices and provide docstrings where appropriate."
        f"In case you adjust or correct any code that you already have provided or that is provided to you, {code_correction_style}")
    return system_prompt


def get_temperature():
    return DEFAULT_TEMPERATURE

def get_default_initial_user_message():
    return DEFAULT_INITIAL_USER_MESSAGE

def get_default_initial_user_message_without_task():
    return INITIAL_USER_MESSAGE_WITHOUT_TASK