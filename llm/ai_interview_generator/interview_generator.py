from llm import ask_llm

def generate_interview_questions(role, experience, skills):

    prompt = f"""
    You are a senior technical interviewer.

    Generate interview questions for:

    Role: {role}
    Experience: {experience}
    Skills: {skills}

    Generate:
    - 5 technical questions
    - 3 practical questions
    - 2 scenario-based questions

    Requirements:
    - Questions should match the candidate's experience.
    - Focus on the provided skills.
    - Avoid unnecessarily advanced questions.
    - Organize the questions by category.
    """

    return ask_llm(prompt)