import os
import uuid

thing = os.environ.get("THING", str(uuid.uuid4()))


def echo(message: str) -> str:
    """
    Echoes the input message.

    Args:
        message (str): The message to echo.

    Returns:
        str: The echoed message.
    """
    return message


def foo():
    pass
