import json

import streamlit as st


def load_tasks():
    with open("resources/tasks/tasks.json", "r") as f:
        return json.load(f)

TASKS = load_tasks()

def display_task(difficulty):
    """

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
        st.code(task['template'], language="python", wrap_lines=True)
        st.divider()
        st.markdown("***Sourced from https://leetcode.com/***")
    else:
        st.error("Invalid task difficulty")

def display_examples(examples):
    with st.expander("📝 See Examples", expanded=True):
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

    return prompt

def get_task_template_for_prompt(difficulty):
    task = TASKS.get(difficulty)
    if not task:
        return "Invalid task difficulty"
    prompt = "The template for the solution is: \n" + task['template']
    return prompt