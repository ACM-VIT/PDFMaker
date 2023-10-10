# Standard Library Imports
import os
import base64

# Third-Party Library Imports
import streamlit as st
from fpdf import FPDF
from PIL import Image
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import ImageFormatter

# Set Streamlit page configuration
st.set_page_config(page_title='PDFMaker', page_icon=':memo:', layout='wide')

def generate_pdf(name, reg_num, ass_name, text_in, file):
    # PDF generation code goes here
    pass

# Create a sidebar
with st.sidebar:
    st.write("")

# Title
st.title('PDF Maker')

# Inputs
user_name = st.text_input('Enter your name')
reg_num = st.text_input('Enter your registration number')
ass_name = st.text_input('Enter assignment name')
user_text_input = st.text_area('Enter anything you want to be printed on the first page: ')

# Create a File Upload widget with customization options
uploaded_file = st.file_uploader(
    label="Choose a file",
    type=["jpg", "png"],  # Specify the allowed file types
    accept_multiple_files=False,  # Set to True if you want to allow multiple file uploads
    help="Upload JPG or PNG files",  # Custom help text
    key="file_uploader"  # Set a unique key to customize the widget
)

if st.button('Generate PDF'):
    if user_name and reg_num and ass_name:
        generate_pdf(user_name, reg_num, ass_name, user_text_input, uploaded_file)
        st.success('PDF generated successfully.')
    else:
        st.error('Please fill in all required fields.')
