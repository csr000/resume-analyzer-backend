import fitz
from fastapi import HTTPException
import openai
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.environ.get("API_KEY")


def pdf_to_txt(file: bytes) -> str:
    """Convert a pdf file to text.

    Args:
    file (bytes): The pdf file to be converted.

    Returns:
    str: Text extracted from the pdf file.
    """
    result = ""
    # Open the PDF file
    pdf_doc = fitz.open("pdf", file)

    # Iterate over each page
    for page in pdf_doc:
        # Extract the text from the page
        page_text = page.get_text()
        # Append the text
        result += page_text
    return result


def post_to_model(prompt: str) -> str:
    """
    Sends a request to model and returns the model's response. 
    
    Args:
        prompt (str): The text prompt to send to the model.
    
    Returns:
        str: The model's response to the given prompt.
    
    Raises:
        HTTPException: If the request to the model is unsuccessful.
    """
    if response := openai.Completion.create(
        model=os.environ.get("model"),
        prompt=prompt,
        temperature=0.9,
        max_tokens=1500,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"],
    ):
        print(response.choices[0].text)
        return response.choices[0].text
    else:
        raise HTTPException(
            status_code=500, detail="Server Error, could not access model."
        )
