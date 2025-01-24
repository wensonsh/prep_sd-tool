import json
import os
import random
import string

# Directory to store participant data
PARTICIPANT_DIR = "data"
os.makedirs(PARTICIPANT_DIR, exist_ok=True)

# Utility functions for saving/loading participant data
def save_participant_data(participant_id, data):
    file_path = os.path.join(PARTICIPANT_DIR, f"{participant_id}.json")
    with open(file_path, "w") as f:
        json.dump(data, f)

def load_participant_data(participant_id):
    file_path = os.path.join(PARTICIPANT_DIR, f"{participant_id}.json")
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return None

# Generate a random Participant ID
def generate_random_id(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
