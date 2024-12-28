import json
import os

import streamlit as st

from utils import generate_random_id

# Initialize session state for navigation and participant ID
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "welcome"
if "participant_id" not in st.session_state:
    st.session_state["participant_id"] = None

# Navigation function
def go_to_page(page_name):
    st.switch_page(page_name)

# Welcome Page
if st.session_state["current_page"] == "welcome":
    st.title("Welcome to the Generative AI Experiment")

    st.write("""
    This experiment explores the effects of persona-driven and task-specific manipulation of generative AI tools in software development.
    Please follow the instructions on each page to participate.
    """)
    st.write("""Before you start: The experiment works best with a total of two monitors. You will be asked to use a GenAI tool in 
    this study's web application (will be introduced to you later on). Because you will have an IDE tbd""")


    st.empty()

    st.write("Here for the first time? Please click the Start button")

    if st.button("Start"):
        # Generate a new Participant ID and initialize their data
        participant_id = generate_random_id()
        st.session_state["participant_id"] = participant_id
        data = {
            "id": participant_id
        }
        if not os.path.exists("data/user_" + participant_id + ".json"):
            with open("data/user_" + participant_id + ".json", "w") as file:
                json.dump(data, file)
        st.switch_page("pages/init_survey.py")



    st.write("Already been here?")
    input_id = st.text_input("Enter your Participant ID to continue:")
    if st.button("Continue →"):
        if not os.path.exists("data/user_" + input_id + ".json"):
            st.warning("ID not found. Please try again.")
        else:
            try:
                with open("data/user_" + input_id + ".json", "r") as f:
                    data = json.load(f)
            except FileNotFoundError:
                st.switch_page("app.py")

            if "next_page" in data:
                next_page = data["next_page"]
            else:
                next_page = "init_survey.py"

            st.session_state["participant_id"] = input_id
            st.switch_page("pages/" + next_page)

# Demographic Survey Page
elif st.session_state["current_page"] == "init_survey":
    pass

# Persona Survey Page
elif st.session_state["current_page"] == "persona_survey":
    pass

# gen_ai_tool Page (Placeholder)
elif st.session_state["current_page"] == "gen_ai_tool":
    st.title("gen_ai_tool Interaction")
    st.write("This is where the gen_ai_tool interaction will be implemented.")


footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: #8a4bff;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: #fafafa;
color: #31333F;
text-align: center;
box-shadow: 0px -0.5px 4px #c5c5c5;
}
</style>
<div class="footer">
<p>In case you've got any questions please contact <a style='display: block; text-align: center;' href="mailto:wendi.shu@stud.tu-darmstadt.de" target="_blank">wendi.shu@stud.tu-darmstadt.de</a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)