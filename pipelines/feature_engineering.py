from zenml import pipeline

from steps import feature_engineering as fe


@pipeline
def feature_engineering(user_full_name: list[str], wait_for: str | list[str] | None = None) -> list[str]:
    retrieved_user_documents = fe.query_data_warehouse(
        user_full_name, after=wait_for)
