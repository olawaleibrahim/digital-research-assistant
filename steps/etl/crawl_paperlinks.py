from loguru import logger
import os
from tqdm import tqdm
from pathlib import Path
from typing_extensions import Annotated
from zenml import get_step_context, step

from digital_research_assistant.domain.documents import UserDocument
from digital_research_assistant.application.extractors import PDFExtractor


@step
def crawl_paperlinks(user: UserDocument, user_full_name: str) -> Annotated[list[str], "crawl_paperlinks"]:

    logger.info(f"Starting to append user filepaths ")

    ROOT_DIR = Path(__file__).resolve().parent.parent.parent
    user_dir = f"/data/input/{user_full_name}/"
    dir_path = str(ROOT_DIR) + user_dir
    filepaths = os.listdir(dir_path)
    extractor = PDFExtractor()

    for filepath in tqdm(filepaths):
        filepath = dir_path + filepath
        successfull_extract = extractor.extract(
            filepath=filepath, user=user, user_full_name=user_full_name)

    step_context = get_step_context()
    step_context.add_output_metadata(
        output_name="crawl_paperlinks", metadata=_get_metadata(user_full_name, filepaths))
    print("filepaths", filepaths)

    return filepaths


def _get_metadata(user_full_name: str, filepaths: list) -> dict:
    return {
        "query": {
            "user_full_name": user_full_name,
        },
        "retrieved": {
            "filepaths": filepaths,
        },
    }
