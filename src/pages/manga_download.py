import os
import subprocess
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
    st.success('Load config done~')


def config_table():
    st.dataframe(config_datas())


@st.cache_resource
def config_datas():
    config_datas = []
    config_folder = 'configs'

    # configs/Akuma wa Rozario ni Kiss wo suru/ตอนที่ 1.json
    title_folders = os.listdir(config_folder)

    for title_folder in title_folders:
        full_title_folder = os.path.join(config_folder, title_folder)
        files = os.listdir(full_title_folder)
        count = len(files)

        config_datas.append({
            'title': title_folder,
            'count': count
        })
    return config_datas


config_table()

if st.button('Download PDFs'):
    # TODO: make golang is command
    # go run main.go
    # Define the command to run
    cmd = ["go", "run", "main.go", "download"]

    # Run the command
    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Get the output and errors
    output, errors = process.communicate()

    # Check if the command was successful
    if process.returncode == 0:
        print("Command executed successfully.")
        st.success('Download PDFs done~')

        # output_substring_list = output.split('\n')
        # print(output_substring_list)
    else:
        print("Error executing command:", errors.decode())
        st.error("Error executing command:", errors.decode())


if st.button('Make PDF'):
    commands = download.commands()
    commands.makePDFs()
    st.success('Make PDF done~')

if st.button('Merge PDF'):
    commands = download.commands()
    commands.mergePDFs()
    st.success('Merge PDF done~')

# TODO: clean pdfs
# TODO: clean readypdf


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
