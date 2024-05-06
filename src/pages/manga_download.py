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


def pdf_preview_table():
    pdf_names = load_title_dir_paths()
    
    if not pdf_names:
        st.write("No PDFs found")
        return
    
    with st.expander("See pdf previews"):
    
        for pdf_name in pdf_names:
            pdf_paths = load_pdf_paths(pdf_name)

            st.dataframe(pd.DataFrame(pdf_paths, columns=['PDF Paths']))

    # if st.button('Save Changes'):
    #     with open(pdf_paths, 'w') as f:
    #         json.dump(edited_data, f, indent=2)

    # Load the JSON file
    # with open(fileName, 'r') as f:
    #     data = json.load(f)

    # # Display the data in an editable table
    # edited_data = st.data_editor(data, num_rows="dynamic")


chapter_pdfs_folder = 'chapterPDFs'


@st.cache_resource
def load_title_dir_paths():
    dirs = os.listdir(chapter_pdfs_folder)
    pathDirs = update_full_path(dirs, chapter_pdfs_folder)

    return natsorted(pathDirs, alg=ns.PATH)


@st.cache_resource
def update_full_path(paths, before_path: str):
    pathDirs = []

    for path in paths:
        pathDirs.append(os.path.join(before_path, path))

    return pathDirs


@st.cache_resource
def load_pdf_paths(title_dir_path: str):
    file_paths = os.listdir(title_dir_path)
    return update_full_path(file_paths, os.path.join(title_dir_path))


pdf_preview_table()
