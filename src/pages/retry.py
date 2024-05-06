import json
import os
import streamlit as st
from natsort import natsorted, ns
import subprocess

# pdfs/Again My Life/newPDF/ตอนที่ 1.pdf
rootConfigRetryFolder: str = 'configs/retries'


def retry_table():
    if st.button('Download retry PDFs'):
        ## TODO: make golang is command
        ## go run main.go      
        # Define the command to run
        cmd = ["go", "run", "main.go"]

        # Run the command
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Get the output and errors
        output, errors = process.communicate()

        # Check if the command was successful
        if process.returncode == 0:
            print("Command executed successfully.")
        else:
            print("Error executing command:", errors.decode())
    
    retry_titles = load_retry_titles()
    st.write("List of retry_titles")
    st.dataframe(retry_titles, width=500)

    jsonFiles = load_json_files_name()

    st.write("List of JsonFiles")
    st.dataframe(jsonFiles)

    configRetries = load_json_config_retry_files_data()

    st.write("List of Config Retries")
    st.dataframe(configRetries)

    # if st.button('Save Changes'):
    #         with open(fileName, 'w') as f:
    #             json.dump(edited_data, f, indent=2)


@st.cache_resource
def load_json_files_name():
    return natsorted(os.listdir(rootConfigRetryFolder), alg=ns.PATH)


@st.cache_resource
def load_json_config_retry_files_data():
    configRetries = []

    jsonFiles = load_json_files_name()

    for file in jsonFiles:
        # read json file
        with open(f'{rootConfigRetryFolder}/{file}', 'r') as f:
            data = json.load(f)

            configRetries += data

    return configRetries


@st.cache_resource
def load_retry_titles():
    titles = []

    jsonFiles = load_json_files_name()

    for file in jsonFiles:
        # read json file
        with open(f'{rootConfigRetryFolder}/{file}', 'r') as f:
            data = json.load(f)

            # full_path: pdfs/Again My Life/ตอนที่ 65/062.jpg
            full_path = data[0]['full_path']
            title = os.path.basename(
                os.path.dirname(os.path.dirname(full_path)))

            if title not in titles:
                titles += [title]

    return titles


retry_table()
