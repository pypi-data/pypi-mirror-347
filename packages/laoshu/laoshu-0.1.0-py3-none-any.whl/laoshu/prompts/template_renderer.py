from laoshu.data.external_data_definitions import InputData, Session


def render_template(input_data: InputData, session: Session) -> str:
    """
    Renders a prompt template with the user input from a session.

    Args:
        input_data: The input data containing the prompt template
        session: The session containing the user input

    Returns:
        The rendered prompt
    """
    prompt_template = input_data.prompt_template
    user_input = session.user_input
    return prompt_template.format(**user_input.model_dump())
