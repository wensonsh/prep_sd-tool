import json
import random

import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from streamlit_ace import st_ace

from pages.config.gen_ai_assistant import get_prompted_assistant, get_default_initial_user_message, get_temperature
from pages.helper.navigation import forward, home, get_header
from pages.tasks.task_template import display_task, get_task_for_prompt, get_task_template_for_prompt

# Constants
DATA_PATH = "data/participants/"
PAGE_TITLE = "Collaborating with your GenAI tool"
ERROR_MSG = "Your solution is empty. Please submit a solution."
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]


def load_participant_data(participant_id):
    try:
        with open(f"{DATA_PATH}participant_{participant_id}.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        home()


def save_participant_data(participant_id, data):
    with open(f"{DATA_PATH}participant_{participant_id}.json", "w") as f:
        json.dump(data, f)


def initialize_session_state(group, difficulty, selected_role, participant_proficiency_level, selected_response_style, selected_response_template, selected_response_length, selected_code_correction_style, lang):
    if group == "group_tailored":
        if ("system_prompt" not in st.session_state or
                st.session_state["system_prompt"] is None or
                st.session_state["system_prompt"] == ""):
            task_description = get_task_for_prompt(difficulty) + "\n\n" + get_task_template_for_prompt(difficulty, lang)
            st.session_state["system_prompt"] = get_prompted_assistant(
                role=selected_role,
                proficiency_level=participant_proficiency_level,
                lang=lang,
                response_style=selected_response_style,
                response_template=selected_response_template,
                response_length=selected_response_length,
                code_correction_style=selected_code_correction_style,
                task=task_description)
        if "initial_user_message" not in st.session_state:
            st.session_state["initial_user_message"] = get_default_initial_user_message()
    else:
        st.session_state["system_prompt"] = ""
        st.session_state["initial_user_message"] = ""
    if "temperature" not in st.session_state:
        st.session_state["temperature"] = get_temperature()


def main():
    st.set_page_config(page_title=PAGE_TITLE, layout="wide", initial_sidebar_state="expanded", menu_items={'Get Help': 'mailto:wendi.shu@stud.tu-darmstadt.de'})

    if 'participant_id' not in st.session_state:
        home()

    participant_id = st.session_state["participant_id"]
    data = load_participant_data(participant_id)

    if "exp_finished" in data and data["exp_finished"]:
        st.switch_page("pages/gen_ai_tool.py")

    get_header(3, "pages/procedure.py", False, False, data, participant_id)
    st.title(PAGE_TITLE)

    middle, right = st.columns([4, 3], gap="small")

    # initialize task difficulty
    if "assigned_task" in data and data["assigned_task"]:
        task_difficulty = data["assigned_task"]
    else:
        task_difficulty = random.choice(["easy", "medium"])
    # initialize assigned group
    if "assigned_group" in data and data["assigned_group"]:
        assigned_group = data["assigned_group"]
    else:
        assigned_group = random.choice(["group_default", "group_tailored"])

    with st.sidebar:
        if "chosen_lang" in data and data["chosen_lang"]:
            chosen_language = data["chosen_lang"]
        else:
            chosen_language = "Python"
        display_task(task_difficulty, chosen_language)

    # initialize proficiency level
    try:
        if chosen_language == "Python":
            proficiency_in_chosen_lang = data["python_proficiency"]
        else:
            proficiency_in_chosen_lang = data["java_proficiency"]
    except KeyError:
        proficiency_in_chosen_lang = "unknown expertise"

    with (middle):
        role = None
        response_style = None
        response_template = None
        response_length = None
        code_adjustment = None
        if assigned_group == "group_tailored":
            with st.expander("***Interaction and Response Settings***", expanded=False):
                # CHOOSE RESPONSE TEMPLATE
                response_template_options = ["Code only", "Step-by-step instructions + code block", "High-level overview + code block + explanation", "Other"]
                response_template_index = None
                if "response_template" in data and data["response_template"] and data["response_template"] in response_template_options:
                    response_template_index = response_template_options.index(data["response_template"])
                response_template = st.radio(label="**Response template for code-related answers**",
                                             options=response_template_options,
                                             index=response_template_index,
                                             key="response_template",
                                             horizontal=True)

                if response_template == "Other":
                    response_template_input = ""
                    if "response_template_other" in data and data["response_template_other"]:
                        response_template_input = data["response_template_other"]
                    response_template_other = st.text_input(label = "Please enter your preferred response template",
                                  label_visibility="collapsed",
                                  placeholder="Please enter your preferred response template",
                                  value=response_template_input)

                # RESPONSE STYLE
                response_style_options = ["Bullet points", "Continuous text", "Other"]
                response_style_index = None
                if "response_style" in data and data["response_style"] and data["response_style"] in response_style_options:
                    response_style_index = response_style_options.index(data["response_style"])

                response_style = st.radio(label="**Response style**",
                                          options=response_style_options,
                                          index=response_style_index,
                                          horizontal=True)
                if response_style == "Other":
                    response_style_input = ""
                    if "response_style_other" in data and data["response_style_other"]:
                        response_style_input = data["response_style_other"]
                    response_style_other = st.text_input(label="Preferred response style",
                                  label_visibility="collapsed",
                                  placeholder="Please enter your preferred response style",
                                  value=response_style_input)

                # ROLE
                role_options = ["Assistant", "Mentor", "None", "Other"]
                role_index = None
                if "role" in data and data["role"] and data["role"] in role_options:
                    role_index = role_options.index(data["role"])
                role = st.radio(label="**Role that is taken on by the GenAI model**",
                                options=role_options,
                                key="role",
                                index=role_index,
                                horizontal=True)
                if role == "Other":
                    role_input = ""
                    if "role_other" in data and data["role_other"]:
                        role_input = data["role_other"]
                    role_other = st.text_input(label="Preferred role",
                                  label_visibility="collapsed",
                                  placeholder="Please enter the preferred role",
                                  value=role_input)

                # RESPONSE LENGTH
                response_length_options = ["Concise", "Short and comprehensive", "Detailed and comprehensive", "Other"]
                response_length_index = None
                if "response_length" in data and data["response_length"] and data["response_length"] in response_length_options:
                    response_length_index = response_length_options.index(data["response_length"])
                response_length = st.radio(label="**Response length**",
                                           options=response_length_options,
                                           key="response_length",
                                           horizontal=True,
                                           index=response_length_index)
                if response_length == "Other":
                    response_length_input = ""
                    if "response_length_other" in data and data["response_length_other"]:
                        response_length_input = data["response_length_other"]
                    response_length_other = st.text_input(label="Preferred response length",
                                  label_visibility="collapsed",
                                  placeholder="Please enter the preferred response length",
                                  value=response_length_input)

                # CODE ADJUSTMENT
                code_adjustment_options = ["Provide the whole code", "Provide the whole code and highlight changed parts", "Only show adjusted code snippets", "Other"]
                code_adjustment_index = None
                if "code_adjustment" in data and data["code_adjustment"] and data["code_adjustment"] in code_adjustment_options:
                    code_adjustment_index = code_adjustment_options.index(data["code_adjustment"])
                code_adjustment = st.radio(label="**How do you prefer adjusted code to be presented?**",
                                           options=code_adjustment_options,
                                           key="code_adjustment",
                                           horizontal=True,
                                           index=code_adjustment_index)
                if code_adjustment == "Other":
                    code_adjustment_input = ""
                    if "code_adjustment_other" in data and data["code_adjustment_other"]:
                        code_adjustment_input = data["code_adjustment_other"]
                    code_adjustment_other = st.text_input(label="Preferred code adjustment style",
                                  label_visibility="collapsed",
                                  placeholder="Please enter the preferred code adjustment style",
                                  value=code_adjustment_input)

                if st.button("Save settings"):
                    data["settings_changed_count"] = data.get("settings_changed_count", 0) + 1
                    task = get_task_for_prompt(task_difficulty) + "\n\n" + get_task_template_for_prompt(task_difficulty, chosen_language)
                    data["response_template"] = response_template
                    if response_template == "Other" and response_template_other:
                        data["response_template_other"] = response_template_other
                        response_template = response_template_other
                    data["response_style"] = response_style
                    if response_style == "Other" and response_style_other:
                        data["response_style_other"] = response_style_other
                        response_style = response_style_other
                    data["role"] = role
                    if role == "Other" and role_other:
                        data["role_other"] = role_other
                        role = role_other
                    data["response_length"] = response_length
                    if response_length == "Other" and response_length_other:
                        data["response_length_other"] = response_length_other
                        response_length = response_length_other
                    data["code_adjustment"] = code_adjustment
                    if code_adjustment == "Other" and code_adjustment_other:
                        data["code_adjustment_other"] = code_adjustment_other
                        code_adjustment = code_adjustment_other
                    st.session_state["system_prompt"] = get_prompted_assistant(
                        role=role,
                        proficiency_level=proficiency_in_chosen_lang,
                        lang=chosen_language,
                        response_style=response_style,
                        response_template=response_template,
                        response_length=response_length,
                        code_correction_style=code_adjustment,
                        task=task)

                    if "system_prompt" in data and data["system_prompt"]:
                        data["system_prompt"] = data["system_prompt"] + "   ->  " + st.session_state["system_prompt"]
                    else:
                        data["system_prompt"] = st.session_state["system_prompt"]
                    save_participant_data(participant_id, data)

        initialize_session_state(group=assigned_group,
                                 difficulty=task_difficulty,
                                 selected_role=role,
                                 participant_proficiency_level=proficiency_in_chosen_lang,
                                 selected_response_style=response_style,
                                 selected_response_template=response_template,
                                 selected_response_length=response_length,
                                 selected_code_correction_style=code_adjustment,
                                 lang=chosen_language)
        chat_template = ChatPromptTemplate.from_messages(
            [
                ("system", st.session_state["system_prompt"]),
                ("placeholder", "{conversation}"),
                ("user", "{user_input}")
            ]
        )

        if "gen_messages" not in st.session_state:
            if "message_generate" not in data and st.session_state["initial_user_message"]:
                st.session_state["gen_messages"] = [{
                    "role": "assistant",
                    "content": st.session_state["initial_user_message"]
                }]
            elif not st.session_state["initial_user_message"] or st.session_state["initial_user_message"] == "":
                st.session_state["gen_messages"] = []
            else:
                st.session_state["gen_messages"] = data["message_generate"]

        with st.expander(":gray[Click here to adjust the chat's and the solution's container height [px]]",
                         expanded=False):
            container_height = st.slider(label="Choose container height in pixels", label_visibility="hidden",
                                         min_value=200, max_value=800, value=400)
        messages_container = st.container(height=container_height)

        for msg in st.session_state.gen_messages:
            messages_container.chat_message(msg["role"]).write(msg["content"], unsafe_allow_html=True)

        if input_text := st.chat_input():
            messages_container.chat_message("user").write(input_text)
            llm = ChatOpenAI(
                model="gpt-4o",
                temperature=get_temperature(),
                openai_api_key=OPENAI_API_KEY
            )

            prompt = chat_template.format_messages(user_input=input_text, conversation=st.session_state.gen_messages)

            try:
                response = llm.invoke(prompt)
                msg = response.content
            except Exception as e:
                msg = f"Error: {str(e)}"

            st.session_state.gen_messages.append({"role": "user", "content": input_text})
            st.session_state.gen_messages.append({"role": "assistant", "content": msg})
            messages_container.chat_message("assistant").write(msg)

            if "live_message_generate" in data:
                data["live_message_generate"] = str(data["live_message_generate"]) + " NEW ANSWER    =>       " + str(
                    st.session_state.gen_messages)
            else:
                data["live_message_generate"] = str(st.session_state.gen_messages)
            save_participant_data(participant_id, data)

    with right:
        st.markdown("**Your Solution:**")
        st.text("")
        solution_value = data.get("solution_generate", "")
        solution = st_ace(
            placeholder="Enter your Python code here",
            theme='monokai',
            height=container_height,
            keybinding='vscode',
            show_gutter=True,
            auto_update=True,
            value=solution_value
        )

        slider_left, slider_middle, slider_right = st.columns([1, 20, 1], gap="small")

        with slider_middle:
            perceived_task_difficulty_values = ["Easy", "Medium", "Hard"]
            perceived_task_difficulty_value = None
            if "perceived_task_difficulty" in data and data['perceived_task_difficulty']:
                perceived_task_difficulty_value = data["perceived_task_difficulty"]
            perceived_task_difficulty = st.select_slider(
                label="I perceived this task as ...",
                options=perceived_task_difficulty_values,
                value=perceived_task_difficulty_value
            )
            data["perceived_task_difficulty"] = perceived_task_difficulty

        if st.button("Submit and continue →", type="primary", use_container_width=True):
            if solution is None or len(solution) == 0:
                st.error(ERROR_MSG)
            else:
                if "solution_generate" not in data:
                    data["solution_generate"] = str(solution)
                    data["live_solution_generate"] = str(solution)
                elif "live_solution_generate" in data:
                    data["live_solution_generate"] = str(data["live_solution_generate"]) + "     ->      " + str(
                        solution)

                save_participant_data(participant_id, data)
                forward("pages/post_survey.py", False, True, data, participant_id)


if __name__ == "__main__":
    main()