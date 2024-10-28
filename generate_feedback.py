import os
import openai
from dotenv import load_dotenv

load_dotenv()

# Load environment variables
open_ai_key = os.getenv("OPENAI_API_KEY")
open_ai_model = os.getenv("OPEN_AI_MODEL")
client = openai.OpenAI(api_key=open_ai_key)


def generate_timeline_with_feedback(timeline_text, feedback):
    messages = [
        {
            "role": "system",
            "content": (
                "You are an assistant that specializes in Machine Learning (ML), Full-Stack (FS), and DevOps engineering. "
                "You are skilled at project management and timeline generation, with a strong understanding of software development processes and best practices. "
                "Be mindful to avoid excessive durations in all tasks and suggest a realistic timeline for efficient project delivery. "
                "Ensure the modifications reflect user feedback while maintaining accurate formatting and realistic durations."
            )
        },
        {
            "role": "user",
            "content": (
                "Based on the existing timeline and the following feedback, please revise the timeline for the project. "
                "Modify the tasks, subtasks, and their durations according to the feedback. The revised timeline should keep the original structure and update the tasks and durations as needed.\n\n"
                f"Original Timeline:\n{timeline_text}\n\n"
                f"Feedback:\n{feedback}\n\n"
                "Output the revised timeline in the same format as below:\n"
                "Phase,Task,Subtask,Total Time (Days),Total Time (Hours)\n"
                "Make sure not to add any additional rows, text, or explanations outside of the given format. "
                "Avoid adding any backticks (```) or quotation marks in the response."
            )
        }
    ]

    response = client.chat.completions.create(
        model=open_ai_model,
        messages=messages,
        max_tokens=int(os.getenv('MAX_TOKENS')),
        n=1,
        temperature=float(os.getenv('TEMPERATURE')),
    )

    modified_timeline_text = response.choices[0].message.content
    return modified_timeline_text

