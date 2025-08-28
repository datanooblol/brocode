import time
from typing import Final


def wait() -> str:
    """Wait for five seconds before returning a completion message.

    This function pauses the current thread for five seconds using
    :func:`time.sleep` and then returns the string ``"Done"``.  It is
    intentionally simple but follows best practices:

    * PEP 8 compliant indentation and naming.
    * Google‑style docstring with clear description, return value,
      and possible exceptions.
    * Type hints for the return type.
    * Minimal error handling – a ``KeyboardInterrupt`` is re‑raised
      so that the caller can decide how to handle it.

    Returns:
        str: The string ``"Done"`` after the five‑second delay.

    Raises:
        KeyboardInterrupt: Propagated if the user aborts the sleep.
    """
    try:
        time.sleep(5)
    except KeyboardInterrupt:
        # Propagate the interrupt to the caller
        raise
    return "Done"


# Example usage
if __name__ == "__main__":
    print("Waiting…")
    result = wait()
    print(result)