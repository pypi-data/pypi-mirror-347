from laoshu.data import InputData, FeedbackData


def load_input_data(file_path: str) -> InputData:
    with open(file_path, "r") as f:
        return InputData.model_validate_json(f.read())


def load_feedback_data(file_path: str) -> FeedbackData:
    with open(file_path, "r") as f:
        return FeedbackData.model_validate_json(f.read())
