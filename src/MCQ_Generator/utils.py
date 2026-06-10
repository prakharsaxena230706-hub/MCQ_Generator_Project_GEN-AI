import os
import PyPDF2
import json 
import traceback
import logging

def read_file(uploaded_file):
    if uploaded_file.name.lower().endswith('.pdf'):
        try:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            raise Exception("Error reading PDF file") from e

    elif uploaded_file.name.lower().endswith('.txt'):
        return uploaded_file.read().decode('utf-8')

    else:
        raise Exception("Unsupported file format. Only PDF and TXT files are supported.")
    
    
def read_pdf(file_path):
    """
    Extract text from a PDF file using PyPDF2.
    
    Args:
        file_path (str): Path to the PDF file
        
    Returns:
        str: Extracted text from the PDF
    """
    try:
        text = ""
        with open(file_path, 'rb') as file:
            # Handle both PyPDF2 1.x and 2.x APIs
            try:
                # PyPDF2 2.x API
                pdf_reader = PyPDF2.PdfReader(file)
                num_pages = len(pdf_reader.pages)
                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n"
            except AttributeError:
                # Fallback to PyPDF2 1.x API
                pdf_reader = PyPDF2.PdfFileReader(file)
                num_pages = pdf_reader.numPages
                for page_num in range(num_pages):
                    page = pdf_reader.getPage(page_num)
                    text += page.extractText() + "\n"
        
        return text
    except Exception as e:
        logging.error(f"Error reading PDF: {str(e)}")
        traceback.print_exc()
        raise


def get_table_data(quiz_str):
    try:
        # If quiz is a string, parse it into a dict first
        if isinstance(quiz_str, str):
            # Clean up the string if it has markdown code fences
            quiz_str = quiz_str.strip()
            if quiz_str.startswith("```"):
                quiz_str = quiz_str.split("```")[1]
                if quiz_str.startswith("json"):
                    quiz_str = quiz_str[4:]
            quiz_dict = json.loads(quiz_str)
        else:
            quiz_dict = quiz_str

        table_data = []

        for key, value in quiz_dict.items():
            try:
                mcq = value.get("MCQ", "")
                options = value.get("Options", {})
                choices_text = " | ".join([f"{k}: {v}" for k, v in options.items()])
                correct = value.get("Correct", "")

                table_data.append({
                    "Question": mcq,
                    "Choices": choices_text,
                    "Correct": correct
                })
            except Exception as e:
                logging.warning(f"Error processing quiz item {key}: {str(e)}")
                continue

        return table_data

    except Exception as e:
        logging.error(f"Error converting quiz to table format: {str(e)}")
        traceback.print_exc()
        raise
