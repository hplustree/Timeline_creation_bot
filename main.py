import streamlit as st
from generate_response import generate_timeline, save_timeline_to_csv
from loaders import split_file
import os


st.title(" Timeline Generator Bot")

# File uploader
uploaded_file = st.file_uploader("Upload a DOCX or PDF file", type=['docx', 'pdf'])

if uploaded_file is not None:
    # Process the file
    file_path = uploaded_file.name  
    with open(file_path, 'wb') as f:
        f.write(uploaded_file.getbuffer())

    # Split the file into chunks
    chunks = split_file(file_path)
    
    # Generate timeline button
    if st.button("Generate Timeline"):
        timeline_text = generate_timeline(chunks)
        # Save timeline to CSV
        csv_file_path = save_timeline_to_csv(timeline_text)

        st.subheader("Generated Timeline:")
        st.text(timeline_text) 
        with open(csv_file_path, 'rb') as f:
            st.download_button(
                label="Download Timeline as CSV",
                data=f,
                file_name='project_timeline.csv',
                mime='text/csv'
            )
        os.remove(file_path)
        os.remove(csv_file_path)