# Timeline Generator Bot

This project allows users to upload a DOCX or PDF file containing project requirements, and automatically generates a project timeline in Excel format. The timeline includes details about project modules, tasks, and subtasks, along with the estimated time (in days and hours) for each task. The final output includes formatted Excel files with merged cells, borders, and font styling for clarity.

## Features

- Upload DOCX or PDF files with project requirements
- Automatically generate a timeline with tasks and subtasks
- Export the generated timeline as a formatted Excel file
- Merged cells for repeated modules and tasks
- Automatic column width adjustment
- Styled headers, central alignment, and borders for clarity
- Download the Excel file directly from the app interface

## Prerequisites

- Python 3.10.15
- Required Python packages:
  - `streamlit`
  - `openpyxl`
  - `pandas`
  - `st_aggrid`

You can install the required packages using the following command:

```bash
python -m venv venv

source venv/bin/activate

pip install -r requirements.txt
```

## How to Use

1. **Clone the Repository**:
   Clone the repository to your local machine.
   ```bash
   git clone https://github.com/your-username/timeline-generator-bot.git
   cd timeline-generator-bot
   ## Run the Streamlit App:

2. Start the Streamlit app using the following command:
    ```bash
    streamlit run app.py
    ```
3. Upload a File
    * Once the app is running, use the **Upload a DOCX or PDF file** button to upload your project requirements document.
    * Supported file types: `.docx` and `.pdf`.

4. Generate Timeline
    * After uploading the file, click the **Generate Timeline** button to process the file.
    * The app will display a preview of the generated timeline.

5. Download Timeline as Excel
    * Once the timeline is generated, you can download the Excel file by clicking on the **Download Timeline as Excel** button.

## Project Structure

```bash
timeline-generator-bot/
│
├── main.py              # Main Streamlit app file
├── generate_response.py # Handles GPT timeline generation
├── generate_excel.py   # Processes GPT response to create Excel file
├── loaders.py         # File loader to split DOCX/PDF into chunks
├── requirements.txt    # Python package dependencies
└── README.md          # Project readme (this file)
```



