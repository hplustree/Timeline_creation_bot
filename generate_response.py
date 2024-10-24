import os
import openai
import csv
from dotenv import load_dotenv
from loaders import split_file

load_dotenv()

# Load environment variables
open_ai_key = os.getenv("OPENAI_API_KEY")
open_ai_model = os.getenv("OPEN_AI_MODEL")
client = openai.OpenAI(api_key=open_ai_key)

def generate_timeline(requirement_chunks):
    # Create messages for the chat model
    messages = [
        {
            "role": "system",
            "content": (
                "You are an assistant that specializes in Machine Learning (ML), Full-Stack (FS) and DevOps engineering. You are skilled at project management and timeline generation, with a strong understanding of software development processes and best practices."
                "Be mindful to avoid excessive durations in all the tasks, and suggest a realistic timeline for efficient project delivery."
                "Strictly ensure that no commas (,) are used in task or subtask descriptions."
                "Your primary goal is to output CSV data with accurate formatting."
                "Don't add backticks (```) in the csv generated, also don't add 'csv' keyword in starting of the csv file")
        },
        {
            "role": "user",
            "content": (
                "Based on the following requirements, please create a comprehensive timeline for the project."
                "The timeline should include all phases, tasks and their respective subtasks, "
                "along with estimated durations in both hours and days for each task.\n\n"
                f"{requirement_chunks}\n\n"
                "Output the timeline strictly in CSV format as follows:\n"
                "Phase,Task,Subtask,Total Time (Days),Total Time (Hours)\n"
                "Ensure that task and subtask descriptions do not contain any commas (,) to avoid issues in CSV parsing."
                "Don't add a row in the end containing the Total duration of the project"
                "Do not include any additional text or explanations."
                "Strictly do not include '''  '''."
            )
        }
    ]

    # Call the OpenAI API to generate the timeline using chat completion
    response = client.chat.completions.create(
        model=open_ai_model,
        messages=messages,
        max_tokens=int(os.getenv('MAX_TOKENS')),
        n=1,
        temperature=float(os.getenv('TEMPERATURE')),
    )

    # Extract the generated timeline from the response
    timeline_text = response.choices[0].message.content

    print(timeline_text)
    return timeline_text