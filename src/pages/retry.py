import json
import os
import streamlit as st
from natsort import natsorted, ns

# pdfs/Again My Life/newPDF/ตอนที่ 1.pdf
rootConfigRetryFolder: str = 'configs/retries'


def retry_table():

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
            configRetries.append(data)

    return configRetries

retry_table()
