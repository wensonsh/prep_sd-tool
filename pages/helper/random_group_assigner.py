import json

import streamlit as st
from pathlib import Path

from pages.persona_survey import non_familiar_programming_lang, non_familiar_programming_lang_exp

#@todo
#todo: write a fallback
GROUP_DATA_FILE = "data/groups.json"
# Initialize group data if it doesn't exist
def initialize_group_data():
    if not Path(GROUP_DATA_FILE).exists():
        with open(GROUP_DATA_FILE, "w") as f:
            json.dump({"group_a": [], "group_b": []}, f)

# Load group data
def load_group_data():
    with open(GROUP_DATA_FILE, "r") as f:
        return json.load(f)

# Save group data
def save_group_data(data):
    with open(GROUP_DATA_FILE, "w") as f:
        json.dump(data, f)

def assign_to_group(participant_id, skill_level):
    """
    Assign a participant to Group A or Group B based on the given skill level.

    :param participant_id: str - identifier of the participant
    :param skill_level: str - one of ["Beginner, "Intermediate", "Advanced", "Expert"]
    """
    initialize_group_data()
    group_data = load_group_data()

    #get current group participants
    group_a = group_data["group_a"]
    group_b = group_data["group_b"]
    # Check if the participant is already in a group
    for participant in group_a:
        if participant["id"] == participant_id:
            return "Already in Group A"

    for participant in group_b:
        if participant["id"] == participant_id:
            return "Already in Group B"
    # count
    count_a = sum(1 for p in group_a if p["skill_level"] == skill_level)
    count_b = sum(1 for p in group_b if p["skill_level"] == skill_level)
    if count_b == 0 or count_b < count_a:
        group_b.append({"id": participant_id, "skill_level": skill_level})
        assigned_group = "Group B"
    else:
        group_a.append({"id": participant_id, "skill_level": skill_level})
        assigned_group = "Group A"

    group_data["group_a"] = group_a
    group_data["group_b"] = group_b
    save_group_data(group_data)
    print(assigned_group)
    return assigned_group
