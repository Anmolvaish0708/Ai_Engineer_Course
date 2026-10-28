import os
from models import ResumeAnalysis
import json
from dotenv import load_dotenv
from groq import Groq
from pydantic import ValidationError

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
        raise RuntimeError("GROQ_API_KEY is missing from the .env file.")

client = Groq(api_key=api_key)

def analyze_resume(resume_text: str, target_job_description: str = "") -> ResumeAnalysis:
    """
    Analyzes a resume and returns structured information about the candidate.
    
    If a target job description is provided, compare the candidate's skills and experience against the job requirements and highlight any gaps or missing skills.
    """
    if not isinstance(resume_text, str):
         raise TypeError("resume_text must be a string.")
    
    if len(resume_text.strip()) < 50:
        raise ValueError("Resume text is too short. Please provide a more detailed resume.")

    if not isinstance(target_job_description, str):
        raise TypeError("target_job_description must be a string.")

    if target_job_description.strip() and len(target_job_description.strip()) < 50:
        raise ValueError(
            "Job description is too short. "
            "Please provide a more detailed description."
        )    

    system_prompt = """
     You are resume information extraction expert.

     You will be given a resume and an optional target job description.
     Your task is to extract structured information from the resume and compare it against the target job description if provided.

     Rules:
     - If a target job description is provided, identify any required skills that are missing from the candidate's resume.
     - Return the information in a structured JSON format with the following keys and types:
        {
            "candidate_name": "string",
            "candidate_skills": ["string"],
            "candidate_experience": ["string"],
            "candidate_qualifications": ["string"],
            "strength": "string",
            "missing_skills": ["string"]
        }
     - Do not invent information. Only use what is present in the resume and job description.
     - If any information is not present, return an empty string or an empty list as appropriate
     1. Every field must be present.
     2. candidate_name and strength must be strings.
     3. candidate_skills, candidate_experience, candidate_qualifications,
     and missing_skills must ALWAYS be arrays of strings.
     4. If a list has no information, return [].
     5. If a string has no information, return "".
     6. Never replace a list with a single string.
     7. Extract information faithfully. Never invent candidate details.
     8. Identify missing skills only by comparing the resume with
     the supplied target job description.
     9. If no job description is supplied, return missing_skills as [].
     10. Return JSON only. Do not include Markdown or explanations.   
"""
    user_prompt = f"""
    Resume:
    {resume_text}

    Target Job Description:
    {target_job_description}

    Please extract the information according to the system instructions and return it in JSON format.
    """
    try:
        response = client.chat.completions.create(
            model = "openai/gpt-oss-20b",
            messages = [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],

            response_format = {
                "type": "json_object"
            }
        )

        result = response.choices[0].message.content

        if not result:
            raise ValueError("The model returned an empty response.")

        return ResumeAnalysis.model_validate_json(result)
    
    except ValidationError as error:
        raise ValueError(
        f"The model returned data that failed validation: {error}"
    ) from error