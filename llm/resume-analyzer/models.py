from pydantic import BaseModel, Field

class ResumeAnalysis(BaseModel):
    candidate_name: str
    candidate_skills: list[str]
    candidate_experience: list[str]
    candidate_qualifications: list[str]
    strength: str
    missing_skills: list[str]