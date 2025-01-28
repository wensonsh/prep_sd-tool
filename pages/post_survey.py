import json
from cProfile import label

import streamlit as st
from streamlit import columns

from pages.helper.navigation import forward
from pages.helper.navigation import get_header
from pages.helper.timer import get_current_time

st.set_page_config(page_title="Post-Experiment Survey", menu_items={'Get Help': 'mailto:wendi.shu@stud.tu-darmstadt.de'}, layout="wide")
# go to start if no session state
if 'participant_id' not in st.session_state:
    st.switch_page("app.py")
participant_id = st.session_state["participant_id"]

try:
    with open("data/participants/participant_" + participant_id + ".json", "r") as f:
        data = json.load(f)
except FileNotFoundError:
    st.switch_page("app.py")

get_header(4, "pages/task.py", True, False, data, participant_id)

st.title("Post Experiment Survey")
st.markdown(f"*Please fill out the following survey to help us understand your experience with the GenAI tool that was provided to you.*")

def validate_form(taif1, taif2, taif3, taif4, taif5, haif1, haif2, haif3, haif4, haif5, rq1, rq2, rq3, ltui1, ltui2, ltui3):
    errors = {}
    if not taif1 or not taif2 or not taif3 or not taif4 or not taif5 or not haif1 or not haif2 or not haif3 or not haif4 or not haif5 or not rq1 or not rq2 or not rq3 or not ltui1 or not ltui2 or not ltui3:
        errors["incomplete"] = "Please answer all questions."
    return errors

BASIC_LIKERT_OPTIONS = ["Strongly disagree", "Disagree", "Somewhat disagree", "Neutral", "Somewhat agree", "Agree", "Strongly agree"]

#TAIF
st.text("")
st.markdown("**The functionalities of the GenAI tool were very compatible with my task.**")
TAIF1_index = None
if "TAIF1" in data and data['TAIF1']:
    TAIF1_index = BASIC_LIKERT_OPTIONS.index(data["TAIF1"])
taif1 = st.radio(
    label="**The functionalities of the GenAI tool were very compatible with my task.**",
    label_visibility="collapsed",
    options=BASIC_LIKERT_OPTIONS,
    index=TAIF1_index,
    horizontal=True)

st.text("")
st.markdown("**The functionalities of the GenAI tool were very useful.**")
TAIF2_index = None
if "TAIF2" in data and data['TAIF2']:
    TAIF2_index = BASIC_LIKERT_OPTIONS.index(data["TAIF2"])
taif2 = st.radio(label="**The functionalities of the GenAI tool were very useful.**",
                 label_visibility="collapsed",
                 options=BASIC_LIKERT_OPTIONS,
                 index=TAIF2_index,
                 horizontal=True)

st.text("")
st.markdown("**The GenAI tool made the task easy.**")
TAIF3_index = None
if "TAIF3" in data and data['TAIF3']:
    TAIF3_index = BASIC_LIKERT_OPTIONS.index(data["TAIF3"])
taif3 = st.radio(label="**The GenAI tool made the task easy.**",
                 label_visibility="collapsed",
                 options=BASIC_LIKERT_OPTIONS,
                 index=TAIF3_index,
                 horizontal=True)

st.text("")
st.markdown("**Using the GenAI tool fitted the way I work.**")
TAIF4_index = None
if "TAIF4" in data and data['TAIF4']:
    TAIF4_index = BASIC_LIKERT_OPTIONS.index(data["TAIF4"])
taif4 = st.radio(label="**Using the GenAI tool fitted the way I work.**",
                 label_visibility="collapsed",
                 options=BASIC_LIKERT_OPTIONS,
                 index=TAIF4_index,
                 horizontal=True)

st.text("")
st.markdown("**In general, the functionalities of the GenAI tool were best fit to the task.**")
TAIF5_index = None
if "TAIF5" in data and data['TAIF5']:
    TAIF5_index = BASIC_LIKERT_OPTIONS.index(data["TAIF5"])
