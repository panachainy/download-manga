import os
from natsort import natsorted, ns
import streamlit as st
import pandas as pd
import json
import commands.download as download


def edit_config():
    file_name = 'config.json'

    # Load the JSON file
    with open(file_name, 'r') as f:
        data = json.load(f)

    # Display the data in an editable table
    edited_data = st.data_editor(data, num_rows="dynamic")

    if st.button('Save Changes'):
        with open(file_name, 'w') as f:
            json.dump(edited_data, f, indent=2)


edit_config()

if st.button('Load config'):
    commands = download.commands()
    commands.load_config()

st.write("on python can't download because we write on golang for easy to make it concurrentcy")

if st.button('Make PDF'):
    commands = download.commands()
    commands.makePDFs()

if st.button('Merge PDF'):
    commands = download.commands()
    commands.mergePDFs()


def d():
    pdf_names = load_pdfs_name()
    print(pdf_names)
    # Load the JSON file
    # with open(fileName, 'r') as f:
    #     data = json.load(f)

    # # Display the data in an editable table
    # edited_data = st.data_editor(data, num_rows="dynamic")


@st.cache_resource
def load_pdf_paths():
    chapter_pdfs_folder = 'chapterPDFs'
    return natsorted(os.listdir(chapter_pdfs_folder), alg=ns.PATH)


d()
