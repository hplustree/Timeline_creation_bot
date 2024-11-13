import os
import openai
from dotenv import load_dotenv
from generate_feedback import generate_timeline_with_user_feedback

load_dotenv()

open_ai_key = os.getenv("OPENAI_API_KEY")
open_ai_model = os.getenv("OPEN_AI_MODEL")
client = openai.OpenAI(api_key=open_ai_key)

def generate_timeline(requirement_chunks):
    # Create messages for the chat model
    messages = [
        {
            "role": "system",
            "content": (
                "You are a project management assistant specializing in Machine Learning (ML), Full-Stack (FS), and DevOps engineering. "
                "Your primary goal is to generate a well-structured timeline in CSV format, specifically focused on providing accurate durations for tasks and subtasks. "
                "Avoid excessive durations; suggest realistic estimates for efficient project delivery based on best practices in software development."
                "Ensure each task has defined subtasks if any are missing, and double-check the timeline for logical sequencing. "
                "Strictly avoid using commas (,) in task or subtask descriptions to prevent CSV formatting issues."
                "Output the CSV data with no backticks (```) or the keyword 'csv' at the beginning. "
                "Finally, anticipate potential questions or clarifications that developers might have based on the timeline provided, and include those developer-side queries."
            )
        },
        {
            "role": "user",
            "content": (
                "Based on the following requirements, please create a comprehensive timeline for the project."
                "The timeline should include all phases, tasks, and their respective subtasks, "
                "along with estimated durations in both hours and days for each task.\n\n"
                f"{requirement_chunks}\n\n"
                "Output the timeline strictly in CSV format as follows:\n"
                "Phase,Task,Subtask,Total Time (Days),Total Time (Hours)\n"
                "Ensure that task and subtask descriptions do not contain any commas (,) to avoid issues in CSV parsing."
                "Strictly do not add any integer value in a subtask or task"
                "Do not add a row at the end containing the total duration of the project."
                "Strictly do not include documentation and planning tasks in the timeline."
                "Do not include any additional text or explanations."
                "Strictly do not include '''  '''.\n\n"
                "After the timeline, include a heading 'Developer Side Queries:' and provide a numbered list of potential developer-side queries based on the requirements."
                "The queries should cover areas that may need clarification, such as technical details, dependencies, assumptions, or any potential challenges that could arise during the project."
                "Ensure that the heading 'Developer Side Queries:' is clearly separate from the timeline."
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

    timeline_text = response.choices[0].message.content
    # print("timeline: ", timeline_text)
    return timeline_text

def validate_timeline(requirement_chunks, timeline_text):
    validation_messages = [
        {
            "role": "system",
            "content": (
                "You are an experienced project reviewer specializing in validating project timelines against requirements. Only validate technical tasks related to development, engineering, and implementation, and ignore non-technical tasks such as tutorials, documentation, planning, or future expansion plans."
                "Strictly identify only technical missing tasks or subtasks and suggest improvements."
                "Do not output explanations. Only provide a verdict 'Valid' if the timeline covers all technical requirements, or list only the technical missing tasks or subtasks."
            )
        },
        {
            "role": "user",
            "content": (
                "Validate the following timeline against the given requirements and identify any missing technical tasks or subtasks:\n\n"
                f"Requirements:\n{requirement_chunks}\n\n"
                f"Timeline:\n{timeline_text}\n\n"
                "Output:\n- 'Valid' if the timeline covers all requirements.\n- List of missing technical tasks or subtasks if there are any."
            )
        }
    ]

    response = client.chat.completions.create(
        model=open_ai_model,
        messages=validation_messages,
        max_tokens=int(os.getenv('MAX_TOKENS')),
        n=1,
        temperature=float(os.getenv('TEMPERATURE')),
    )

    validation_result = response.choices[0].message.content.strip()

    if validation_result.lower() == "valid":
        validation_result = None

    return validation_result

def refine_timeline(requirement_chunks, max_iterations=5):
    timeline_text = generate_timeline(requirement_chunks)
    # print(f"initial timeline: {timeline_text}\n")
    sections = timeline_text.split("\n\n")
    developer_queries_section = None
    if len(sections) > 1 and sections[1].strip().lower().startswith("developer side queries"):
        developer_queries_section = sections[1]

    for iteration in range(max_iterations):
        # print(f"iteration: {iteration + 1}\n")
        feedback = validate_timeline(requirement_chunks, timeline_text)
        # print(f"feedback: {feedback}\n")
        if feedback is None or feedback.strip().lower() in ["", "valid", "-none","- none"]:
            break
        else:
            timeline_text = generate_timeline_with_user_feedback(timeline_text, feedback)
            # print(f"after feedback : {timeline_text}\n")

    # Append the Developer Side Queries to the modified timeline if they exist
    if developer_queries_section:
        timeline_text += f"\n\n{developer_queries_section}"

    return timeline_text
