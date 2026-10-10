import os
from models import ResumeAnalysis
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

def analyze_resume(resume_text: str) -> ResumeAnalysis:
    """
    Analyzes a resume and returns structured information about the candidate.
    
    Args:
        resume_text (str): The text content of the resume to analyze.
        
    Returns:
        ResumeAnalysis: Structured information about the candidate.
    """

    prompt = f"""
         you are a resume analyzer.

         Analyze the following resume.
         {resume_text}

        Extract the following information from the resume and return it in a structured format:
        
        candidate_name: str
        candidate_skills: list[str]
        candidate_experience: list[str] 
        candidate_qualifications: list[str]
        strength: str
        missing_skills: list[str]

        Return only valid JSON.
        Do not include any additional text or explanations. The output should be a valid JSON object with the specified fields.
        Do not include markdown.
        Do not invent any information that is not present in the resume. If a field cannot be determined from the resume, return an empty string or an empty list for that field. 

      """

    response = client.chat.completions.create(
        model = "openai/gpt-oss-20b",
        messages = [
            {
                "role": "system",
                "content": "You are a professional resume analyzer. Extract structured information from resumes."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        response_format = {
            "type": "json_object"
        }
    )

    result = response.choices[0].message.content
    data = json.loads(result)
    return ResumeAnalysis(**data)