import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
from generate_response import generate_timeline
from generate_excel import process_gpt_timeline_response
from loaders import split_file
import pandas as pd
import os

# Set the page layout to wide
st.set_page_config(layout="wide")

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
        # Save timeline to Excel
        # if os.path.exists('project_timeline.xlsx'):
        #     os.remove('project_timeline.xlsx')
        excel_file_path = process_gpt_timeline_response(timeline_text)

        st.subheader("Generated Timeline:")
        # Display the Excel content as a DataFrame
        df = pd.read_excel(excel_file_path)
        # Create AgGrid options
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_default_column(resizable=True, filterable=False, sortable=False, editable=False)
        gb.configure_grid_options(domLayout='normal')  # Adjust height based on content
        grid_options = gb.build()

        # # Display the DataFrame using AgGrid with auto-sizing columns
        AgGrid(df, gridOptions=grid_options, fit_columns_on_grid_load=True, theme="alpine")

        with open(excel_file_path, 'rb') as f:
            st.download_button(
                label="Download Timeline as Excel",
                data=f,
                file_name='project_timeline.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
        os.remove(excel_file_path)
    os.remove(file_path)