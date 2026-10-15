from groq_analyzer import analyze_resume
# resume = """
# Rahul Sharma

# Software Engineer with 2 years of experience.

# Skills:
# Python, Machine Learning, NumPy, Pandas, AWS

# Education:
# B.Tech in Computer Science

# Experience:
# 2 years working as a Software Engineer.
# Built machine learning applications using Python.
# Worked with AWS services.

# The candidate has strong Python and machine learning
# skills but has limited experience with Docker and Kubernetes.
# """

# result = analyze_resume(resume)

# print("\nResume Analysis Result:\n")


# print("Name:", result.candidate_name)
# print("Skills:", result.candidate_skills)
# print("Experience:", result.candidate_experience)
# print("Qualifications:", result.candidate_qualifications)
# print("Strengths:", result.strength)
# print("Missing Skills:", result.missing_skills)




# Test Case 1: Complete resume
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


# Test Case 2: Resume without education details
resume_without_education = """
Priya Verma

Python Developer with 3 years of experience.

Skills:
Python, Django, REST APIs, PostgreSQL

Experience:
Worked on backend applications and API development
for 3 years.
"""


# Test Case 3: Very little information
minimal_resume = "Python developer"


test_cases = [
    ("Complete Resume", complete_resume),
    ("Missing Education", resume_without_education),
    ("Minimal Resume", minimal_resume),
]


for test_name, resume_text in test_cases:
    print("\n" + "=" * 60)
    print(f"TEST: {test_name}")
    print("=" * 60)

    try:
        result = analyze_resume(resume_text)

        print(result.model_dump_json(indent=2))

    except Exception as error:
        print(f"ERROR: {type(error).__name__}: {error}")
