import streamlit as st


def progress(action):

    with st.status(label="Running...", expanded=True, state="running") as status:
        try:
            action()
            status.update(label='Completed', expanded=False, state="complete")
        except Exception as e:
            status.update(label=f"An error occurred: {e}", state="error")
