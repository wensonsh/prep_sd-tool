import json
from os import system

from streamlit import success
from streamlit_ace import st_ace

import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from pages.config.gen_ai_assistant import get_prompted_assistant, get_default_initial_user_message, get_temperature
from pages.helper.timer import initialize_timer, save_elapsed_time

st.set_page_config(page_title="Task", layout="wide", initial_sidebar_state="expanded", menu_items={'Get Help': 'mailto:wendi.shu@stud.tu-darmstadt.de'})
st.title("Collaborating with your GenAI assistant")
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
#initialize the timer
initialize_timer()

def forward():
    st.switch_page("pages/code_editor.py")
def back():
    st.switch_page("pages/experiment_explanation.py")

# go to start if no session state
if 'participant_id' not in st.session_state:
    st.switch_page("app.py")
id = st.session_state["participant_id"]

#open the file of the user
try:
    with open("data/participants/participant_" + id + ".json", "r") as f:
        data = json.load(f)
except FileNotFoundError:
    st.switch_page("app.py")

middle, right = st.columns([5, 2], gap= "small")

#@TODO
def resetUI():
    st.session_state["gen_messages"] = [{
        "role": "assistant",
        "content": st.session_state["initial_user_message"]
    }]
    st.rerun()


TASK = (f"Given two strings needle and haystack, return the index of the first occurrence of needle in haystack, or -1 if needle is not part of haystack.\n"
        f"Example 1: Input: haystack = 'sadbutsad', needle = 'sad'\n"
        f"Output: 0 \n"
        f"Explanation: 'sad' occurs at index 0 and 6.\n"
        f"The first occurrence is at index 0, so we return 0.\n"
        f"Example 2:\n"
        f"Input: haystack = 'leetcode', needle = 'leeto'\n"
        f"Output: -1\n"
        f"Explanation: 'leeto' did not occur in 'leetcode', so we return -1.\n"
        f"Constraints: 1 <= haystack.length, needle.length <= 104 haystack and needle consist of only lowercase English characters.\n"
        f"The template for the solution is: \n")
TASK_TEMPLATE = (
    f"def strStr(self, haystack, needle):\n"
    f"  #CODE")

with st.sidebar:
    # Main task description
    st.markdown("""
    ### Your Task
    Given two strings `needle` and `haystack`, return the index of the first occurrence of `needle` in `haystack`, or `-1` if `needle` is not part of `haystack`.
    """)

    # Examples in an expander
    with st.expander("📝 See Examples", expanded=True):

        st.markdown("""
        ### Example 1
        **Input:**
        ```
        haystack = 'sadbutsad'
        needle = 'sad'
        ```
        **Output:** `0`

        **Explanation:**  
        'sad' occurs at index 0 and 6.
        The first occurrence is at index 0, so we return 0.
        """)

        st.markdown("""
        ### Example 2
        **Input:**
        ```
        haystack = 'leetcode'
        needle = 'leeto'
        ```
        **Output:** `-1`

        **Explanation:**  
        'leeto' did not occur in 'leetcode', so we return -1.
        """)

    # Constraints in a special container
    st.info("""
    ### Additional Information
    - 1 <= haystack.length, needle.length <= 104
    - haystack and needle consist of only lowercase English characters
    """)

    # Optional: Add a code template section
    st.markdown("### Solution Template")

    # https://docs.streamlit.io/develop/api-reference/text/st.code
    code = TASK_TEMPLATE
    st.code(code, language="python", wrap_lines=True)
    st.divider()


    #@TODO: in variablen verschieben und in json reinschreiben
    perceived_task_difficulty_values = ["Easy", "Medium", "Hard"]
    perceived_task_difficulty_index = None
    if "perceived_task_difficulty" in data and data['perceived_task_difficulty']:
        perceived_task_difficulty_index = perceived_task_difficulty_values.index(data["perceived_task_difficulty"])
    perceived_task_difficulty = st.select_slider(
        label="I perceive this task as ...",
        options=perceived_task_difficulty_values
    )

