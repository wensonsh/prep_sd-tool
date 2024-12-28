import streamlit as st

#@TODO
def forward():
    st.switch_page("pages/code_editor.py")
def back():
    st.switch_page("pages/persona_survey.py")

#@TODO: make a swtich button or something like that out of this:
st.write("For this task, I would actually prefer not to use the GenAI tool and solve it on my own. "
         "// If I faced a task like this at work, I would purpoesely not use the GenAI tool")

# https://docs.streamlit.io/develop/api-reference/text/st.code
code = '''def hello():
    print("Hello, this is a test!")'''
st.code(code, language="python")


if st.button("Back"):
    back()