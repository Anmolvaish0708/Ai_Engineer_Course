from pydantic import BaseModel,Field, ValidationError

class ResumeAnalysis(BaseModel):
    """
    A Pydantic model representing the structured information extracted from a resume.

    """
    candidate_name: str = Field(default="", description="The name of the candidate or empty string if unknown.")
    candidate_skills: list[str] = Field(
        default_factory=list,
        description="A list of skills mentioned in the resume or an empty list if none are found."
    )
    candidate_experience: list[str] = Field(
        default_factory=list,
        description="A list of experiences mentioned in the resume or an empty list if none are found."
    )
    candidate_qualifications: list[str] = Field(
        default_factory=list,
        description="A list of qualifications mentioned in the resume or an empty list if none are found."
    )
    strength: str = Field(
        default="",
        description="A brief summary of the candidate's strengths or an empty string if not provided."
    )
    missing_skills: list[str] = Field(
        default_factory=list,
        description="Required skills not evidenced in the resume, "
            "based on a supplied target job description."
    )