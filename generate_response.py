from loaders import *
import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

requirments_file_path=os.getenv('DOCX_PATH')
requirement_chunks=split_file(requirments_file_path)
open_ai_key = os.getenv("OPENAI_API_KEY")
open_ai_model=os.getenv("OPEN_AI_MODEL")
client=OpenAI(api_key=open_ai_key)


def generate_timeline(requirement_chunks):

    # Create messages for the chat model
    messages = [
        {"role": "system", "content": "You are an assistant that specializes in project management and timeline generation."},
        {
            "role": "user",
            "content": (
                "Based on the following requirements, please create a comprehensive timeline for the project."
                "The timeline should b strict."
                "Include all tasks and their respective subtasks, and provide estimated durations in both hours and days for each task:\n\n"
                f"{requirement_chunks}\n\n"
                "Present the timeline in a clear, structured format."
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
    timeline = response.choices[0].message.content
    return timeline

# Generate and print the timeline
timeline = generate_timeline(requirement_chunks)
print("Generated Timeline:")
print(timeline)
