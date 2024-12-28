import streamlit as st


def prompt_builder(proficiency_level, response_length, bla, blaa):
    basic_prompt = ("You are an assistant/mentor for a " + proficiency_level + " software developer. "
                     "Please explain everything as comprehensible as possible in case they have any questions."
                     "Also mind the following adjustments for your responses: ")
