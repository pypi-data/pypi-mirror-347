from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class UserInput(BaseModel):
    """
    Represents the user input in a session.
    Contains dynamic fields based on the prompt template.
    """

    model_config = ConfigDict(extra="allow")


class Session(BaseModel):
    """
    Represents a single session with user input and prompt output.
    """

    id: str
    user_input: UserInput
    prompt_output: str


class InputData(BaseModel):
    """
    Represents the input file format containing the prompt template and sessions.
    """

    prompt_template: str
    sessions: List[Session]


class FeedbackItem(BaseModel):
    """
    Represents feedback for a single session.
    """

    id: str
    is_correct: bool
    message: str
    expected_output: Optional[str] = None


class FeedbackData(BaseModel):
    """
    Represents the feedback file format containing feedback for sessions.
    """

    feedback: List[FeedbackItem]
