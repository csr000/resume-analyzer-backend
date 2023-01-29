import os, spacy
from rake_nltk import Rake

# en_core_web_lg = os.path.join(os.path.dirname(__file__), 'en_core_web_lg-2.3.1/en_core_web_lg/en_core_web_lg-2.3.1')

nlp = spacy.load("en_core_web_lg")
r = Rake()


def prepare_keywords(phrase: str) -> str:
    """
    Extracts keywords from a given phrase and returns them as a string, separated by commas.

    Args:
    phrase (str): The phrase to extract keywords from.

    Returns:
    str: A string containing the extracted keywords, separated by commas.
    """
    r.extract_keywords_from_text(phrase)
    return ", ".join(map(str, set(r.get_ranked_phrases())))


def get_similarity(keywords1: str, keywords2: str):
    """Compute the similarity between two sets of keywords using spaCy's Doc.similarity method.

    Args:
        keywords1 (str): The first set of keywords to compare.
        keywords2 (str): The second set of keywords to compare.

    Returns:
        str: Similarity score as a string rounded to 2 decimal points.
    """
    # Create Doc objects
    doc1 = nlp(keywords1)
    doc2 = nlp(keywords2)

    # Compute the similarity between the two Doc objects
    similarity = doc1.similarity(doc2) * 100
    return "{:.2f}".format(similarity)


def get_grade(job_description: str, resume_content: str):
    """Calculate the grade of a resume based on its similarity to a given job description.

    Args:
        job_description (str): The job description to compare the resume against.
        resume_content (str): The content of the resume to be graded.

    Returns:
        str: Similarity score as a string rounded to 2 decimal points.
    """
    return get_similarity(
        prepare_keywords(job_description), prepare_keywords(resume_content)
    )
