
# try:
#     num1 = int(input("enter a number: "))
#     num2 = int(input("enter a number: "))

#     result = num1/num2
#     print(result)
# except ValueError:
#     print("Value must be an integer.")
# except ZeroDivisionError:
#     print("cannot divide by zero!")    


# def generate_embeddings(texts):
#     if not isinstance(texts,list):
#         raise TypeError("texts should be a list.")
#     if not texts:
#         raise ValueError("texts can not be empty.")

#     for text in texts:
#             if not isinstance(text,str):
#                 raise TypeError("text must be a string.")

#     if any(not text.strip() for text in texts if isinstance(text,str)):
#         raise ValueError("text cannot be empty.")

        
#     print("Input validated successfully.")

# generate_embeddings(["hello",123,"world"])

from pathlib import Path

# def load_faq_data(file_path):
#     file = Path(file_path)

#     if not file.exists():
#         raise FileNotFoundError("file not found..")

#     try:
#         with open(file, "r", encoding="utf-8") as f:
#             text_content = f.read()
#             return text_content
#     except OSError as e:
#          raise RuntimeError("Failed to read FAQ file.") from e

# load_faq_data(r"C:\Users\ADMIN\OneDrive\Documents\HomeMatchReadme.txt")

print(Path(__file__).resolve().parent.parent)