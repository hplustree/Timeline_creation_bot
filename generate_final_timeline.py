import os
import openai
from dotenv import load_dotenv

load_dotenv()

open_ai_key = os.getenv("OPENAI_API_KEY")
open_ai_model = os.getenv("OPEN_AI_MODEL")
client = openai.OpenAI(api_key=open_ai_key)

def generate_timeline(requirement_chunks):
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
                f"{requirement_chunks}\n\n"
                "Output the timeline strictly in CSV format as follows:\n"
                "Phase,Task,Subtask\n"
                "Ensure that task and subtask descriptions do not contain any commas (,) to avoid issues in CSV parsing."
                "Strictly do not add any integer value in a subtask or task"
                "If there is no subtasks then simply add '-' in that field. "
                "Strictly do not include documentation and planning tasks in the timeline."
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
    return timeline_text

def generate_timeline_with_feedback(timeline_text, feedback):
    messages = [
        {
            "role": "system",
            "content": (
                "You are an assistant that specializes in Machine Learning (ML), Full-Stack (FS), and DevOps engineering. "
                "You are skilled at project management and timeline generation, with a strong understanding of software development processes and best practices. "
                "Ensure the modifications reflect user feedback while maintaining accurate formatting and realistic durations."
                "Strictly ensure that no commas (,) are used in task or subtask descriptions."
                "Strictly ensure that the number of columns are same throughout the generated csv, correct it by removing or adding the commas if missed earlier"
            )
        },
        {
            "role": "user",
            "content": (
                "Based on the existing timeline and the following feedback, please revise the timeline for the project. "
                "Modify the tasks, subtasks according to the feedback. The revised timeline should keep the original structure and update the tasks, subtasks and durations as needed.\n\n"
                f"Original Timeline:\n{timeline_text}\n\n"
                f"Feedback:\n{feedback}\n\n"
                "Output the revised timeline in the same format as below:\n"
                "Phase,Task,Subtask\n"
                "Ensure that task and subtask descriptions do not contain any commas (,) to avoid issues in CSV parsing."
                "Do not add a row at the end containing the total duration of the project."
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

def generate_durations_for_timeline(timeline_text):
    duration_messages = [
        {
            "role": "system",
            "content": (
                "You are a project assistant skilled in estimating durations for tasks and subtasks for  Machine Learning (ML), Full-Stack (FS), and DevOps engineering based on the tasks and subtasks in the provided timeline, "
                "Estimate realistic durations in days and hours. Update the timeline by adding 'Total Time (Days)' and 'Total Time (Hours)' columns."
                "Strictly ignore durations in Developer Side Queries if there is any."
                "Strictly ensure that if there are no subtask or there is a dash (-), then estimate the duration based on the task associated, don't estimate any duration as 0"
                "Strictly ensure that if there are no subtask then add a dash (-) in place of that if not already there"
                "Strictly ensure that the number of columns are same throughout the generated csv, correct it by removing or adding the commas if missed earlier"
                "Output the CSV data with no backticks (```) or the keyword 'csv' at the beginning."
            )
        },
        {
            "role": "user",
            "content": (
                "Add estimated durations to the following timeline:\n\n"
                f"{timeline_text}\n\n"
                "Output the timeline strictly in CSV format as follows:\n"
                "Phase,Task,Subtask,Total Time (Days),Total Time (Hours)\n"
                "Ensure no extra text or formatting outside of this structure."
            )
        }
    ]

    response = client.chat.completions.create(
        model=open_ai_model,
        messages=duration_messages,
        max_tokens=int(os.getenv('MAX_TOKENS')),
        n=1,
        temperature=float(os.getenv('TEMPERATURE')),
    )

    duration_timeline_text = response.choices[0].message.content
    return duration_timeline_text


def evaluate_durations(timeline_text, max_duration_iterations=2):
    timeline_with_durations = generate_durations_for_timeline(timeline_text)
    for iteration in range(max_duration_iterations):
        validation_result = validate_timeline_for_durations(timeline_with_durations)
        if validation_result is None:
            break
    return timeline_with_durations


def validate_timeline_for_durations(timeline_text):
    validation_messages = [
        {
            "role": "system",
            "content": (
                "You are an experienced project reviewer. Validate the estimated durations in the provided timeline. "
                "Modify the timeline based on subtask durations if required. "
            )
        },
        {
            "role": "user",
            "content": (
                f"Review the following timeline for its duration estimates:\n\n"
                f"{timeline_text}\n\n"
                "You just have to modify the durations(if any), do not output anything else."
                "Strictly output the modified timeline."
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
    # return validation_result if validation_result.lower() != "valid" else None
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
        if feedback is None:
            break
        timeline_text = generate_timeline_with_feedback(timeline_text, feedback)
        # print(f"after feedback : {timeline_text}\n")

    timeline_text = evaluate_durations(timeline_text)
    if developer_queries_section:
        timeline_text += f"\n\n{developer_queries_section}"
    return timeline_text
