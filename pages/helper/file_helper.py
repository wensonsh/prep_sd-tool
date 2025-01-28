import json
import os

import streamlit as st


def open_json(path, participant_id):
    data = {
        "id": participant_id
    }
    if not os.path.exists(path):
        os.makedirs(path)

    try:
        if not os.path.exists(path + "participant_" + participant_id + ".json"):
            with open(path + "participant_" + participant_id + ".json", "w") as file:
                json.dump(data, file)
        with open(path + "participant_" + participant_id + ".json", "r") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return st.switch_page("app.py")


def write_json(path, participant_id, data):
    with open(path + "participant_" + participant_id + ".json", "w") as f:
        json.dump(data, f)