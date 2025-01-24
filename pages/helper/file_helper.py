
import json

import streamlit as st



def open_json(path, participant_id):
    try:
        with open(path + "participant_" + participant_id + ".json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return st.switch_page("app.py")

def write_json(participant_id, data):
    with open("data/participants/participant_" + participant_id + ".json", "w") as f:
        json.dump(data, f)