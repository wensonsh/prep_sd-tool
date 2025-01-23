import streamlit as st


DEFAULT_INITIAL_USER_MESSAGE = """Welcome, 
    I'm here to assist you in completing the task you were given on {}. Feel free to ask me anything about the task. 
    <br>
    Let's start! 🚀
    """

def show_messages_container():
    messages_container = st.container(height=650)
    # Display chat messages from history on app rerun
    # for msg in st.session_state.gen_messages:
    #     messages_container.chat_message(msg["role"]).write(msg["content"], unsafe_allow_html=True)

    # React to user input and check if it's not None
    if input_text := st.chat_input():
        # Display user message in chat message container
        messages_container.chat_message("user").write(input_text)
        # llm = ChatOpenAI(
        #     model="gpt-4o",
        #     temperature=st.session_state["temperature"],
        #     openai_api_key=OPENAI_API_KEY
        # )
        #
        # # apply template for prompt engineering
        # prompt = chat_template.format_messages(user_input=input_text, conversation=st.session_state.gen_messages)
        #
        # try:
        #     response = llm.invoke(prompt)
        #     msg = response.content
        # except Exception as e:
        #     msg = f"Error: {str(e)}"
        #
        # # Add user message to chat history
        # st.session_state.gen_messages.append({"role": "user", "content": input_text})
        #
        # # Add assistant message to chat history
        # st.session_state.gen_messages.append({"role": "assistant", "content": msg})
        # messages_container.chat_message("assistant").write(msg)
        #
        # if "live_message_generate" in data:
        #     data["live_message_generate"] = str(data["live_message_generate"]) + " NEW ANSWER    =>       " + str(
        #         st.session_state.gen_messages)
        # else:
        #     data["live_message_generate"] = str(st.session_state.gen_messages)
        # with open("data/participants/participant_" + id + ".json", "w") as f:
        #     json.dump(data, f)
#
# def show_sidebar():
#     with st.sidebar:
#         st.header("Admin Panel")
#         with st.form(key='admin_settings_form'):
#
#             temperature = st.slider("Set Temperature", min_value=0.0, max_value=1.0,
#                                     value=0.7, step=0.1)
#
#             st.divider()
#
#             system_prompt = st.text_area("System Prompt", value="st.session_state['system_prompt']",
#                                          key="system_prompt_input")
#
#             st.divider()
#             initial_user_message = st.text_area("Initial User Message",
#                                                 value="st.session_state['initial_user_message']",
#                                                 key="user_message_input")
#
#             submit_button = st.form_submit_button(label="Update Settings", type="primary")
#
#
#         if st.button("Reset Temperature to Default"):
#
#             st.success("Temperature reset to default.")
#             print("User Message reset to default")
#
#         if st.button("Reset System Prompt to Default"):
#
#             st.success("System prompt reset to default.")
#             print("User Message reset to default")
#
#         if st.button("Reset User Message to Default"):
#
#             st.success("User Message reset to default.")
#             print("User Message reset to default")
#
#         else:
#             st.warning("Incorrect password. Access denied.")
