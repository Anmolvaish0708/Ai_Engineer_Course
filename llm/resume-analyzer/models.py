from pydantic import BaseModel,Field, computed_field

class ResumeAnalysis(BaseModel):
    """
    A Pydantic model representing the structured information extracted from a resume.

    """


    candidate_name: str = Field(default="", description="The name of the candidate or empty string if unknown.")
    listed_skills: list[str] = Field(
    default_factory=list,
    description="Skills explicitly listed in the dedicated Skills section."
    )

    demonstrated_skills: list[str] = Field(
    default_factory=list,
    description="Skills supported by evidence in projects and work experience."
    )

    @computed_field
    @property
    def candidate_skills(self) -> list[str]:
        return list(dict.fromkeys(
            self.listed_skills + self.demonstrated_skills
        ))
    
    candidate_experience: list[str] = Field(
        default_factory=list,
        description="A list of experiences mentioned in the resume's experience section or an empty list if none are found."
    )
    candidate_qualifications: list[str] = Field(
        default_factory=list,
        description="Formal academic qualifications only, including school "
        "education, college degrees, and university degrees. "
        "Exclude certifications, job simulations, competitions, "
        "volunteering, and extracurricular activities."
    )
    certifications: list[str] = Field(
        default_factory=list,
        description= "Professional certifications, licenses, and completed "
        "formal training credentials. Do not include ordinary "
        "job simulations unless explicitly identified as certifications."
        )

    achievements: list[str] = Field(
        default_factory=list,
        description="Notable accomplishments, awards, or recognitions mentioned in the resume.")

    leadership_and_activities: list[str] = Field(
        default_factory=list,
        description="Leadership roles and extracurricular activities mentioned in the resume."
    )
    required_skills: list[str] = Field(
    default_factory=list,
    description="Skills explicitly required by the supplied job description."
    )
    strength: str = Field(
        default="",
        description="A brief summary of the candidate's strengths or an empty string if not provided."
    )

    @computed_field
    @property
    def missing_skills(self) -> list[str]:
        candidate_skills = {
            skill.strip().lower()
            for skill in self.candidate_skills
        }

        return [
            skill for skill in self.required_skills
            if skill.strip().lower() not in candidate_skills
        ]