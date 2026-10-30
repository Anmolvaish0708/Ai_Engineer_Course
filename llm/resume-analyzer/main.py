
from groq_analyzer import analyze_resume
from pdf_reader import extract_resume_text_from_pdf


complete_resume = """
Rahul Sharma

Software Engineer with 2 years of experience.

Skills:
Python, Machine Learning, NumPy, Pandas, AWS

Education:
B.Tech in Computer Science

Experience:
Worked as a Software Engineer for 2 years.
Built Python applications and machine learning solutions.
Used AWS services for deployment.
"""

resume_without_education = """
Priya Verma

Python Developer with 3 years of experience.

Skills:
Python, Django, REST APIs, PostgreSQL

Experience:
Worked on backend applications and API development
for 3 years.
"""

minimal_resume = "Python developer"

job_description = """
AI Engineer

Required skills:
Python, AWS, Docker, REST APIs, LLM integration.
Experience building and deploying AI applications is preferred.
"""


test_cases = [
    ("Complete Resume", complete_resume, job_description),
    ("Missing Education", resume_without_education, job_description),
    ("Minimal Resume", minimal_resume, job_description),
]


def test_text_resumes():
    for test_name, resume_text, job_description in test_cases:

        print("\n" + "=" * 60)
        print(f"TEST: {test_name}")
        print("=" * 60)

        try:
            result = analyze_resume(
                resume_text=resume_text,
                target_job_description=job_description
            )

            print(result.model_dump_json(indent=2))

        except (ValueError, TypeError) as error:
            print(f"Input or validation error: {error}")

        except Exception as error:
            print(f"Unexpected failure: {type(error).__name__}: {error}")


def test_pdf_resume():
    pdf_path = r"C:\Users\ADMIN\Desktop\sample_resume.pdf"

    print("\n" + "=" * 60)
    print("TEST: PDF RESUME")
    print("=" * 60)

    try:
        resume_text = extract_resume_text_from_pdf(pdf_path)

        result = analyze_resume(
            resume_text=resume_text,
            target_job_description=job_description
        )

        print(result.model_dump_json(indent=2))

    except (ValueError, TypeError) as error:
        print(f"Input or validation error: {error}")

    except Exception as error:
        print(f"Unexpected failure: {type(error).__name__}: {error}")


if __name__ == "__main__":
    test_pdf_resume()
