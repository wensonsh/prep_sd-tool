import json
import os

import streamlit as st

from utils import generate_random_id

st.session_state.clear()
st.set_page_config(page_title="Welcome", menu_items={'Get Help': 'mailto:wendi.shu@stud.tu-darmstadt.de'})
# Initialize session state for navigation and participant ID
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "welcome"
if "participant_id" not in st.session_state:
    st.session_state["participant_id"] = None

# create directory for participant data if it doesn't exist
directory = "data/participants/"
if not os.path.exists(directory):
    os.makedirs(directory)

# Navigation function
def go_to_page(page_name):
    st.switch_page(page_name)

# Welcome Page
if st.session_state["current_page"] == "welcome":
    st.title("Welcome to the Generative AI Experiment")

    st.write("""
    This experiment explores the use of Generative AI (GenAI) tools for software development.
    You will be guided through this experiment. The experiment should take a maximum of 30 minutes. 
    Please make sure that you have a stable internet connection and that you are doing this experiment on a PC.  
    \n\n If you face any problems or in case you've got questions, feel free to contact wendi.shu@stud.tu-darmstadt.de.
    """)

    st.empty()

    st.write("Please click the button below to start the experiment.")

    # START
    if st.button("Start"):
        # generate a new Participant ID and initialize their data
        participant_id = generate_random_id()
        while os.path.exists("data/participants/participant_" + participant_id + ".json"):
            # make sure that the id doesn't exist already
            participant_id = generate_random_id()
        st.session_state["participant_id"] = participant_id
        data = {
            "id": participant_id
        }
        if not os.path.exists("data/participants/participant_" + participant_id + ".json"):
            with open("data/participants/participant_" + participant_id + ".json", "w") as file:
                json.dump(data, file)
        st.switch_page("pages/init_survey.py")

    # CONTINUE
    st.divider()
    st.write("If you've already been here and want to revisit the tool, please enter your participant ID and click the 'Continue →' button.")
    input_id = st.text_input("Enter your Participant ID to continue:")
    if st.button("Continue →"):
        if not os.path.exists("data/participants/participant_" + input_id + ".json"):
            st.warning("ID not found. Please try again.")
        else:
            try:
                with open("data/participants/participant_" + input_id + ".json", "r") as f:
                    data = json.load(f)
            except FileNotFoundError:
                st.switch_page("app.py")

            next_page = "gen_ai_tool.py"

            st.session_state["participant_id"] = input_id
            st.switch_page("pages/" + next_page)

# Demographic Survey Page
elif st.session_state["current_page"] == "init_survey":
    pass

# Persona Survey Page
elif st.session_state["current_page"] == "persona_survey":
    pass

# Explanation Page
elif st.session_state["current_page"] == "procedure":
    pass

# gen_ai_tool Page
elif st.session_state["current_page"] == "gen_ai_tool":
    pass