from streamlit_pdf_viewer import pdf_viewer
import streamlit as st

# Retrieve query parameters
query_params = st.query_params

# Check if the query parameter 'id' exists
if 'pdf_name' in query_params:
    pdfName = query_params['pdf_name']
    # Process the 'id' parameter
    print(f"Received PdfName: {pdfName}")
    pdf_viewer(pdfName)
else:
    print("No pdf_name provided")
    

# # Display the PDF file using the streamlit-pdf-viewer component
# pdf_viewer("20220311-EB-Designing_Event_Driven_Systems.pdf")