taif5 = st.radio(label="**In general, the functionalities of the GenAI tool were best fit to the task.**",
                 label_visibility="collapsed",
                 options=BASIC_LIKERT_OPTIONS,
                 index=TAIF5_index,
                 horizontal=True)

st.divider()
# HAIF
st.markdown("**The GenAI tool was very compatible with my needs for completing the task.**")
HAIF1_index = None
if "HAIF1" in data and data['HAIF1']:
    HAIF1_index = BASIC_LIKERT_OPTIONS.index(data["HAIF1"])
haif1 = st.radio(label="**The GenAI tool was very compatible with my needs for completing the task.**",
                 label_visibility="collapsed",
                 options=BASIC_LIKERT_OPTIONS,
                 index=HAIF1_index,
                 horizontal=True)

st.text("")
st.markdown("**The GenAI tool fitted my way of seeking assistance or information.**")
HAIF2_index = None
if "HAIF2" in data and data['HAIF2']:
    HAIF2_index = BASIC_LIKERT_OPTIONS.index(data["HAIF2"])
haif2 = st.radio(label="**The GenAI tool fitted my way of seeking assistance or information.**",
                 label_visibility="collapsed",
                 options=BASIC_LIKERT_OPTIONS,
                 index=HAIF2_index,
                 horizontal=True)

st.text("")
st.markdown("**The overall interaction with the GenAI tool aligned with my preferences.**")
HAIF3_index = None
if "HAIF3" in data and data['HAIF3']:
    HAIF3_index = BASIC_LIKERT_OPTIONS.index(data["HAIF3"])
haif3 = st.radio(label="**The overall interaction with the GenAI tool aligned with my preferences.**",
                 label_visibility="collapsed",
                 options=BASIC_LIKERT_OPTIONS,
                 index=HAIF3_index,
                 horizontal=True)

st.text("")
st.markdown("**The response style of the GenAI tool aligned with my preferences.**")
HAIF4_index = None
if "HAIF4" in data and data['HAIF4']:
    HAIF4_index = BASIC_LIKERT_OPTIONS.index(data["HAIF4"])
haif4 = st.radio(label="**The response style of the GenAI tool aligned with my preferences.**",
                 label_visibility="collapsed",
                 options=BASIC_LIKERT_OPTIONS,
                 index=HAIF4_index,
                 horizontal=True)

st.text("")
st.markdown("**I felt very frustrated during the interaction with the GenAI tool.**")
HAIF5_index = None
if "HAIF5" in data and data['HAIF5']:
    HAIF5_index = BASIC_LIKERT_OPTIONS.index(data["HAIF5"])
haif5 = st.radio(label="**I felt very frustrated during the interaction with the GenAI tool.**",
                 label_visibility="collapsed",
                 options=BASIC_LIKERT_OPTIONS,
                 index=HAIF5_index,
                 horizontal=True)

st.divider()
# RQ
st.markdown("**The GenAI tool helped me solve my task more effectively.**")
RQ1_index = None
if "RQ1" in data and data['RQ1']:
    RQ1_index = BASIC_LIKERT_OPTIONS.index(data["RQ1"])
rq1 = st.radio(label="**The GenAI tool helped me solve my task more effectively.**",
               label_visibility="collapsed",
               options=BASIC_LIKERT_OPTIONS,
               index=RQ1_index,
               horizontal=True)

st.text("")
st.markdown("**The GenAI tool had a positive impact on my ability to complete the task efficiently.**")
RQ2_index = None
if "RQ2" in data and data['RQ2']:
    RQ2_index = BASIC_LIKERT_OPTIONS.index(data["RQ2"])
rq2= st.radio(label="**The GenAI tool had a positive impact on my ability to complete the task efficiently.**",
              label_visibility="collapsed",
              options=BASIC_LIKERT_OPTIONS,
              index=RQ2_index,
              horizontal=True)

st.text("")
RQ3_index = None
if "RQ3" in data and data['RQ3']:
    RQ3_index = BASIC_LIKERT_OPTIONS.index(data["RQ3"])
