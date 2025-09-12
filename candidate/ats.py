import streamlit as st
import io
import streamlit_scrollable_textbox as stx

from utility.text_extractor import extract_text
# Initialize session state variables
if "text_input" not in st.session_state:
    st.session_state.text_input = ""
if "file_content" not in st.session_state:
    st.session_state.file_content = ""

# uploaded_file = st.file_uploader("Choose your file")
input_method = st.radio(
    "Select input method:",
    ("Text Area", "File Uploader")
)

user_input = None

if input_method == "Text Area":
    st.session_state.text_input = st.text_area(
        "Enter your text here:", height = 40,
        value=st.session_state.text_input, placeholder = "Write your Resume here..."
    )
    user_input = st.session_state.text_input
elif input_method == "File Uploader":
    uploaded_file = st.file_uploader("Upload a text file", type=["txt","pdf","docx"])
    if uploaded_file is not None:
        Bytes = uploaded_file.read()
        stream = io.BytesIO(Bytes)
        st.session_state.file_content = extract_text(file_path=uploaded_file.name,file_stream = Bytes)
    if st.session_state.file_content:
        user_input = st.session_state.file_content
# Display result
if user_input:
    st.write("Your Input:")
    stx.scrollableTextbox(user_input, height=90)

user_jd = st.text_area("Enter your multi-line text here:", 
                          height=100, 
                          max_chars=500, 
                          placeholder="Write job description...")

st.write("You entered:")
stx.scrollableTextbox(user_jd, height=90)