import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
from generate_response import refine_timeline
from generate_excel import process_gpt_timeline_response
from generate_feedback import generate_timeline_with_feedback
from loaders import split_file
import pandas as pd
import os
import uuid
import glob
import time

# Set the page layout to wide
st.set_page_config(layout="wide")

st.title("Timeline Generator Bot")

# Initialize session state variables
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())  # Generate unique user ID
# Initialize session state variables
if "uploaded_file_path" not in st.session_state:
    st.session_state.uploaded_file_path = None
if "timeline_text" not in st.session_state:
    st.session_state.timeline_text = None
if "excel_file_path" not in st.session_state:
    st.session_state.excel_file_path = None
if "updated_timeline_text" not in st.session_state:
    st.session_state.updated_timeline_text = None
if "modified_excel_file_path" not in st.session_state:
    st.session_state.modified_excel_file_path = None

# File uploader
uploaded_file = st.file_uploader("Upload a DOCX or PDF file", type=['docx', 'pdf', 'txt'])

# Helper function to remove a file if it exists
def remove_file(filepath):
    if filepath and os.path.exists(filepath):
        os.remove(filepath)

if uploaded_file is not None:
    if not os.path.exists("user_files"):
        os.makedirs("user_files")
    # Remove previously uploaded file and Excel file for this session
    remove_file(st.session_state.uploaded_file_path)
    # remove_file(st.session_state.excel_file_path)
    # Process the file
    user_file_path = f"user_files/{st.session_state.user_id}_{uploaded_file.name}"  # Unique file name based on user_id
    # Process the file
    with open(user_file_path, 'wb') as f:
        f.write(uploaded_file.getbuffer())

    # Store the uploaded file path in session state
    st.session_state.uploaded_file_path = user_file_path

    # Split the file into chunks
    chunks = split_file(user_file_path)
    
    # Generate timeline button
    if st.button("Generate Timeline"):
        timeline_text = refine_timeline(chunks)
        # print("Timeline: ", timeline_text)
        
        # Store the generated timeline text in session state
        st.session_state.timeline_text = timeline_text
        st.session_state.updated_timeline_text = timeline_text

        # Save timeline to Excel
        excel_file_path = process_gpt_timeline_response(timeline_text, st.session_state.user_id)
        # Store the Excel file path in session state
        st.session_state.excel_file_path = excel_file_path

if st.session_state.excel_file_path:
    st.subheader("Generated Timeline:")
    # Display the Excel content as a DataFrame
    df = pd.read_excel(st.session_state.excel_file_path)
    # Create AgGrid options
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(resizable=True, filterable=False, sortable=False, editable=False)
    gb.configure_grid_options(domLayout='normal')  # Adjust height based on content
    grid_options = gb.build()

    # Display the DataFrame using AgGrid with auto-sizing columns
    AgGrid(df, gridOptions=grid_options, fit_columns_on_grid_load=True, theme="alpine")

    with open(st.session_state.excel_file_path, 'rb') as f:
        st.download_button(
            label="Download Timeline as Excel",
            data=f,
            file_name='project_timeline.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

if st.session_state.timeline_text:
    # Feedback Section
    st.subheader("Feedback on Timeline")
    feedback = st.text_area("Provide your feedback to improve the timeline:")

    # Button to apply feedback and modify the timeline
    if st.button("Update Timeline Based on Feedback"):
        if feedback:
            # Extract Developer Side Queries from the original timeline
            original_timeline_text = st.session_state.updated_timeline_text
            sections = original_timeline_text.split("\n\n")
            developer_queries_section = None
            if len(sections) > 1 and sections[1].strip().lower().startswith("developer side queries"):
                developer_queries_section = sections[1]

            # Generate the modified timeline based on feedback
            modified_timeline_text = generate_timeline_with_feedback(st.session_state.updated_timeline_text, feedback)

            # Append the Developer Side Queries to the modified timeline if they exist
            if developer_queries_section:
                modified_timeline_text += f"\n\n{developer_queries_section}"

            # Update the session state with the modified timeline text
            st.session_state.updated_timeline_text = modified_timeline_text
            # Save the modified timeline to a new Excel file
            modified_excel_file_path = process_gpt_timeline_response(modified_timeline_text, st.session_state.user_id, feedback=True)
            st.session_state.excel_file_path = modified_excel_file_path
        else:
            st.warning("Please provide feedback before updating the timeline.")

        if st.session_state.excel_file_path:
            st.subheader("Updated Timeline:")
            # Display the modified Excel content as a DataFrame
            modified_df = pd.read_excel(st.session_state.excel_file_path)
            # Create AgGrid options for the modified timeline
            gb = GridOptionsBuilder.from_dataframe(modified_df)
            gb.configure_default_column(resizable=True, filterable=False, sortable=False, editable=False)
            gb.configure_grid_options(domLayout='normal')  # Adjust height based on content
            modified_grid_options = gb.build()

            # Display the modified DataFrame using AgGrid with auto-sizing columns
            AgGrid(modified_df, gridOptions=modified_grid_options, fit_columns_on_grid_load=True, theme="alpine", key="NewTimeline")

            with open(st.session_state.excel_file_path, 'rb') as f:
                st.download_button(
                    label="Download Updated Timeline as Excel",
                    data=f,
                    file_name='updated_project_timeline.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )

            # Clean up the modified file
            # os.remove(modified_excel_file_path)

# Clean up the uploaded file if needed
# if st.session_state.uploaded_file_path:
#     os.remove(st.session_state.uploaded_file_path)
#     st.session_state.uploaded_file_path = None

# if st.session_state.excel_file_path:
#     os.remove(st.session_state.excel_file_path)
#     st.session_state.excel_file_path = None

# Periodic cleanup of old files (e.g., files older than 1 hour)
def cleanup_old_files(directory, age_threshold_sec=3600):
    for filepath in glob.glob(f"{directory}/*"):
        if os.path.isfile(filepath) and time.time() - os.path.getmtime(filepath) > age_threshold_sec:
            os.remove(filepath)

# Run the cleanup function (customize directory as needed)
cleanup_old_files(directory="user_files", age_threshold_sec=3600)  # Customize age threshold as needed
