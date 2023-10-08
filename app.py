import streamlit as st
from fpdf import FPDF
from PIL import Image
import base64
import os
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import ImageFormatter

st.set_page_config(page_title='PDFMaker', page_icon=':memo:', layout='wide')

with st.sidebar:
    st.write("")


st.title('PDF Maker')

name = st.text_input('Enter your name')
reg_num = st.text_input('Enter your registration number')
ass_name = st.text_input('Enter assignment name')
text_in = st.text_area('Enter anything you want to be printed on the first page: ')

