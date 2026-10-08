from interview_generator import generate_interview_questions

role = input("Enter the role: ")
experience = input("Enter the experience level: ")
skills = input("Enter the skills (comma-separated): ")

result = generate_interview_questions(role, experience, skills)

print("\nGenerated Interview Questions:\n")
print(result)