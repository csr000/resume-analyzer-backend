from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Union
from utils import pdf_to_txt, post_to_model
from functions.rank import get_grade
import uvicorn, json
from starlette.responses import JSONResponse

# TODO update docstring of parse
# TODO update docstring of compare

app = FastAPI(debug=True)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def home():
    return {"message": "running"}


@app.post("/parse")
async def parse(file: bytes = File(...)):
    """Get pdf, parse it and return json with a specific format.

    Args:
        file (bytes, optional): resume pdf. Defaults to File(...).

    Returns:
        json:  {
                    "name": <name>,
                    "email": <email>
                    "skills": <an array of skills>
                }
    """
    text = pdf_to_txt(file)

    stringified_structure = str(
        {
            "name": "<name>",
            "email": "<email>",
            "location": "<location>",
            "education": "<education>",
            "skills": "<an array of skills>",
        }
    )

    template = f"""I extracted this information from a resume pdf: 
    {text}. 
    Extract the necessary information and return it using the template below:
    {stringified_structure}. Make sure its a valid json and each key value is enclosed in double quotes.
    """
    return json.loads(post_to_model(template))


@app.post("/rank")
async def rank(
    job_description: str, files: List[UploadFile]
) -> List[Dict[str, Union[str, float]]]:
    """
    Given a job description and a list of resumes, this function ranks the resumes based on how well they match the job description.

    Args:
    - job_description (str): A string representing the job description.
    - files (List[UploadFile]): A list of resume files as UploadFile objects.

    Returns:
    - List[Dict[str, Union[str, float]]]: A list of dictionaries, where each dictionary contains the grade (float) and the file name (str) of a resume.
    """
    grades = []
    for file in files:
        pdf_bytes = await file.read()
        resume_content = pdf_to_txt(pdf_bytes)
        grade = get_grade(job_description, resume_content)
        grades.append({"grade": grade, "file": file.filename})
    return grades


@app.post("/compare")
async def compare(job_description: str, files: List[UploadFile]):
    """
    This function compares resumes against a given job description.

    Args:
        job_description (str): The job description to compare against
        files (List[UploadFile]): A list of UploadFile objects representing the resumes to be compared

    Returns:
        str: A string containing a summary of each resume and a comparison against the job description.
    """

    resumes = []
    for file in files:
        pdf_bytes = await file.read()
        resume_content = pdf_to_txt(pdf_bytes)
        resumes.append(resume_content)

    stringified_structure = str(
        {
            "resume1": "<resume 1>",
            "resume2": "<resume 2>",
            "compare": "<comparing the resumes against the job description>",
        }
    )

    template = f"""I have an array of {len(resumes)} resumes extracted from pdfs. 
    Using this template: {stringified_structure}, 
    Write a summary about each resume and compare them against this Job description: {job_description}.
    Choose which of the resumes fits best. These as the resumes: {resumes}.
    Return the template and Make sure its a valid json and each key value is enclosed in double quotes.
    """

    return json.loads(post_to_model(template))


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
