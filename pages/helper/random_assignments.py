import json
import random
from pathlib import Path

GROUP_DATA_FILE = 'data/groups.json'
TASK_DATA_FILE = 'data/tasks.json'

# Initialize group data if it doesn't exist
def initialize_group_data():
    if not Path(GROUP_DATA_FILE).exists():
        with open(GROUP_DATA_FILE, 'w') as f:
            json.dump([], f)

# Load group data
def load_group_data():
    with open(GROUP_DATA_FILE, 'r') as f:
        return json.load(f)

# Save group data
def save_group_data(data):
    with open(GROUP_DATA_FILE, 'w') as f:
        json.dump(data, f)

# Initialize task data if it doesn't exist
def initialize_task_data():
    if not Path(TASK_DATA_FILE).exists():
        with open(TASK_DATA_FILE, 'w') as f:
            json.dump({"write_easy": [], "write_medium": [], "write_hard": []}, f)

# Load task data
def load_task_data():
    with open(TASK_DATA_FILE, 'r') as f:
        return json.load(f)

# Save task data
def save_task_data(data):
    with open(TASK_DATA_FILE, 'w') as f:
        json.dump(data, f)

def assign_to_group(participant_id):
    """
    Assign a participant to a group and task ensuring balance within each group.

    :param participant_id: str - identifier of the participant
    """
    initialize_group_data()
    group_data = load_group_data()

    # Check if the participant is already assigned
    for participant in group_data:
        if participant['id'] == participant_id:
            return participant['group']

    # Count participants in each group
    count_default = sum(1 for p in group_data if p['group'] == 'group_default')
    count_tailored = sum(1 for p in group_data if p['group'] == 'group_tailored')

    # Determine the group with fewer participants
    if count_default < count_tailored:
        assigned_group = 'group_default'
    elif count_tailored < count_default:
        assigned_group = 'group_tailored'
    else:
        assigned_group = random.choice(['group_default', 'group_tailored'])

    # Count tasks within the assigned group
    group_tasks = [p['task'] for p in group_data if p['group'] == assigned_group]
    task_counts = {
        "easy": group_tasks.count("easy"),
        "medium": group_tasks.count("medium"),
        "hard": group_tasks.count("hard")
    }
    assigned_task = min(task_counts, key=task_counts.get)

    # Assign the participant to the group and task
    group_data.append({'id': participant_id, 'group': assigned_group, 'task': assigned_task})
    save_group_data(group_data)

    # Update participant's JSON file with group and task
    participant_file = f'data/participants/participant_{participant_id}.json'
    with open(participant_file, 'r') as f:
        participant_data = json.load(f)
    participant_data['assigned_group'] = assigned_group
    participant_data['assigned_task'] = assigned_task
    with open(participant_file, 'w') as f:
        json.dump(participant_data, f)

    return assigned_group