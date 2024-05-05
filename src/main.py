import os
import streamlit as st
from natsort import natsorted, ns

st.page_link("main.py", label="Home", icon="🏠")
st.page_link("pages/manga_download.py", label="Page 1", icon="1️⃣")

st.page_link("http://localhost:8501/preview_pdf?pdf_name=20220311-EB-Designing_Event_Driven_Systems.pdf",
             label="ExamplePreview PDF", icon="🌎")

# TODO: continue
# def preview_pdf():

#     # pdfs/Again My Life/newPDF/ตอนที่ 1.pdf
#     rootPDFs: str = 'pdfs'

#     folders = natsorted(os.listdir(rootPDFs), alg=ns.PATH)

#     st.write("List of PDFs")
#     st.dataframe(folders)
 

# preview_pdf()