rq3 = st.radio(label="**The GenAI tool was able to aid me in completing the task successfully.**", options=BASIC_LIKERT_OPTIONS, index=RQ3_index,
    horizontal=True)

st.divider()
#LTUI
st.markdown("**Given that I had access, I intend to continue using this GenAI tool rather than discontinue it.**")
LTUI1_index = None
if "LTUI1" in data and data['LTUI1']:
    LTUI1_index = BASIC_LIKERT_OPTIONS.index(data["LTUI1"])
ltui1 = st.radio(label="**Given that I had access, I intend to continue using this GenAI tool rather than discontinue it.**",
                 label_visibility="collapsed",
                 options=BASIC_LIKERT_OPTIONS,
                 index=LTUI1_index,
                 horizontal=True)

st.text("")
LTUI2_index = None
if "LTUI2" in data and data['LTUI2']:
    LTUI2_index = BASIC_LIKERT_OPTIONS.index(data["LTUI2"])
LTUI2_label_default = "I would prefer using this GenAI tool rather than using any alternative means."
LTUI2_label_tailored = "I would prefer using this GenAI tool with the given features rather than using any alternative means."
LTUI2_label = LTUI2_label_default
st.markdown(f"**{LTUI2_label}**")
if "assigned_group" in data and data["assigned_group"] == "group_tailored":
    LTUI2_label = LTUI2_label_tailored
ltui2 = st.radio(label=f"**{LTUI2_label}**",
                 label_visibility="collapsed",
                 options=BASIC_LIKERT_OPTIONS,
                 index=LTUI2_index,
                 horizontal=True)

st.text("")

LTUI3_index = None
LTUI3_label_default = "Given that I had access, I will not discontinue my use of this GenAI tool for software development tasks."
LTUI3_label_tailored = "Given that I had access, I will not discontinue my use of this GenAI tool with the given features for software development tasks."
LTUI3_label = LTUI3_label_default
if "assigned_group" in data and data["assigned_group"] == "group_tailored":
    LTUI3_label = LTUI3_label_tailored
if "LTUI3" in data and data['LTUI3']:
    LTUI3_index = BASIC_LIKERT_OPTIONS.index(data["LTUI3"])
st.markdown(f"**{LTUI3_label}**")
ltui3 = st.radio(label=f"**{LTUI3_label}**",
                 label_visibility="collapsed",
                 options=BASIC_LIKERT_OPTIONS,
                 index=LTUI3_index,
                 horizontal=True)


# Finish
st.text("")
st.text("")
st.text("")

st.divider()
left, middle, right = st.columns([12,8,4])
if right.button("Submit", key="submit", type="primary"):
    # Clear previous error messages
    errors = validate_form(taif1, taif2, taif3, taif4, taif5, haif1, haif2, haif3, haif4, haif5, rq1, rq2, rq3, ltui1, ltui2, ltui3)
    if errors:
        st.error("Please fill out all fields.")
    else:
        if taif1:
            data['TAIF1'] = taif1
        if taif2:
            data['TAIF2'] = taif2
        if taif3:
            data['TAIF3'] = taif3
        if taif4:
            data['TAIF4'] = taif4
        if taif5:
            data['TAIF5'] = taif5
        if haif1:
            data['HAIF1'] = haif1
        if haif2:
            data['HAIF2'] = haif2
        if haif3:
            data['HAIF3'] = haif3
        if haif4:
            data['HAIF4'] = haif4
        if haif5:
            data['HAIF5'] = haif5
        if rq1:
            data['RQ1'] = rq1
        if rq2:
            data['RQ2'] = rq2
        if rq3:
            data['RQ3'] = rq3
        if ltui1:
            data['LTUI1'] = ltui1
        if ltui2:
            data['LTUI2'] = ltui2
        if ltui3:
            data['LTUI3'] = ltui3
        data["next_page"] = "finish.py"
        data["exp_finished"] = True
        data["end_time_general"] = get_current_time()
        with open("data/participants/participant_" + participant_id + ".json", "w") as f:
            json.dump(data, f)
        forward("pages/finish.py", False, False, None, None)

