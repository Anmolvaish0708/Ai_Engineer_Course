import os

from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel, Field, ValidationError


load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise RuntimeError("GROQ_API_KEY is missing from the .env file.")

client = Groq(api_key=api_key)


class Candidate(BaseModel):
    name: str = Field(
        min_length=1,
        description="The candidate's name.",
    )
    skills: list[str]
    experience_years: float = Field(
        ge=0,
        description="The candidate's years of experience.",
    )


def main():
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Extract candidate information from the user's text. "
                        "Return a JSON object with name, skills, and "
                        "experience_years. Extract values faithfully. "
                        "Do not invent missing information."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        "Candidate: Anmol Pandey. "
                        "Skills: Python, AWS, GenAI. "
                        "Experience: 2 years."
                    ),
                },
            ],
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content

        if not content:
            raise ValueError("The model returned an empty response.")

        candidate = Candidate.model_validate_json(content)

    except ValidationError as error:
        print("The model returned data that failed validation:")
        print(error)
        return

    except Exception as error:
        print(f"Request failed: {error}")
        return

    print(candidate)
    print("\nCandidate name:", candidate.name)
    print("Skills:", candidate.skills)
    print("Experience:", candidate.experience_years)


if __name__ == "__main__":
    main()