import os
import shutil
import subprocess
from natsort import natsorted, ns
import streamlit as st
import pandas as pd
import json
import commands.download as download
from utils.streamlit_widget import progress


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
    progress(commands.load_config)
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


if st.button('Download images before pdf'):

    def download_pdfs():
        # TODO: make golang is command
        # go run main.go
        # Define the command to run
        cmd = ["go", "run", "main.go", "download"]

        # Run the command
        process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if process.stdout:
            for line in process.stdout:
                print(line.decode().strip())

        if process.stderr:
            for line in process.stderr:
                print(line.decode().strip())

        # Wait for the process to finish
        process.wait()

        # Check if the command was successful
        if process.returncode == 0:
            print("Command executed successfully.")

        else:
            print("Error executing command")

    progress(download_pdfs)
    st.success('Download PDF done~')


def image_table():
    st.dataframe(image_datas())


@st.cache_resource
def image_datas():
    image_datas = []
    image_folder = 'pdfs'

    # pdfs/990k Ex-Life Hunter/ตอนที่ 3/001.jpg
    title_folders = os.listdir(image_folder)

    for title_folder in title_folders:
        full_title_folder = os.path.join(image_folder, title_folder)
        files = os.listdir(full_title_folder)
        count = len(files)

        image_datas.append({
            'title': title_folder,
            'count': count
        })
    return image_datas


image_table()

if st.button('Make PDF each chapters'):
    commands = download.commands()

    progress(commands.makePDFs)
    st.success('Make PDF done~')


def chapters_table():
    st.dataframe(chapters_datas())


@st.cache_resource
def chapters_datas():
    datas = []
    folder = 'chapterPDFs'

    # pdfs/990k Ex-Life Hunter/ตอนที่ 3/001.jpg
    title_folders = os.listdir(folder)

    for title_folder in title_folders:
        full_title_folder = os.path.join(folder, title_folder)
        files = os.listdir(full_title_folder)
        count = len(files)

        datas.append({
            'title': title_folder,
            'count': count
        })
    return datas


chapters_table()

if st.button('Merge PDF'):
    commands = download.commands()

    progress(commands.mergePDFs)
    st.success('Merge PDF done~')


def merged_pdf_table():
    st.dataframe(merged_pdf_datas())


@st.cache_resource
def merged_pdf_datas():
    datas = []
    folder = 'readypdf'

    # pdfs/990k Ex-Life Hunter/ตอนที่ 3/001.jpg
    files = os.listdir(folder)

    for file in files:
        datas.append({
            'title': file,
        })
    return datas


merged_pdf_table()


def remove_dirs(directory_path: str):
    # os.removedirs(directory_path)

    # Check if the directory exists
    if os.path.exists(directory_path):
        # Check if the directory is empty
        if os.listdir(directory_path):
            # If the directory is not empty, remove all contents
            for filename in os.listdir(directory_path):
                file_path = os.path.join(directory_path, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            # After removing all contents, remove the directory
            shutil.rmtree(directory_path)
        else:
            # If the directory is empty, remove it directly
            shutil.rmtree(directory_path)
    else:
        print(f"The directory '{directory_path}' does not exist.")


if st.button('Clean all'):
    # remove all files in pdfs
    pdfs = 'pdfs'
    readypdf = 'readypdf'
    configs = 'configs'
    chapterPDFs = 'chapterPDFs'

    remove_dirs(pdfs)
    remove_dirs(readypdf)
    remove_dirs(configs)
    remove_dirs(chapterPDFs)
    os.makedirs(pdfs, exist_ok=True)
    os.makedirs(readypdf, exist_ok=True)
    os.makedirs(configs, exist_ok=True)
    os.makedirs(chapterPDFs, exist_ok=True)


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
