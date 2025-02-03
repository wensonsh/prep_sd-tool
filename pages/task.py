import json
import random

import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from streamlit.components.v1 import html
from streamlit_ace import st_ace

from pages.config.gen_ai_assistant import get_prompted_assistant, get_default_initial_user_message, get_temperature
from pages.helper.navigation import forward, home, get_header
from pages.tasks.task_template import display_task, get_task_for_prompt, get_task_template_for_prompt

# Constants
DATA_PATH = "data/participants/"
PAGE_TITLE = "Collaborating with your GenAI tool"
ERROR_MSG = "Your solution is empty. Please submit a solution."
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# JavaScript Timer
timer_script = """
<script>
    let startTime;  // The time when the timer starts
    let elapsedTime = 0;  // Time elapsed in milliseconds
    let timerInterval;  // Interval for updating the timer
    let isPaused = false;  // Tracks whether the timer is paused

    function startTimer() {
        if (!startTime) {
            startTime = Date.now();  // Record the start time
        } else {
            startTime = Date.now() - elapsedTime;  // Adjust for paused duration
        }
        isPaused = false;
        document.getElementById('pause-btn').style.display = 'inline-block';
        document.getElementById('resume-btn').style.display = 'none';

        // Start updating the timer every second
        timerInterval = setInterval(updateTimer, 1000);

        // Set a timeout for the popup after 15 minutes (900000 ms)
        setTimeout(function() {
            alert("⏰ 15 minutes have passed! Please consider submitting your solution soon.");
        }, 900000); // 900000 ms = 15 minutes
    }

    function pauseTimer() {
        if (!isPaused) {
            clearInterval(timerInterval);  // Stop updating the timer
            elapsedTime = Date.now() - startTime;  // Calculate elapsed time so far
            isPaused = true;
            document.getElementById('pause-btn').style.display = 'none';
            document.getElementById('resume-btn').style.display = 'inline-block';
        }
    }

    function resumeTimer() {
        if (isPaused) {
            startTimer();  // Resume the timer
        }
    }

    function updateTimer() {
        const currentTime = Date.now();
        const totalElapsedTime = currentTime - startTime;
        const seconds = Math.floor((totalElapsedTime / 1000) % 60);
        const minutes = Math.floor((totalElapsedTime / (1000 * 60)) % 60);

        document.getElementById('timer-display').textContent =
            `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;

        // Save elapsed time to a hidden input field for Python access
        document.getElementById('elapsed-time').value = `${minutes}:${seconds}`;
    }

    document.addEventListener('DOMContentLoaded', () => {
        startTimer();  // Automatically start the timer when the page loads
        document.getElementById('pause-btn').addEventListener('click', pauseTimer);
        document.getElementById('resume-btn').addEventListener('click', resumeTimer);
    });
</script>

<div style="font-size: 24px; font-weight: bold; margin-bottom: 10px;">
    Elapsed Time: <span id="timer-display">00:00</span>
</div>
<input type="hidden" id="elapsed-time" name="elapsed-time" value="00:00">
<button id="pause-btn" style="background-color: #2A2F33; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer;">⏸️ Pause</button>
<button id="resume-btn" style="background-color: #397AB3; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; display: none;">▶️ Resume</button>
"""

def clear_gen_messages():
    st.session_state["gen_messages"] = []

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

def update_system_prompt():
    st.session_state["user_system_prompt"] = st.session_state["system_prompt_text_area"]


