import json

import streamlit as st


def load_tasks():
    with open("resources/tasks/tasks.json", "r") as f:
        return json.load(f)

TASKS = load_tasks()

def display_task(difficulty, chosen_language):
    """

    :param chosen_language: language that was chosen by the user
    :param difficulty: difficulty level of the task
    :return:
    """
    task = TASKS.get(difficulty)
    if task:
        st.markdown(f"### Your Task\n{task['description']}")
        display_examples(task['examples'])
        st.markdown("### Additional Info")
        display_additional_info(task['additional_info'])
        st.markdown("### Solution Template")
        chosen_language = chosen_language.lower()
        if chosen_language not in task['template']:
            chosen_language = "python"
        st.code(task['template'][chosen_language], language=chosen_language, wrap_lines=True)
        st.divider()
        st.markdown("***Sourced from https://leetcode.com/***")
    else:
        st.error("Invalid task difficulty")

def display_examples(examples):
    with st.expander("📝 See/hide examples", expanded=True):
        for example in examples:
            st.markdown(f"### {example['title']}")
            st.markdown(f"**Input:**\n```\n{example['input']}\n```")
            st.markdown(f"**Output:** `{example['output']}`")
            st.markdown(f"**Explanation:**\n{example['explanation']}")

def display_additional_info(info):
    info = info.split('\n')
    info_list = "\n".join([f"- {i}" for i in info])
    st.markdown(info_list)

def get_task_for_prompt(difficulty):
    task = TASKS.get(difficulty)
    if not task:
        return "Invalid task difficulty"

    prompt = f"Task Description: {task['description']}\n\n"
    prompt += "Examples:\n"
    for example in task['examples']:
        prompt += f"{example['title']}:\n"
        prompt += f"Input: {example['input']}\n"
        prompt += f"Output: {example['output']}\n"
        prompt += f"Explanation: {example['explanation']}\n\n"
    prompt += f"Additional Info: {task['additional_info']}\n"

    for hint in task["hints"]:
        prompt += f"{hint['title']}:\n"
        prompt += f"{hint['description']}\n"

    return prompt

def get_task_template_for_prompt(difficulty, chosen_language):
    task = TASKS.get(difficulty)
    if not task:
        return "Invalid task difficulty"
    chosen_language = chosen_language.lower()
    if chosen_language not in task['template']:
        chosen_language = "python"
    template = task['template'][chosen_language].replace("{", "curly_bracket_left").replace("}", "curly_bracket_right")
    prompt = f"The template for the solution in {chosen_language} is: \n" + template
    return prompt

def get_task_description(difficulty, chosen_language):
    return get_task_for_prompt(difficulty) + "\n\n" + get_task_template_for_prompt(difficulty, chosen_language)
