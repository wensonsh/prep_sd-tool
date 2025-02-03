import random

import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from pages.config.gen_ai_assistant import get_temperature, \
    get_default_initial_user_message_without_task, get_prompted_assistant_without_task
from pages.helper.file_helper import open_json, write_json
from pages.helper.navigation import home

# Constants
PAGE_TITLE = "GenAI Tool"
REVISITED_FILE_PATH = "data/revisited/"
PARTICIPANT_FILE_PATH = "data/participants/"

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]


def initialize_session_state(group, selected_role, lang_input, participant_proficiency_level, selected_response_style, selected_response_template, selected_response_length, selected_code_correction_style):
    if group == "group_tailored":
        if ("system_prompt" not in st.session_state or
                st.session_state["system_prompt"] is None or
                st.session_state["system_prompt"] == ""):
            st.session_state["system_prompt"] = get_prompted_assistant_without_task(
                role=selected_role,
                proficiency_level=participant_proficiency_level,
                lang=lang_input,
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
    revisited_data = open_json(REVISITED_FILE_PATH, participant_id)

    st.title(PAGE_TITLE)

    # get assigned group
    if "assigned_group" in revisited_data and revisited_data["assigned_group"]:
        assigned_group = revisited_data["assigned_group"]
    else:
        assigned_group = random.choice(["group_default", "group_tailored"])


    middle, right = st.columns([4, 1], gap="small")
    with middle:
        st.warning(
            "Please note that your data will be processed by OpenAI, as this GenAI tool utilizes OpenAI's gpt-4o model. Avoid entering any personal or sensitive information.\n\nThe developers of this tool do not take any responsibility for the data entered or processed.")
        role = None
        response_style = None
        response_template = None
        response_length = None
        code_adjustment = None
        proficiency = None
        chosen_language = None
        if assigned_group == "group_tailored":
            # INTERACTION SETTINGS
            with st.expander("***Interaction and Response Settings***", expanded=False):
                if st.button("⏮️ Reset settings", type="tertiary"):
                    st.session_state["system_prompt"] = get_prompted_assistant_without_task(
                        role=None,
                        proficiency_level=None,
                        lang=None,
                        response_style=None,
                        response_template=None,
                        response_length=None,
                        code_correction_style=None)
                    st.success("Your settings have been reset.", icon="⏮️")
                    revisited_data["role"] = None
                    revisited_data["response_style"] = None
                    revisited_data["response_template"] = None
                    revisited_data["response_length"] = None
                    revisited_data["code_adjustment"] = None
                    write_json(REVISITED_FILE_PATH, participant_id, revisited_data)


                prev_chosen_language = ""
                if "chosen_lang" in revisited_data and revisited_data["chosen_lang"]:
                    prev_chosen_language = revisited_data["chosen_lang"]
                chosen_language = st.text_input(
                    label=f"**If you wish the GenAI tool to adapt to a specific programming language, please enter the language here:**",
                    placeholder="Please enter",
                    value=prev_chosen_language)

                if chosen_language and chosen_language != "":
                    proficiency_values = ["No Experience", "Beginner", "Intermediate", "Advanced", "Expert"]
                    proficiency_index = None

                    if "proficiency" in revisited_data and revisited_data["proficiency"]:
                        proficiency_index = proficiency_values.index(revisited_data["proficiency"])

                    proficiency = st.selectbox(
                        label="How proficient are you with Java?*",
                        options=proficiency_values,
                        index=proficiency_index,
                        placeholder="Please select"
                    )
                    revisited_data["proficiency"] = proficiency

                # CHOOSE RESPONSE TEMPLATE
                response_template_options = ["Code only", "Step-by-step instructions + code block", "High-level overview + code block + explanation", "Others"]
                response_template_index = None
                if "response_template" in revisited_data and revisited_data["response_template"] and revisited_data["response_template"] in response_template_options:
                    response_template_index = response_template_options.index(revisited_data["response_template"])
                response_template = st.radio(label="**Response template for code-related answers**",
                                             options=response_template_options,
                                             index=response_template_index,
                                             key="response_template",
                                             horizontal=True)

                if response_template == "Other":
                    response_template_input = ""
                    if "response_template_other" in revisited_data and revisited_data["response_template_other"]:
                        response_template_input = revisited_data["response_template_other"]
                    response_template_other = st.text_input(label="Please enter your preferred response template",
                                                            label_visibility="collapsed",
                                                            placeholder="Please enter your preferred response template",
                                                            value=response_template_input)
                    revisited_data["response_template_other"] = response_template_other

                # RESPONSE STYLE
                response_style_options = ["Bullet points", "Continuous text", "Other"]
                response_style_index = None
                if "response_style" in revisited_data and revisited_data["response_style"] and revisited_data["response_style"] in response_style_options:
                    response_style_index = response_style_options.index(revisited_data["response_style"])

                response_style = st.radio(label="**Response style**",
                                          options=response_style_options,
                                          index=response_style_index,
                                          horizontal=True)
                if response_style == "Other":
                    response_style_input = ""
                    if "response_style_other" in revisited_data and revisited_data["response_style_other"]:
                        response_style_input = revisited_data["response_style_other"]
                    response_style_other = st.text_input(label="Preferred response style",
                                                         label_visibility="collapsed",
                                                         placeholder="Please enter your preferred response style",
                                                         value=response_style_input)
                    revisited_data["response_style_other"] = response_style_other

                # ROLE
                role_options = ["Assistant", "Mentor", "None", "Other"]
                role_index = None
                if "role" in revisited_data and revisited_data["role"] and revisited_data["role"] in role_options:
                    role_index = role_options.index(revisited_data["role"])
                role = st.radio(label="**Role that is taken on by the GenAI model**",
                                options=role_options,
                                key="role",
                                index=role_index,
                                horizontal=True)
                if role == "Other":
                    role_input = ""
                    if "role_other" in revisited_data and revisited_data["role_other"]:
                        role_input = revisited_data["role_other"]
                    role_other = st.text_input(label="Preferred role",
                                               label_visibility="collapsed",
                                               placeholder="Please enter the preferred role",
                                               value=role_input)
                    revisited_data["role_other"] = role_other

                # RESPONSE LENGTH
                response_length_options = ["Concise", "Short and comprehensive", "Detailed and comprehensive", "Others"]
                response_length_index = None
                if "response_length" in revisited_data and revisited_data["response_length"] and revisited_data["response_length"] in response_length_options:
                    response_length_index = response_length_options.index(revisited_data["response_length"])
                response_length = st.radio(label="**Response length**",
                                           options=response_length_options,
                                           key="response_length",
                                           horizontal=True,
                                           index=response_length_index)
                if response_length == "Other":
                    response_length_input = ""
                    if "response_length_other" in revisited_data and revisited_data["response_length_other"]:
                        response_length_input = revisited_data["response_length_other"]
                    response_length_other = st.text_input(label="Preferred response length",
                                                          label_visibility="collapsed",
                                                          placeholder="Please enter the preferred response length",
                                                          value=response_length_input)
                    revisited_data["response_length_other"] = response_length_other

                # CODE ADJUSTMENT
                code_adjustment_options = ["Provide the whole code", "Provide the whole code and highlight changed parts", "Only show adjusted code snippets", "Others"]
                code_adjustment_index = None
                if "code_adjustment" in revisited_data and revisited_data["code_adjustment"] and revisited_data["code_adjustment"] in code_adjustment_options:
                    code_adjustment_index = code_adjustment_options.index(revisited_data["code_adjustment"])
                code_adjustment = st.radio(label="**How do you prefer adjusted code to be presented?**",
                                           options=code_adjustment_options,
                                           key="code_adjustment",
                                           horizontal=True,
                                           index=code_adjustment_index)
                if code_adjustment == "Other":
                    code_adjustment_input = ""
                    if "code_adjustment_other" in revisited_data and revisited_data["code_adjustment_other"]:
                        code_adjustment_input = revisited_data["code_adjustment_other"]
                    code_adjustment_other = st.text_input(label="Preferred code adjustment style",
                                                          label_visibility="collapsed",
                                                          placeholder="Please enter the preferred code adjustment style",
                                                          value=code_adjustment_input)
                    revisited_data["code_adjustment_other"] = code_adjustment_other

                if st.button("Save settings"):
                    if "chosen_lang" not in revisited_data and chosen_language:
                        revisited_data["chosen_lang"] = chosen_language
                        revisited_data["chosen_lang_rep"] = chosen_language
                    elif "chosen_lang_rep" in revisited_data:
                        revisited_data["chosen_lang_rep"] = str(
                            revisited_data["chosen_lang_rep"]) + " -> " + chosen_language
                    revisited_data["chosen_lang"] = chosen_language
                    revisited_data["proficiency"] = proficiency
                    revisited_data["response_template"] = response_template
                    revisited_data["response_style"] = response_style
                    revisited_data["role"] = role
                    revisited_data["response_length"] = response_length
                    revisited_data["code_adjustment"] = code_adjustment

                    if response_template == "Other" and response_template_other:
                        response_template = response_template_other
                    if response_style == "Other" and response_style_other:
                        response_style = response_style_other
                    if role == "Other" and role_other:
                        role = role_other
                    if response_length == "Other" and response_length_other:
                        response_length = response_length_other
                    if code_adjustment == "Other" and code_adjustment_other:
                        code_adjustment = code_adjustment_other

                    st.session_state["system_prompt"] = get_prompted_assistant_without_task(
                        role=role,
                        proficiency_level=proficiency,
                        lang=chosen_language,
                        response_style=response_style,
                        response_template=response_template,
                        response_length=response_length,
                        code_correction_style=code_adjustment)

                    st.success("Your settings have been saved.", icon="✅")
                    write_json(REVISITED_FILE_PATH, participant_id, revisited_data)

        if response_template == "Other" and response_template_other:
            response_template = response_template_other
        if response_style == "Other" and response_style_other:
            response_style = response_style_other
        if role == "Other" and role_other:
            role = role_other
        if response_length == "Other" and response_length_other:
            response_length = response_length_other
        if code_adjustment == "Other" and code_adjustment_other:
            code_adjustment = code_adjustment_other
        if not proficiency:
            proficiency = "unknown proficiency level"

        initialize_session_state(assigned_group, role, chosen_language, proficiency, response_style, response_template, response_length, code_adjustment)
        chat_template = ChatPromptTemplate.from_messages(
            [
                ("system", st.session_state["system_prompt"]),
                ("placeholder", "{conversation}"),
                ("user", "{user_input}")
            ]
        )

        if "gen_messages" not in st.session_state:
            if "message_generate" not in revisited_data and st.session_state["initial_user_message"]:
                st.session_state["gen_messages"] = [{
                    "role": "assistant",
                    "content": st.session_state["initial_user_message"]
                }]
            elif not st.session_state["initial_user_message"] or st.session_state["initial_user_message"] == "":
                st.session_state["gen_messages"] = []
            else:
                st.session_state["gen_messages"] = revisited_data["message_generate"]

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

    with right:
        usage = st.text_input('Do you mind telling us what you used the GenAI tool for this time?', key="widget")
        if 'usage' not in st.session_state:
            st.session_state.usage = ''

        def submit():
            st.session_state.usage = st.session_state.widget
            if "usage" not in revisited_data:
                revisited_data["usage"] = usage
                revisited_data["usage_revisited"] = usage
            elif "usage_revisited" not in revisited_data:
                revisited_data["usage_revisited"] = usage
            else:
                revisited_data["usage_revisited"] = revisited_data["usage_revisited"] + " -> rev -> " + usage
            write_json(REVISITED_FILE_PATH, participant_id, revisited_data)
            st.session_state.widget = ''

        if st.button("Save", on_click=submit, type="primary"):
            st.success("Your answer has been saved. Thank you!", icon="✅")

if __name__ == "__main__":
    main()