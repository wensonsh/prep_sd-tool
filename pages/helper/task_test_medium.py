import streamlit as st
from typing import List
from collections import defaultdict

# Simulated JSON content


# Test cases
test_cases = [
    {"input": [1,2,3,4,5,6], "k": 1, "expected_output": 2},
    {"input": [10,2,3,4,5,5,4,3,2,2], "k": 10, "expected_output": 4},
]

def test_solution_medium(solution_code: str):
    # Strip leading/trailing whitespace from the solution code
    solution_code = solution_code.strip()

    # Define a dictionary to hold the local variables for exec
    local_vars = {}

    # Execute the solution code
    exec(solution_code, globals(), local_vars)

    # Check if the Solution class is defined
    if "Solution" not in local_vars:
        raise ValueError("Solution class not found in the provided code.")

    # Create an instance of the Solution class
    solution_instance = local_vars["Solution"]()

    # Run the test cases
    for i, test_case in enumerate(test_cases):
        input_data = test_case["input"]
        input_data_k = test_case["k"]
        expected_output = test_case["expected_output"]

        # Call the maxFrequency method
        result = solution_instance.maxFrequency(input_data, input_data_k)

        # Check if the result matches the expected output
        # Check if the result matches the expected output
        if result == expected_output:
            st.success(
                f"Test case {i + 1} with input {input_data} and k={input_data_k}passed.\n\nExpected {expected_output}, got {result}.",
                icon="✅")
        else:
            st.warning(
                f"Test case {i + 1} with input {input_data} and k={input_data_k} failed. \n\nExpected {expected_output}, got {result}.",
                icon="❌")
