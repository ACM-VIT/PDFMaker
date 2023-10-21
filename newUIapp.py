import os
import tempfile
import streamlit as st
from fpdf import FPDF

# Set Streamlit page configuration
st.set_page_config(page_title='PDFMaker', page_icon=':memo:', layout='wide')

# Define custom CSS for styling
st.markdown(
    """
    <style>
    body {
        background-color: #f0f0f0;
    }
    .stApp {
        padding: 1rem;
        background-color: #ffffff;
        border: 2px solid #0077b6;
        border-radius: 10px;
    }
    .stMarkdown {
        color: #0077b6;
    }
    .stButton > button {
        background-color: #0077b6;
        color: #ffffff;
    }
    .stText > p {
        color: #333;
    }
    .input-header {
        color: #0077b6;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Function to generate PDF
def generate_pdf(name, reg_num, ass_name, text_in, files):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt=ass_name, ln=True, align="C")
    pdf.cell(200, 10, txt=f"Name: {name}", ln=True, align="C")
    pdf.cell(200, 10, txt=f"Registration Number: {reg_num}", ln=True, align="C")

    pdf.multi_cell(0, 10, txt=text_in)

    for uploaded_file in files:
        if uploaded_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_image:
                temp_image.write(uploaded_file.read())
                temp_image.seek(0)
                pdf.image(temp_image.name, x=10, w=190)

    pdf_filename = f"{name}_{ass_name}.pdf"
    pdf.output(pdf_filename)
    return pdf_filename

# Sidebar
with st.sidebar:
    st.title('PDFMaker')
    st.markdown('An easy tool to help you make your assignments into a PDF in seconds.')
    st.markdown('Just four simple steps:')
    
    st.markdown('\n'.join([
        "👉 Fill in your personal details",
        "👉 Enter the content to print on the first page",
        "👉 Upload images of your assignment",
        "👉 Click 'Generate PDF'",
    ]))

# Main content
st.title('PDF Maker')
st.markdown('Fill in your assignment details', unsafe_allow_html=True)

# Input fields with colored headings
user_name = st.text_input('Your Name')
reg_num = st.text_input('Registration Number')
ass_name = st.text_input('Assignment Name')

st.markdown('<p class="input-header">Content for the first page</p>', unsafe_allow_html=True)
user_text_input = st.text_area('Enter text to print on the first page: ')

# File upload section with colored heading
st.markdown('<p class="input-header">Upload Images</p>', unsafe_allow_html=True)
st.write("Upload JPG or PNG images to include in the PDF.")

uploaded_files = st.file_uploader(
    label="Choose image files",
    type=["jpg", "png"],
    accept_multiple_files=True,
    help="Upload JPG or PNG files"
)

# Generate PDF button
if st.button('Generate PDF'):
    if user_name and reg_num and ass_name:
        pdf_filename = generate_pdf(user_name, reg_num, ass_name, user_text_input, uploaded_files)
        st.success('PDF generated successfully.')

        with open(pdf_filename, "rb") as f:
            pdf_data = f.read()

        st.download_button(
            label="Download Your PDF",
            data=pdf_data,
            file_name=f'{user_name}_{ass_name}.pdf',
            mime='application/pdf'
        )
    else:
        st.error('Please fill in all required fields.')
