from groq_analyzer import analyze_resume
resume = """
Rahul Sharma

Software Engineer with 2 years of experience.

Skills:
Python, Machine Learning, NumPy, Pandas, AWS

Education:
B.Tech in Computer Science

Experience:
2 years working as a Software Engineer.
Built machine learning applications using Python.
Worked with AWS services.

The candidate has strong Python and machine learning
skills but has limited experience with Docker and Kubernetes.
"""

result = analyze_resume(resume)

print("\nResume Analysis Result:\n")


print("Name:", result.candidate_name)
print("Skills:", result.candidate_skills)
print("Experience:", result.candidate_experience)
print("Qualifications:", result.candidate_qualifications)
print("Strengths:", result.strength)
print("Missing Skills:", result.missing_skills)