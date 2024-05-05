
import streamlit as st

st.page_link("main.py", label="Home", icon="🏠")
st.page_link("pages/manga_download.py", label="Page 1", icon="1️⃣")

st.page_link("http://localhost:8501/preview_pdf?pdf_name=20220311-EB-Designing_Event_Driven_Systems.pdf",
             label="ExamplePreview PDF", icon="🌎")
