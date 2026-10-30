from pypdf import PdfReader

def extract_resume_text_from_pdf(file_path):
    """
    Extracts text from resume pdf.

    Args:
        file_path (str): Path to the PDF file.

    Returns:
        str: Extracted text from the PDF.        
    """
    reader = PdfReader(file_path)
    extracted_text = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            extracted_text.append(text)

    resume_text = "\n".join(extracted_text).strip()      

    if not resume_text:
        raise ValueError("No text could be extracted from the PDF. "
               "Please ensure the PDF is not a scanned image and contains selectable text.")  
    return resume_text