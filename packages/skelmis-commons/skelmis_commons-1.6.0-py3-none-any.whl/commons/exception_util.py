import traceback
from typing import Sequence


def exception_as_string(error: Exception) -> str:
    """Given an exception, return the traceback as a string."""
    return "".join(traceback.format_exception(error))

def exceptions_as_string(errors: Sequence[Exception]) -> str:
    """Given a sequence of exceptions,
    return the tracebacks as a string seperated by \n---\n.
    """
    return "\n---\n".join(exception_as_string(e) for e in errors)
