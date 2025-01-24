import json
import os
import random

import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from pages.config.gen_ai_assistant import get_temperature, \
    get_default_initial_user_message_without_task, get_prompted_assistant_without_task
from pages.helper.navigation import home

# Constants

PAGE_TITLE = "GenAI Tool"

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]


def load_participant_data(participant_id):
    DATA_PATH = "data/participants/"
    try:
        with open(f"{DATA_PATH}participant_{participant_id}.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        home()

def load_revisit_data(participant_id):
    DATA_PATH = "data/revisited/"
    data = {
        "id": participant_id
    }
    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH)

    try:
        if not os.path.exists(DATA_PATH + "participant_" + participant_id + ".json"):
            with open(DATA_PATH + "participant_" + participant_id + ".json", "w") as file:
                json.dump(data, file)
        with open(DATA_PATH + "participant_" + participant_id + ".json", "r") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        home()


def save_participant_data(participant_id, data):
    with open(f"data/revisited/participant_{participant_id}.json", "w") as f:
        json.dump(data, f)


def initialize_session_state(group, selected_role, participant_proficiency_level, selected_response_style, selected_response_template, selected_response_length, selected_code_correction_style):
    if group == "group_tailored":
        if ("system_prompt" not in st.session_state or
                st.session_state["system_prompt"] is None or
                st.session_state["system_prompt"] == ""):
            st.session_state["system_prompt"] = get_prompted_assistant_without_task(
                role=selected_role,
                proficiency_level=participant_proficiency_level,
                response_style=selected_response_style,
                response_template=selected_response_template,
                response_length=selected_response_length,
                code_correction_style=selected_code_correction_style)
        if "initial_user_message" not in st.session_state:
            st.session_state["initial_user_message"] = get_default_initial_user_message_without_task()
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

    st.title(PAGE_TITLE)

    # initialize assigned group
    participant_data = load_participant_data(participant_id)
    if "assigned_group" in participant_data and participant_data["assigned_group"]:
        assigned_group = participant_data["assigned_group"]
    else:
        assigned_group = random.choice(["group_default", "group_tailored"])

    st.warning("Please note that your data will be processed by OpenAI, as this GenAI tool utilizes OpenAI's gpt-4o model. Avoid entering any personal or sensitive information.\n\nThe developers of this tool do not take any responsibility for the data entered or processed.")
    with st.expander("***Interaction and Response Settings***", expanded=False):
        # CHOOSE RESPONSE TEMPLATE
        response_template_options = ["Code only", "Step-by-step instructions + code block", "High-level overview + code block + explanation", "Others"]
        response_template_index = 0
        if "response_template" in participant_data and participant_data["response_template"] and participant_data["response_template"] in response_template_options:
            response_template_index = response_template_options.index(data["response_template"])
        response_template = st.radio(label="**Response template for code-related answers**",
                                     options=response_template_options,
                                     index=response_template_index,
                                     key="response_template",
                                     horizontal=True)

        if response_template == "Others":
            response_template_input = ""
            if "response_template" in participant_data and participant_data["response_template"] and participant_data["response_template"] not in response_template_options:
                response_template_input = participant_data["response_template"]
            st.text_input(label = "Please enter your preferred response template",
                          label_visibility="collapsed",
                          placeholder="Please enter your preferred response template",
                          value=response_template_input)

        # RESPONSE STYLE
        response_style_options = ["Bullet points", "Flowtext", "Other"]
        response_style_index = 0
        if "response_style" in participant_data and participant_data["response_style"] and participant_data["response_style"] in response_template_options:
            response_style_index = response_style_options.index(participant_data["response_style"])

        response_style = st.radio(label="**Response style**",
                                  options=response_style_options,
                                  index=response_style_index,
                                  horizontal=True)
        if response_style == "Other":
            response_style_input = ""
            if "response_style" in participant_data and participant_data["response_style"] and participant_data["response_style"] not in response_style_options:
                response_style_input = participant_data["response_style"]
            st.text_input(label="Preferred response style",
                          label_visibility="collapsed",
                          placeholder="Please enter your preferred response style",
                          value=response_style_input)

        # ROLE
        role_options = ["Assistant", "Mentor", "None", "Other"]
        role_index = 0
        if "role" in participant_data and participant_data["role"] and participant_data["role"] in role_options:
            role_index = role_options.index(participant_data["role"])
        role = st.radio(label="**Role that is taken on by the GenAI model**",
                        options=role_options,
                        key="role",
                        index=role_index,
                        horizontal=True)
        if role == "Other":
            role_input = ""
            if "role" in participant_data and participant_data["role"] and participant_data["role"] not in role_options:
                role_input = participant_data["role"]
            st.text_input(label="Preferred role",
                          label_visibility="collapsed",
                          placeholder="Please enter the preferred role",
                          value=role_input)

        # RESPONSE LENGTH
        response_length_options = ["Concise", "Short and comprehensive", "Detailed and comprehensive", "Others"]
        response_length_index = 0
        if "response_length" in participant_data and participant_data["response_length"] and participant_data["response_length"] in response_length_options:
            response_length_index = response_length_options.index(participant_data["response_length"])
        response_length = st.radio(label="**Response length**",
                                   options=response_length_options,
                                   key="response_length",
                                   horizontal=True,
                                   index=response_length_index)
        if response_length == "Others":
            if "response_length" in participant_data and participant_data["response_length"] and participant_data["response_length"] not in response_length_options:
                response_length_input = participant_data["response_length"]
            st.text_input(label="Preferred response length",
                          label_visibility="collapsed",
                          placeholder="Please enter the preferred response length",
                          value=response_length_input)

        # CODE ADJUSTMENT
        code_adjustment_options = ["Provide the whole code", "Provide the whole code and highlight changed parts", "Only show adjusted code snippets", "Others"]
        code_adjustment_index = 0
        if "code_adjustment" in participant_data and participant_data["code_adjustment"] and participant_data["code_adjustment"] in code_adjustment_options:
            code_adjustment_index = code_adjustment_options.index(participant_data["code_adjustment"])
        code_adjustment = st.radio(label="**How do you prefer adjusted code to be presented?**",
                                   options=code_adjustment_options,
                                   key="code_adjustment",
                                   horizontal=True,
                                   index=code_adjustment_index)
        if code_adjustment == "Others":
            if "code_adjustment" in participant_data and participant_data["code_adjustment"] and participant_data["code_adjustment"] not in code_adjustment_options:
                code_adjustment_input = participant_data["code_adjustment"]
            st.text_input(label="Preferred code adjustment style",
                          label_visibility="collapsed",
                          placeholder="Please enter the preferred code adjustment style",
                          value=code_adjustment_input)

        if st.button("Save settings"):
            st.session_state["system_prompt"] = get_prompted_assistant_without_task(
                role=role,
                proficiency_level=participant_data["python_proficiency"],
                response_style=response_style,
                response_template=response_template,
                response_length=response_length,
                code_correction_style=code_adjustment)
            data["response_template"] = response_template
            data["response_style"] = response_style
            data["role"] = role
            data["response_length"] = response_length
            data["code_adjustment"] = code_adjustment
            if "system_prompt" in data and data["system_prompt"]:
                data["system_prompt"] = data["system_prompt"] + "   ->  " + st.session_state["system_prompt"]
            else:
                data["system_prompt"] = st.session_state["system_prompt"]
            save_participant_data(participant_id, data)

    initialize_session_state(assigned_group, role, data["python_proficiency"], response_style, response_template, response_length, code_adjustment)
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


if __name__ == "__main__":
    main()