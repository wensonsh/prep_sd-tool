import json
from typing import List
import streamlit as st
from itertools import permutations

# Simulated JSON content


# Test cases
test_cases = [
    {"input": ["ab", "ba"], "expected_output": [[1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]},
    {"input": ["aa","ac"], "expected_output": [[2,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]},
    {"input": ["aa","bb","cc"], "expected_output": [[2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]},
]

def test_solution_hard(solution_code: str):
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
        expected_output = test_case["expected_output"]

        # Call the supersequences method
        result = solution_instance.supersequences(input_data)

        # Check if the result matches the expected output
        # Check if the result matches the expected output
        if result == expected_output:
            st.success(
                f"Test case {i + 1} with input {input_data} passed.\n\nExpected {expected_output}, got {result}.",
                icon="✅")
        else:
            st.warning(
                f"Test case {i + 1} with input {input_data} failed. \n\nExpected {expected_output}, got {result}.",
                icon="❌")
