import os
from models import ResumeAnalysis
from dotenv import load_dotenv
from pydantic import ValidationError
from groq import (
    Groq,
    APIConnectionError,
    APIStatusError,
    AuthenticationError,
    RateLimitError,
)

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

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
    You are a professional resume information extraction assistant.

    You will receive a resume and an optional target job description.
    Extract accurate information from the resume and return it
    in the required JSON structure.

    EXTRACTION RULES:

    1. Extract only information supported by the resume.
    Never invent details or make unsupported assumptions.

    2. candidate_name:
    Extract the candidate's full name.

    3. listed_skills:
    Extract skills only from the dedicated Skills section
    of the resume.

    4. demonstrated_skills:
    Extract technologies and skills supported by projects
    and work experience. Do not assume proficiency simply
    because a technology is mentioned.

    5. candidate_experience:
    Extract entries only from the dedicated Work Experience,
    Professional Experience, or Employment History section.
    Do not include projects, extracurricular activities,
    volunteering, or student leadership positions.

    6. candidate_qualifications:
    Extract formal academic qualifications, including school
    education, college degrees, and university degrees.
    Do not include certifications or job simulations.

    7. certifications:
    Extract certifications, licenses, and professional
    credentials mentioned in the resume. Do not include
    ordinary achievements or awards.

    8. achievements:
    Extract awards, competition rankings, job simulations,
    virtual experience programs, and other notable
    accomplishments mentioned in the resume.

    9. leadership_and_activities:
    Extract leadership positions, student society roles,
    volunteering, extracurricular activities, and
    event responsibilities.

    10. Preserve the original section context when classifying
        information. Do not move an entry into another category
        merely because of its description.

    11. A bullet point and its following descriptive lines
        belong to the same entry. Preserve the main title and
        relevant supporting details.

    12. Extract all relevant entries. Do not silently omit
        information or duplicate the same entry across categories.

    13. If information for a field is unavailable, return
        an empty string for string fields or [] for list fields.

    STRENGTH SUMMARY:

    1. Write a brief summary of the candidate's strengths
    using explicit evidence from the resume.

    2. Mention relevant technical experience, projects,
    teaching, achievements, or leadership where supported.

    3. Do not invent personality traits, interests,
    motivations, or professional capabilities.

    4. Avoid proficiency labels such as expert, proficient,
    advanced, or highly skilled unless explicitly supported
    by the resume.

    5. Use grammatically correct sentences and proper spacing.

    JOB DESCRIPTION COMPARISON:

    1. Extract required_skills from the explicitly required
    skills in the supplied job description.

    2. Do not include optional or preferred skills as required.

    3. Compare job requirements against both listed_skills
    and demonstrated_skills.

    4. Do not add job description skills to the candidate's
    resume skills.

    5. If no job description is supplied, return
    required_skills as [].

    OUTPUT RULES:

    1. Return only a valid JSON object.
    2. Do not include Markdown, explanations, or additional text.
    3. candidate_name and strength must be strings.
    4. All other fields must be arrays of strings.
    5. Never replace an array with a single string.
    6. Do not generate candidate_skills or missing_skills.
    These fields are calculated by the Python application.

    REQUIRED JSON STRUCTURE:

    {
        "candidate_name": "string",
        "listed_skills": ["string"],
        "demonstrated_skills": ["string"],
        "candidate_experience": ["string"],
        "candidate_qualifications": ["string"],
        "certifications": ["string"],
        "achievements": ["string"],
        "leadership_and_activities": ["string"],
        "required_skills": ["string"],
        "strength": "string"
    }
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
            model = MODEL,
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

        # this only validates the json format, not the schema. The schema validation is done below with Pydantic.
            response_format = {
                "type": "json_object"
            }
        )

          
        
        result = response.choices[0].message.content

        if not result:
            raise ValueError("The model returned an empty response.")

        return ResumeAnalysis.model_validate_json(result)

        

    except AuthenticationError as error:
        raise RuntimeError(
            "Invalid Groq API key. Check your .env configuration."
        ) from error

    except RateLimitError as error:
        raise RuntimeError(
            "Groq request limit or quota exceeded. "
            "Check your API usage and try again later."
        ) from error

    except APIConnectionError as error:
        raise RuntimeError(
            "Unable to connect to Groq. Check your internet connection."
        ) from error

    except APIStatusError as error:
        raise RuntimeError(
            f"Groq API returned an error. Status code: {error.status_code}"
        ) from error

    except ValidationError as error:
        raise ValueError(
            f"The model returned data that failed validation: {error}"
        ) from error