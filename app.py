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

col1, col2= st.columns(2)
with col1:
   number = st.number_input('Insert the number of questions', step=1, min_value=1)

with col2:
   theme = st.selectbox(
    'Choose a theme!',
    ('default', 'github-dark', 'sas', 'rrt', 'rainbow_dash', 'stata-light', 'gruvbox-light', 'gruvbox-light', 'monokai', 'vim', 'inkpot'))

question_images = []
code_inputs = []
output_images = []

st.write("---")
for i in range(int(number)):
    st.write(f'Question {i+1}')
    question_image = st.file_uploader(f'Upload question image for question {i+1}', type=['jpg', 'jpeg', 'png'])
    if question_image is not None:
        img = Image.open(question_image)
        img = img.convert('RGB') # convert image to RGB format
        img.save(f'temp_question_{i}.png', format='png') # save image as a PNG file
        question_images.append(f'temp_question_{i}.png')
    code_input = st.text_area(f'Paste code for question {i+1}')
    if code_input:
        code_inputs.append(code_input)
    output_image = st.file_uploader(f'Upload output image for question {i+1}', type=['jpg', 'jpeg', 'png'])
    if output_image is not None:
        img = Image.open(output_image)
        img = img.convert('RGB') # convert image to RGB format
        img.save(f'temp_output_{i}.png', format='png') # save image as a PNG file
        output_images.append(f'temp_output_{i}.png')
    st.write("---")

# set minimum line length for code inputs else shit blows up
min_line_length = 40 
for i in range(len(code_inputs)):
    code_lines = code_inputs[i].split('\n')
    max_line_length = max(len(line) for line in code_lines)
    if max_line_length < min_line_length:
        padding = ' ' * (min_line_length - max_line_length)
        code_inputs[i] = '\n'.join(line + padding for line in code_lines)

pdf = FPDF()

pdf.add_page()

pdf.set_font('Arial', 'B', 16)

# Add the name, registration number, and assignment name as a heading
pdf.cell(0, 20, f"{name} - {reg_num}", 0, 1, 'C')
pdf.cell(0, 10, f"{ass_name}", 0, 1, 'C')

# Add a blank line
pdf.cell(0, 10, '', 0, 1)

# Reset font and size for the body text
pdf.set_font('Arial', '', 12)
pdf.cell(0, 20, f"{text_in}", 0, 1, 'C')

page_width = pdf.w
max_image_width = page_width * 0.8 # set maximum image width to 80% of page width

for i in range(int(number)):
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    y_offset = 30
    padding = 0

    pdf.cell(200, 10, txt=f"Q{i+1})", ln=1, align='L')
    pdf.cell(200, 10, txt="Code & Output:", ln=1, align='L')

    if i < len(question_images):
        img = Image.open(question_images[i])
        width, height = img.size
        image_width = min(max_image_width, width) # set image width to the smaller of max_image_width and original image width
        X = (page_width - image_width) / 2
        pdf.image(question_images[i], x=X, y=y_offset, w=image_width)
        page_height = pdf.h
        padding = page_height * 0.125
        y_offset += height * (100 / width) + padding
        img.close()
    if i < len(code_inputs):
        formatter = ImageFormatter(style=theme)
        with open(f'temp_code_{i}.png', 'wb') as f:
            f.write(highlight(code_inputs[i], PythonLexer(), formatter))
        img = Image.open(f'temp_code_{i}.png')
        width, height = img.size
        image_width = min(max_image_width, width) # set image width to the smaller of max_image_width and original image width
        X = (page_width - image_width) / 2
        pdf.image(f'temp_code_{i}.png', x=X, y=y_offset, w=image_width)
        y_offset += height * (100 / width) + padding
        img.close()
        os.remove(f'temp_code_{i}.png')
    if y_offset > pdf.w - 20: # check if y_offset exceeds page height
        pdf.add_page() # add a new page
        y_offset = 30 # reset y_offset
    if i < len(output_images):
        img = Image.open(output_images[i])
        width, height = img.size
        image_width = min(max_image_width, width) # set image width to the smaller of max_image_width and original image width
        X = (page_width - image_width) / 2
        pdf.image(output_images[i], x=X, y=y_offset, w=image_width)
        y_offset += height * (100 / width) + 10
        img.close()

pdf.output(f"code_submission.pdf")

#changes

def generate_pdf():

# Display download button for PDF file
    st.download_button(
    label="Download PDF",
    data=open('code_submission.pdf', 'rb'),
    file_name='code_submission.pdf',
    )
    # code to generate the PDF file
    with open("code_submission.pdf", "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)

if st.button('Generate PDF'):
    generate_pdf()
    for i in range(int(number)):
        if os.path.exists(f'temp_question_{i}.png'):
            os.remove(f'temp_question_{i}.png')
        if os.path.exists(f'temp_code_{i}.png'):
            os.remove(f'temp_code_{i}.png')
        if os.path.exists(f'temp_output_{i}.png'):
            os.remove(f'temp_output_{i}.png')