with middle:
    # Load the system prompt, temperature, and intial usermsg from session state or set to default
    if ("system_prompt" not in st.session_state or
        st.session_state["system_prompt"] is None or
        st.session_state["system_prompt"] == ""):
        #@TODO

        st.session_state["system_prompt"] = get_prompted_assistant("Assistant", "Expert", "bullet points", "C", "concise", TASK+TASK_TEMPLATE)


    if "temperature" not in st.session_state:
        st.session_state["temperature"] = get_temperature()

    if "initial_user_message" not in st.session_state:
        st.session_state["initial_user_message"] = get_default_initial_user_message()

    chat_template = ChatPromptTemplate.from_messages(
        [
            ("system", st.session_state.get("system_prompt", get_prompted_assistant("Assistant", "Expert", "bullet points", "C", "concise", TASK))),
            ("placeholder", "{conversation}"),
            ("user", "{user_input}")
        ]
    )

    # Initialize chat history
    if "gen_messages" not in st.session_state:
        if "message_generate" not in data:
            st.session_state["gen_messages"] = [{
                "role": "assistant",
                "content": st.session_state["initial_user_message"]
            }]
        else:
            st.session_state["gen_messages"] = data["message_generate"]



    messages_container = st.container(height=650)

    # Display chat messages from history on app rerun
    for msg in st.session_state.gen_messages:
        messages_container.chat_message(msg["role"]).write(msg["content"], unsafe_allow_html=True)

    # React to user input and check if it's not None
    if input_text := st.chat_input():
        # Display user message in chat message container
        messages_container.chat_message("user").write(input_text)
        llm = ChatOpenAI(
            model="gpt-4o",
            temperature=get_temperature(),
            openai_api_key=OPENAI_API_KEY
        )

        # apply template for prompt engineering
        prompt = chat_template.format_messages(user_input=input_text, conversation=st.session_state.gen_messages)

        try:
            response = llm.invoke(prompt)
            msg = response.content
        except Exception as e:
            msg = f"Error: {str(e)}"

        # Add user message to chat history
        st.session_state.gen_messages.append({"role": "user", "content": input_text})

        # Add assistant message to chat history
        st.session_state.gen_messages.append({"role": "assistant", "content": msg})
        messages_container.chat_message("assistant").write(msg)

        if "live_message_generate" in data:
            data["live_message_generate"] = str(data["live_message_generate"]) + " NEW ANSWER    =>       " + str(
                st.session_state.gen_messages)
        else:
            data["live_message_generate"] = str(st.session_state.gen_messages)
        with open("data/participants/participant_" + id + ".json", "w") as f:
            json.dump(data, f)


with right:
    st.write("How much does the following sentence apply to you?")
    # LLM usage private
    actual_usage_preference_values = ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]
    actual_usage_preference_index = None
    if "actual_usage_preference" in data and data['actual_usage_preference']:
        actual_usage_preference_index = actual_usage_preference_values.index(data["actual_usage_preference"])

    actual_usage_preference = st.select_slider(
        label="If I faced a task like this at work, I would actually NOT use the GenAI tool.",
        options=actual_usage_preference_values
    )

    st.divider()

    # # SOLUTION
    # if "solution_generate" in data:
    #     text = st.text_area("Your solution", value=data["solution_generate"], height=650)
    # else:
    #     text = st.text_area("Your solution", height=650)

    solution = st_ace(
        placeholder="Enter your Python code here",
        language='python',
        theme='monokai',
        height=300,
        keybinding='vscode',
        show_gutter=True,
        auto_update=True
    )
    # If you want to execute the code
    if st.button("Run Code"):
        try:
            exec(solution)
            print("success")
        except Exception as e:
            st.error(f"Error: {str(e)}")

    if st.button("Submit", type="primary", use_container_width=True):
        #if text is None or len(text) == 0:
        if solution is None or len(solution) == 0:
            st.error("Your solution is empty. Please submit a solution.")
        else:
            # stop the timer and save the time in the json file
            st.session_state.timer.stop()
            elapsed_time = st.session_state.timer.get_elapsed_time_in_minutes()
            save_elapsed_time(id, elapsed_time)
            # save the messages
            # data["message_generate"] = st.session_state.gen_messages
            if "live_solution_generate" in data and data["live_solution_generate"] != str(solution):
                data["live_solution_generate"] = str(
                    data["live_solution_generate"]) + " NEW ANSWER    =>           " + str(solution)
            else:
                data["live_solution_generate"] = str(solution)
            data["solution_generate"] = str(solution)


            with open("data/participants/participant_" + id + ".json", "w") as f:
                json.dump(data, f)
            st.switch_page("pages/post_survey.py")
if st.button("Back"):
    back()
