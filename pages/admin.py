import json
import os
import streamlit as st
import zipfile
import io


ADMIN_PASSWORD = st.secrets["ADMIN_PASSWORD"]
def openFile(path, name):
    data = {}
    try:
        with open(os.path.join(path, name), "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        st.error("File not found.")
    return data

def create_zip(directory):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for file in os.listdir(directory):
            if file.endswith(".json"):
                file_path = os.path.join(directory, file)
                zip_file.write(file_path, os.path.basename(file_path))
    zip_buffer.seek(0)
    return zip_buffer

def main():
    st.title("Admin Area")

    # Password protection
    password = st.text_input("Enter password", type="password")
    if password == "":
        return
    if password != ADMIN_PASSWORD:
        st.error("Incorrect password.")
        return

    section = st.selectbox("Select section", ["Participants", "Revisited", "Groups.json"])

    if section == "Participants":
        directory = "data/participants"
        json_files = [f for f in os.listdir("data/participants") if f.endswith(".json")]
        if not json_files:
            st.write("No JSON files found.")
        else:
            zip_buffer = create_zip(directory)
            st.download_button(
                label="Download All JSON files as ZIP",
                data=zip_buffer,
                file_name="participants_json_files.zip",
                mime="application/zip",
                type="primary",
                use_container_width=True
            )
            for file in json_files:
                st.write(f"**{file}**")
                data = openFile(directory, file)
                st.json(data)
                st.download_button(
                    label="Download JSON file",
                    data=json.dumps(data),
                    file_name=file,
                    mime="application/json",
                    type="primary",
                    use_container_width=True
                )


    elif section == "Revisited":
        directory = "data/revisited"
        json_files = [f for f in os.listdir(directory) if f.endswith(".json")]
        if not json_files:
            st.write("No JSON files found.")
        else:
            zip_buffer = create_zip(directory)
            st.download_button(
                label="Download All JSON files as ZIP",
                data=zip_buffer,
                file_name="revisited_json_files.zip",
                mime="application/zip",
                type="primary",
                use_container_width=True
            )
            for file in json_files:
                st.write(f"**{file}**")
                data = openFile("data/revisited", file)
                st.json(data)
                st.download_button(
                    label="Download JSON file",
                    data=json.dumps(data),
                    file_name=file,
                    mime="application/json",
                    type="primary",
                    use_container_width=True
                )

    elif section == "Groups.json":
        file_path = "data/groups.json"
        if not os.path.exists(file_path):
            st.write("No groups.json file found.")
        else:
            data = openFile("data", "groups.json")
            st.json(data)
            st.download_button(
                label="Download groups.json",
                data=json.dumps(data),
                file_name="groups.json",
                mime="application/json",
                type="primary",
                use_container_width=True
            )

if __name__ == "__main__":
    main()