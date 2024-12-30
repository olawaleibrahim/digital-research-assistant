import re
import PyPDF2
from loguru import logger

from digital_research_assistant.domain.documents import PDFDocument


def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text


def clean_text(text):

    cleaned_text = re.sub(r"[^\w\s.,!?]", " ", text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)

    return cleaned_text.strip()


def extract_pdf(filepath=None):

    print(f"Extracting text from {filepath}...")
    raw_text = extract_text_from_pdf(filepath)

    cleaned_text = clean_text(raw_text)

    return cleaned_text


class PDFExtractor():
    model = PDFDocument

    def extract(self, filepath: str, **kwargs) -> None:
        old_model = self.model.find(filepath=filepath)
        if old_model is not None:
            logger.info(f"PDF already exists in the database: {filepath}")

            return

        logger.info(f"Starting extracting PDF: {filepath}")

        data = {
            "Title": filepath,
            "Content": extract_pdf(filepath)
        }

        user = kwargs["user"]
        user_full_name = kwargs["user_full_name"]
        instance = self.model(
            filetype="pdf",
            content=data,
            filepath=filepath,
            author_id=user.id,
            author_full_name=user_full_name,
        )

        instance.save()

        logger.info(f"Successfully extracted and saved file: {filepath}")