def main():
    st.set_page_config(page_title=PAGE_TITLE, layout="wide", initial_sidebar_state="expanded", menu_items={'Get Help': 'mailto:wendi.shu@stud.tu-darmstadt.de'})

    if 'participant_id' not in st.session_state:
        home()

    participant_id = st.session_state["participant_id"]
    data = load_participant_data(participant_id)
    st.session_state["user_system_prompt"] = ""

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
            task = get_task_for_prompt(task_difficulty) + "\n\n" + get_task_template_for_prompt(difficulty=task_difficulty,
                                                                                                chosen_language=chosen_language)
            if "session_state_initialized" in st.session_state and st.session_state["session_state_initialized"]:
                st.session_state["session_state_initialized"] = True
            else:
                st.session_state["session_state_initialized"] = False

            with st.expander("**Interaction and Response Settings**", expanded=False):
                if st.button("Reset settings",
                             type="tertiary",
                             help="This will reset your interaction and response settings to default",
                             icon=":material/reset_settings:"):
                    st.session_state["system_prompt"] = get_prompted_assistant(
                        role=None,
                        proficiency_level=proficiency_in_chosen_lang,
                        lang=chosen_language,
                        response_style=None,
                        response_template=None,
                        response_length=None,
                        code_correction_style=None,
                        task = task)
                    st.success("Your settings have been reset.", icon="⏮️")
                    data["role"] = None
                    data["response_style"] = None
                    data["response_template"] = None
                    data["response_length"] = None
                    data["code_adjustment"] = None
                    save_participant_data(participant_id, data)

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
                    st.success("Settings updated successfully.")

            button_save_prompt_clicked = False
            if "user_system_prompt" in st.session_state and st.session_state["user_system_prompt"]:
                user_system_prompt_value = st.session_state["user_system_prompt"]
            else:
                user_system_prompt_value = st.session_state["system_prompt"]

            with st.expander("**Prompt Editor**", expanded=False):
                user_sys_prompt = st.text_area("Current System Prompt for the GenAI model",
                                               value=user_system_prompt_value,
                                               height=400,
                                               key="system_prompt_text_area",
                                               on_change=update_system_prompt)
                if st.button("Save prompt"):
                    button_save_prompt_clicked = True
                    st.session_state["system_prompt"] = user_sys_prompt
                    data["user_system_prompt_changed_count"] = data.get("user_system_prompt_changed_count", 0) + 1
                    if "user_system_prompt" in data and data["user_system_prompt"]:
                        data["user_system_prompt"] = data["user_system_prompt"] + "   ->  " + user_sys_prompt
                    else:
                        data["user_system_prompt"] = user_sys_prompt
                    save_participant_data(participant_id, data)
                    st.success("Prompt updated successfully.")

            if st.session_state["user_system_prompt"] and button_save_prompt_clicked:
                # only if save prompt button was clicked, save and update the prompt for the model
                st.session_state["system_prompt"] = st.session_state["user_system_prompt"]


        if "session_state_initialized" not in st.session_state or not st.session_state["session_state_initialized"]:
            initialize_session_state(group=assigned_group,
                                     difficulty=task_difficulty,
                                     selected_role=role,
                                     participant_proficiency_level=proficiency_in_chosen_lang,
                                     selected_response_style=response_style,
                                     selected_response_template=response_template,
                                     selected_response_length=response_length,
                                     selected_code_correction_style=code_adjustment,
                                     lang=chosen_language)
            st.session_state["session_state_initialized"] = True

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
                clear_gen_messages()
            else:
                st.session_state["gen_messages"] = data["message_generate"]

            # Update live_message_generate when a new conversation is started
            data["live_message_generate"] = str(st.session_state["gen_messages"])
            save_participant_data(participant_id, data)

        if data["assigned_group"] == "group_tailored":
            with st.expander(":gray[Click here to adjust the chat's and the solution's container height [px]]",
                             expanded=False):
                container_height = st.slider(
                    label="Choose container height in pixels",
                    label_visibility="hidden",
                    min_value=200,
                    max_value=800,
                    value=400,
                    on_change=lambda: (
                        data.update(
                            {"container_height_adjusted_count": data.get("container_height_adjusted_count", 0) + 1}),
                        save_participant_data(participant_id, data)
                    )
                )

                save_participant_data(participant_id, data)
        else:
            container_height = 500
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

        st.divider()
        col_reset_button1, col_reset_button2 = st.columns([2, 1])
        if data["assigned_group"] == "group_tailored":
            with col_reset_button1:
                if st.button(label="Reset Conversation (with initial message)",
                             help="This will start the conversation but keep the initial message",
                             icon=":material/undo:"):
                    # save messages in data
                    if "live_message_generate" in data:
                        data["live_message_generate"] += " " + str(st.session_state.gen_messages)
                    else:
                        data["live_message_generate"] = str(st.session_state.gen_messages)
                    save_participant_data(participant_id, data)

                    st.session_state["gen_messages"] = [{
                        "role": "assistant",
                        "content": st.session_state["initial_user_message"]
                    }]
                    if "live_message_generate" in data:
                        data["live_message_generate"] += " NEW ANSWER    =>       "
                    else:
                        data["live_message_generate"] = ""
                    data["reset_conversation_count"] = data.get("reset_conversation_count", 0) + 1
                    save_participant_data(participant_id, data)
                    st.rerun()
            with col_reset_button2:
                if st.button(label="Clear all messages",
                             help="This will clear all messages in the chat and start a new conversation",
                             icon=":material/delete:"):
                    # save messages in data
                    if "live_message_generate" in data:
                        data["live_message_generate"] += " " + str(st.session_state.gen_messages)
                    else:
                        data["live_message_generate"] = str(st.session_state.gen_messages)
                    save_participant_data(participant_id, data)

                    clear_gen_messages()
                    if "live_message_generate" in data:
                        data["live_message_generate"] += " NEW ANSWER    =>       "
                    else:
                        data["live_message_generate"] = ""
                    data["clear_all_messages_count"] = data.get("clear_all_messages_count", 0) + 1
                    save_participant_data(participant_id, data)
                    st.rerun()
        else:
            if st.button("Reset and start new conversation",
                         help="This will clear all messages in the chat and start a new conversation",
                         icon=":material/restart_alt:"):
                # save messages in data
                if "live_message_generate" in data:
                    data["live_message_generate"] += " " + str(st.session_state.gen_messages)
                else:
                    data["live_message_generate"] = str(st.session_state.gen_messages)
                save_participant_data(participant_id, data)

                clear_gen_messages()
                if "live_message_generate" in data:
                    data["live_message_generate"] += " NEW ANSWER    =>       "
                else:
                    data["live_message_generate"] = ""
                data["clear_all_messages_count"] = data.get("clear_all_messages_count", 0) + 1
                save_participant_data(participant_id, data)
                st.rerun()

    with right:
        # TIMER
        show_timer = st.toggle("Show Timer", value=True)
        if show_timer:
            st.info(
                "A timer has been added to help you monitor the time spent on this task, as the whole experiment is designed to be completed within 30 minutes. However, please do not worry if you cannot submit a complete or correct solution within this timeframe.")
            html(timer_script, height=100)

        st.markdown(f"#### Your Solution:")
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
            perceived_task_difficulty_index = None
            if "perceived_task_difficulty" in data and data['perceived_task_difficulty']:
                perceived_task_difficulty_index = perceived_task_difficulty_values.index(data['perceived_task_difficulty'])
            perceived_task_difficulty = st.radio(
                label="I perceived this task as ...",
                options=perceived_task_difficulty_values,
                index=perceived_task_difficulty_index,
                horizontal=True)
            data["perceived_task_difficulty"] = perceived_task_difficulty

        if st.button("Submit and continue →", type="primary", use_container_width=True):
            if solution is None or len(solution) == 0:
                st.error(ERROR_MSG)
            else:
                # save messages in data
                if "live_message_generate" in data:
                    data["live_message_generate"] += " " + str(st.session_state.gen_messages)
                else:
                    data["live_message_generate"] = str(st.session_state.gen_messages)
                # save solution in data
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