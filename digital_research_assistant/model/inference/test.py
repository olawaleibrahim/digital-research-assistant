from loguru import logger

from digital_research_assistant.model.inference.inference import LLMInferenceSagemakerEndpoint
from digital_research_assistant.model.inference.run import InferenceExecutor
from digital_research_assistant.settings import settings

if __name__ == "__main__":
    text = "Write me a post about AWS SageMaker inference endpoints."
    logger.info(f"Running inference for text: '{text}'")
    llm = LLMInferenceSagemakerEndpoint(
        endpoint_name=settings.SAGEMAKER_ENDPOINT_INFERENCE, inference_component_name=None
    )
    answer = InferenceExecutor(llm, text).execute()

    logger.info(f"Answer: '{answer}'")
