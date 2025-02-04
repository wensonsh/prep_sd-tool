import streamlit as st
from typing import List

# Test cases
test_cases = [
    {'input': [10, 10, 3, 7, 6], 'expected_output': 4},
    {'input': [1, 2, 2], 'expected_output': 0},
    {'input': [2, 4, 6, 8], 'expected_output': 3},
]

def test_solution_easy(solution_code: str):
    # Strip leading/trailing whitespace from the solution code
    solution_code = solution_code.strip()

    # Define a dictionary to hold the local variables for exec
    local_vars = {}

    # Execute the solution code
    exec(solution_code, globals(), local_vars)

    # Check if the Solution class is defined
    if 'Solution' not in local_vars:
        raise ValueError("Solution class not found in the provided code.")

    # Create an instance of the Solution class
    solution_instance = local_vars['Solution']()

    # Run the test cases
    for i, test_case in enumerate(test_cases):
        input_data = test_case['input']
        expected_output = test_case['expected_output']

        # Call the countPartitions method
        result = solution_instance.countPartitions(input_data)

        # Check if the result matches the expected output
        if result == expected_output:
            st.success(f"Test case {i + 1} with input {input_data} passed.\n\nExpected {expected_output}, got {result}.", icon="✅")
        else:
            st.warning(f"Test case {i + 1} with input {input_data} failed. \n\nExpected {expected_output}, got {result}.", icon="❌")

